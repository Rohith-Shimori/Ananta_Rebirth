# 🚀 OPTIMIZATION COMPONENTS - QUICK REFERENCE

**Quick access guide for all new optimization components**

---

## 📦 Component Locations

| Component | File | Lines | Purpose |
|-----------|------|-------|---------|
| Batch Inference | `core/batch_inference_engine.py` | 273 | Process multiple queries efficiently |
| Context Window Mgr | `core/context_window_manager.py` | 340 | Optimize context per model |
| Agent Orchestrator | `core/lightweight_agent_orchestrator.py` | 336 | Multi-agent task execution |
| Usage Tracker | `core/usage_pattern_tracker.py` | 380 | Learn usage patterns |
| Preloader | `core/intelligent_preloader.py` | 360 | Predictive model loading |
| Vector DB | `memory/lightweight_vector_db.py` | 304 | Semantic search |

---

## 🎯 Quick Usage Examples

### 1. Batch Inference Engine

**Process multiple queries at once:**

```python
from core.batch_inference_engine import BatchInferenceEngine

engine = BatchInferenceEngine()

# Add queries
queries = [
    "What is Python?",
    "Explain machine learning",
    "Write a function",
    "Prove P=NP",
]

# Process batch
results = await engine.process_batch(queries)

# Get stats
engine.print_batch_stats()
```

**Key Methods:**
- `add_query(query_id, query, priority)` - Add single query
- `process_batch(queries)` - Process list of queries
- `classify_queries()` - Group by complexity
- `get_batch_stats()` - Get statistics

---

### 2. Context Window Manager

**Optimize context for each model:**

```python
from core.context_window_manager import ContextWindowManager

mgr = ContextWindowManager()

# Get optimal size for model
optimal_size = mgr.get_optimal_context_size("sentinel")
print(f"Optimal context: {optimal_size} tokens")

# Compress context while preserving facts
long_context = "Important: ... Key: ... Note: ..."
compressed, ratio = mgr.compress_context(long_context, "sentinel")
print(f"Compression ratio: {ratio:.2f}")

# Auto-fit context to model
fitted = mgr.fit_context_to_model(context, "sentinel")

# Get window info
info = mgr.get_window_info("sentinel")
print(f"Max tokens: {info['max_tokens']}")

# Print stats
mgr.print_window_info()
mgr.print_compression_stats()
```

**Key Methods:**
- `get_optimal_context_size(model)` - Get optimal window
- `compress_context(context, model, ratio)` - Compress with preservation
- `fit_context_to_model(context, model)` - Auto-fit
- `should_compress_context(tokens, model)` - Check if compression needed
- `get_all_windows()` - Get all configurations

---

### 3. Agent Orchestrator

**Execute complex multi-step tasks:**

```python
from core.lightweight_agent_orchestrator import LightweightAgentOrchestrator

orchestrator = LightweightAgentOrchestrator()

# Execute complex task
result = await orchestrator.execute_complex_task(
    "Build a Python web scraper with error handling"
)

# Result structure:
# {
#     "main_task": "...",
#     "plan": {...},
#     "subtask_results": [...],
#     "final_review": "...",
#     "status": "completed",
#     "total_steps": 6
# }

# Get stats
stats = orchestrator.get_orchestrator_stats()
orchestrator.print_orchestrator_info()
```

**Agents:**
- **Planner** (flash) - Fast planning
- **Researcher** (sentinel) - Deep research
- **Coder** (architect) - Code generation
- **Critic** (oracle) - Quality review

**Key Methods:**
- `execute_complex_task(task)` - Run multi-step task
- `route_subtask(subtask)` - Route to appropriate agent
- `switch_model(model)` - Switch models
- `get_orchestrator_stats()` - Get statistics

---

### 4. Usage Pattern Tracker

**Learn and predict usage patterns:**

```python
from core.usage_pattern_tracker import UsagePatternTracker

tracker = UsagePatternTracker()

# Track query execution
tracker.track_query(
    model="sentinel",
    response_time=2.5,
    success=True,
    query_type="general"
)

# Track model switches
tracker.track_model_switch(
    from_model="sentinel",
    to_model="architect",
    switch_time=2.5,
    context="code task detected"
)

# Predict next model
next_model = tracker.predict_next_model()
print(f"Next model: {next_model}")

# Get statistics
stats = tracker.get_all_statistics()
model_stats = tracker.get_model_statistics("sentinel")

# Print stats
tracker.print_statistics()
tracker.print_model_statistics("sentinel")

# Save patterns
tracker._save_patterns()
```

**Key Methods:**
- `track_query(model, response_time, success, query_type)` - Record query
- `track_model_switch(from, to, time, context)` - Record switch
- `predict_next_model()` - Predict next model
- `get_model_statistics(model)` - Get per-model stats
- `get_all_statistics()` - Get all stats

---

### 5. Intelligent Preloader

**Predictively preload models:**

```python
from core.intelligent_preloader import IntelligentPreloader
from core.usage_pattern_tracker import UsagePatternTracker

# Create with usage tracker
tracker = UsagePatternTracker()
preloader = IntelligentPreloader(usage_tracker=tracker)

# Predict next models
predictions = preloader.predict_next_models(k=3)
for model, confidence in predictions:
    print(f"{model}: {confidence:.1%}")

# Schedule preloads
for model, confidence in predictions:
    priority = int(confidence * 10)
    task = preloader.schedule_preload(model, priority=priority)

# Process preload queue
for task in preloader.preload_queue:
    success = await preloader.preload_model(task.model)
    print(f"{task.model}: {'✅' if success else '❌'}")

# Get stats
stats = preloader.get_preload_stats()
preloader.print_preload_stats()

# Unload model
preloader.unload_model("sentinel")
```

