// Support any model name - can be used with any OpenAI-compatible API
export type TyphoonModel = string;

export interface TyphoonMessage {
    role: 'system' | 'user' | 'assistant';
    content: string;
}

export interface TyphoonResponse {
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

// Get default model from environment or use fallback
const DEFAULT_MODEL = 'typhoon-v2.1-12b-instruct';

export async function fetchTyphoonCompletion(
    messages: TyphoonMessage[],
    model?: TyphoonModel,
    temperature: number = 0.7,
    max_tokens: number = 800
): Promise<string> {
    // Use provided model or default
    const modelToUse = model || DEFAULT_MODEL;
    try {
        console.log(`Calling LLM API with model: ${modelToUse}`);

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
                model: modelToUse,
                temperature,
                max_tokens,
            }),
            signal: controller.signal
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`LLM API error: Status ${response.status}`, errorText);
            throw new Error(`LLM API error (${response.status}): ${errorText}`);
        }

        const data = await response.json();

        if (!data.response) {
            console.error('Server API returned invalid response:', data);
            throw new Error('Received invalid response from server');
        }

        return data.response;
    } catch (error) {
        console.error('Error calling LLM API:', error);
        if (error instanceof DOMException && error.name === 'AbortError') {
            throw new Error('Request timed out. The server took too long to respond.');
        }
        throw error;
    }
} 