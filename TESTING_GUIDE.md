# Ananta Rebirth - Testing Guide

## Quick Start

### Prerequisites
1. **Start Ollama** (required for full testing)
   ```bash
   ollama serve
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### Option 1: Run All Tests (Recommended)
```bash
python run_tests.py
```

This will:
- ✅ Check project structure
- ✅ Verify dependencies
- ✅ Verify Ollama setup
- ✅ Run individual feature tests
- ✅ Run comprehensive tests
- ✅ Generate test report

### Option 2: Run Individual Feature Tests Only
```bash
python tests/test_features_individual.py
```

Tests each feature independently:
- 🔍 **Retriever** - Vector database (ChromaDB)
- 🤖 **Ollama Client** - LLM integration
- ❤️ **Emotional Intelligence** - Emotion analysis
- 🧠 **Context Engine** - Context management
- 🔒 **Security Engine** - Safety checks
- 📊 **System Monitor** - System metrics
- 💻 **Code Executor** - Code execution
- 🎤 **Voice Interface** - Voice I/O
- 🏗️ **Project Scaffolder** - Project generation
- 🎨 **Creative Engine** - Creative content
- 🧠 **Memory System** - Memory storage

### Option 3: Run Comprehensive Tests
```bash
python comprehensive_test.py
```

Tests:
- Core functionality
- GUI components
- File structure

### Option 4: Run Terminal Interface
```bash
python main.py
```

Interactive commands:
- `help` - Show available commands
- `status` - Show system status
- `capabilities` - Show all capabilities
- `image <path>` - Analyze image
- `quit` - Exit

### Option 5: Run GUI Interface
```bash
python gui_launcher.py
```

## Test Results

### Understanding the Output

**Status Indicators:**
- ✅ **PASS** - Test passed successfully
- ❌ **FAIL** - Test failed
- ⏭️ **SKIP** - Test skipped (e.g., Ollama not running)
- ⚠️ **ERROR** - Unexpected error occurred

**Example Output:**
```
✅ Retriever (0.45s) - PASS
❌ Ollama Client (0.02s) - FAIL
⏭️ Voice Interface (0.00s) - SKIP
```

### Test Report
After running tests, a report is generated:
- **Location**: `test_report.json`
- **Contains**: Timestamp, duration, detailed results
- **Use**: Track test history and identify issues

## Individual Feature Testing

### 1. Testing Retriever (Vector Database)
```python
from core.retriever import Retriever

retriever = Retriever()
retriever.add_documents(
    ids=["doc1", "doc2"],
    documents=["Text 1", "Text 2"],
    metadatas=[{"type": "test"}, {"type": "test"}]
)
results = retriever.query("search text", top_k=2)
```

### 2. Testing Ollama Client
```python
from core.ollama_client import OllamaClient

client = OllamaClient()
response = client.generate("What is AI?", max_tokens=100)
print(response)
```

### 3. Testing Emotional Intelligence
```python
from core.emotional_intelligence import EmotionalIntelligence

ei = EmotionalIntelligence()
sentiment = ei.analyze_sentiment("I am very happy!")
print(sentiment)  # {'emotion': 'joy', 'score': 0.95}
```

### 4. Testing Context Engine
```python
from core.context_engine import ContextEngine

context = ContextEngine()
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
]
result = context.build_context(messages)
```

### 5. Testing Security Engine
```python
from core.security_engine import SecurityEngine

security = SecurityEngine()
is_safe = security.is_safe_prompt("What is Python?")
print(is_safe)  # True
```

### 6. Testing System Monitor
```python
from core.system_monitor import SystemMonitor

monitor = SystemMonitor()
stats = monitor.get_system_stats()
print(f"CPU: {stats['cpu_percent']}%")
print(f"RAM: {stats['memory_percent']}%")
```

### 7. Testing Code Executor
```python
from features.code_executor import CodeExecutor

executor = CodeExecutor()
result = executor.execute("print('Hello')")
```

### 8. Testing Voice Interface
```python
from features.voice_interface import VoiceInterface

