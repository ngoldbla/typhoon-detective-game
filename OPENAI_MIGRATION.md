# OpenAI Migration Guide

This document describes the changes made to adapt the Typhoon Detective Game to use OpenAI instead of the Typhoon AI API.

## Overview

The game has been successfully migrated from Typhoon AI to OpenAI. All AI-powered features now use OpenAI's GPT models, specifically `gpt-4o` as the default model.

## Changes Made

### 1. Environment Variables

**File:** `.env.example`

The environment variables have been updated to use OpenAI:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here

# Optional: Override the OpenAI base URL (useful for proxies, Azure OpenAI, or compatible APIs)
# Default: https://api.openai.com/v1
OPENAI_BASE_URL=https://api.openai.com/v1

# Optional: Choose the default OpenAI model
# Options: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo, o1-preview, o1-mini
# Default: gpt-4o
OPENAI_MODEL=gpt-4o
```

**Setup Instructions:**

1. Create a `.env.local` file in the root directory
2. Add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=sk-...your-api-key-here
   ```
3. (Optional) Configure the base URL for custom endpoints:
   ```bash
   # For OpenAI API (default)
   OPENAI_BASE_URL=https://api.openai.com/v1

   # For Azure OpenAI
   OPENAI_BASE_URL=https://your-resource.openai.azure.com

   # For OpenAI-compatible APIs (e.g., LocalAI, LM Studio)
   OPENAI_BASE_URL=http://localhost:1234/v1
   ```
4. (Optional) Choose your preferred model:
   ```bash
   # Use GPT-4o (default, best quality)
   OPENAI_MODEL=gpt-4o

   # Or use a faster/cheaper alternative
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_MODEL=gpt-3.5-turbo

   # Or use reasoning models
   OPENAI_MODEL=o1-preview
   OPENAI_MODEL=o1-mini
   ```

### 2. API Route

**File:** `src/app/api/typhoon/route.ts`

The API route has been updated to:
- Call OpenAI's API instead of Typhoon
- Support multiple OpenAI models: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`, `o1-preview`, `o1-mini`
- Handle OpenAI's o1 model requirements (uses `max_completion_tokens` instead of `temperature` and `max_tokens`)
- Default model is now `gpt-4o`

### 3. Core Library Files

**File:** `src/lib/typhoon.ts`

This file has been renamed conceptually to use OpenAI:
- Type `TyphoonModel` → `OpenAIModel`
- Type `TyphoonMessage` → `OpenAIMessage`
- Type `TyphoonResponse` → `OpenAIResponse`
- Function `fetchTyphoonCompletion` → `fetchOpenAICompletion`
- Default model: `gpt-4o`

**Files Updated:**
- `src/lib/caseGenerator.ts` - Case generation using GPT-4o
- `src/lib/suspectAnalyzer.ts` - Suspect analysis and interviews using GPT-4o
- `src/lib/clueAnalyzer.ts` - Clue analysis using GPT-4o
- `src/lib/caseSolver.ts` - Solution validation using GPT-4o
- `src/lib/translator.ts` - Translation using GPT-4o

### 4. React Hook

**File:** `src/hooks/useTyphoon.ts`

Updated to use OpenAI types and models while maintaining the same function name for backward compatibility:
- Interface `UseTyphoonOptions` → `UseOpenAIOptions`
- Uses `OpenAIMessage` and `OpenAIModel` types
- Default model: `gpt-4o`

### 5. Configuration API

**File:** `src/app/api/config/route.ts`

Updated to reflect OpenAI models and expose configuration:
```typescript
models: {
  default: process.env.OPENAI_MODEL || 'gpt-4o',
  advanced: process.env.OPENAI_MODEL || 'gpt-4o',
  available: ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo', 'o1-preview', 'o1-mini']
}
```

## Configuration Options

### Base URL Configuration

The `OPENAI_BASE_URL` environment variable allows you to customize the API endpoint. This is useful for:

1. **Using Azure OpenAI**:
   ```bash
   OPENAI_BASE_URL=https://your-resource.openai.azure.com
   OPENAI_API_KEY=your-azure-key
   ```

2. **Using OpenAI-compatible APIs** (LocalAI, LM Studio, Ollama with OpenAI compatibility, etc.):
   ```bash
   OPENAI_BASE_URL=http://localhost:1234/v1
   # API key may not be required for local APIs
   OPENAI_API_KEY=not-needed
   ```

3. **Using a proxy or custom gateway**:
   ```bash
   OPENAI_BASE_URL=https://your-proxy.example.com/v1
   OPENAI_API_KEY=your-api-key
   ```

The base URL should NOT include `/chat/completions` - that path is automatically appended.

### Model Selection

The `OPENAI_MODEL` environment variable sets the default model for all AI operations. You can override this in your `.env.local`:

```bash
# For best quality (most expensive)
OPENAI_MODEL=gpt-4o

