import { v4 as uuidv4 } from 'uuid';
import { fetchOpenAICompletion, OpenAIMessage } from './typhoon';
import { CaseGenerationParams, GeneratedCase, Case, Clue, Suspect } from '@/types/game';

// System prompt templates for case generation
const CASE_GENERATION_PROMPT_EN = `You are creating fun detective stories for 7-year-old children (2nd/3rd grade reading level).

CRITICAL SAFETY RULES - YOU MUST FOLLOW THESE:
❌ NO violence, weapons, death, murder, or killing
❌ NO scary or frightening content
❌ NO adult themes (divorce, gambling, drugs, alcohol, etc.)
❌ NO harm to people or animals
✅ ONLY mysteries about: lost items, missing pets (that are found safe), harmless pranks, switched belongings, or simple school mysteries

LANGUAGE REQUIREMENTS:
- Use ONLY simple words a 7-year-old can read
- Keep sentences SHORT (under 15 words)
- Make it FUN and cheerful, not scary
- Use concrete, not abstract concepts

CREATE:
1. A fun mystery with a title, short summary, school/home location, and time
2. 4-6 simple clues that kids can understand
3. 3-4 suspects (other children, teachers, or friendly adults - NO criminals)
4. One suspect who did it (but they're not in trouble - just made a mistake or had good intentions)

EXAMPLE GOOD TOPICS:
- Missing cookie recipe
- Lost homework
- Switched lunch boxes
- Who drew on the chalkboard
- Missing class pet (found safely)
- Borrowed toy that wasn't returned

The mystery should be solvable by a 7-year-old using simple logic.
Respond in a structured JSON format that can be parsed by JavaScript.`;

const CASE_GENERATION_PROMPT_TH = `คุณกำลังสร้างเรื่องสืบสวนสนุกๆ สำหรับเด็กอายุ 7 ขวบ (ระดับชั้นประถมศึกษาปีที่ 2-3)

กฎความปลอดภัยสำคัญ - คุณต้องปฏิบัติตาม:
❌ ห้ามมีความรุนแรง อาวุธ การตาย การฆาตกรรม
❌ ห้ามมีเนื้อหาที่น่ากลัวหรือน่าตกใจ
❌ ห้ามมีเนื้อหาสำหรับผู้ใหญ่ (การหย่าร้าง การพนัน ยาเสพติด แอลกอฮอล์ ฯลฯ)
❌ ห้ามทำร้ายคนหรือสัตว์
✅ เฉพาะปริศนาเกี่ยวกับ: ของหาย สัตว์เลี้ยงหาย (ที่พบตัวอย่างปลอดภัย) การเล่นซุกซนที่ไม่เป็นอันตราย ของที่สลับกัน หรือปริศนาโรงเรียนง่ายๆ

ความต้องการด้านภาษา:
- ใช้คำง่ายๆ ที่เด็ก 7 ขวบอ่านได้เท่านั้น
- ประโยคสั้น (ไม่เกิน 15 คำ)
- ทำให้สนุกและร่าเริง ไม่น่ากลัว
- ใช้แนวคิดที่เป็นรูปธรรม ไม่ใช่นามธรรม

สร้าง:
1. ปริศนาสนุกๆ พร้อมชื่อเรื่อง สรุปสั้นๆ สถานที่ (โรงเรียน/บ้าน) และเวลา
2. เบาะแส 4-6 อย่างที่เด็กเข้าใจได้
3. ผู้ต้องสงสัย 3-4 คน (เด็กคนอื่น ครู หรือผู้ใหญ่ที่เป็นมิตร - ไม่ใช่อาชญากร)
4. ผู้ต้องสงสัยหนึ่งคนที่ทำ (แต่ไม่ได้มีปัญหา - เพียงแค่ทำผิดพลาดหรือมีเจตนาดี)

หัวข้อที่ดี:
- สูตรคุกกี้หาย
- การบ้านหาย
- กล่องอาหารกลางวันสลับกัน
- ใครวาดบนกระดานดำ
- สัตว์เลี้ยงในชั้นเรียนหาย (พบตัวอย่างปลอดภัย)
- ของเล่นที่ยืมไปไม่ได้คืน

ปริศนาควรแก้ได้โดยเด็ก 7 ขวบด้วยตรรกะง่ายๆ
ตอบในรูปแบบ JSON ที่มีโครงสร้างซึ่ง JavaScript สามารถแปลงได้`;