voice = VoiceInterface()
voice.speak("Hello, this is a test")
```

### 9. Testing Project Scaffolder
```python
from engines.project_scaffolder import ProjectScaffolder

scaffolder = ProjectScaffolder()
structure = scaffolder.generate_structure({
    "name": "my_project",
    "type": "python"
})
```

### 10. Testing Creative Engine
```python
from engines.creative_engine import CreativeEngine

creative = CreativeEngine()
result = creative.generate("Write a poem about AI")
```

### 11. Testing Memory System
```python
from memory.personal_memory import PersonalMemory

memory = PersonalMemory()
memory.store("key", {"data": "value"})
retrieved = memory.retrieve("key")
```

## Troubleshooting

### Ollama Not Running
**Error**: `Ollama not running - skipping`

**Solution**:
1. Install Ollama from https://ollama.ai
2. Run `ollama serve` in a terminal
3. Run tests again

### GPU Not Available
**Error**: `GPU not available, using CPU`

**Solution**:
1. Ensure NVIDIA GPU drivers are installed
2. Install CUDA toolkit
3. Reinstall PyTorch with CUDA support:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Memory Issues
**Error**: `CUDA out of memory`

**Solution**:
1. Reduce batch size in `config.py`
2. Use CPU instead of GPU temporarily
3. Close other GPU-intensive applications

### Import Errors
**Error**: `ModuleNotFoundError: No module named 'X'`

**Solution**:
1. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```
2. Ensure you're in the correct directory
3. Check Python version (3.8+)

## Performance Benchmarks

Expected test times (with Ollama running):
- Individual tests: ~30-60 seconds
- Comprehensive tests: ~20-40 seconds
- Total: ~1-2 minutes

## Continuous Testing

### Run Tests on Schedule
```bash
# Run tests every hour
while true; do
    python run_tests.py
    sleep 3600
done
```

### Monitor Test Results
```bash
# Watch test report changes
watch -n 5 'cat test_report.json | python -m json.tool'
```

## Advanced Testing

### Test Specific Feature
```bash
python -c "
from tests.test_features_individual import FeatureTester
tester = FeatureTester()
tester.test_retriever()
"
```

### Run with Verbose Output
```bash
python run_tests.py 2>&1 | tee test_output.log
```

### Profile Performance
```bash
python -m cProfile -s cumulative tests/test_features_individual.py
```

## Test Coverage

Current test coverage:
- ✅ Core AI engines
- ✅ Memory systems
- ✅ Specialized engines
- ✅ Features
- ✅ System monitoring
- ✅ Security
- ⚠️ GUI components (manual testing)
- ⚠️ Voice interface (manual testing)

## Contributing Tests

To add new tests:

1. Create test method in `FeatureTester` class
2. Follow naming convention: `test_<feature_name>`
3. Return `TestResult` object
4. Add to `run_all_tests()` method

Example:
```python
def test_new_feature(self):
    """Test New Feature"""
    print("\n✨ Testing New Feature...")
    start = time.time()
    try:
        from module.new_feature import NewFeature
        feature = NewFeature()
        result = feature.do_something()
        
        if result:
            duration = time.time() - start
            result = TestResult("New Feature", "PASS", "Success", duration)
            self.results.append(result)
            return result
        else:
            raise Exception("Failed")
    except Exception as e:
        duration = time.time() - start
        result = TestResult("New Feature", "FAIL", str(e), duration)
        self.results.append(result)
        return result
```

## Support

For issues or questions:
1. Check test output for error messages
2. Review `test_report.json` for details
3. Check individual feature documentation
4. Review logs in `data/` directory

## Next Steps

After successful testing:
1. ✅ Run `python main.py` for terminal interface
2. ✅ Run `python gui_launcher.py` for GUI
3. ✅ Explore features and capabilities
4. ✅ Customize configuration in `config.py`
5. ✅ Add personal memories and knowledge
