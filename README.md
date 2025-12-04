# 🚀 Ananta Ultimate Backend

## Quick Setup (5 Minutes)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Voice (Windows)
```bash
pip install pyttsx3 speechrecognition

# For PyAudio on Windows:
pip install pipwin
pipwin install pyaudio
```

### 3. Install Best Model
```bash
# Best for your RTX 4050
ollama pull llama3:8b-instruct-q6_K

# Optional: For complex tasks
ollama pull mixtral:8x7b-instruct-v0.1-q4_K_M
```

### 4. Run
```bash
python -m app.main
```

✅ **API running at**: http://127.0.0.1:8000
✅ **Docs**: http://127.0.0.1:8000/docs

---

## Features

- ✅ Voice interface with emotion
- ✅ Proactive assistant
- ✅ Real-time code execution
- ✅ Self-improvement
- ✅ Multi-language code generation
- ✅ Creative thinking
- ✅ Adaptive memory

---

## API Endpoints

### Core
- `POST /query` - Main query
- `GET /health` - Health check
- `GET /features` - List features

### Voice
- `GET /voice/capabilities` - Check voice
- `POST /voice/speak` - Make Ananta speak
- `GET /voice/listen` - Listen to user

### Proactive
- `GET /proactive/checkin` - Get check-in
- `POST /proactive/reminder` - Add reminder
- `POST /proactive/work/start` - Start session

### Code
- `POST /code/execute` - Run code
- `POST /code/generate` - Generate code
- `POST /code/test` - Test code

### Memory
- `GET /memory/stats` - Statistics
- `GET /memory/personal` - Personal memory
- `GET /memory/knowledge` - Knowledge

---

## Configuration

Edit `app/config.py`:

```python
# Change model
DEFAULT_MODEL = "llama3:8b-instruct-q6_K"

# Adjust personality
DEFAULT_PERSONALITY_LEVEL = 7  # 1-10

# Voice settings
VOICE_ENABLED = True
VOICE_RATE = 175

# Proactive settings
CHECKIN_FREQUENCY = 180  # minutes
```

---

## Test

```bash
# Health check
curl http://127.0.0.1:8000/health

# Query
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello Ananta!"}'

# Voice capabilities
curl http://127.0.0.1:8000/voice/capabilities
```

---

## Troubleshooting

**PyAudio won't install?**
```bash
pip install pipwin
pipwin install pyaudio
```

**Voice not working?**
- Check microphone permissions
- Test: `python -c "import speech_recognition"`

**Model not found?**
```bash
ollama pull llama3:8b-instruct-q6_K
```

---

## Project Structure

```
backend/
├── app/              # API layer
├── core/             # Core functionality
├── engines/          # AI engines
├── memory/           # Memory systems
├── intelligence/     # Self-improvement
├── features/         # Voice, proactive, executor
├── utils/            # Utilities
└── data/             # Storage
```

---

**Ready!** 🎉