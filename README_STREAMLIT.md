# 🔍 Emerson Detective Game - Streamlit Version

An AI-powered interactive detective mystery game for children (ages 7+), now running on Streamlit!

## 🌟 Features

- **AI-Generated Cases**: Create custom detective mysteries using OpenAI's GPT models
- **Interactive Investigations**: Examine clues and interview AI-powered suspects
- **Child-Friendly Content**: All mysteries are safe, fun, and age-appropriate
- **Smart Analysis**: AI helps analyze clues and evaluate solutions
- **Progress Tracking**: Keep track of your detective journey
- **Bilingual Support**: Available in English and Thai

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/typhoon-detective-game.git
   cd emerson-detective-game
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

4. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser**
   The app will automatically open at `http://localhost:8501`

## 🎮 How to Play

### 1. Generate a New Case
- Click "🆕 New Case" in the sidebar
- Choose difficulty (very easy, easy, medium)
- Select a theme (school, home, playground, etc.)
- Click "Generate Mystery"

### 2. Investigate
- **Examine Clues**: Click "🔍 Examine" on each clue to get AI analysis
- **Interview Suspects**: Click "💬 Interview" to ask suspects questions
- Take notes and look for connections!

### 3. Solve the Case
- Go to the "✅ Solve Case" tab
- Select who you think did it
- Choose the evidence that supports your theory
- Explain your reasoning
- Submit your solution!

## 📁 Project Structure

```
emerson-detective-game/
├── streamlit_app.py          # Main application file
├── pages/                    # Streamlit pages
│   ├── 1_🆕_New_Case.py     # Case generation page
│   ├── 2_📋_All_Cases.py    # Cases list page
│   └── 3_🔍_Case_Details.py # Case investigation page
├── lib/                      # Core Python libraries
│   ├── types.py             # Type definitions
│   ├── openai_client.py     # OpenAI integration
│   ├── case_generator.py    # Case generation logic
│   ├── clue_analyzer.py     # Clue analysis logic
│   ├── suspect_analyzer.py  # Suspect analysis & interviews
│   └── case_solver.py       # Solution evaluation
├── .streamlit/              # Streamlit configuration
│   └── config.toml          # Theme and settings
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
└── README_STREAMLIT.md     # This file
```

## 🎨 Customization

### Themes
The game uses a comic book-style theme defined in `.streamlit/config.toml`. You can customize colors and fonts there.

### Difficulty Levels
- **Very Easy**: Simple mysteries perfect for beginners
- **Easy**: Great for most 7-year-olds
- **Medium**: More challenging but still age-appropriate

### Mystery Themes
- School
- Home
- Playground
- Pet
- Toy
- Random

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your-api-key-here    # Required
OPENAI_MODEL=gpt-4o                  # Optional (default: gpt-4o)
OPENAI_BASE_URL=                     # Optional (for custom endpoints)
```

### Supported Models
- `gpt-4o` (recommended, default)
- `gpt-4o-mini` (faster, more economical)
- `gpt-4-turbo`
- Other OpenAI chat models

## 📊 Technical Details

### Built With
- **Streamlit**: Web framework for Python
- **OpenAI API**: AI-powered case generation and analysis
- **Python 3.8+**: Core programming language

### Data Storage
- Cases and progress are stored in Streamlit's session state
- Data persists during a session but is cleared when you close the app
- No database required!

## 🛡️ Safety & Privacy

- All generated content is child-appropriate (no violence, scary content, or adult themes)
- No personal data is collected or stored
- API calls are made directly to OpenAI (or your configured endpoint)
- Session data is temporary and local to your browser

## 🤝 Contributing

This is a transformation of the original Next.js version. Contributions are welcome!

## 📝 License

Same as the original project license.

## 🆚 Differences from Next.js Version

| Feature | Next.js Version | Streamlit Version |
|---------|----------------|-------------------|
| Framework | React/Next.js | Python/Streamlit |
| Deployment | Vercel | Any Python host |
| State Management | Context API + localStorage | Session state |
| Styling | Tailwind CSS | Custom CSS in config |
| API Routes | Next.js API routes | Direct Python calls |
| Persistence | localStorage (browser) | Session state (temporary) |

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you created a `.env` file
- Ensure it contains `OPENAI_API_KEY=your-key`
- Restart the Streamlit app

### "Failed to generate case"
- Check your API key is valid
- Ensure you have OpenAI API credits
- Check your internet connection

### "Module not found" errors
- Run `pip install -r requirements.txt`
- Make sure you're in the project directory

## 📧 Support

For issues or questions:
1. Check the original project documentation
2. Review this README
3. Open an issue on GitHub

## 🎉 Enjoy!

Have fun solving mysteries, young detective! 🕵️✨
