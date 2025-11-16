import { fetchOpenAICompletion, OpenAIMessage } from './typhoon';
import { ClueAnalysis, Clue, Suspect, Case } from '@/types/game';

// System prompts for clue analysis (child-friendly for 7-year-olds)
const CLUE_ANALYSIS_PROMPT_EN = `You are a helpful detective friend helping a 7-year-old child understand clues!

Use SIMPLE words that a 2nd or 3rd grader can read. Make it FUN and easy to understand!

Look at the clue and tell me:
1. What does this clue tell us? (Keep it simple!)
2. How does this clue connect to the people we're asking about?
3. What should we look at next? (Give simple steps)

Remember: Use SHORT sentences and EASY words that kids can read!

IMPORTANT: You must respond in valid JSON format with the following structure:
{
  "summary": "A simple explanation of what this clue means",
  "connections": [
    {
      "suspect": "Name of person",
      "connectionType": "How they're connected (like 'found near them' or 'they were there')",
      "description": "How this clue connects to this person (use simple words!)"
    }
  ],
  "nextSteps": [
    "First thing we should check next",
    "Second thing we should check next"
  ]
}`;

const CLUE_ANALYSIS_PROMPT_TH = `คุณเป็นเพื่อนนักสืบที่ช่วยเด็กอายุ 7 ขวบทำความเข้าใจเบาะแส!

ใช้คำง่ายๆ ที่เด็กป.2-ป.3 อ่านได้ ทำให้สนุกและเข้าใจง่าย!

ดูเบาะแสและบอกฉัน:
1. เบาะแสนี้บอกเราว่าอะไร? (ให้ง่ายๆ!)
2. เบาะแสนี้เชื่อมโยงกับคนที่เราถามอย่างไร?
3. เราควรดูอะไรต่อไป? (ให้ขั้นตอนง่ายๆ)

จำไว้: ใช้ประโยคสั้นๆ และคำง่ายๆ ที่เด็กอ่านได้!

สำคัญ: คุณต้องตอบในรูปแบบ JSON ที่ถูกต้องตามโครงสร้างต่อไปนี้:
{
  "summary": "อธิบายง่ายๆ ว่าเบาะแสนี้หมายความว่าอะไร",
  "connections": [
    {
      "suspect": "ชื่อคน",
      "connectionType": "เชื่อมโยงกันอย่างไร (เช่น 'พบใกล้เขา' หรือ 'เขาอยู่ที่นั่น')",
      "description": "เบาะแสนี้เชื่อมโยงกับคนนี้อย่างไร (ใช้คำง่ายๆ!)"
    }
  ],
  "nextSteps": [
    "สิ่งแรกที่เราควรตรวจสอบต่อไป",
    "สิ่งที่สองที่เราควรตรวจสอบต่อไป"
  ]
}`;

/**
 * Analyzes a clue in the context of a case using the Typhoon LLM
 */
export async function analyzeClue(
    clue: Clue,
    suspects: Suspect[],
    caseData: Case,
    discoveredClues: Clue[],
    language: 'en' | 'th'
): Promise<ClueAnalysis> {
    // Choose appropriate prompt based on language
    const systemPrompt = language === 'th' ? CLUE_ANALYSIS_PROMPT_TH : CLUE_ANALYSIS_PROMPT_EN;

    // Create user prompt with case context
    let userPrompt = '';

    if (language === 'th') {
        userPrompt = `ข้อมูลคดี:
ชื่อคดี: ${caseData.title}
สรุป: ${caseData.summary}
สถานที่: ${caseData.location}
วันที่และเวลา: ${caseData.dateTime}

หลักฐานที่ต้องการวิเคราะห์:
ชื่อ: ${clue.title}
คำอธิบาย: ${clue.description}
สถานที่พบ: ${clue.location}
ประเภท: ${clue.type}
ความสำคัญ: ${clue.relevance}

ผู้ต้องสงสัย:
${suspects.map(s => `${s.name}: ${s.description}`).join('\n')}

หลักฐานอื่นที่พบแล้ว:
${discoveredClues.filter(c => c.id !== clue.id).map(c => `${c.title}: ${c.description}`).join('\n')}

กรุณาวิเคราะห์หลักฐานนี้และให้:
1. สรุปความสำคัญของหลักฐาน
2. ความเชื่อมโยงกับผู้ต้องสงสัย
3. ขั้นตอนการสืบสวนต่อไปที่แนะนำ

ตอบในรูปแบบ JSON ตามโครงสร้างที่กำหนดในคำแนะนำระบบ`;
    } else {
        userPrompt = `Case Information:
Title: ${caseData.title}
Summary: ${caseData.summary}
Location: ${caseData.location}
Date and Time: ${caseData.dateTime}

Clue to Analyze:
Title: ${clue.title}
Description: ${clue.description}
Location Found: ${clue.location}
Type: ${clue.type}
Relevance: ${clue.relevance}

Suspects:
${suspects.map(s => `${s.name}: ${s.description}`).join('\n')}

Other Discovered Clues:
${discoveredClues.filter(c => c.id !== clue.id).map(c => `${c.title}: ${c.description}`).join('\n')}

Please analyze this clue and provide:
1. A summary of the clue's significance
2. Connections to suspects
3. Suggested next investigative steps

Respond in the JSON format specified in the system instructions.`;
    }

    // Prepare messages for API call
    const messages: OpenAIMessage[] = [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
    ];

    try {
        // Use the standard model for clue analysis
        const response = await fetchOpenAICompletion(
            messages,
            undefined,
            0.7,
            2048
        );

        // Parse the JSON response
        try {
            // First try to parse the response directly
            let jsonContent = response;
            
            // If direct parsing fails, try to extract JSON
            try {
                JSON.parse(jsonContent);
            } catch {
                // Look for JSON block in markdown or text
                const jsonMatch = response.match(/```json\n([\s\S]*?)\n```/) ||
                    response.match(/```([\s\S]*?)```/) ||
                    response.match(/({[\s\S]*})/);
                
                if (jsonMatch) {
                    jsonContent = jsonMatch[1];
                }
            }
            
            const parsedData = JSON.parse(jsonContent);

            // Format the response into our expected structure
            return formatClueAnalysis(parsedData, suspects);
        } catch (parseError) {
            console.error('Failed to parse clue analysis as JSON:', parseError);
            console.log('Raw response:', response);

            // If JSON parsing fails, try to extract information from raw text
            return extractClueAnalysisFromText(response, suspects);
        }
    } catch (apiError) {
        console.error('Failed to get clue analysis from API:', apiError);
        throw new Error('Failed to analyze clue. Please try again later.');
    }
}

