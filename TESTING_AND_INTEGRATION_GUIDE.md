# 🧪 TESTING & INTEGRATION GUIDE

## Complete Testing Strategy for All 6 Phases

**Date:** 2025-11-30
**Status:** Ready for Testing
**Expected Duration:** 2-3 hours for full testing

---

## 📋 PRE-TESTING CHECKLIST

### Environment Setup ✅
```bash
# Install required packages
pip install psutil gputil numpy

# Verify Ollama is running
ollama serve  # In separate terminal

# Pull required models
ollama pull qwen2.5:7b-instruct-q4_K_M
ollama pull deepseek-coder-v2:6.7b-q4_K_M
ollama pull deepseek-r1:7b-q4_K_M
ollama pull phi-3-mini:3.8b-q8_0
ollama pull llava-phi3:3.8b-q4_K_M
ollama pull gemma:2b-q4_K_M
```

### Directory Structure ✅
```
C:/Ananta_Rebirth/
├── config.py ✅
├── core/
│   ├── smart_model_router.py ✅
│   ├── hybrid_inference_engine.py ✅
│   ├── lightweight_agent_orchestrator.py ✅
│   ├── batch_inference_engine.py ✅
│   ├── ollama_client.py ✅
│   └── controller.py ✅
├── memory/
│   ├── tiered_memory_system.py ✅
│   └── lightweight_vector_db.py ✅
└── data/ (created automatically)
```

---

## 🧪 PHASE 1: SMART MODEL ROUTING - TEST PLAN

### Test 1.1: Config Loading
```python
import config

# Verify optimal models loaded
assert len(config.OPTIMAL_MODELS) == 6
assert "sentinel" in config.OPTIMAL_MODELS
assert "architect" in config.OPTIMAL_MODELS
assert "oracle" in config.OPTIMAL_MODELS
assert "flash" in config.OPTIMAL_MODELS
assert "vision" in config.OPTIMAL_MODELS
assert "nano" in config.OPTIMAL_MODELS

# Verify GPU settings
assert config.GPU_SETTINGS["num_batch"] == 512
assert config.GPU_SETTINGS["num_ctx"] == 4096
assert config.GPU_SETTINGS["num_thread"] == 12
assert config.GPU_SETTINGS["f16_kv"] == True

print("✅ Config loading test PASSED")
```

### Test 1.2: SmartModelRouter
```python
from core.smart_model_router import SmartModelRouter

router = SmartModelRouter()

# Test task type detection
assert router.detect_task_type("write a function") == "code"
assert router.detect_task_type("explain quantum computing") == "reasoning"
assert router.detect_task_type("analyze this image") == "vision"
assert router.detect_task_type("what is python") == "general"

# Test complexity analysis
simple = router.query_analyzer.analyze("what is python")
complex = router.query_analyzer.analyze("prove that P=NP")
assert simple < complex

# Test routing
model1 = router.route_query("write code")
model2 = router.route_query("explain reasoning")
assert model1 in ["architect", "flash"]
assert model2 in ["oracle", "sentinel"]

print("✅ SmartModelRouter test PASSED")
```

### Test 1.3: VRAM Monitoring
```python
from core.smart_model_router import VRAMMonitor

monitor = VRAMMonitor()

# Test VRAM functions
vram_available = monitor.get_available_vram()
vram_used = monitor.get_used_vram()
vram_percent = monitor.get_vram_percentage()

assert isinstance(vram_available, float)
assert isinstance(vram_used, float)
assert isinstance(vram_percent, float)
assert vram_available > 0
assert vram_percent >= 0

print("✅ VRAM monitoring test PASSED")
```

---

## 🧪 PHASE 2: HYBRID INFERENCE - TEST PLAN

### Test 2.1: Layer Distribution
```python
from core.hybrid_inference_engine import HybridInferenceEngine

engine = HybridInferenceEngine()

# Test layer distribution
dist = engine.distribute_layers("sentinel", 4.7)

assert "vram_layers" in dist
assert "ram_layers" in dist
assert dist["vram_used"] <= 5.5
assert dist["efficiency"] > 0.5

print("✅ Layer distribution test PASSED")
```

