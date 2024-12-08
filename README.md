# Zedd: The Ultimate Personal Assistant

## Overview

Zedd is a sophisticated AI assistant with a unique retro-style terminal interface that combines multiple AI capabilities to create an engaging and helpful user experience.

![Demo](demo.gif)

---

## Key Features

### Voice Interaction

- **Voice Commands**: Press and hold SPACEBAR to speak naturally with Zedd.
- **Speech-to-Text**: Powered by Whisper AI for accurate voice recognition.
- **Text-to-Speech**: Natural voice responses using Open-Edge-TTS.

### Task Management

- **Todo Lists**: Create, manage, and track your tasks.
- **Task Status**: Mark tasks as complete or delete them.
- **Reminders**: Get notifications for pending tasks.

### Media Control

- **Music Playback**: Control Spotify with voice commands.
- **Video Control**: Play YouTube videos through voice commands.
- **Application Control**: Open and manage applications.

### AI Features

- **Image Generation**: Create images from text descriptions using Flux.
- **Natural Conversations**: Engage in human-like dialogue.
- **Web Search**: Perform Google searches and get instant results.
- **News Updates**: Get the latest news headlines.

### Interface

- **Retro CRT Style**: Unique terminal interface with phosphor effects.
- **Sound Effects**: Authentic retro computer sounds.
- **Dynamic Animations**: Matrix-style visual effects.


## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment tool (e.g., `venv`)
- [openai-edge-tts](https://github.com/travisvn/openai-edge-tts)
- Node.js and npm (for `openai-edge-tts`)

### Step 1: Clone the Repository

```bash
git clone https://github.com/TulipJani/Zedd.git
cd Zedd
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
CLOUDFLARE_ACCOUNT_ID=api_key
CLOUDFLARE_API_TOKEN=api_key

```

### Step 3: Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run Zedd

```bash
python main.py
```

---

## Usage

### Voice Commands

- Hold SPACEBAR to speak.
- Release to process the command.
- Wait for Zedd's response.

### Common Commands

- `"generate [prompt]"` - Create images.
- `"play [song] on spotify"` - Play music.
- `"add [task] on my todo"` - Create tasks.
- `"what's in my todo"` - View tasks.
- `"search [query]"` - Web search.
- `"fetch news"` - Get news updates.
- `"open [app_name]"` - Launch applications.

### Terminal Commands

- `help` - Display available commands.
- `status` - Show system status.
- `matrix` - Display matrix effect.
- `clear` - Clear screen.
- `exit` - Close Zedd.

---

## Project Structure

```
Zedd/
├── main.py              # Main application file
├── Whisper.py          # Voice recognition
├── imageGen.py         # Image generation
├── chat.py             # Chat/response handling
├── utils.py            # Utility functions
├── Todo.py             # Todo list functionality
├── calendar_handler.py # Calendar functionality
├── requirements.txt    # Dependencies
├── .env               # Environment variables
└── README.md          # Documentation
```

## Dependencies

Key packages used:

- `pygame`
- `rich`
- `simpleaudio`
- `requests`
- `numpy`
- `sounddevice`
- `python-dotenv`

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Cloudflare AI for image generation.
- ElevenLabs for text-to-speech.
- Google AI for natural language processing.
- Edge TTS for text-to-speech processing.
- LLaMa for natural language understanding.

---

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/TulipJani/Zedd/issues).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=TulipJani/Zedd&type=Date)](https://star-history.com/#TulipJani/Zedd&Date)
