# 🚀 Vercel Deployment Guide - Hybrid Next.js + Python

This project now supports **two deployment modes**:

1. **Streamlit Version** (standalone Python app)
2. **Vercel Hybrid** (Next.js frontend + Python API routes) ⭐ **You are here**

## Architecture

```
┌─────────────────────────────────────────┐
│         Vercel Deployment               │
│                                         │
│  ┌──────────────┐    ┌──────────────┐ │
│  │   Next.js    │───▶│   Python     │ │
│  │   Frontend   │    │   API Routes │ │
│  │  (React/TS)  │    │  (Serverless)│ │
│  └──────────────┘    └──────────────┘ │
│         │                    │         │
│         │                    │         │
│         └────────────────────┘         │
│                  │                      │
│                  ▼                      │
│           OpenAI API                    │
└─────────────────────────────────────────┘
```

## Why This Approach?

✅ **Best of Both Worlds**
- Keep your beautiful Next.js/React frontend
- Use Python for AI logic (cleaner, more maintainable)
- Deploy everything to Vercel with zero config

✅ **Serverless Python Functions**
- Each API route runs as a serverless function
- Automatic scaling
- Pay only for what you use

✅ **Shared Libraries**
- Python libraries in `/lib` are used by both:
  - Streamlit app (for standalone deployment)
  - Vercel API routes (for hybrid deployment)

## Project Structure

```
typhoon-detective-game/
├── src/                          # Next.js app (TypeScript/React)
│   ├── app/                      # Next.js pages
│   ├── components/               # React components
│   └── lib/                      # TypeScript utilities
│
├── api/python/                   # Python Vercel serverless functions
│   ├── generate-case.py          # Case generation endpoint
│   ├── analyze-clue.py           # Clue analysis endpoint
│   ├── interview-suspect.py      # Suspect interview endpoint
│   ├── solve-case.py             # Solution evaluation endpoint
│   └── requirements.txt          # Python dependencies for API
│
├── lib/                          # Shared Python libraries
│   ├── case_generator.py         # AI case generation logic
│   ├── clue_analyzer.py          # AI clue analysis logic
│   ├── suspect_analyzer.py       # AI interview logic
│   ├── case_solver.py            # AI solution evaluation
│   ├── openai_client.py          # OpenAI API client
│   └── types.py                  # Python type definitions
│
├── pages/                        # Streamlit pages (for standalone mode)
├── streamlit_app.py              # Streamlit app (for standalone mode)
├── vercel.json                   # Vercel configuration
└── package.json                  # Node.js dependencies
```

## Quick Start

### 1. Install Dependencies

```bash
# Install Node.js dependencies
pnpm install

# Install Python dependencies (for local development)
pip install -r api/python/requirements.txt
```

### 2. Environment Variables

Create a `.env.local` file:

```env
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o
```

### 3. Run Locally

```bash
# Start Next.js dev server
pnpm dev

# The app will run at http://localhost:3000
# Python API routes will automatically work!
```

## Deploy to Vercel

### Option A: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# For production
vercel --prod
```

### Option B: Using Vercel Dashboard

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Python API routes"
   git push
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js

3. **Add Environment Variables**
   - Go to Project Settings → Environment Variables
   - Add:
     - `OPENAI_API_KEY` (your OpenAI API key)
     - `OPENAI_MODEL` (optional, default: gpt-4o)

4. **Deploy**
   - Click "Deploy"
   - Vercel will automatically:
     - Build the Next.js app
     - Install Python dependencies from `api/python/requirements.txt`
     - Deploy Python functions as serverless endpoints

## API Endpoints

Once deployed, your API routes will be available at:

- `https://your-app.vercel.app/api/python/generate-case`
- `https://your-app.vercel.app/api/python/analyze-clue`
- `https://your-app.vercel.app/api/python/interview-suspect`
- `https://your-app.vercel.app/api/python/solve-case`

## How It Works

### Python Serverless Functions

Vercel automatically detects Python files in `/api` and creates serverless functions:

```python
# api/python/generate-case.py
from http.server import BaseHTTPRequestHandler
import sys
import os

# Add lib directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from lib.case_generator import generate_case

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Handle request
        result = generate_case(params)
        # Return JSON response
```

### Next.js Integration

Your existing Next.js app calls these endpoints:

```typescript
// src/lib/caseGeneratorPython.ts
export async function generateCase(params: CaseGenerationParams) {
    const response = await fetch('/api/python/generate-case', {
        method: 'POST',
        body: JSON.stringify(params)
    });
    return response.json();
}
```

## Switching Between Implementations

You can choose which implementation to use:

### Use Python API Routes (Recommended for Vercel)

```typescript
// Use Python implementation
import { generateCase } from '@/lib/caseGeneratorPython';
```

### Use Direct TypeScript Implementation

```typescript
// Use TypeScript implementation
import { generateCase } from '@/lib/caseGenerator';
```

## Vercel Configuration

The `vercel.json` automatically configures Python support:

```json
{
  "buildCommand": "pnpm run build",
  "framework": "nextjs",
  "regions": ["iad1"]
}
```

Vercel detects Python files in `/api` and:
- Installs dependencies from `api/python/requirements.txt`
- Creates serverless functions for each `.py` file
- Handles routing automatically

## Environment Variables

### Required
- `OPENAI_API_KEY` - Your OpenAI API key

### Optional
- `OPENAI_MODEL` - Model to use (default: gpt-4o)
- `OPENAI_BASE_URL` - Custom API endpoint (for proxies/Azure)

## Troubleshooting

### Python API routes return 404
- Make sure files are in `/api/python/` directory
- Check file names match the routes you're calling
- Redeploy to Vercel

### Python dependencies not found
- Ensure `api/python/requirements.txt` exists
- Check that required packages are listed
- Try redeploying

### Import errors in Python
- Make sure `sys.path.insert` is correct
- Check that `/lib` directory is at project root
- Verify Python files use correct import statements

### Function timeout
- Vercel free tier: 10 second timeout
- Vercel Pro: 60 second timeout
- Consider upgrading if AI calls take too long

## Performance

### Cold Starts
- First request may be slower (~2-3 seconds)
- Subsequent requests are faster
- Consider Vercel Pro for better performance

### Optimization Tips
1. Use `gpt-4o-mini` for faster/cheaper responses
2. Reduce `max_tokens` in API calls
3. Cache results when possible
4. Consider edge functions for static data

## Cost Considerations

### Vercel Costs
- **Hobby (Free)**: 100GB bandwidth, 100hrs compute
- **Pro ($20/mo)**: 1TB bandwidth, 1000hrs compute

### OpenAI Costs
- **gpt-4o**: $5.00 / 1M input tokens, $15.00 / 1M output tokens
- **gpt-4o-mini**: $0.15 / 1M input tokens, $0.60 / 1M output tokens

💡 **Tip**: Use `gpt-4o-mini` for development to save costs!

## Monitoring

View logs in Vercel dashboard:
1. Go to your project
2. Click "Functions" tab
3. Select a function to see logs
4. Monitor performance and errors

## Next Steps

- ✅ Deploy to Vercel
- 📊 Monitor function performance
- 🎨 Customize the Next.js frontend
- 🚀 Add more AI features
- 📈 Scale as needed

## Support

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Vercel Deployment Docs](https://vercel.com/docs/deployments/overview)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

**Both deployment options are fully supported:**
- 🌐 **Vercel Hybrid** (This guide) - Next.js + Python APIs
- 🎈 **Streamlit** (See README_STREAMLIT.md) - Standalone Python app
