import { ClueAnalysis, Clue, Suspect, Case } from '@/types/game';

/**
 * Analyzes a clue using the Python API route
 */
export async function analyzeClue(
    clue: Clue,
    suspects: Suspect[],
    caseData: Case,
    discoveredClues: Clue[],
    language: 'en' | 'th'
): Promise<ClueAnalysis> {
    try {
        console.log("Calling Python API for clue analysis");

        const response = await fetch('/api/python/analyze-clue', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                clue,
                suspects,
                case: caseData,
                discoveredClues,
                language
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: `HTTP error ${response.status}` }));
            throw new Error(errorData.error || 'Failed to analyze clue');
        }

        const data = await response.json();
        return data as ClueAnalysis;
    } catch (error) {
        console.error('Clue analysis error:', error);
        throw new Error('Failed to analyze clue. Please try again later.');
    }
}
