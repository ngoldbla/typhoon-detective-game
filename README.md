# 🔍 Emerson Detective Game

An AI-powered interactive detective mystery game for children (ages 7+), built with Python and Streamlit.

![Python](https://img.shields.io/badge/python-3.11-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.39-red)
![OpenAI](https://img.shields.io/badge/openai-powered-green)
![Railway](https://img.shields.io/badge/deploy-railway-blueviolet)

## 🌟 Features

- **🎲 AI-Generated Cases** - Create unique detective mysteries using OpenAI's GPT models
- **🎨 AI-Generated Art** - Beautiful scene, suspect, and clue images powered by DALL-E
- **🔍 Smart Clue Analysis** - AI helps analyze evidence and find connections
- **💬 Dynamic Interviews** - Have natural conversations with AI-powered suspects
- **✅ Solution Evaluation** - AI evaluates your detective work and reasoning
- **🎭 Comic Book UI** - Fun, child-friendly interface with comic styling
- **🌍 Bilingual Support** - Available in English and Thai
- **📊 Progress Tracking** - Track examined clues and interviewed suspects
- **🛡️ Child-Safe Content** - All mysteries are age-appropriate (no violence/scary content)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/ngoldbla/typhoon-detective-game.git
cd emerson-detective-game

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Run the app
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## 🚂 Deploy to Railway

### One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/ngoldbla/typhoon-detective-game)

### Manual Deployment

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `typhoon-detective-game`

3. **Add Environment Variables**
   - Go to Variables tab
   - Add: `OPENAI_API_KEY` = your-api-key-here
   - Optional: `OPENAI_MODEL` = gpt-4o

4. **Deploy**
   - Railway automatically detects Python
   - Installs dependencies from `requirements.txt`
   - Uses `Procfile` for start command
   - Your app will be live at: `https://your-app.railway.app`

### Railway Configuration

The project includes:
- `railway.json` - Railway build configuration
- `Procfile` - Start command for the web service
- `runtime.txt` - Python version specification
- `.python-version` - Python version for Nixpacks

## 📁 Project Structure

```
emerson-detective-game/
├── streamlit_app.py          # Main Streamlit application
├── pages/                    # Streamlit multi-page app
│   ├── 1_🆕_New_Case.py     # AI case generation
│   ├── 2_📋_All_Cases.py    # Cases browser
│   └── 3_🔍_Case_Details.py # Investigation interface
├── lib/                      # Core Python libraries
│   ├── types.py             # Data structures
│   ├── openai_client.py     # OpenAI integration
│   ├── case_generator.py    # AI case generation
│   ├── clue_analyzer.py     # AI clue analysis
│   ├── suspect_analyzer.py  # AI interviews
│   └── case_solver.py       # Solution evaluation
├── .streamlit/              # Streamlit configuration
│   └── config.toml          # Theme and server settings
├── requirements.txt         # Python dependencies
├── railway.json             # Railway configuration
├── Procfile                 # Railway start command
└── runtime.txt              # Python version

```

## 🎮 How to Play

### 1. Generate a New Case
- Click "🆕 New Case" in the sidebar
- Choose difficulty (very easy, easy, medium)
- Select a theme (school, home, playground, etc.)
- Click "Generate Mystery"

### 2. Investigate
- **Examine Clues**: Click "🔍 Examine" to get AI analysis
- **Interview Suspects**: Click "💬 Interview" to ask questions
- AI helps you find connections and next steps

### 3. Solve the Mystery
- Go to "✅ Solve Case" tab
- Select who you think did it
- Choose supporting evidence
- Explain your reasoning
- Submit for AI evaluation!

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
# Required
OPENAI_API_KEY=your-api-key-here

# Optional
OPENAI_MODEL=gpt-4o              # default: gpt-4o
OPENAI_BASE_URL=                  # for custom endpoints
```

### Supported OpenAI Models

- `gpt-4o` (recommended) - Best quality
- `gpt-4o-mini` - Faster and cheaper
- `gpt-4-turbo` - Legacy model
- Other OpenAI chat models

## 💰 Cost Estimates

### Railway Hosting
- **Free Tier**: $5 credit/month (~550 hours)
- **Hobby Plan**: $5/month (unlimited hours)
- **Pro Plan**: $20/month (more resources)

### OpenAI API
- **gpt-4o**: ~$0.03 per case generated
- **gpt-4o-mini**: ~$0.001 per case (cheaper!)

💡 **Tip**: Use `gpt-4o-mini` for development!

## 🛡️ Safety & Privacy

- ✅ All content is child-appropriate (ages 7+)
- ✅ No violence, scary content, or adult themes
- ✅ No personal data stored
- ✅ API calls go directly to OpenAI
- ✅ Session data is temporary (browser-only)

## 🏗️ Architecture

```
┌─────────────────────────────────┐
│   Streamlit Web App             │
│   (Python/Streamlit)            │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Python Core Libraries         │
│   • Case Generator              │
│   • Clue Analyzer               │
│   • Suspect Analyzer            │
│   • Case Solver                 │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   OpenAI GPT API                │
│   (gpt-4o or gpt-4o-mini)       │
└─────────────────────────────────┘
```

## 📊 Tech Stack

- **Framework**: [Streamlit](https://streamlit.io) - Python web framework
- **AI**: [OpenAI](https://openai.com) - GPT-4o for case generation
- **Language**: Python 3.11
- **Hosting**: [Railway](https://railway.app) - Cloud deployment
- **Storage**: Session state (temporary, browser-local)

## 🤝 Contributing

Contributions are welcome! This is a complete rewrite focused on:
- Pure Python implementation
- Streamlit for UI
- Railway deployment
- Production-ready code

## 📝 License

MIT License - See LICENSE file for details

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Ensure `.env` file exists
- Check it contains `OPENAI_API_KEY=your-key`
- Restart the app

### "Failed to generate case"
- Verify API key is valid
- Check you have OpenAI credits
- Try `gpt-4o-mini` (cheaper)

### Images not appearing or disappearing after an hour
- **Known Limitation**: OpenAI image URLs are temporary and expire after ~1 hour
- Images will display correctly immediately after generation
- For production use with persistent images, you would need to:
  - Download images and save them locally, OR
  - Upload them to cloud storage (S3, Cloudinary, etc.)
- Current implementation prioritizes simplicity over persistence

### Railway deployment issues
- Check environment variables are set
- View logs in Railway dashboard
- Ensure Python 3.11+ is specified

## 📧 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/ngoldbla/typhoon-detective-game/issues)
- 📖 **Docs**: See this README
- 💬 **Questions**: Open a discussion

## 🎉 Credits

Built with ❤️ using:
- [Streamlit](https://streamlit.io)
- [OpenAI](https://openai.com)
- [Railway](https://railway.app)

---

**Have fun solving mysteries, young detective!** 🕵️✨
