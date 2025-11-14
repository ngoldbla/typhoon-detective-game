import { NextRequest, NextResponse } from 'next/server';

// Configurable values with defaults
// Support both new generic names and legacy Typhoon-specific names
const LLM_API_ENDPOINT = process.env.LLM_API_ENDPOINT || process.env.TYPHOON_API_ENDPOINT || 'https://api.opentyphoon.ai/v1/chat/completions';
const DEFAULT_MODEL = process.env.LLM_MODEL || 'typhoon-v2.1-12b-instruct';

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { messages, model = DEFAULT_MODEL, temperature = 0.7, max_tokens = 800 } = body;

        if (!messages || !Array.isArray(messages)) {
            console.error('API route error: Invalid messages format', messages);
            return NextResponse.json(
                { error: 'Invalid messages format. Messages should be an array.' },
                { status: 400 }
            );
        }

        console.log(`API route processing request for model: ${model}`);

        // Support both new LLM_API_KEY and legacy TYPHOON_API_KEY
        const apiKey = process.env.LLM_API_KEY || process.env.TYPHOON_API_KEY;

        if (!apiKey) {
            console.error('LLM_API_KEY (or TYPHOON_API_KEY) is not defined in environment variables');
            return NextResponse.json(
                { error: 'API key is missing. Please set LLM_API_KEY in your environment variables.' },
                { status: 500 }
            );
        }

        // Set up timeout controller
        const controller = new AbortController();

        try {
            const llmResponse = await fetch(LLM_API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`,
                },
                body: JSON.stringify({
                    model,
                    messages,
                    temperature,
                    max_tokens,
                }),
                signal: controller.signal
            });
            if (!llmResponse.ok) {
                const errorText = await llmResponse.text();
                console.error(`LLM API error: Status ${llmResponse.status}`, errorText);
                return NextResponse.json(
                    { error: `LLM API error (${llmResponse.status}): ${errorText}` },
                    { status: llmResponse.status }
                );
            }

            const data = await llmResponse.json();

            if (!data.choices || data.choices.length === 0) {
                console.error('LLM API returned no choices:', data);
                return NextResponse.json(
                    { error: 'Received invalid response from LLM API' },
                    { status: 500 }
                );
            }

            let content = data.choices[0]?.message?.content || '';

            // Filter out <think> tags for reasoning models (e.g., typhoon-v2-r1, o1-preview)
            if (model.includes('-r1-') || model.includes('o1-')) {
                content = content.replace(/<think>[\s\S]*?<\/think>/g, '');
            }

            return NextResponse.json({ response: content });
        } catch (fetchError) {
            if (fetchError instanceof DOMException && fetchError.name === 'AbortError') {
                return NextResponse.json(
                    { error: 'LLM API request timed out' },
                    { status: 504 }
                );
            }
            throw fetchError;
        }
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
        console.error('API route error:', errorMessage);

        return NextResponse.json(
            { error: errorMessage },
            { status: 500 }
        );
    }
} 