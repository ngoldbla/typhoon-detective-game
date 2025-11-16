import { fetchOpenAICompletion, OpenAIMessage } from './typhoon';
import { SuspectAnalysis, Suspect, Clue, Case, Interview } from '@/types/game';

// System prompts for suspect analysis
const SUSPECT_ANALYSIS_PROMPT_EN = `You are helping a 7-year-old child solve a fun mystery!
You need to look at a person and the clues to help figure out what happened.

Remember: Use SIMPLE words a 7-year-old can read. Keep it FUN and friendly!

Tell me:
1. How much can we trust what this person says? (Give a number from 0 to 100, where 100 means we can trust them a lot)
2. Are there things in their story that don't match up? (Use simple words!)
3. Which clues are connected to this person?
4. What questions should we ask this person next? (Keep questions simple!)

Make it fun and easy to understand. Remember this is for a child!`;

const SUSPECT_ANALYSIS_PROMPT_TH = `คุณกำลังช่วยเด็กอายุ 7 ขวบแก้ปริศนาสนุกๆ!
คุณต้องดูที่คนและเบาะแสเพื่อช่วยหาว่าเกิดอะไรขึ้น

จำไว้: ใช้คำง่ายๆ ที่เด็ก 7 ขวบอ่านได้ ทำให้สนุกและเป็นมิตร!

บอกฉัน:
1. เราเชื่อคำพูดของคนนี้ได้แค่ไหน? (ให้ตัวเลข 0 ถึง 100 โดย 100 หมายความว่าเราเชื่อเขามาก)
2. มีอะไรในเรื่องของเขาที่ไม่ตรงกันไหม? (ใช้คำง่ายๆ!)
3. เบาะแสไหนเชื่อมโยงกับคนนี้?
4. เราควรถามคำถามอะไรกับคนนี้ต่อไป? (ให้คำถามง่ายๆ!)

ทำให้สนุกและเข้าใจง่าย จำไว้ว่านี่สำหรับเด็ก!`;

/**
 * Analyzes a suspect in the context of a case using the Typhoon LLM
 */
export async function analyzeSuspect(
    suspect: Suspect,
    clues: Clue[],
    caseData: Case,
    interview: Interview | null,
    language: 'en' | 'th'
): Promise<SuspectAnalysis> {
    // Choose appropriate prompt based on language
    const systemPrompt = language === 'th' ? SUSPECT_ANALYSIS_PROMPT_TH : SUSPECT_ANALYSIS_PROMPT_EN;

    // Create user prompt with case context
    let userPrompt = '';

    if (language === 'th') {
        userPrompt = `ข้อมูลคดี:
ชื่อคดี: ${caseData.title}
สรุป: ${caseData.summary}
สถานที่: ${caseData.location}
วันที่และเวลา: ${caseData.dateTime}

ผู้ต้องสงสัยที่ต้องการวิเคราะห์:
ชื่อ: ${suspect.name}
คำอธิบาย: ${suspect.description}
ประวัติ: ${suspect.background}
แรงจูงใจที่เป็นไปได้: ${suspect.motive}
ข้ออ้างที่อยู่: ${suspect.alibi}

หลักฐานที่พบ:
${clues.map(c => `${c.title}: ${c.description} (พบที่: ${c.location})`).join('\n')}`;

        // Add interview data if available
        if (interview && interview.questions.some(q => q.asked)) {
            userPrompt += `\n\nบันทึกการสัมภาษณ์:
${interview.questions.filter(q => q.asked).map(q => `คำถาม: ${q.question}\nคำตอบ: ${q.answer}`).join('\n\n')}`;
        }

        userPrompt += `\n\nกรุณาวิเคราะห์ผู้ต้องสงสัยนี้และให้:
1. การประเมินความน่าเชื่อถือของผู้ต้องสงสัย (ในระดับ 0-100)
2. ความไม่สอดคล้องที่อาจเกิดขึ้นในเรื่องราวหรือประวัติของพวกเขา
3. ความเชื่อมโยงกับหลักฐานที่ค้นพบ
4. คำถามที่แนะนำสำหรับการสอบสวนเพิ่มเติม

ตอบในรูปแบบ JSON ที่มีโครงสร้างซึ่งสามารถแปลงโดย JavaScript ได้`;
    } else {
        userPrompt = `Case Information:
Title: ${caseData.title}
Summary: ${caseData.summary}
Location: ${caseData.location}
Date and Time: ${caseData.dateTime}

Suspect to Analyze:
Name: ${suspect.name}
Description: ${suspect.description}
Background: ${suspect.background}
Possible Motive: ${suspect.motive}
Alibi: ${suspect.alibi}

Discovered Clues:
${clues.map(c => `${c.title}: ${c.description} (Found at: ${c.location})`).join('\n')}`;

        // Add interview data if available
        if (interview && interview.questions.some(q => q.asked)) {
            userPrompt += `\n\nInterview Records:
${interview.questions.filter(q => q.asked).map(q => `Question: ${q.question}\nAnswer: ${q.answer}`).join('\n\n')}`;
        }

        userPrompt += `\n\nPlease analyze this suspect and provide:
1. Assessment of the suspect's trustworthiness (on a scale of 0-100)
2. Potential inconsistencies in their story or background
3. Connections to discovered clues
4. Suggested questions for further interrogation

Respond in a structured JSON format that can be parsed by JavaScript.`;
    }

    // Prepare messages for API call
    const messages: OpenAIMessage[] = [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
    ];

    // Use the standard model for suspect analysis
    const response = await fetchOpenAICompletion(
        messages,
        undefined,
        0.7,
        2048
    );

    // Parse the JSON response
    try {
        // Use a fallback technique to extract JSON if direct parsing fails
        const jsonMatch = response.match(/```json\n([\s\S]*?)\n```/) ||
            response.match(/```([\s\S]*?)```/) ||
            response.match(/({[\s\S]*})/);

        const jsonContent = jsonMatch ? jsonMatch[1] : response;
        const parsedData = JSON.parse(jsonContent);

        // Format the response into our expected structure
        return formatSuspectAnalysis(parsedData, clues, suspect.id);
    } catch (error) {
        console.error('Failed to parse suspect analysis:', error);

        // If JSON parsing fails, try to extract information from raw text
        return extractSuspectAnalysisFromText(response, clues, suspect.id);
    }
}

