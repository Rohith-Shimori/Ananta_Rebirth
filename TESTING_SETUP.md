# Ananta Rebirth - Testing Setup & Execution Guide

## 🎯 Overview

This guide provides step-by-step instructions to test each feature individually and organize the project cleanly.

## 📋 Prerequisites

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Ollama Service
```bash
ollama serve
```

This should output:
```
Listening on 127.0.0.1:11434
```

Keep this terminal open while running tests.

## 🚀 Quick Start (Recommended)

### Option A: Run Quick Test (2-3 minutes)
```bash
python quick_test.py
```

This runs 10 essential tests quickly:
- ✅ Retriever (Vector Database)
- ✅ Emotional Intelligence
- ✅ Context Engine
- ✅ Security Engine
- ✅ System Monitor
- ✅ Memory System
- ✅ Code Executor
- ✅ Voice Interface
- ✅ Creative Engine
- ✅ Ollama Client

### Option B: Run Individual Feature Tests (5-10 minutes)
```bash
python tests/test_features_individual.py
```

Tests each feature with detailed output:
- 🔍 Retriever
- 🤖 Ollama Client
- ❤️ Emotional Intelligence
- 🧠 Context Engine
- 🔒 Security Engine
- 📊 System Monitor
- 💻 Code Executor
- 🎤 Voice Interface
- 🏗️ Project Scaffolder
- 🎨 Creative Engine
- 🧠 Memory System

### Option C: Run All Tests (10-15 minutes)
```bash
python run_tests.py
```

Comprehensive testing including:
- Project structure verification
- Dependency checking
- Ollama setup verification
- Individual feature tests
- Comprehensive test suite
- Test report generation

## 📊 Understanding Test Output

### Test Status Indicators
```
✅ PASS   - Feature working correctly
❌ FAIL   - Feature has an error
⏭️ SKIP   - Feature skipped (e.g., Ollama not running)
⚠️ ERROR  - Unexpected error occurred
🟢 RUNNING - Ollama is running
🔴 NOT_RUNNING - Ollama is not running
```

### Example Output
```
🚀 ANANTA REBIRTH - INDIVIDUAL FEATURE TEST SUITE
======================================================================

🔍 Checking Ollama availability...
✅ Ollama is running on localhost:11434

======================================================================
📋 RUNNING INDIVIDUAL FEATURE TESTS
======================================================================

🔍 Testing Retriever (Vector Database)...
  ✅ Added documents and retrieved results

🤖 Testing Ollama Client...
  ✅ Generated response: What is 2+2? The answer is 4...

❤️ Testing Emotional Intelligence...
  ✅ Sentiment: joy (score: 0.95)

... (more tests)

======================================================================
📊 TEST RESULTS SUMMARY
======================================================================

📈 Overall Statistics:
  ✅ Passed:  11/11
  ❌ Failed:  0/11
  ⏭️ Skipped: 0/11
  📊 Success Rate: 100.0%

🎉 ALL TESTS PASSED! Ananta Rebirth is fully functional!
```

## 🧪 Individual Feature Testing

### 1. Test Retriever (Vector Database)
```bash
python -c "
from core.retriever import Retriever
r = Retriever()
r.add_documents(['id1'], [{'type': 'test'}], ['Test document'])
results = r.query('test', top_k=1)
print('✅ Retriever working' if results else '❌ Retriever failed')
"
```

### 2. Test Ollama Client
```bash
python -c "
from core.ollama_client import OllamaClient
client = OllamaClient()
response = client.generate('What is 2+2?', max_tokens=50)
print(f'✅ Response: {response[:50]}...' if response else '❌ No response')
"
```

### 3. Test Emotional Intelligence
```bash
python -c "
from core.emotional_intelligence import EmotionalIntelligence
ei = EmotionalIntelligence()
sentiment = ei.analyze_sentiment('I am very happy!')
print(f'✅ Emotion: {sentiment.get(\"emotion\")}' if sentiment else '❌ Failed')
"
```

### 4. Test Context Engine
```bash
python -c "
from core.context_engine import ContextEngine
ctx = ContextEngine()
messages = [{'role': 'user', 'content': 'Hello'}]
result = ctx.build_context(messages)
print('✅ Context engine working' if result else '❌ Failed')
"
```

### 5. Test Security Engine
```bash
python -c "
from core.security_engine import SecurityEngine
sec = SecurityEngine()
is_safe = sec.is_safe_prompt('What is Python?')
print(f'✅ Safe prompt: {is_safe}' if is_safe is not None else '❌ Failed')
"
```

### 6. Test System Monitor
```bash
python -c "
from core.system_monitor import SystemMonitor
monitor = SystemMonitor()
stats = monitor.get_system_stats()
print(f'✅ CPU: {stats[\"cpu_percent\"]:.1f}%, RAM: {stats[\"memory_percent\"]:.1f}%')
"
```

### 7. Test Code Executor
```bash
python -c "
from features.code_executor import CodeExecutor
executor = CodeExecutor()
result = executor.execute('x = 1 + 1')
print('✅ Code executor working' if result is not None else '❌ Failed')
"
```

### 8. Test Voice Interface
```bash
python -c "
from features.voice_interface import VoiceInterface
voice = VoiceInterface()
print('✅ Voice interface loaded')
"
```

### 9. Test Project Scaffolder
```bash
python -c "
from engines.project_scaffolder import ProjectScaffolder
scaffolder = ProjectScaffolder()
structure = scaffolder.generate_structure({'name': 'test', 'type': 'python'})
print(f'✅ Generated {len(structure)} files' if structure else '❌ Failed')
"
```

