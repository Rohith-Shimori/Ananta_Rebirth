# Ananta Rebirth - Project Structure

## Overview
Ananta Rebirth is a comprehensive local AI assistant with vision, automation, and intelligence capabilities.

## Directory Organization

```
Ananta_Rebirth/
├── 📋 Configuration & Entry Points
│   ├── config.py                 # Global configuration
│   ├── main.py                   # Terminal interface entry point
│   ├── gui_launcher.py           # GUI launcher
│   └── requirements.txt          # Python dependencies
│
├── 🧠 Core AI Engines (core/)
│   ├── controller.py             # Main orchestrator
│   ├── ollama_client.py          # Ollama LLM integration
│   ├── retriever.py              # Vector database (ChromaDB)
│   ├── context_engine.py         # Context management
│   ├── emotional_intelligence.py # Emotion analysis
│   ├── security_engine.py        # Security & safety
│   ├── system_monitor.py         # System metrics
│   ├── brain_manager.py          # Brain state management
│   ├── batch_inference_engine.py # Batch processing
│   ├── hybrid_inference_engine.py# Hybrid inference
│   ├── lightweight_agent_orchestrator.py # Agent coordination
│   ├── proactive_intelligence.py # Proactive suggestions
│   └── smart_model_router.py     # Model routing
│
├── 🎯 Intelligence Engines (intelligence/)
│   ├── reasoning_engine.py       # Advanced reasoning
│   ├── learning_engine.py        # Self-improvement
│   ├── knowledge_base.py         # Knowledge storage
│   └── ... (other intelligence modules)
│
├── 🤖 Automation (automation/)
│   ├── workflow_engine.py        # Workflow automation
│   ├── task_scheduler.py         # Task scheduling
│   ├── rule_engine.py            # Rule-based automation
│   └── ... (other automation modules)
│
├── 💾 Memory Systems (memory/)
│   ├── personal_memory.py        # Personal memories
│   ├── knowledge_memory.py       # Knowledge storage
│   ├── episodic_memory.py        # Event memories
│   └── ... (other memory modules)
│
├── 🎨 Specialized Engines (engines/)
│   ├── code_expert.py            # Code analysis & generation
│   ├── creative_engine.py        # Creative content
│   ├── personality_engine.py     # Personality traits
│   ├── project_scaffolder.py     # Project generation
│   └── data/                     # Engine data files
│
├── ✨ Features (features/)
│   ├── voice_interface.py        # Voice I/O
│   ├── advanced_voice_interface.py # Advanced voice features
│   ├── code_executor.py          # Code execution
│   ├── proactive_assistant.py    # Proactive features
│   └── __init__.py
│
├── 🎨 User Interface (ui/)
│   ├── main_window.py            # Main GUI window
│   ├── components.py             # UI components
│   ├── advanced_avatar.py        # Avatar system
│   ├── styles.py                 # Styling
│   └── ... (other UI modules)
│
├── 🛠️ Utilities (utils/)
│   ├── helpers.py                # Helper functions
│   ├── validators.py             # Input validation
│   └── ... (other utilities)
│
├── 📊 Data Storage (data/)
│   ├── chroma_db/                # Vector database
│   ├── memories/                 # Memory storage
│   └── ... (other data)
│
├── ✅ Tests (tests/)
│   ├── test_features_individual.py # Individual feature tests
│   ├── test_core.py              # Core functionality tests
│   └── ... (other tests)
│
└── 📚 Documentation
    ├── README.md                 # Main documentation
    ├── QUICK_START_GUIDE.md      # Quick start
    ├── TESTING_AND_INTEGRATION_GUIDE.md
    └── ... (other docs)
```

## Key Components

### 1. Core AI Engines (`core/`)
- **controller.py**: Main orchestrator that coordinates all engines
- **ollama_client.py**: Interface to Ollama LLM service
- **retriever.py**: Vector database for semantic search
- **context_engine.py**: Manages conversation context
- **emotional_intelligence.py**: Analyzes and responds to emotions
- **security_engine.py**: Validates prompts and ensures safety

### 2. Intelligence Systems (`intelligence/`)
- Advanced reasoning and decision-making
- Self-learning and improvement
- Knowledge base management
- Context awareness

### 3. Automation (`automation/`)
- Workflow automation
- Task scheduling
- Rule-based automation
- Batch processing

### 4. Memory Systems (`memory/`)
- Personal memories (user interactions)
- Knowledge memories (learned information)
- Episodic memories (events and contexts)
- Semantic memories (concepts and relationships)

### 5. Specialized Engines (`engines/`)
- **code_expert.py**: Code analysis, review, and generation
- **creative_engine.py**: Creative content generation
- **personality_engine.py**: Personality and persona management
- **project_scaffolder.py**: Project structure generation

### 6. Features (`features/`)
- **voice_interface.py**: Speech recognition and synthesis
- **code_executor.py**: Safe code execution
- **proactive_assistant.py**: Proactive suggestions and help

### 7. User Interface (`ui/`)
- Modern PyQt6-based GUI
- Advanced avatar system
- Real-time visualizations
- Interactive components

## Testing

### Individual Feature Tests
Run individual feature tests with:
```bash
python tests/test_features_individual.py
```

This tests:
- Retriever (Vector Database)
- Ollama Client (LLM)
- Emotional Intelligence
- Context Engine
- Security Engine
- System Monitor
- Code Executor
- Voice Interface
- Project Scaffolder
- Creative Engine
- Memory System

### Comprehensive Tests
Run comprehensive tests with:
```bash
python comprehensive_test.py
```

## Entry Points

### Terminal Interface
```bash
python main.py
```

### GUI Interface
```bash
python gui_launcher.py
```

## Configuration

Edit `config.py` to customize:
- Model selection
- GPU settings
- Memory limits
- Feature toggles
- API endpoints

## Dependencies

See `requirements.txt` for all dependencies. Key packages:
- **torch**: Deep learning framework
- **transformers**: Hugging Face models
- **sentence-transformers**: Embedding models
- **chromadb**: Vector database
- **PyQt6**: GUI framework
- **ollama**: LLM client

## Performance Optimization

- GPU acceleration enabled for NVIDIA GPUs
- Batch processing for efficiency
- Model caching and reuse
- Memory management and cleanup
- Async operations where applicable

## Security

- Prompt injection detection
- Input validation
- Safe code execution sandbox
- Rate limiting
- Access control

## Future Enhancements

- [ ] Multi-modal learning
- [ ] Advanced reasoning chains
- [ ] Custom model fine-tuning
- [ ] Distributed processing
- [ ] Advanced analytics