**Key Methods:**
- `predict_next_models(k)` - Predict k models
- `schedule_preload(model, priority, delay)` - Schedule preload
- `preload_model(model)` - Preload model
- `process_preload_queue()` - Process queue
- `predictive_preload()` - Background preloading
- `get_preload_stats()` - Get statistics

---

### 6. Lightweight Vector Database

**Semantic search with embeddings:**

```python
from memory.lightweight_vector_db import LightweightVectorDB

db = LightweightVectorDB()

# Store documents
db.store_and_index(
    "Python is a programming language",
    {"category": "programming", "importance": 8}
)

# Search
results = db.search("programming languages", k=5)
for result in results:
    print(f"Distance: {result['distance']:.3f}")
    print(f"Metadata: {result['metadata']}")

# Get stats
stats = db.get_stats()
db.print_stats()
```

**Key Methods:**
- `store_and_index(text, metadata)` - Store document
- `search(query, k)` - Semantic search
- `get_stats()` - Get statistics

---

## 🔌 Integration in Controller

All components are initialized in `AnantaController`:

```python
from core.controller import AnantaController

controller = AnantaController()

# Access components
batch_engine = controller.batch_engine
context_mgr = controller.context_window_mgr
orchestrator = controller.agent_orchestrator
tracker = controller.usage_tracker
preloader = controller.preloader
vector_db = controller.vector_db
```

---

## 📊 Performance Targets

| Component | Metric | Target | Status |
|-----------|--------|--------|--------|
| Batch Inference | Throughput | 3-5x | ✅ |
| Context Window | Compression | 30% reduction | ✅ |
| Agent Orchestrator | Task Handling | Multi-step | ✅ |
| Usage Tracker | Prediction | Real-time | ✅ |
| Preloader | Switch Time | 2-3s | ✅ |
| Vector DB | Search Speed | 10x faster | ✅ |

---

## 🧪 Testing

**Run full test suite:**

```bash
python test_optimization_integration.py
```

**Expected Output:**
```
✅ 7/7 tests passed
- Batch Inference Engine
- Agent Orchestrator
- Vector Database
- Context Window Manager
- Usage Pattern Tracker
- Intelligent Preloader
- Full Integration
```

---

## 📈 Workflow Example

**Complete optimization workflow:**

```python
import asyncio
from core.controller import AnantaController

async def optimized_query_workflow(user_input: str):
    controller = AnantaController()
    
    # 1. Track usage pattern
    start_time = time.time()
    controller.usage_tracker.track_query(
        model="sentinel",
        response_time=0,
        success=True,
        query_type="general"
    )
    
    # 2. Predict next model
    next_model = controller.usage_tracker.predict_next_model()
    
    # 3. Preload next model
    controller.preloader.schedule_preload(next_model, priority=9)
    
    # 4. Optimize context
    context = "..."  # Get context
    optimal_context = controller.context_window_mgr.fit_context_to_model(
        context, "sentinel"
    )
    
    # 5. Store in vector DB
    controller.vector_db.store_and_index(
        user_input,
        {"importance": 8}
    )
    
    # 6. Process query (existing logic)
    response = controller.query(user_input)
    
    # 7. Track response time
    response_time = time.time() - start_time
    controller.usage_tracker.track_query(
        model="sentinel",
        response_time=response_time,
        success=True
    )
    
    return response

# Run
result = asyncio.run(optimized_query_workflow("Your query here"))
```

---

## 🎯 Configuration

**All components use settings from `config.py`:**

```python
# GPU Settings (Already Optimized)
GPU_SETTINGS = {
    "num_gpu": 1,
    "main_gpu": 0,
    "num_thread": 12,
    "use_mmap": True,
    "use_mlock": True,
    "num_batch": 512,
    "num_ctx": 4096,
    "f16_kv": True,
    "low_vram": False,
}

# Model Configuration
OPTIMAL_MODELS = {
    "sentinel": {...},
    "architect": {...},
    "oracle": {...},
    "flash": {...},
    "vision": {...},
    "nano": {...},
}

# Context Windows
CONTEXT_WINDOW = 4096
MAX_CONTEXT_WINDOW = 8192
```

---

## 🔍 Debugging & Monitoring

**Print component info:**

```python
# Batch engine stats
controller.batch_engine.print_batch_stats()

# Context window info
controller.context_window_mgr.print_window_info()
controller.context_window_mgr.print_compression_stats()

# Agent orchestrator info
controller.agent_orchestrator.print_orchestrator_info()

# Usage tracker stats
controller.usage_tracker.print_statistics()
controller.usage_tracker.print_model_statistics("sentinel")

# Preloader stats
controller.preloader.print_preload_stats()

# Vector DB stats
controller.vector_db.print_stats()
```

---

## 📚 Additional Resources

- **Full Implementation:** `IMPLEMENTATION_COMPLETE.md`
- **Analysis Document:** `DEEP_ANALYSIS_AND_IMPROVEMENT_PLAN.md`
- **Test Suite:** `test_optimization_integration.py`
- **Component Code:** See individual files in `core/` and `memory/`

---

**Happy Optimizing!** 🚀
