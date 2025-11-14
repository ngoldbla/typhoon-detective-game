# Deploying to Vercel

This guide walks you through deploying the Typhoon Detective Game to Vercel.

## Prerequisites

- A Vercel account (sign up at https://vercel.com)
- An OpenAI API key (get one at https://platform.openai.com/api-keys)
- This repository pushed to GitHub, GitLab, or Bitbucket

## Quick Deploy

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Connect Your Repository**
   - Go to https://vercel.com/new
   - Click "Import Project"
   - Select your Git provider (GitHub, GitLab, or Bitbucket)
   - Import your `typhoon-detective-game` repository

2. **Configure Project**
   - Framework Preset: **Next.js** (should auto-detect)
   - Root Directory: `./` (leave as default)
   - Build Command: `npm run build` (should auto-fill)
   - Output Directory: `.next` (should auto-fill)

3. **Set Environment Variables**

   Click "Environment Variables" and add:

   | Key | Value | Description |
   |-----|-------|-------------|
   | `OPENAI_API_KEY` | `sk-...` | Your OpenAI API key (required) |
   | `OPENAI_MODEL` | `gpt-4o` | Model to use (optional, defaults to gpt-4o) |
   | `OPENAI_BASE_URL` | `https://api.openai.com/v1` | API endpoint (optional) |

   **Important**: Make sure to set these for **Production**, **Preview**, and **Development** environments.

4. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete (usually 2-3 minutes)
   - Your app will be live at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

   Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - What's your project's name? `typhoon-detective-game`
   - In which directory is your code located? `./`
   - Want to override the settings? **N**

4. **Add Environment Variables**
   ```bash
   vercel env add OPENAI_API_KEY
   # Paste your API key when prompted
   # Select: Production, Preview, Development

   vercel env add OPENAI_MODEL
   # Enter: gpt-4o
   # Select: Production, Preview, Development
   ```

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Environment Variables

### Required Variables

- **OPENAI_API_KEY**: Your OpenAI API key
  - Get from: https://platform.openai.com/api-keys
  - Format: `sk-...`
  - **Security Note**: Never commit this to Git!

### Optional Variables

- **OPENAI_MODEL**: Choose which OpenAI model to use
  - Default: `gpt-4o`
  - Options: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`, `o1-preview`, `o1-mini`
  - Cost consideration: `gpt-4o-mini` or `gpt-3.5-turbo` for lower costs

- **OPENAI_BASE_URL**: Custom API endpoint
  - Default: `https://api.openai.com/v1`
  - Use for: Azure OpenAI, proxies, or compatible APIs
  - Example (Azure): `https://your-resource.openai.azure.com`

## Post-Deployment Configuration

### 1. Verify Deployment

After deployment, test your app:
1. Visit your deployment URL
2. Try creating a new case at `/cases/new`
3. Interview suspects and analyze clues
4. Ensure all AI features work correctly

### 2. Set Up Custom Domain (Optional)

1. Go to your project in Vercel dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

### 3. Configure Budget Alerts (Recommended)

To avoid unexpected OpenAI costs:
1. Go to https://platform.openai.com/usage
2. Set up usage limits
3. Enable email notifications

## Vercel Configuration File

This project includes a `vercel.json` file with:
- Build and dev commands
- Framework detection
- Default environment variables
- Region configuration (defaults to US East)

You can customize this file if needed:

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "OPENAI_API_KEY": "@openai_api_key",
    "OPENAI_BASE_URL": "https://api.openai.com/v1",
    "OPENAI_MODEL": "gpt-4o"
  }
}
```

## Performance Optimization

### 1. Choose the Right Region

Vercel automatically serves your app globally via CDN, but the serverless functions run in a specific region. Choose based on your primary audience:

- **US East** (default): `iad1`
- **US West**: `sfo1`
- **Europe**: `fra1`
- **Asia Pacific**: `hnd1`

Modify `regions` in `vercel.json` to change this.

### 2. Optimize Model Selection

For production, consider:
- **gpt-4o**: Best quality, highest cost (~$0.20-0.40 per case)
- **gpt-4o-mini**: Balanced quality/cost (~$0.02-0.04 per case)
- **gpt-3.5-turbo**: Fastest/cheapest (~$0.01-0.02 per case)

Set via `OPENAI_MODEL` environment variable.

### 3. Function Timeout

API routes have a default timeout of 10 seconds on Hobby plan, 60 seconds on Pro. Case generation might need more time with slower models. If you hit timeouts:
- Upgrade to Pro plan for longer timeouts
- Use faster models (`gpt-3.5-turbo`, `gpt-4o-mini`)
- Optimize token limits in the code

## Troubleshooting

### Build Fails

**Error: Module not found**
```bash
# Solution: Ensure all dependencies are in package.json
npm install
npm run build  # Test locally first
```

**Error: TypeScript errors**
```bash
# Solution: Fix TypeScript issues before deploying
npm run lint
```

### Runtime Errors

**Error: "API key for OpenAI is missing"**
- **Cause**: `OPENAI_API_KEY` environment variable not set
- **Solution**: Add the environment variable in Vercel dashboard
- **Redeploy**: Trigger a new deployment after adding env vars

**Error: "OpenAI API error (401)"**
- **Cause**: Invalid API key
- **Solution**: Verify your API key at https://platform.openai.com/api-keys
- **Update**: Replace the environment variable in Vercel

**Error: "OpenAI API error (429)"**
- **Cause**: Rate limit exceeded
- **Solution**:
  - Check OpenAI usage dashboard
  - Upgrade OpenAI account tier
  - Switch to less expensive model

**Error: Function timeout**
- **Cause**: API request took too long
- **Solution**:
  - Upgrade to Vercel Pro for longer timeouts
  - Use faster model (`gpt-4o-mini` or `gpt-3.5-turbo`)
  - Reduce `max_tokens` in API calls

### Preview Deployments

Every Git push to non-main branches creates a preview deployment. This is useful for:
- Testing changes before merging to main
- Sharing work-in-progress with team members
- Running E2E tests in a production-like environment

Preview deployments use the same environment variables as production.

## Monitoring and Logs

### View Logs

1. Go to your project in Vercel dashboard
2. Click "Deployments"
3. Click on any deployment
4. Navigate to "Functions" tab
5. Click on a function to see logs

### Monitor Usage

**Vercel Usage**:
- Dashboard → Settings → Usage
- Track bandwidth, function invocations, build minutes

**OpenAI Usage**:
- https://platform.openai.com/usage
- Track API costs and token usage

## Security Best Practices

1. **Never commit API keys**: Always use environment variables
2. **Use Vercel's encrypted secrets**: Keys are encrypted at rest
3. **Rotate keys regularly**: Update in both OpenAI and Vercel
4. **Set usage limits**: Configure in OpenAI dashboard
5. **Monitor logs**: Check for suspicious activity

## Cost Management

### Vercel Costs
- **Hobby Plan**: Free (includes 100GB bandwidth, 100 hours function time)
- **Pro Plan**: $20/month (includes more resources)
- See: https://vercel.com/pricing

### OpenAI Costs
Estimated per game session:
- **gpt-4o**: $0.20-0.40 per case
- **gpt-4o-mini**: $0.02-0.04 per case
- **gpt-3.5-turbo**: $0.01-0.02 per case

**Cost Optimization Tips**:
1. Use `gpt-4o-mini` or `gpt-3.5-turbo` for most users
2. Reserve `gpt-4o` for premium users
3. Implement caching for repeated queries
4. Set rate limits on API endpoints
5. Monitor usage daily

## Continuous Deployment

Vercel automatically deploys:
- **Production**: Every push to `main` branch
- **Preview**: Every push to other branches
- **Rollback**: Instant rollback to previous deployments

To disable auto-deployment:
1. Dashboard → Settings → Git
2. Uncheck "Production Branch"
3. Deploy manually via CLI or dashboard

## Advanced Configuration

### Custom Build Configuration

Create a `vercel.json` in your project root:

```json
{
  "buildCommand": "npm run build",
  "framework": "nextjs",
  "regions": ["iad1"],
  "functions": {
    "src/app/api/**/*.ts": {
      "maxDuration": 30
    }
  }
}
```

### Edge Functions

For faster response times, consider moving lightweight API routes to Edge Functions. However, OpenAI API calls are better suited for Serverless Functions due to their latency.

## Support and Resources

- **Vercel Documentation**: https://vercel.com/docs
- **Next.js Documentation**: https://nextjs.org/docs
- **OpenAI Documentation**: https://platform.openai.com/docs
- **Project Issues**: Check the GitHub repository

## Next Steps

After successful deployment:

1. ✅ Test all features thoroughly
2. ✅ Set up custom domain
3. ✅ Configure monitoring and alerts
4. ✅ Set OpenAI usage limits
5. ✅ Share your deployed app!

Your detective game is now live and ready for players worldwide! 🎮🔍