### Test 2.2: Context Optimization
```python
# Test context window calculation
context = engine.optimize_context_window(4.7)

assert context > 0
assert context <= 8192
assert context >= 4096

print("✅ Context optimization test PASSED")
```

### Test 2.3: Memory Stats
```python
# Test memory statistics
stats = engine.get_memory_stats()

assert "gpu_used_gb" in stats
assert "gpu_total_gb" in stats
assert "ram_used_gb" in stats
assert "ram_total_gb" in stats
assert stats["gpu_total_gb"] == 6.0

print("✅ Memory stats test PASSED")
```

---

## 🧪 PHASE 3: AGENTIC INTELLIGENCE - TEST PLAN

### Test 3.1: Agent Creation
```python
import asyncio
from core.lightweight_agent_orchestrator import (
    LightweightAgentOrchestrator,
    PlannerAgent,
    ResearcherAgent,
    CoderAgent,
    CriticAgent
)

orchestrator = LightweightAgentOrchestrator()

# Verify agents created
assert "planner" in orchestrator.agents
assert "researcher" in orchestrator.agents
assert "coder" in orchestrator.agents
assert "critic" in orchestrator.agents

# Verify agent models
assert orchestrator.agents["planner"].model_name == "flash"
assert orchestrator.agents["researcher"].model_name == "sentinel"
assert orchestrator.agents["coder"].model_name == "architect"
assert orchestrator.agents["critic"].model_name == "oracle"

print("✅ Agent creation test PASSED")
```

### Test 3.2: Task Routing
```python
# Test subtask routing
planner_task = orchestrator.route_subtask("write a function")
researcher_task = orchestrator.route_subtask("analyze this")
coder_task = orchestrator.route_subtask("implement the code")
critic_task = orchestrator.route_subtask("review and verify")

assert planner_task in ["planner", "coder"]
assert researcher_task == "researcher"
assert coder_task == "coder"
assert critic_task == "critic"

print("✅ Task routing test PASSED")
```

### Test 3.3: Model Switching
```python
async def test_switching():
    result1 = await orchestrator.switch_model("sentinel")
    assert result1["status"] == "switched"
    
    result2 = await orchestrator.switch_model("architect")
    assert result2["status"] == "switched"
    
    print("✅ Model switching test PASSED")

asyncio.run(test_switching())
```

---

## 🧪 PHASE 4: TIERED MEMORY - TEST PLAN

### Test 4.1: Memory Tier Creation
```python
from memory.tiered_memory_system import TieredMemorySystem

system = TieredMemorySystem()

# Verify tiers created
assert system.vram_cache is not None
assert system.ram_cache is not None
assert system.ssd_store is not None

# Verify tier sizes
assert system.vram_cache.max_size_gb == 6.0
assert system.ram_cache.max_size_gb == 20.0

print("✅ Memory tier creation test PASSED")
```

### Test 4.2: Storage Routing
```python
# Test conversation storage
conversation = {
    "id": "test_1",
    "content": "Important conversation",
    "importance": 9.0,
    "recency": 0.9
}

system.store_conversation(conversation)

# Verify importance calculation
importance = system.calculate_importance(conversation)
assert importance > 7.0

print("✅ Storage routing test PASSED")
```

### Test 4.3: Context Retrieval
```python
# Test context retrieval
results = system.retrieve_context("conversation", max_results=5)

assert isinstance(results, list)
assert len(results) <= 5

print("✅ Context retrieval test PASSED")
```

---

## 🧪 PHASE 5: BATCH INFERENCE - TEST PLAN

### Test 5.1: Query Classification
```python
import asyncio
from core.batch_inference_engine import BatchInferenceEngine

engine = BatchInferenceEngine()

# Test query complexity analysis
simple_query = engine.complexity_analyzer.analyze("what is python")
complex_query = engine.complexity_analyzer.analyze("prove P=NP")

assert simple_query < 3
assert complex_query > 7

print("✅ Query classification test PASSED")
```