/**
 * Processes an interview question and generates a realistic response
 */
export async function processInterviewQuestion(
    question: string,
    suspect: Suspect,
    clues: Clue[],
    caseData: Case,
    previousQuestions: { question: string, answer: string }[],
    language: 'en' | 'th'
): Promise<string> {
    // System prompt for generating interview responses
    const systemPrompt = language === 'th'
        ? `คุณเป็น${suspect.name} ตอบคำถามด้วยคำง่ายๆ ที่เด็ก 7 ขวบเข้าใจได้ เป็นมิตรและสุภาพ`
        : `You are ${suspect.name}. Answer questions using simple words that a 7-year-old can understand. Be friendly and polite.`;

    // Create context message
    let contextMessage = '';

    if (language === 'th') {
        contextMessage = `ข้อมูลของคุณ:
ชื่อ: ${suspect.name}
คำอธิบาย: ${suspect.description}
ประวัติ: ${suspect.background}
เหตุผล: ${suspect.motive}
เรื่องของคุณ: ${suspect.alibi}

สิ่งสำคัญ:
- ${suspect.isGuilty ? 'คุณทำสิ่งนี้จริง แต่คุณไม่ได้ตั้งใจทำผิด' : 'คุณไม่ได้ทำ แต่คุณอาจมีเรื่องที่คุณอาย'}
- ตอบด้วยคำง่ายๆ ที่เด็กเข้าใจ
- อย่าบอกตรงๆ ว่าคุณทำหรือไม่ทำ
- ทำตัวเป็นธรรมชาติและเป็นมิตร`;
    } else {
        contextMessage = `Your information:
Name: ${suspect.name}
Description: ${suspect.description}
Background: ${suspect.background}
Reason: ${suspect.motive}
Your story: ${suspect.alibi}

Important rules:
- ${suspect.isGuilty ? 'You did this thing, but you didn\'t mean to do anything wrong' : 'You didn\'t do it, but you might have something you\'re embarrassed about'}
- Answer using simple words that children can understand
- Don\'t say directly if you did it or didn\'t do it
- Act natural and friendly`;
    }

    // Prepare the conversation history
    const messages: OpenAIMessage[] = [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: contextMessage },
    ];

    // Add previous questions to conversation history
    for (const prevQ of previousQuestions) {
        messages.push({ role: 'user', content: prevQ.question });
        messages.push({ role: 'assistant', content: prevQ.answer });
    }

    // Add the current question
    messages.push({ role: 'user', content: question });

    const response = await fetchOpenAICompletion(
        messages,
        undefined,
        0.7,
        2048
    );

    return response;
}

