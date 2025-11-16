import { CaseSolution, Case, Suspect, Clue } from '@/types/game';

/**
 * Analyzes a solution using the Python API route
 */
export async function analyzeSolution(
    caseData: Case,
    suspects: Suspect[],
    clues: Clue[],
    accusedSuspectId: string,
    evidenceIds: string[],
    reasoning: string,
    language: 'en' | 'th'
): Promise<CaseSolution> {
    try {
        console.log("Calling Python API for solution analysis");

        const response = await fetch('/api/python/solve-case', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                case: caseData,
                suspects,
                clues,
                accusedSuspectId,
                evidenceIds,
                reasoning,
                language
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: `HTTP error ${response.status}` }));
            throw new Error(errorData.error || 'Failed to analyze solution');
        }

        const data = await response.json();
        return data as CaseSolution;
    } catch (error) {
        console.error('Solution analysis error:', error);
        throw new Error('Failed to analyze solution. Please try again later.');
    }
}