### 10. Test Creative Engine
```bash
python -c "
from engines.creative_engine import CreativeEngine
creative = CreativeEngine()
result = creative.generate('Write a poem')
print('✅ Creative engine working' if result else '❌ Failed')
"
```

### 11. Test Memory System
```bash
python -c "
from memory.personal_memory import PersonalMemory
mem = PersonalMemory()
mem.store('test', {'value': 'test'})
retrieved = mem.retrieve('test')
print('✅ Memory system working' if retrieved else '❌ Failed')
"
```

## 📁 Project Organization

### Current Structure
```
Ananta_Rebirth/
├── 📋 Entry Points
│   ├── main.py              # Terminal interface
│   ├── gui_launcher.py      # GUI launcher
│   └── run_tests.py         # Test runner
│
├── 🧠 Core Engines (core/)
│   ├── controller.py        # Main orchestrator
│   ├── ollama_client.py     # LLM integration
│   ├── retriever.py         # Vector database
│   ├── context_engine.py    # Context management
│   ├── emotional_intelligence.py
│   ├── security_engine.py
│   ├── system_monitor.py
│   └── ... (more engines)
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
│   └── test_features_individual.py
│
└── 📚 Documentation
    ├── README.md
    ├── PROJECT_STRUCTURE.md
    ├── TESTING_GUIDE.md
    ├── TESTING_SETUP.md
    └── ... (more docs)
```

### File Organization Checklist
- ✅ All core engines in `core/`
- ✅ All intelligence modules in `intelligence/`
- ✅ All automation in `automation/`
- ✅ All memory systems in `memory/`
- ✅ All specialized engines in `engines/`
- ✅ All features in `features/`
- ✅ All UI components in `ui/`
- ✅ All utilities in `utils/`
- ✅ All tests in `tests/`
- ✅ All documentation in root or `docs/`

## 🔍 Troubleshooting

### Ollama Not Running
```
Error: Ollama not running - skipping
```

**Solution:**
1. Open a new terminal
2. Run: `ollama serve`
3. Wait for: `Listening on 127.0.0.1:11434`
4. Run tests again

### GPU Not Available
```
Error: GPU not available, using CPU
```

**Solution:**
1. Check NVIDIA GPU drivers: `nvidia-smi`
2. Install CUDA toolkit
3. Reinstall PyTorch with CUDA:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Memory Issues
```
Error: CUDA out of memory
```

**Solution:**
1. Reduce batch size in `config.py`
2. Close other GPU applications
3. Use CPU temporarily

### Import Errors
```
Error: ModuleNotFoundError: No module named 'X'
```

**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

## 📈 Test Results

### Expected Results
- **Quick Test**: ~10 tests, 2-3 minutes
- **Individual Tests**: ~11 tests, 5-10 minutes
- **All Tests**: ~30+ tests, 10-15 minutes

### Success Criteria
- ✅ All core engines load successfully
- ✅ All features initialize without errors
- ✅ Ollama integration works (if running)
- ✅ Memory systems function correctly
- ✅ Security checks pass
- ✅ System monitoring works

## 🎯 Next Steps

### After Successful Testing

1. **Run Terminal Interface**
   ```bash
   python main.py
   ```
   
   Commands:
   - `help` - Show commands
   - `status` - Show system status
   - `capabilities` - Show features
   - `image <path>` - Analyze image
   - `quit` - Exit

2. **Run GUI Interface**
   ```bash
   python gui_launcher.py
   ```

3. **Customize Configuration**
   - Edit `config.py`
   - Set preferred model
   - Configure GPU settings
   - Enable/disable features

4. **Add Personal Memories**
   - Use memory system to store information
   - Build knowledge base
   - Customize personality

## 📚 Documentation

- **README.md** - Main documentation
- **PROJECT_STRUCTURE.md** - Architecture overview
- **TESTING_GUIDE.md** - Detailed testing guide
- **QUICK_START_GUIDE.md** - Quick start instructions
- **FILE_ORGANIZATION_CHECKLIST.md** - Organization details

## 🆘 Support

### Getting Help
1. Check test output for error messages
2. Review `test_report.json` for details
3. Check individual feature documentation
4. Review logs in `data/` directory

### Common Issues
- Ollama not running → Start with `ollama serve`
- GPU not available → Check NVIDIA drivers
- Memory issues → Reduce batch size
- Import errors → Reinstall dependencies

## ✅ Verification Checklist

Before considering setup complete:
- [ ] All dependencies installed
- [ ] Ollama running (if needed)
- [ ] Quick test passes
- [ ] Individual tests pass
- [ ] Project structure verified
- [ ] Documentation reviewed
- [ ] Terminal interface works
- [ ] GUI interface works

## 🎉 Success!

Once all tests pass, you have:
- ✅ Fully functional Ananta Rebirth
- ✅ All features working
- ✅ Clean project organization
- ✅ Comprehensive testing setup
- ✅ Complete documentation

Ready to use Ananta for:
- 🤖 AI conversations
- 👁️ Image analysis
- 🤖 Automation
- 💾 Memory management
- 🎨 Creative generation
- 💻 Code analysis
- 🎤 Voice interaction

## 📞 Quick Commands Reference

```bash
# Quick test (2-3 min)
python quick_test.py

# Individual feature tests (5-10 min)
python tests/test_features_individual.py

# All tests (10-15 min)
python run_tests.py

# Terminal interface
python main.py

# GUI interface
python gui_launcher.py

# Start Ollama (in separate terminal)
ollama serve
```

---

**Status**: ✅ Ready for testing and use!