// Fallback example case in case of API failures
const FALLBACK_CASE = {
    case: {
        title: "The Missing Backpack",
        description: "Alex's backpack is missing from the classroom! It has a special dinosaur patch on it. The backpack was on the hook this morning. Now it's gone. Can you help find it?",
        summary: "Help find Alex's backpack with the dinosaur patch.",
        difficulty: "easy",
        location: "Elementary School Classroom",
        dateTime: new Date().toISOString()
    },
    clues: [
        {
            title: "Empty Hook",
            description: "Alex's hook is empty. The hook next to it has two backpacks on it.",
            location: "Coat Room",
            type: "physical",
            relevance: "critical"
        },
        {
            title: "Dinosaur Sticker",
            description: "A small dinosaur sticker was found on the floor near the hooks.",
            location: "Coat Room Floor",
            type: "physical",
            relevance: "important"
        },
        {
            title: "Student Note",
            description: "A note says 'I borrowed a backpack by mistake. I'll bring it back tomorrow!'",
            location: "Teacher's Desk",
            type: "physical",
            relevance: "important"
        }
    ],
    suspects: [
        {
            name: "Jamie",
            description: "A student who also has a blue backpack",
            background: "Jamie's backpack looks just like Alex's. Jamie loves dinosaurs too.",
            motive: "Jamie probably took the wrong backpack by mistake. They look the same!",
            alibi: "Jamie says they grabbed their own backpack. They didn't notice it was the wrong one.",
            isGuilty: true
        },
        {
            name: "Taylor",
            description: "A helpful student who organizes the coat room",
            background: "Taylor helps hang up backpacks that fall down. Taylor is very organized.",
            motive: "Taylor might have moved the backpack to make more room on the hooks.",
            alibi: "Taylor says they only hung up backpacks that fell down. They didn't move Alex's backpack.",
            isGuilty: false
        }
    ],
    solution: "Jamie took the wrong backpack by mistake because it looked just like their own backpack. Both backpacks are blue with dinosaur patches!"
};

/**
 * Generates a detective case using the Typhoon LLM
 */
export async function generateCase(params: CaseGenerationParams): Promise<GeneratedCase> {
    const { difficulty, theme, location, era, language } = params;

    try {
        console.log("Starting case generation with params:", params);

        // Choose appropriate prompt based on language
        const systemPrompt = language === 'th' ? CASE_GENERATION_PROMPT_TH : CASE_GENERATION_PROMPT_EN;

        // Create user prompt with additional parameters
        let userPrompt = language === 'th'
            ? `สร้างคดีสืบสวนที่มีความยาก ${difficulty === 'easy' ? 'ง่าย' : difficulty === 'medium' ? 'ปานกลาง' : 'ยาก'}`
            : `Create a ${difficulty} difficulty detective case`;

        if (theme) {
            userPrompt += language === 'th' ? ` ในธีม ${theme}` : ` with a ${theme} theme`;
        }

        if (location) {
            userPrompt += language === 'th' ? ` ที่เกิดขึ้นใน ${location}` : ` set in ${location}`;
        }

        if (era) {
            userPrompt += language === 'th' ? ` ในยุค ${era}` : ` during the ${era} era`;
        }

        // Prepare messages for API call
        const messages: OpenAIMessage[] = [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userPrompt }
        ];

        // Use the client-side API route instead of direct API call for better error handling
        let response;

        // If running on client-side, use the API route
        if (typeof window !== 'undefined') {
            console.log("Using client-side API route for case generation");
            const result = await fetch('/api/typhoon', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    messages,
                    temperature: 0.7,
                    max_tokens: 8192
                }),
            });

            if (!result.ok) {
                const errorData = await result.json().catch(() => ({ error: `HTTP error ${result.status}` }));
                throw new Error(errorData.error || `Failed to generate case: ${result.status}`);
            }

            const data = await result.json();
            response = data.response;
        } else {
            // If running on server-side, use direct API call
            console.log("Using server-side direct API call for case generation");
            response = await fetchOpenAICompletion(
                messages,
                'gpt-4o',
                0.7,
                8192
            );
        }

        console.log("Received response from OpenAI API");

        // Parse the JSON response
        try {
            // Use a fallback technique to extract JSON if direct parsing fails
            const jsonMatch = response.match(/```json\n([\s\S]*?)\n```/) ||
                response.match(/```([\s\S]*?)```/) ||
                response.match(/({[\s\S]*})/);

            const jsonContent = jsonMatch ? jsonMatch[1] : response;
            console.log("Attempting to parse JSON response");
            const parsedData = JSON.parse(jsonContent);

            // Format the response into our expected structure
            return formatGeneratedCase(parsedData, language);
        } catch (parseError) {
            console.error('Failed to parse case data:', parseError);
            console.log('Raw response:', response);
            throw new Error('Failed to parse the generated case data. Please try again.');
        }
    } catch (error) {
        console.error('Case generation error:', error);

        // Provide a fallback case if generation fails
        if (process.env.NODE_ENV === 'development') {
            console.log("Using fallback case due to error");
            return formatGeneratedCase(FALLBACK_CASE, language);
        }

        throw error;
    }
}

