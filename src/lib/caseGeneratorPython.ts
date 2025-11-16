import { CaseGenerationParams, GeneratedCase } from '@/types/game';

/**
 * Generates a detective case using the Python API route
 */
export async function generateCase(params: CaseGenerationParams): Promise<GeneratedCase> {
    try {
        console.log("Calling Python API for case generation:", params);

        const response = await fetch('/api/python/generate-case', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: `HTTP error ${response.status}` }));
            throw new Error(errorData.error || `Failed to generate case: ${response.status}`);
        }

        const data = await response.json();

        console.log("Successfully generated case");

        return data as GeneratedCase;
    } catch (error) {
        console.error('Case generation error:', error);
        throw error;
    }
}
