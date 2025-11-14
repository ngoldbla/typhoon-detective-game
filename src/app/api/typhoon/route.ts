import { NextRequest, NextResponse } from 'next/server';

// Configurable values with defaults
const OPENAI_BASE_URL = process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1';
const DEFAULT_MODEL = process.env.OPENAI_MODEL || 'gpt-4o';

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

        // Skip model validation when using custom base URLs, as they may support different models
        // Only validate for standard OpenAI endpoint
        if (OPENAI_BASE_URL === 'https://api.openai.com/v1') {
            const validModels = ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo', 'o1-preview', 'o1-mini'];
            if (!validModels.includes(model)) {
                console.error('API route error: Invalid model', model);
                return NextResponse.json(
                    { error: `Invalid model. Must be one of: ${validModels.join(', ')}.` },
                    { status: 400 }
                );
            }
        }

        console.log(`API route processing request for model: ${model}`);

        // Call OpenAI API directly from the server
        const apiKey = process.env.OPENAI_API_KEY;

        if (!apiKey) {
            console.error('OPENAI_API_KEY is not defined in environment variables');
            return NextResponse.json(
                { error: 'API key for OpenAI is missing. Please check your server configuration.' },
                { status: 500 }
            );
        }

        // Set up timeout controller
        const controller = new AbortController();

        try {
            // OpenAI o1 models don't support temperature or max_tokens, they use max_completion_tokens
            const isO1Model = model.startsWith('o1-');
            // gpt-5 models only support temperature=1
            const isGpt5Model = model.toLowerCase().includes('gpt-5');
            const requestBody: any = {
                model,
                messages,
            };

            if (isO1Model) {
                // o1 models use max_completion_tokens instead
                requestBody.max_completion_tokens = max_tokens;
            } else {
                // Standard models use temperature and max_tokens
                // gpt-5 models require temperature=1
                requestBody.temperature = isGpt5Model ? 1.0 : temperature;
                requestBody.max_tokens = max_tokens;
            }

            // Construct the full endpoint URL
            const endpoint = `${OPENAI_BASE_URL}/chat/completions`;

            const openaiResponse = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`,
                },
                body: JSON.stringify(requestBody),
                signal: controller.signal
            });
            if (!openaiResponse.ok) {
                const errorText = await openaiResponse.text();
                console.error(`OpenAI API error: Status ${openaiResponse.status}`, errorText);
                return NextResponse.json(
                    { error: `OpenAI API error (${openaiResponse.status}): ${errorText}` },
                    { status: openaiResponse.status }
                );
            }

            const data = await openaiResponse.json();

            if (!data.choices || data.choices.length === 0) {
                console.error('OpenAI API returned no choices:', data);
                return NextResponse.json(
                    { error: 'Received invalid response from OpenAI API' },
                    { status: 500 }
                );
            }

            const content = data.choices[0]?.message?.content || '';

            return NextResponse.json({ response: content });
        } catch (fetchError) {
            if (fetchError instanceof DOMException && fetchError.name === 'AbortError') {
                return NextResponse.json(
                    { error: 'OpenAI API request timed out' },
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