# For balanced performance and cost
OPENAI_MODEL=gpt-4o-mini

# For fastest response time (cheapest)
OPENAI_MODEL=gpt-3.5-turbo

# For advanced reasoning
OPENAI_MODEL=o1-preview
```

**Note**: If you don't set `OPENAI_MODEL`, it defaults to `gpt-4o`.

## Supported Models

The following OpenAI models are supported:

1. **gpt-4o** (default) - Latest GPT-4 optimized model
2. **gpt-4o-mini** - Smaller, faster GPT-4o variant
3. **gpt-4-turbo** - GPT-4 Turbo model
4. **gpt-4** - Standard GPT-4
5. **gpt-3.5-turbo** - Fast, cost-effective option
6. **o1-preview** - Reasoning model (preview)
7. **o1-mini** - Smaller reasoning model

## Token Allocations

The following token limits are used for different features:

- **Case Generation**: 8,192 tokens (longest generation)
- **Suspect Analysis**: 2,048 tokens
- **Clue Analysis**: 2,048 tokens
- **Interview Responses**: 2,048 tokens
- **Solution Validation**: 2,048 tokens
- **Translation**: 2,048 tokens

## Temperature Settings

All features use a temperature of `0.7` for balanced creativity and determinism.

## API Compatibility

The OpenAI API is compatible with the previous Typhoon API structure because both follow the OpenAI-compatible chat completions format. The main differences handled are:

1. **Authentication**: Changed from `TYPHOON_API_KEY` to `OPENAI_API_KEY`
2. **Endpoint**: Changed to OpenAI's endpoint
3. **Model names**: Changed to OpenAI model identifiers
4. **o1 models**: Special handling for reasoning models that don't support temperature

## Testing

To test the integration:

1. Set up your OpenAI API key in `.env.local`
2. Run the development server: `npm run dev`
3. Try creating a new case at `/cases/new`
4. Interview suspects and analyze clues
5. Submit a solution to verify the full flow

## Cost Considerations

OpenAI pricing differs from Typhoon. Current usage patterns:

- Case generation: ~8K tokens (most expensive operation)
- Per-interview: ~2K tokens
- Per-analysis: ~2K tokens

Monitor your OpenAI usage dashboard to track costs.

## Backward Compatibility

The migration maintains backward compatibility by:
- Keeping the `/api/typhoon` endpoint path
- Maintaining the `useTyphoon` hook name
- Using the same message format and response structure

This allows the game to function without breaking existing component code.

## Future Improvements

Potential enhancements:
1. Add model selection in settings UI
2. Implement streaming responses for better UX
3. Add retry logic with exponential backoff
4. Implement response caching for repeated queries
5. Add usage tracking and cost estimation

## Troubleshooting

**Error: "API key for OpenAI is missing"**
- Ensure `.env.local` exists with valid `OPENAI_API_KEY`
- Restart the development server after adding the key

**Error: "Invalid model"**
- Check that the model name matches one of the supported models
- Verify the model is available in your OpenAI account

**Error: Rate limit exceeded**
- OpenAI has rate limits based on your account tier
- Implement retry logic or upgrade your account

**Error: Token limit exceeded**
- Reduce the max_tokens parameter in individual features
- Consider using a model with larger context windows

## Support

For issues related to:
- **OpenAI API**: Consult [OpenAI Documentation](https://platform.openai.com/docs)
- **Game functionality**: Check the main README and repository issues
