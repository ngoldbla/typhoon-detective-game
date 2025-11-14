# Quick Setup Guide

This guide will help you quickly set up the Typhoon Detective Game with OpenAI.

## Prerequisites

- Node.js 18+ installed
- An OpenAI API key (or compatible API)

## Quick Start

### 1. Get Your API Key

**For OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-`)

**For Azure OpenAI:**
1. Get your Azure OpenAI endpoint and key from Azure Portal
2. You'll need both the endpoint URL and API key

**For Local APIs (LocalAI, LM Studio, etc.):**
1. Start your local API server
2. Note the base URL (e.g., `http://localhost:1234/v1`)

### 2. Configure Environment

Create a `.env.local` file in the project root:

```bash
# Basic setup (OpenAI)
OPENAI_API_KEY=sk-your-api-key-here

# Optional: Choose a different model (default is gpt-4o)
OPENAI_MODEL=gpt-4o-mini

# Optional: Use a custom base URL
# OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3. Install Dependencies

```bash
npm install
```

### 4. Run Development Server

```bash
npm run dev
```

### 5. Open in Browser

Visit http://localhost:3000

## Common Configurations

### Configuration 1: OpenAI (Default)

Best quality, most expensive:

```bash
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
```

### Configuration 2: OpenAI (Budget-Friendly)

Good quality, lower cost:

```bash
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
# or
OPENAI_MODEL=gpt-3.5-turbo
```

### Configuration 3: Azure OpenAI

```bash
OPENAI_API_KEY=your-azure-key
OPENAI_BASE_URL=https://your-resource.openai.azure.com
OPENAI_MODEL=gpt-4o
```

### Configuration 4: Local API (Free)

For LocalAI, LM Studio, or Ollama:

```bash
OPENAI_API_KEY=not-needed
OPENAI_BASE_URL=http://localhost:1234/v1
OPENAI_MODEL=gpt-3.5-turbo
# Use whatever model name your local API expects
```

## Testing Your Setup

1. Navigate to http://localhost:3000/cases/new
2. Click "Generate Case" to create a new detective case
3. If successful, you'll see a case with suspects and clues
4. Try interviewing a suspect to test the full flow

## Troubleshooting

### Error: "API key for OpenAI is missing"

**Solution**:
- Ensure `.env.local` exists in the project root
- Verify `OPENAI_API_KEY` is set correctly
- Restart the dev server after creating/editing `.env.local`

### Error: "Invalid model"

**Solution**:
- Check your `OPENAI_MODEL` value matches one of: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`, `o1-preview`, `o1-mini`
- For local APIs, you may need to use a different model name

### Error: "OpenAI API error (401)"

**Solution**:
- Your API key is invalid or expired
- Get a new API key from OpenAI dashboard
- For Azure, check your endpoint URL and key are correct

### Error: "OpenAI API error (429)"

**Solution**:
- You've hit rate limits
- Wait a few minutes and try again
- Consider upgrading your OpenAI account tier
- Switch to a less expensive model (`gpt-4o-mini` or `gpt-3.5-turbo`)

### Error: "fetch failed" or connection errors

**Solution**:
- For local APIs: Ensure your local server is running
- Check your `OPENAI_BASE_URL` is correct
- Verify there's no firewall blocking the connection

### Case generation takes too long

**Solution**:
- Switch to a faster model: `gpt-3.5-turbo` or `gpt-4o-mini`
- Check your internet connection
- For local APIs, ensure sufficient GPU/CPU resources

## Cost Estimation

Approximate costs per game session (using OpenAI pricing):

**Using gpt-4o:**
- Case generation: ~$0.10
- Per suspect interview: ~$0.02
- Per clue analysis: ~$0.02
- Total per case: ~$0.20-0.40

**Using gpt-4o-mini:**
- Case generation: ~$0.01
- Per suspect interview: ~$0.002
- Per clue analysis: ~$0.002
- Total per case: ~$0.02-0.04

**Using gpt-3.5-turbo:**
- Case generation: ~$0.005
- Per suspect interview: ~$0.001
- Per clue analysis: ~$0.001
- Total per case: ~$0.01-0.02

**Using local APIs:**
- Free (runs on your hardware)

## Next Steps

Once your setup is working:

1. Read the full [OPENAI_MIGRATION.md](./OPENAI_MIGRATION.md) for detailed configuration options
2. Explore the game features: case generation, suspect interviews, clue analysis
3. Try different models to find the best balance of quality and cost
4. Consider setting up a local API for unlimited free usage

## Support

For additional help:
- Check the [OPENAI_MIGRATION.md](./OPENAI_MIGRATION.md) documentation
- Review OpenAI API documentation: https://platform.openai.com/docs
- Check the main README for game-specific information
