export type OpenAIModel = 'gpt-5' | 'gpt-4o' | 'gpt-4o-mini' | 'gpt-4-turbo' | 'gpt-4' | 'gpt-3.5-turbo' | 'o1-preview' | 'o1-mini' | string;

export interface OpenAIMessage {
    role: 'system' | 'user' | 'assistant';
    content: string;
}

export interface OpenAIResponse {
    id: string;
    object: string;
    created: number;
    model: string;
    choices: {
        index: number;
        message: {
            role: string;
            content: string;
        };
        finish_reason: string;
    }[];
    usage: {
        prompt_tokens: number;
        completion_tokens: number;
        total_tokens: number;
    };
}

import { withRetry } from './retry';

export async function fetchOpenAICompletion(
    messages: OpenAIMessage[],
    model?: OpenAIModel,
    temperature: number = 0.7,
    max_tokens: number = 800,
    enableRetry: boolean = true
): Promise<string> {
    const makeRequest = async (): Promise<string> => {
        console.log(`Calling OpenAI API with model: ${model}`);

        // Get base URL for the API endpoint
        const baseUrl = typeof window !== 'undefined'
            ? window.location.origin
            : process.env.NEXT_PUBLIC_BASE_URL || '';

        const apiUrl = `${baseUrl}/api/typhoon`;

        const controller = new AbortController();

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                messages,
                model,
                temperature,
                max_tokens,
            }),
            signal: controller.signal
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`OpenAI API error: Status ${response.status}`, errorText);
            throw new Error(`OpenAI API error (${response.status}): ${errorText}`);
        }

        const data = await response.json();

        if (!data.response) {
            console.error('Server API returned invalid response:', data);
            throw new Error('Received invalid response from server');
        }

        return data.response;
    };

    try {
        if (enableRetry) {
            // Use retry logic for more robust API calls
            return await withRetry(makeRequest, {
                maxAttempts: 3,
                delayMs: 1000,
                backoffMultiplier: 2,
                retryableStatuses: [408, 429, 500, 502, 503, 504],
                onRetry: (attempt, error) => {
                    console.log(`Retrying OpenAI API call (attempt ${attempt}):`, error.message);
                }
            });
        } else {
            return await makeRequest();
        }
    } catch (error) {
        console.error('Error calling OpenAI API:', error);
        if (error instanceof DOMException && error.name === 'AbortError') {
            throw new Error('Request timed out. The server took too long to respond.');
        }
        throw error;
    }
} 