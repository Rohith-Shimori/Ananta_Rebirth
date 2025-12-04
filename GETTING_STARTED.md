# Ananta Rebirth - Getting Started Guide

## 🎯 Welcome to Ananta Rebirth!

A comprehensive local AI assistant with vision, automation, and intelligence capabilities.

## ⚡ Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Ollama (in separate terminal)
```bash
ollama serve
```

Wait for: `Listening on 127.0.0.1:11434`

### Step 3: Run Quick Test
```bash
python quick_test.py
```

Expected output:
```
✅ Passed:  10
❌ Failed:  0
📊 Success: 100.0%

🎉 ALL TESTS PASSED! Ananta is ready to use!
```

### Step 4: Start Using Ananta

**Terminal Interface:**
```bash
python main.py
```

**GUI Interface:**
```bash
python gui_launcher.py
```

## 📚 Documentation Guide

### For Testing
- **[TESTING_SETUP.md](TESTING_SETUP.md)** - Step-by-step testing instructions
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Detailed testing reference
- **[TESTING_SUMMARY.md](TESTING_SUMMARY.md)** - What was done and why

### For Understanding the Project
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Architecture and organization
- **[FILE_ORGANIZATION_CHECKLIST.md](FILE_ORGANIZATION_CHECKLIST.md)** - File organization details

### For Using Ananta
- **[README.md](README.md)** - Main documentation
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Quick start instructions

## 🚀 Available Commands

### Testing
```bash
# Quick test (2-3 minutes)
python quick_test.py

# Individual feature tests (5-10 minutes)
python tests/test_features_individual.py

# All tests (10-15 minutes)
python run_tests.py

# Comprehensive test suite
python comprehensive_test.py
```

### Running Ananta
```bash
# Terminal interface
python main.py

# GUI interface
python gui_launcher.py

# Start Ollama (separate terminal)
ollama serve
```

## 🎯 What Each Test Does

### Quick Test (`quick_test.py`)
- 10 essential features
- 2-3 minutes
- Perfect for quick verification

### Individual Feature Tests (`tests/test_features_individual.py`)
- 11 detailed feature tests
- 5-10 minutes
- Detailed output for each feature

### All Tests (`run_tests.py`)
- Project structure verification
- Dependency checking
- Ollama setup verification
- Individual feature tests
- Comprehensive test suite
- 10-15 minutes
- Generates test report

## 🧠 Features Tested

| Feature | Test | Time |
|---------|------|------|
| Retriever (Vector DB) | ✅ | <1s |
| Ollama Client (LLM) | ✅ | 1-2s |
| Emotional Intelligence | ✅ | <1s |
| Context Engine | ✅ | <1s |
| Security Engine | ✅ | <1s |
| System Monitor | ✅ | <1s |
| Code Executor | ✅ | <1s |
| Voice Interface | ✅ | <1s |
| Project Scaffolder | ✅ | 1-2s |
| Creative Engine | ✅ | 1-2s |
| Memory System | ✅ | <1s |

## 📊 Project Organization

```
Ananta_Rebirth/
├── 🚀 Entry Points
│   ├── main.py              # Terminal interface
│   ├── gui_launcher.py      # GUI launcher
│   └── quick_test.py        # Quick test
│
├── 🧠 Core Engines (core/)
│   ├── controller.py        # Main orchestrator
│   ├── ollama_client.py     # LLM integration
│   ├── retriever.py         # Vector database
│   ├── context_engine.py    # Context management
│   └── ... (10+ more engines)
│
├── 🎯 Intelligence (intelligence/)
├── 🤖 Automation (automation/)
├── 💾 Memory (memory/)
├── 🎨 Engines (engines/)
├── ✨ Features (features/)
├── 🎨 UI (ui/)
├── 🛠️ Utils (utils/)
├── 📊 Data (data/)
├── ✅ Tests (tests/)
│
└── 📚 Documentation
    ├── GETTING_STARTED.md (this file)
    ├── TESTING_SETUP.md
    ├── PROJECT_STRUCTURE.md
    └── ... (more docs)
```

## ✅ Verification Checklist

Before you start:
- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Ollama installed and running: `ollama serve`
- [ ] Quick test passes: `python quick_test.py`

## 🎯 Common Tasks

### Test a Specific Feature
```bash
# Test Retriever
python -c "from core.retriever import Retriever; r = Retriever(); print('✅ OK')"

# Test Emotional Intelligence
python -c "from core.emotional_intelligence import EmotionalIntelligence; ei = EmotionalIntelligence(); print('✅ OK')"

# Test Memory System
python -c "from memory.personal_memory import PersonalMemory; m = PersonalMemory(); print('✅ OK')"
```

### Run Terminal Interface
```bash
python main.py

# Commands:
# help        - Show available commands
# status      - Show system status
# capabilities - Show all capabilities
# image <path> - Analyze image
# quit        - Exit
```

