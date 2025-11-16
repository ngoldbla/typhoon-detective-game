# 🚂 Railway Deployment Guide

## Quick Deploy

### One-Click Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/ngoldbla/typhoon-detective-game)

### Manual Deploy

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Create Railway Project**
   - Visit [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `typhoon-detective-game`

3. **Add Environment Variables**
   - Go to Variables tab
   - Add: `OPENAI_API_KEY` = your-key-here
   - Optional: `OPENAI_MODEL` = gpt-4o

4. **Add Persistent Volume (Important!)**
   - Go to "Settings" tab
   - Scroll to "Volumes"
   - Click "Add Volume"
   - Mount path: `/data`
   - This ensures your SQLite database persists across deployments

5. **Deploy!**
   - Railway auto-detects Python from `requirements.txt`
   - Uses `railway.toml` for deployment config
   - App goes live at `https://your-app.railway.app`

## Configuration Files

- **railway.toml** - Railway deployment config with volume mount
- **railway.json** - Legacy Railway build config
- **Procfile** - Web service command
- **runtime.txt** - Python 3.11.6
- **.python-version** - Nixpacks version
- **requirements.txt** - Dependencies

## Database Persistence

This app uses SQLite for data persistence:
- **Location**: `/data/detective_game.db`
- **Volume**: Mounted at `/data` (configured in `railway.toml`)
- **Data Stored**: Cases, clues, suspects, images, interview history
- **Important**: Without the volume mount, all data will be lost on each deployment!

## Environment Variables

```env
OPENAI_API_KEY=your-key      # Required
OPENAI_MODEL=gpt-4o          # Optional (default: gpt-4o)
```

## Cost

- **Free Tier**: $5 credit/month (~550 hours)
- **Hobby**: $5/month unlimited
- **Pro**: $20/month more resources

## Monitoring

View logs in Railway dashboard:
- Select your service
- Click "Deployments"
- View real-time logs

## Support

Issues? Check:
1. Environment variables are set
2. Python 3.11+ specified
3. Railway dashboard logs

---

**Your game is ready for Railway!** 🚂✨
