import { Suspect, Clue, Case } from '@/types/game';

/**
 * Processes an interview question using the Python API route
 */
export async function processInterviewQuestion(
    question: string,
    suspect: Suspect,
    clues: Clue[],
    caseData: Case,
    previousQuestions: { question: string, answer: string }[],
    language: 'en' | 'th'
): Promise<string> {
    try {
        console.log("Calling Python API for suspect interview");

        const response = await fetch('/api/python/interview-suspect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question,
                suspect,
                clues,
                case: caseData,
                previousQuestions,
                language
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: `HTTP error ${response.status}` }));
            throw new Error(errorData.error || 'Failed to process interview question');
        }

        const data = await response.json();
        return data.answer;
    } catch (error) {
        console.error('Interview error:', error);
        throw new Error('Failed to process interview question. Please try again later.');
    }
}
