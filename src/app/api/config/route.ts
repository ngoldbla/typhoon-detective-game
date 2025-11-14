import { NextRequest, NextResponse } from 'next/server';

const DEFAULT_MODEL = process.env.LLM_MODEL || 'typhoon-v2.1-12b-instruct';

export async function GET(_request: NextRequest) {
    // Basic config that can be exposed to the client
    const config = {
        apiVersion: '1.0.0',
        features: {
            multiLanguage: true,
            darkMode: true,
            debugMode: process.env.NODE_ENV === 'development'
        },
        models: {
            default: DEFAULT_MODEL,
            advanced: DEFAULT_MODEL
        },
        maxGenerationLength: 1000
    };

    return NextResponse.json(config);
} 