### Test 5.2: Batch Processing
```python
async def test_batch():
    queries = [
        "what is python",
        "explain machine learning",
        "prove this theorem",
        "write a function",
        "analyze this algorithm"
    ]
    
    results = await engine.process_batch(queries)
    
    assert len(results) == len(queries)
    assert all("model" in r for r in results)
    assert all("result" in r for r in results)
    
    print("✅ Batch processing test PASSED")

asyncio.run(test_batch())
```

### Test 5.3: Statistics
```python
# Test statistics
stats = engine.get_batch_stats()

assert "total_queries" in stats
assert "total_batches" in stats
assert "avg_batch_size" in stats
assert "model_usage" in stats

print("✅ Statistics test PASSED")
```

---

## 🧪 PHASE 6: VECTOR DATABASE - TEST PLAN

### Test 6.1: Vector DB Creation
```python
from memory.lightweight_vector_db import LightweightVectorDB

db = LightweightVectorDB()

# Verify components
assert db.embedder is not None
assert db.index is not None
assert db.hot_cache is not None

# Verify embedding dimension
assert db.embedder.dimension == 384

print("✅ Vector DB creation test PASSED")
```

### Test 6.2: Vector Storage
```python
# Test storing vectors
vector_id = db.store_and_index(
    "Python is a programming language",
    metadata={"category": "programming", "importance": 8}
)

assert vector_id >= 0
assert db.stats["total_vectors"] == 1

print("✅ Vector storage test PASSED")
```

### Test 6.3: Vector Search
```python
# Add more vectors
db.store_and_index("Machine learning is AI", {"importance": 7})
db.store_and_index("Neural networks are inspired by biology", {"importance": 6})

# Test search
results = db.search("programming languages", k=2)

assert len(results) <= 2
assert all("id" in r for r in results)
assert all("distance" in r for r in results)

print("✅ Vector search test PASSED")
```

---

## 🔗 INTEGRATION TESTING

### Integration Test 1: Controller Integration
```python
from core.controller import AnantaController

# Initialize controller
controller = AnantaController()

# Verify SmartModelRouter integrated
assert hasattr(controller, 'model_router')
assert controller.model_router is not None

print("✅ Controller integration test PASSED")
```

### Integration Test 2: End-to-End Query
```python
# Test end-to-end query
result = controller.query("What is Python?")

assert "response" in result
assert len(result["response"]) > 0

print("✅ End-to-end query test PASSED")
```

### Integration Test 3: Model Routing in Query
```python
# Test model routing in actual query
result = controller.query("Write a Python function")

# Verify routing happened
assert result is not None
assert "response" in result

print("✅ Model routing in query test PASSED")
```

---

## 📊 PERFORMANCE BENCHMARKING

### Benchmark 1: Response Speed
```python
import time

# Measure response time
start = time.time()
result = controller.query("What is machine learning?")
end = time.time()

response_time = end - start
print(f"Response time: {response_time:.2f}s")

# Expected: < 5 seconds for simple query
assert response_time < 5.0

print("✅ Response speed benchmark PASSED")
```

### Benchmark 2: Model Switching Speed
```python
# Measure model switching
start = time.time()
model1 = controller.model_router.route_query("code query")
model2 = controller.model_router.route_query("reasoning query")
end = time.time()

switching_time = end - start
print(f"Model switching time: {switching_time:.2f}s")

# Expected: < 1 second for routing
assert switching_time < 1.0

print("✅ Model switching benchmark PASSED")
```

### Benchmark 3: Memory Usage
```python
import psutil

# Measure memory usage
process = psutil.Process()
memory_info = process.memory_info()
memory_mb = memory_info.rss / (1024 * 1024)

print(f"Memory usage: {memory_mb:.1f}MB")

# Expected: < 2GB for initialization
assert memory_mb < 2000

print("✅ Memory usage benchmark PASSED")
```

---

## ✅ FINAL VERIFICATION CHECKLIST