/**
 * Formats the raw LLM JSON output into our ClueAnalysis structure
 */
function formatClueAnalysis(data: unknown, suspects: Suspect[]): ClueAnalysis {
    const connections: Array<{
        suspectId: string;
        connectionType: string;
        description: string;
    }> = [];

    // Process connections data
    if ((data as any).connections && Array.isArray((data as any).connections)) {
        for (const connection of (data as any).connections) {
            // Try to find the suspect this connection refers to
            const suspectName = connection.suspect || connection.suspectName || connection.name || '';
            const connectionType = connection.connectionType || connection.type || 'related';
            const description = connection.description || '';

            if (suspectName) {
                const matchedSuspect = suspects.find(s =>
                    s.name.toLowerCase().includes(suspectName.toLowerCase()) ||
                    suspectName.toLowerCase().includes(s.name.toLowerCase())
                );

                if (matchedSuspect) {
                    connections.push({
                        suspectId: matchedSuspect.id,
                        connectionType,
                        description
                    });
                }
            }
        }
    }

    // If no connections were found but there's a connections text field
    if (connections.length === 0 && typeof (data as any).connections === 'string') {
        // Try to find mentions of suspect names in the connections text
        for (const suspect of suspects) {
            if ((data as any).connections.toLowerCase().includes(suspect.name.toLowerCase())) {
                connections.push({
                    suspectId: suspect.id,
                    connectionType: 'mentioned',
                    description: (data as any).connections
                });
            }
        }
    }

    // Ensure we have a valid summary
    const summary = (data as any).summary || 'No summary available';
    
    // Process next steps - ensure it's an array
    let nextSteps: string[] = [];
    if ((data as any).nextSteps) {
        if (Array.isArray((data as any).nextSteps)) {
            nextSteps = (data as any).nextSteps;
        } else if (typeof (data as any).nextSteps === 'string') {
            // Split by newlines if it's a string
            nextSteps = [(data as any).nextSteps];
        }
    }

    return {
        summary,
        connections,
        nextSteps: nextSteps.length > 0 ? nextSteps : ['Continue investigating']
    };
}

/**
 * Falls back to extracting information from raw text when JSON parsing fails
 */
function extractClueAnalysisFromText(text: string, suspects: Suspect[]): ClueAnalysis {
    const summary = text.match(/summary[:\s]+(.*?)(?:\n|$)/i)?.[1] ||
        text.match(/significance[:\s]+(.*?)(?:\n|$)/i)?.[1] ||
        text.match(/1\.([\s\S]*?)(?:2\.|$)/)?.[1]?.trim() ||
        'Analysis unavailable';

    const connections: Array<{
        suspectId: string;
        connectionType: string;
        description: string;
    }> = [];

    // Try to extract connections by finding suspect names in the text
    for (const suspect of suspects) {
        const suspectNameIndex = text.toLowerCase().indexOf(suspect.name.toLowerCase());
        if (suspectNameIndex !== -1) {
            // Extract some context around the suspect mention
            const start = Math.max(0, suspectNameIndex - 50);
            const end = Math.min(text.length, suspectNameIndex + suspect.name.length + 100);
            const context = text.substring(start, end);

            connections.push({
                suspectId: suspect.id,
                connectionType: 'mentioned',
                description: context
            });
        }
    }

    // Try to extract next steps - look for section "3." or "Next steps"
    let nextSteps: string[] = [];
    const nextStepsRegex = /(?:3\.|next steps?)[:\s]+([\s\S]*?)(?:\n\n|$)/i;
    const nextStepsMatch = text.match(nextStepsRegex);
    
    if (nextStepsMatch && nextStepsMatch[1]) {
        nextSteps = nextStepsMatch[1]
            .split(/\n|-|\*/)  // Split by newlines or bullet points
            .map(s => s.trim())
            .filter(s => s.length > 0); // Remove empty lines
    }
    
    if (nextSteps.length === 0) {
        nextSteps = ['Continue investigating'];
    }

    return {
        summary,
        connections,
        nextSteps
    };
} 