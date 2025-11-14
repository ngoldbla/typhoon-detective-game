# Typhoon Detective Game

## Introduction

[Typhoon Detective Game](https://detective.apps.opentyphoon.ai) is an interactive mystery-solving experience where players take on the role of a detective to solve dynamically generated cases. Through examining evidence, interviewing suspects, and piecing together clues, players must identify the culprit and solve the mystery.

This project is part of [Typhoon Application Week](https://apps.opentyphoon.ai), showcasing the capabilities of the [Typhoon platform](https://opentyphoon.ai). Please note that this application is not maintained for production use and is not production-ready. Use at your own risk.

## Highlighted Features + Typhoon Integration

- **Dynamic Case Generation**: Typhoon creates unique cases with customizable settings, themes, and difficulties, generating complex plots, motives, and characters on demand.

- **Interactive Suspect Interviews**: Leverage Typhoon's conversational abilities to question suspects naturally, with the AI generating context-aware responses based on the case details and suspect personalities.

- **Evidence Analysis**: Typhoon powers the evidence examination system, providing insights and connections between clues that help players build their case.

- **Multiple Language Support**: Typhoon's multilingual capabilities enable gameplay in both English and Thai with natural, fluent interactions.

- **Adaptive Difficulty**: Typhoon adjusts the complexity of cases and hints based on player performance and selected difficulty level.

## Getting Started (Local Development)

### Prerequisites

- Node.js 18+ 
- pnpm 8+
- Typhoon API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/typhoon-detective-game.git
   cd typhoon-detective-game
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env.local` and configure your LLM settings (see [LLM Configuration](#llm-configuration) below)

4. Run the development server:
   ```bash
   pnpm dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## LLM Configuration

This game now supports any OpenAI-compatible LLM provider! You can use Typhoon, OpenAI, local models via Ollama, or any other compatible API.

### Configuration Options

Create a `.env.local` file with the following variables:

```bash
# API Key (required for most providers)
LLM_API_KEY=your_api_key_here

# API Endpoint (optional - defaults to Typhoon)
# Default: https://api.opentyphoon.ai/v1/chat/completions
LLM_API_ENDPOINT=https://api.opentyphoon.ai/v1/chat/completions

# Model Name (optional - defaults to typhoon-v2.1-12b-instruct)
LLM_MODEL=typhoon-v2.1-12b-instruct
```

### Provider Examples

#### Typhoon (Default)
```bash
LLM_API_KEY=your_typhoon_api_key
LLM_API_ENDPOINT=https://api.opentyphoon.ai/v1/chat/completions
LLM_MODEL=typhoon-v2.1-12b-instruct
```

#### OpenAI
```bash
LLM_API_KEY=your_openai_api_key
LLM_API_ENDPOINT=https://api.openai.com/v1/chat/completions
LLM_MODEL=gpt-4o
```

#### Ollama (Local)
```bash
# No API key needed for local Ollama
LLM_API_ENDPOINT=http://localhost:11434/v1/chat/completions
LLM_MODEL=llama3.1
```

#### LM Studio (Local)
```bash
# No API key needed for local LM Studio
LLM_API_ENDPOINT=http://localhost:1234/v1/chat/completions
LLM_MODEL=your-model-name
```

#### Other OpenAI-Compatible APIs
Any provider with an OpenAI-compatible endpoint should work. Just configure:
- `LLM_API_KEY`: Your API key
- `LLM_API_ENDPOINT`: The `/v1/chat/completions` endpoint
- `LLM_MODEL`: The model identifier

### Legacy Configuration

For backward compatibility, you can still use `TYPHOON_API_KEY` instead of `LLM_API_KEY`:
```bash
TYPHOON_API_KEY=your_api_key_here
```

### Recommended Models

For the best experience, use models with:
- Strong reasoning capabilities
- Good JSON output formatting
- Context window of at least 4K tokens
- Support for system prompts

Tested models:
- ✅ typhoon-v2.1-12b-instruct
- ✅ gpt-4o, gpt-4-turbo
- ✅ claude-3-5-sonnet (via proxy)
- ✅ llama3.1 8B+ (via Ollama)

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the LICENSE file for details.

## Connect With Us

- Website: [Typhoon](https://opentyphoon.ai)
- GitHub: [SCB 10X](https://github.com/scb-10x)
- Hugging Face: [SCB 10X](https://huggingface.co/scb10x)
- Discord: [Join our community](https://discord.com/invite/9F6nrFXyNt)
- X (formerly Twitter): [Typhoon](https://x.com/opentyphoon)
