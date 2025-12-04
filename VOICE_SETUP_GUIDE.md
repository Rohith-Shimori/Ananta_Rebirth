# 🎤 ANANTA VOICE SETUP GUIDE

## License Information

The XTTS-v2 model used by Ananta requires license confirmation on first use. This is a **one-time setup**.

### License Options

**Option 1: Non-Commercial Use (Recommended for Personal Projects)**
- Free to use
- Governed by CPML (Coqui Public Model License)
- Perfect for local AI assistants
- Read more: https://coqui.ai/cpml

**Option 2: Commercial Use**
- Contact: licensing@coqui.ai
- For commercial applications
- Custom licensing terms

---

## Setup Methods

### Method 1: Interactive Setup (First Time Only)

When you first run the voice system, you'll see this prompt:

```
> You must confirm the following:
| > "I have purchased a commercial license from Coqui: licensing@coqui.ai"
| > "Otherwise, I agree to the terms of the non-commercial CPML: https://coqui.ai/cpml" - [y/n]
| | >
```

**Simply type `y` and press Enter** to accept the non-commercial license.

The model will then download (~1.5GB) and be cached for future use.

### Method 2: Automatic Setup (Recommended)

Use the voice system with automatic license acceptance:

```python
from voice.ananta_voice import AnantaVoice

# Automatically accepts non-commercial license
voice = AnantaVoice(skip_license=True)

# Generate speech
audio = voice.speak("Hello! I'm Ananta", emotion="happy")
```

### Method 3: Environment Variable

Set the environment variable before running:

```bash
# Windows
set TTS_HOME=C:\Ananta_Rebirth\voice\voice_samples

# Linux/Mac
export TTS_HOME=/path/to/Ananta_Rebirth/voice/voice_samples
```

Then run your code normally.

---

## Troubleshooting

### Issue: "You must confirm the following..."

**Solution:** Type `y` and press Enter to accept the license.

### Issue: KeyboardInterrupt when running tests

**Solution:** The test was interrupted. Run again and accept the license when prompted.

### Issue: Model download is slow

**Solution:** This is normal. The XTTS-v2 model is ~1.5GB and only downloads once.
- First run: 5-15 minutes (depending on internet speed)
- Subsequent runs: <1 second (model is cached)

### Issue: "GPU not available"

**Solution:** The system will automatically fall back to CPU. Performance will be slower but still functional.

---

## Quick Start

### Step 1: Accept License (One-Time)

```python
from voice.ananta_voice import AnantaVoice

# First run - will prompt for license
voice = AnantaVoice()
```

When prompted, type `y` and press Enter.

### Step 2: Use Voice

```python
# Generate speech with emotion
audio = voice.speak_with_emotion(
    "Hello! I'm Ananta, your AI partner.",
    emotion="happy"
)

# Save to file
voice.speak_with_emotion(
    "I'm here to help",
    emotion="warm",
    output_path="ananta_greeting.wav"
)
```

### Step 3: Integrate with Ananta

```python
from voice.ananta_voice import AnantaVoice
from ui.ananta_avatar import AnantaAvatar
from engines.ananta_personality import AnantaPersonality

# Create components
voice = AnantaVoice()
avatar = AnantaAvatar()
personality = AnantaPersonality()

# Full workflow
context = {"text": "That's amazing!"}
response = personality.shape_response("Great job!", context)
avatar.set_emotion(response.emotion)
audio = voice.speak_with_emotion(response.text, response.emotion)
```

---

## Testing

### Test Without Voice (No License Needed)

```bash
python test_ananta_quick.py
```

This tests avatar, personality, and UI without requiring voice setup.

### Test With Voice (License Required)

```bash
python test_ananta_identity.py
```

When prompted, type `y` to accept the license.

---

## Performance Notes

### First Run (With License Acceptance)
- Model download: 5-15 minutes
- Model initialization: 10-30 seconds
- First speech generation: 5-10 seconds
- **Total: 15-55 minutes**

### Subsequent Runs
- Model loading: <1 second (cached)
- Speech generation: 100-500ms per sentence
- **Total: <1 second startup**

### GPU vs CPU
- **GPU (RTX 4050):** 100-200ms per sentence
- **CPU (i5 12th Gen):** 500-1000ms per sentence

---

## FAQ

### Q: Is the license free?
**A:** Yes, for non-commercial use. The CPML is a free, open-source license.

### Q: Can I use this commercially?
**A:** Not with the default license. Contact licensing@coqui.ai for commercial licensing.

### Q: Will the model download every time?
**A:** No, only the first time. It's cached locally after that.

### Q: Can I use a different voice?
**A:** Yes! Record your own 6-10 second voice sample and place it at:
```
voice/voice_samples/ananta_voice_reference.wav
```

### Q: What if I don't want to use voice?
**A:** No problem! The avatar, personality, and UI systems work perfectly without voice.

---

## Next Steps

1. **Accept License** (one-time setup)
   ```python
   voice = AnantaVoice()  # Type 'y' when prompted
   ```

2. **Record Custom Voice** (optional)
   - Record 6-10 seconds of audio
   - Save as `voice/voice_samples/ananta_voice_reference.wav`

3. **Integrate with Ananta**
   - Add voice to the main controller
   - Use in chat interface

4. **Deploy**
   - Create web UI with Flask/FastAPI
   - Build desktop app with PyQt
   - Deploy locally or on server

---

## Resources

- **CPML License:** https://coqui.ai/cpml
- **XTTS-v2 GitHub:** https://github.com/coqui-ai/TTS
- **TTS Documentation:** https://tts.readthedocs.io/

---

## Support

If you encounter issues:

1. Check this guide
2. Review the error message
3. Check TTS documentation
4. Contact Coqui support: licensing@coqui.ai

---

**Ready to give Ananta her voice?** 🎤

Accept the license and start creating amazing interactions! ✨