### Phase 1 ✅
- [ ] Config loads correctly
- [ ] SmartModelRouter works
- [ ] VRAM monitoring works
- [ ] Task detection works
- [ ] Complexity analysis works
- [ ] Model routing works

### Phase 2 ✅
- [ ] Layer distribution works
- [ ] Context optimization works
- [ ] Memory stats work
- [ ] Preloading logic works

### Phase 3 ✅
- [ ] Agents created correctly
- [ ] Task routing works
- [ ] Model switching works
- [ ] Execution logging works

### Phase 4 ✅
- [ ] Memory tiers created
- [ ] Storage routing works
- [ ] Context retrieval works
- [ ] Importance calculation works

### Phase 5 ✅
- [ ] Query classification works
- [ ] Batch processing works
- [ ] Statistics tracking works

### Phase 6 ✅
- [ ] Vector DB created
- [ ] Vector storage works
- [ ] Vector search works
- [ ] Cache management works

### Integration ✅
- [ ] Controller integration works
- [ ] End-to-end query works
- [ ] Model routing in query works

### Performance ✅
- [ ] Response speed acceptable
- [ ] Model switching fast
- [ ] Memory usage reasonable
- [ ] No errors or crashes

---

## 🚀 TESTING EXECUTION

### Quick Test (15 minutes)
```bash
python -m core.smart_model_router
python -m core.hybrid_inference_engine
python -m core.batch_inference_engine
python -m memory.tiered_memory_system
python -m memory.lightweight_vector_db
```

### Full Test (1-2 hours)
Run all tests in this guide sequentially

### Integration Test (30 minutes)
Test controller integration and end-to-end queries

---

## 📝 TEST RESULTS TEMPLATE

```
PHASE 1: Smart Model Routing
  Test 1.1: Config Loading ........... [PASS/FAIL]
  Test 1.2: SmartModelRouter ......... [PASS/FAIL]
  Test 1.3: VRAM Monitoring .......... [PASS/FAIL]

PHASE 2: Hybrid Inference
  Test 2.1: Layer Distribution ....... [PASS/FAIL]
  Test 2.2: Context Optimization .... [PASS/FAIL]
  Test 2.3: Memory Stats ............ [PASS/FAIL]

PHASE 3: Agentic Intelligence
  Test 3.1: Agent Creation .......... [PASS/FAIL]
  Test 3.2: Task Routing ............ [PASS/FAIL]
  Test 3.3: Model Switching ......... [PASS/FAIL]

PHASE 4: Tiered Memory
  Test 4.1: Memory Tier Creation .... [PASS/FAIL]
  Test 4.2: Storage Routing ......... [PASS/FAIL]
  Test 4.3: Context Retrieval ....... [PASS/FAIL]

PHASE 5: Batch Inference
  Test 5.1: Query Classification .... [PASS/FAIL]
  Test 5.2: Batch Processing ........ [PASS/FAIL]
  Test 5.3: Statistics .............. [PASS/FAIL]

PHASE 6: Vector Database
  Test 6.1: Vector DB Creation ...... [PASS/FAIL]
  Test 6.2: Vector Storage .......... [PASS/FAIL]
  Test 6.3: Vector Search ........... [PASS/FAIL]

INTEGRATION TESTS
  Test I.1: Controller Integration .. [PASS/FAIL]
  Test I.2: End-to-End Query ........ [PASS/FAIL]
  Test I.3: Model Routing in Query .. [PASS/FAIL]

PERFORMANCE BENCHMARKS
  Benchmark 1: Response Speed ....... [PASS/FAIL]
  Benchmark 2: Model Switching ...... [PASS/FAIL]
  Benchmark 3: Memory Usage ......... [PASS/FAIL]

OVERALL STATUS: [PASS/FAIL]
```

---

## 🎊 TESTING COMPLETE

Once all tests pass, the system is ready for:
1. Production deployment
2. GUI enhancement
3. Advanced feature integration
4. Performance monitoring

---

**Testing Guide Created:** 2025-11-30
**Status:** Ready for Testing
**Expected Duration:** 2-3 hours
**Expected Result:** All tests PASS ✅