### Run GUI Interface
```bash
python gui_launcher.py
```

### Customize Configuration
Edit `config.py`:
- Model selection
- GPU settings
- Memory limits
- Feature toggles

## 🔧 Troubleshooting

### Ollama Not Running
```
Error: Ollama not running - skipping
```
**Fix**: Run `ollama serve` in a separate terminal

### GPU Not Available
```
Error: GPU not available, using CPU
```
**Fix**: Check NVIDIA drivers with `nvidia-smi`

### Memory Issues
```
Error: CUDA out of memory
```
**Fix**: Reduce batch size in `config.py`

### Import Errors
```
Error: ModuleNotFoundError
```
**Fix**: Run `pip install -r requirements.txt --force-reinstall`

## 📖 Learning Path

### Beginner
1. Read this file (GETTING_STARTED.md)
2. Run `python quick_test.py`
3. Run `python main.py` and explore
4. Read TESTING_SETUP.md

### Intermediate
1. Read PROJECT_STRUCTURE.md
2. Run `python run_tests.py`
3. Explore individual features
4. Read TESTING_GUIDE.md

### Advanced
1. Read FILE_ORGANIZATION_CHECKLIST.md
2. Explore source code in `core/`, `intelligence/`, etc.
3. Customize configuration in `config.py`
4. Add personal memories and knowledge

## 🎯 Next Steps

### Immediate (Now)
1. ✅ Install dependencies
2. ✅ Start Ollama
3. ✅ Run quick test
4. ✅ Start using Ananta

### Short Term (Today)
1. ✅ Run full tests
2. ✅ Explore terminal interface
3. ✅ Try GUI interface
4. ✅ Read documentation

### Medium Term (This Week)
1. ✅ Customize configuration
2. ✅ Add personal memories
3. ✅ Explore features
4. ✅ Build knowledge base

### Long Term (Ongoing)
1. ✅ Use for daily tasks
2. ✅ Improve with feedback
3. ✅ Add custom features
4. ✅ Optimize performance

## 🌟 Key Features

### 🧠 Intelligence
- Advanced reasoning & context
- Emotional intelligence
- Proactive suggestions
- Self-improvement learning

### 👁️ Vision
- Code analysis & review
- Screenshot understanding
- Document OCR & analysis
- Error detection & fixes

### 🤖 Automation
- Smart workflow generation
- Custom automation rules
- Batch processing
- Real-time monitoring

### 🔧 Features
- Personal memory system
- Knowledge base integration
- Security analysis
- System monitoring
- Voice interface
- Context awareness

## 📞 Quick Commands

```bash
# Install
pip install -r requirements.txt

# Test
python quick_test.py
python tests/test_features_individual.py
python run_tests.py

# Run
python main.py              # Terminal
python gui_launcher.py      # GUI

# Start Ollama (separate terminal)
ollama serve
```

## 🎊 Success!

You're all set! Ananta Rebirth is ready to use. 

### What You Can Do Now
- ✅ Chat with Ananta in terminal or GUI
- ✅ Analyze images and code
- ✅ Automate tasks
- ✅ Store and retrieve memories
- ✅ Get emotional intelligence
- ✅ Execute code safely
- ✅ Generate creative content
- ✅ Monitor system performance

### Where to Go From Here
1. **Explore Features**: Try different commands in `python main.py`
2. **Read Docs**: Check out PROJECT_STRUCTURE.md and TESTING_GUIDE.md
3. **Customize**: Edit config.py for your preferences
4. **Build**: Add personal memories and knowledge
5. **Extend**: Create custom features and automations

## 📚 Documentation Index

| Document | Purpose | Time |
|----------|---------|------|
| GETTING_STARTED.md | This file - quick overview | 5 min |
| TESTING_SETUP.md | Step-by-step testing | 10 min |
| PROJECT_STRUCTURE.md | Architecture overview | 15 min |
| TESTING_GUIDE.md | Detailed testing reference | 20 min |
| FILE_ORGANIZATION_CHECKLIST.md | Organization details | 15 min |
| QUICK_START_GUIDE.md | Quick start instructions | 10 min |
| README.md | Main documentation | 20 min |

## 🆘 Need Help?

1. **Check Documentation**: Start with TESTING_SETUP.md
2. **Review Errors**: Check test output for error messages
3. **Check Logs**: Look in `data/` directory for logs
4. **Troubleshoot**: See troubleshooting section above
5. **Reinstall**: Run `pip install -r requirements.txt --force-reinstall`

## 🎉 Ready?

```bash
# 1. Start Ollama (separate terminal)
ollama serve

# 2. Run quick test
python quick_test.py

# 3. Start using Ananta
python main.py
```

**Enjoy Ananta Rebirth!** 🚀

---

**Last Updated**: 2024
**Status**: ✅ Ready for use
**Version**: 1.0