/**
 * Formats the raw LLM JSON output into our SuspectAnalysis structure
 */
function formatSuspectAnalysis(data: unknown, clues: Clue[], suspectId: string): SuspectAnalysis {
    const connections: SuspectAnalysis['connections'] = [];

    // Process connections data
    if ((data as any).connections && Array.isArray((data as any).connections)) {
        for (const connection of (data as any).connections) {
            // Try to find the clue this connection refers to
            const clueTitle = connection.clue || connection.clueTitle || connection.title;
            const connectionType = connection.type || connection.connectionType || 'related';
            const description = connection.description || '';

            const matchedClue = clues.find(c =>
                c.title.toLowerCase().includes(clueTitle.toLowerCase()) ||
                clueTitle.toLowerCase().includes(c.title.toLowerCase())
            );

            if (matchedClue) {
                connections.push({
                    clueId: matchedClue.id,
                    connectionType,
                    description
                });
            }
        }
    }

    // Ensure trustworthiness is within range
    let trustworthiness = typeof (data as any).trustworthiness === 'number'
        ? (data as any).trustworthiness
        : parseInt((data as any).trustworthiness);

    if (isNaN(trustworthiness)) {
        trustworthiness = 50; // Default if not a number
    } else {
        trustworthiness = Math.max(0, Math.min(100, trustworthiness)); // Clamp between 0-100
    }

    // Process inconsistencies
    let inconsistencies: string[] = [];
    if (Array.isArray((data as any).inconsistencies)) {
        inconsistencies = (data as any).inconsistencies;
    } else if (typeof (data as any).inconsistencies === 'string') {
        inconsistencies = [(data as any).inconsistencies];
    }

    // Process suggested questions
    let suggestedQuestions: string[] = [];
    if (Array.isArray((data as any).suggestedQuestions)) {
        suggestedQuestions = (data as any).suggestedQuestions;
    } else if (typeof (data as any).suggestedQuestions === 'string') {
        suggestedQuestions = [(data as any).suggestedQuestions];
    }

    return {
        suspectId,
        trustworthiness,
        inconsistencies,
        connections,
        suggestedQuestions
    };
}

/**
 * Falls back to extracting information from raw text when JSON parsing fails
 */
function extractSuspectAnalysisFromText(text: string, clues: Clue[], suspectId: string): SuspectAnalysis {
    // Extract trustworthiness
    const trustworthinessMatch = text.match(/trustworthiness[:\s]+(\d+)/i);
    const trustworthiness = trustworthinessMatch ? parseInt(trustworthinessMatch[1]) : 50;

    // Extract inconsistencies
    const inconsistenciesSection = text.match(/inconsistencies[:\s]+([\s\S]*?)(?=\n\n|connections|$)/i);
    let inconsistencies: string[] = [];

    if (inconsistenciesSection) {
        inconsistencies = inconsistenciesSection[1]
            .split(/\n/) // Split by newlines
            .map(s => s.replace(/^[-*]\s*/, '').trim()) // Remove bullet points
            .filter(s => s.length > 0); // Remove empty lines
    }

    // Extract connections to clues
    const connections: SuspectAnalysis['connections'] = [];
    for (const clue of clues) {
        if (text.toLowerCase().includes(clue.title.toLowerCase())) {
            connections.push({
                clueId: clue.id,
                connectionType: 'mentioned',
                description: `The suspect may be connected to the ${clue.title}`
            });
        }
    }

    // Extract suggested questions
    const questionsSection = text.match(/questions[:\s]+([\s\S]*?)(?=\n\n|$)/i);
    let suggestedQuestions: string[] = [];

    if (questionsSection) {
        suggestedQuestions = questionsSection[1]
            .split(/\n/) // Split by newlines
            .map(s => s.replace(/^[-*]\s*/, '').trim()) // Remove bullet points
            .filter(s => s.length > 0 && s.includes('?')); // Keep only question lines
    }

    if (suggestedQuestions.length === 0) {
        // If no questions were extracted, create some generic ones
        suggestedQuestions = [
            "Can you provide more details about your alibi?",
            "Where were you at the time of the incident?",
            "Do you know any of the other suspects?"
        ];
    }

    return {
        suspectId,
        trustworthiness,
        inconsistencies,
        connections,
        suggestedQuestions
    };
} 