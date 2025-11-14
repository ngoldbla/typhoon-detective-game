import { NextRequest, NextResponse } from 'next/server';

export async function GET(_request: NextRequest) {
    // Get the configured model from environment or use default
    const defaultModel = process.env.OPENAI_MODEL || 'gpt-4o';

    // Basic config that can be exposed to the client
    const config = {
        apiVersion: '1.0.0',
        features: {
            multiLanguage: true,
            darkMode: true,
            debugMode: process.env.NODE_ENV === 'development'
        },
        models: {
            default: defaultModel,
            advanced: defaultModel,
            available: ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo', 'o1-preview', 'o1-mini']
        },
        maxGenerationLength: 1000
    };

    return NextResponse.json(config);
} 