/**
 * Formats the raw LLM output into our application's data structure
 */
function formatGeneratedCase(data: unknown, _language: 'en' | 'th'): GeneratedCase {
    // Extract and format case data
    const caseData: Case = {
        id: uuidv4(),
        title: (data as any)?.case?.title || (data as any)?.case_details?.title || (data as any)?.title || 'Untitled Case',
        description: (data as any)?.case?.description || (data as any)?.case_details?.synopsis || (data as any)?.description || '',
        summary: (data as any)?.case?.summary || (data as any)?.case_details?.synopsis || (data as any)?.summary || '',
        difficulty: (data as any)?.case?.difficulty || 'medium',
        solved: false,
        location: (data as any)?.case?.location || (data as any)?.case_details?.location || (data as any)?.location || '',
        dateTime: (data as any)?.case?.dateTime ||
            ((data as any)?.case_details?.date ?
                new Date(`${(data as any)?.case_details?.date} ${(data as any)?.case_details?.time || '00:00'}`).toISOString() :
                (data as any)?.dateTime || new Date().toISOString()),
        imageUrl: `/case-file.png`,
        isLLMGenerated: true
    };

    // Extract and format clues (handle both clues and evidence field names)
    const cluesData = (data as any)?.clues || (data as any)?.evidence || [];
    const clues: Clue[] = cluesData.map((clue: unknown) => ({
        id: uuidv4(),
        caseId: caseData.id,
        title: (clue as any)?.title || (clue as any)?.item || 'Untitled Clue',
        description: (clue as any)?.description || '',
        location: (clue as any)?.location || (clue as any)?.position_found || '',
        type: (clue as any)?.type || 'physical',
        discovered: false,
        examined: false,
        relevance: (clue as any)?.relevance || (clue as any)?.significance || 'important'
    }));

    // Extract and format suspects
    const suspects: Suspect[] = ((data as any)?.suspects || []).map((suspect: unknown) => ({
        id: uuidv4(),
        caseId: caseData.id,
        name: (suspect as any)?.name || 'Unknown Suspect',
        description: (suspect as any)?.description || '',
        background: (suspect as any)?.background || '',
        motive: (suspect as any)?.motive || '',
        alibi: (suspect as any)?.alibi || '',
        isGuilty: (suspect as any)?.isGuilty || false,
        interviewed: false
    }));

    // Find the guilty suspect based on the solution
    const solutionData = (data as any)?.solution;
    const solutionText = typeof solutionData === 'string'
        ? solutionData
        : (solutionData?.reasoning || solutionData?.narrative || '');
    const guiltySuspectName = solutionData?.culprit || solutionData?.culpritId || '';

    if ((solutionText || guiltySuspectName) && suspects.length > 0) {
        if (guiltySuspectName) {
            // Mark the identified suspect from solution.culprit as guilty
            suspects.forEach(suspect => {
                if (suspect.name.toLowerCase() === guiltySuspectName.toLowerCase()) {
                    suspect.isGuilty = true;
                }
            });
        } else if (solutionText) {
            // Try to identify the guilty suspect from the solution text
            const guiltyName = suspects.map(s => s.name).find(name =>
                solutionText.toLowerCase().includes(name.toLowerCase())
            );

            if (guiltyName) {
                // Mark the identified suspect as guilty
                suspects.forEach(suspect => {
                    if (suspect.name.toLowerCase() === guiltyName.toLowerCase()) {
                        suspect.isGuilty = true;
                    }
                });
            } else {
                // If we can't identify by name, mark the first suspect as guilty
                suspects[0].isGuilty = true;
            }
        }
    }

    return {
        case: caseData,
        clues,
        suspects,
        solution: solutionText
    };
} 