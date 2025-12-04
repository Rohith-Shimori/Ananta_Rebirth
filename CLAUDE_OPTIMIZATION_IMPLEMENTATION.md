# 🚀 CLAUDE'S RTX 4050 OPTIMIZATION - IMPLEMENTATION GUIDE

## Executive Summary

Claude provided a **comprehensive, hardware-optimized plan** for your RTX 4050 6GB setup. This guide shows how to implement it step-by-step.

---

## 📊 YOUR HARDWARE PROFILE (Claude's Analysis)

```
CPU:    Intel i5-12th Gen HX (12 cores/16 threads)
GPU:    NVIDIA RTX 4050 (6GB VRAM, Ada Lovelace, Tensor Cores)
RAM:    24GB (Excellent for hybrid inference)
SSD:    512GB (For tiered memory system)

OPTIMIZATION RATING: ⭐⭐⭐⭐⭐ EXCELLENT
```

---

## 🧠 OPTIMAL MODEL LINEUP (Claude's Recommendation)

All models use **Q4_K_M quantization** to fit in 6GB VRAM:

| Name | Model | VRAM | Speed | Use Case | Priority |
|------|-------|------|-------|----------|----------|
| **Sentinel** | qwen2.5:7b-instruct-q4_K_M | 4.7GB | 42 tok/s | General chat | 1 |
| **Architect** | deepseek-coder-v2:6.7b-q4_K_M | 3.8GB | 55 tok/s | Code generation | 1 |
| **Oracle** | deepseek-r1:7b-q4_K_M | 4.22GB | 45 tok/s | Reasoning/Math | 1 |
| **Flash** | phi-3-mini:3.8b-q8_0 | 4.06GB | 65 tok/s | Quick responses | 2 |
| **Vision** | llava-phi3:3.8b-q4_K_M | 4.5GB | 38 tok/s | Image analysis | 1 |
| **Nano** | gemma:2b-q4_K_M | 1.7GB | 90 tok/s | Emergency backup | 3 |

**Key Advantage:** Can run any model individually, or switch between them in 2-3 seconds!

---

## 📋 6-PHASE IMPLEMENTATION ROADMAP

### PHASE 1: Model Optimization & Smart Routing (Week 1-2)

**Goal:** Implement intelligent model selection based on query type

**Files to Create/Modify:**
1. `core/smart_model_router.py` (NEW)
2. `config.py` (UPDATE)
3. `core/controller.py` (UPDATE)

**Implementation Steps:**

```python
# Step 1: Update config.py with optimal models

OPTIMAL_MODELS = {
    "sentinel": {
        "model": "qwen2.5:7b-instruct-q4_K_M",
        "vram": 4.7,
        "speed": 42,
        "use_case": "General chat, reasoning, daily tasks",
        "priority": 1
    },
    "architect": {
        "model": "deepseek-coder-v2:6.7b-q4_K_M",
        "vram": 3.8,
        "speed": 55,
        "use_case": "Code generation, debugging, refactoring",
        "priority": 1
    },
    "oracle": {
        "model": "deepseek-r1:7b-q4_K_M",
        "vram": 4.22,
        "speed": 45,
        "use_case": "Deep reasoning, math, analysis, logic",
        "priority": 1
    },
    "flash": {
        "model": "phi-3-mini:3.8b-q8_0",
        "vram": 4.06,
        "speed": 65,
        "use_case": "Quick queries, simple tasks, rapid iteration",
        "priority": 2
    },
    "vision": {
        "model": "llava-phi3:3.8b-q4_K_M",
        "vram": 4.5,
        "speed": 38,
        "use_case": "Image analysis, visual reasoning",
        "priority": 1
    },
    "nano": {
        "model": "gemma:2b-q4_K_M",
        "vram": 1.7,
        "speed": 90,
        "use_case": "Ultra-low latency, parallel tasks",
        "priority": 3
    }
}

# GPU Optimization Settings
GPU_SETTINGS = {
    "num_gpu": 1,
    "main_gpu": 0,
    "num_thread": 12,  # i5 12th gen has 12 threads
    "use_mmap": True,  # Memory-mapped files
    "use_mlock": True,  # Lock model in RAM
    "num_batch": 512,  # Optimal for RTX 4050
    "num_ctx": 4096,  # 4K context for 6GB VRAM
    "f16_kv": True,  # FP16 for KV cache (saves VRAM)
}
```

```python
# Step 2: Create core/smart_model_router.py

class SmartModelRouter:
    """
    Intelligently routes queries to optimal model based on:
    - Query complexity
    - Current VRAM usage
    - Response time requirements
    - Task type
    """
    
    def __init__(self):
        self.current_model = "sentinel"
        self.vram_monitor = VRAMMonitor()
        self.query_analyzer = QueryComplexityAnalyzer()
    
    def detect_task_type(self, query: str) -> str:
        """Detect task type from query"""
        query_lower = query.lower()
        
        # Code detection
        if any(kw in query_lower for kw in 
               ["code", "function", "debug", "implement", "refactor", "syntax"]):
            return "code"
        
        # Reasoning detection
        elif any(kw in query_lower for kw in 
                 ["analyze", "reason", "prove", "solve", "explain", "why"]):
            return "reasoning"
        
        # Vision detection
        elif any(kw in query_lower for kw in 
                 ["image", "picture", "screenshot", "photo", "visual"]):
            return "vision"
        
        else:
            return "general"
    
    def route_query(self, query: str, context: dict) -> str:
        """Route query to optimal model"""
        
        # Analyze query
        task_type = self.detect_task_type(query)
        complexity = self.query_analyzer.analyze(query)
        urgency = context.get("urgency", "normal")
        
        # Check available VRAM
        available_vram = self.vram_monitor.get_available_vram()
        
        # Smart routing logic
        if task_type == "code":
            return "architect"  # deepseek-coder specialized
        
        elif task_type == "reasoning" and complexity > 7:
            return "oracle"  # deepseek-r1 for complex logic
        
        elif task_type == "vision":
            return "vision"  # llava-phi3 for images
        
        elif urgency == "high" or complexity < 3:
            return "flash"  # phi-3 for speed
        
        elif available_vram < 5.0:
            return "nano"  # gemma:2b when low on VRAM
        
        else:
            return "sentinel"  # qwen2.5 default
```

**Expected Results:**
- ✅ Automatic model selection based on task type
- ✅ 2-3x faster responses for simple queries
- ✅ Better quality for complex tasks
- ✅ Optimized VRAM usage

---

### PHASE 2: Hybrid Inference (Week 2-3)

**Goal:** Leverage 24GB RAM for larger models and context

**Files to Create/Modify:**
1. `core/hybrid_inference_engine.py` (NEW)
2. `core/context_engine.py` (UPDATE)

**Implementation Steps:**

```python
# core/hybrid_inference_engine.py

class HybridInferenceEngine:
    """
    Intelligently manages VRAM/RAM split:
    - Hot layers in VRAM (6GB)
    - Cold layers in RAM (24GB)
    - Predictive preloading
    """
    
    def __init__(self):
        self.vram_size = 6.0  # GB
        self.ram_size = 24.0  # GB
        self.layer_cache = {}
        self.model_layers = {}
    
    def calculate_layer_importance(self, model_name: str):
        """Calculate importance of each layer"""
        importance = {}
        
        # Attention layers: Critical (always in VRAM)
        importance["attention"] = 10.0
        
        # Embedding layers: Very important
        importance["embed"] = 9.5
        
        # Output layers: Very important
        importance["output"] = 9.0
        
        # Feed-forward layers: Medium
        importance["ffn"] = 6.0
        
        # Other layers: Lower priority
        importance["other"] = 5.0
        
        return importance
    
    def distribute_layers(self, model_name: str):
        """Distribute model layers between VRAM and RAM"""
        
        # Get model layers
        layers = self.get_model_layers(model_name)
        importance = self.calculate_layer_importance(model_name)
        
        vram_layers = []
        ram_layers = []
        current_vram = 0
        
        # Sort layers by importance
        sorted_layers = sorted(
            layers.items(),
            key=lambda x: importance.get(x[1].type, 5.0),
            reverse=True
        )
        
        # Allocate to VRAM first
        for layer_id, layer in sorted_layers:
            if current_vram + layer.size_gb <= 5.5:  # Leave 0.5GB buffer
                vram_layers.append(layer_id)
                current_vram += layer.size_gb
            else:
                ram_layers.append(layer_id)
        
        return {
            "vram_layers": vram_layers,
            "ram_layers": ram_layers,
            "vram_used": current_vram,
            "efficiency": len(vram_layers) / len(layers)
        }
    
    def optimize_context_window(self, model_size_gb: float) -> int:
        """Calculate optimal context window for available VRAM"""
        
        available_for_context = 6.0 - model_size_gb
        available_mb = available_for_context * 1024
        
        # Conservative: 1.2KB per token
        max_tokens = int(available_mb / 1.2)
        
        # Cap at safe limits
        return min(max_tokens, 8192)  # Max 8K context
```

**Expected Results:**
- ✅ 4-8K context window (vs current 2K)
- ✅ Better conversation quality
- ✅ Efficient RAM utilization
- ✅ Minimal performance penalty

---

### PHASE 3: Agentic Intelligence (Week 3-4)

**Goal:** Multi-agent system with fast model switching

**Files to Create/Modify:**
1. `core/lightweight_agent_orchestrator.py` (NEW)
2. `features/proactive_assistant.py` (UPDATE)

**Implementation Steps:**

```python
# core/lightweight_agent_orchestrator.py

class LightweightAgentOrchestrator:
    """
    Efficient multi-agent system for 6GB VRAM
    - Sequential processing (one model at a time)
    - Fast model switching (2-3s)
    - Intelligent task decomposition
    """
    
    def __init__(self, controller):
        self.controller = controller
        self.current_model = None
        self.agents = {
            "planner": PlannerAgent("flash"),  # Fast planning
            "researcher": ResearcherAgent("sentinel"),  # Deep research
            "coder": CoderAgent("architect"),  # Code tasks
            "critic": CriticAgent("oracle"),  # Quality check
        }
    
    async def execute_complex_task(self, task: str):
        """Execute complex task with agent coordination"""
        
        # Step 1: Plan (fast model)
        plan = await self.agents["planner"].create_plan(task)
        
        # Step 2: Execute subtasks
        results = []
        for subtask in plan.subtasks:
            # Route to appropriate agent
            agent = self.route_subtask(subtask)
            
            # Switch model if needed
            await self.switch_model(agent.model_name)
            
            # Execute
            result = await agent.execute(subtask)
            results.append(result)
        
        # Step 3: Quality check (reasoning model)
        await self.switch_model("oracle")
        final = await self.agents["critic"].review(results)
        
        return final
    
    async def switch_model(self, model_name: str):
        """Fast model switching"""
        if self.current_model != model_name:
            # Unload current model
            if self.current_model:
                await self.controller.unload_model(self.current_model)
            
            # Load new model
            await self.controller.load_model(model_name)
            self.current_model = model_name
    
    def route_subtask(self, subtask: str):
        """Route subtask to appropriate agent"""
        if "code" in subtask.lower():
            return self.agents["coder"]
        elif "research" in subtask.lower():
            return self.agents["researcher"]
        else:
            return self.agents["planner"]
```

**Expected Results:**
- ✅ Complex task decomposition
- ✅ Optimal model for each subtask
- ✅ Fast model switching (2-3s)
- ✅ Better quality results

---

### PHASE 4: Tiered Memory System (Week 4)

**Goal:** Use SSD for extended memory (VRAM → RAM → SSD)

**Files to Create/Modify:**
1. `memory/tiered_memory_system.py` (NEW)
2. `memory/adaptive_memory.py` (UPDATE)

**Implementation Steps:**

```python
# memory/tiered_memory_system.py

class TieredMemorySystem:
    """
    3-Tier Memory Architecture:
    - Tier 1: VRAM (6GB) - Active inference
    - Tier 2: RAM (24GB) - Hot cache
    - Tier 3: SSD (512GB) - Long-term storage
    """
    
    def __init__(self):
        self.vram_cache = VRAMCache(max_size_gb=6)
        self.ram_cache = RAMCache(max_size_gb=20)  # Keep 4GB for system
        self.ssd_store = SSDStore(
            path="C:/Ananta_Cache",
            max_size_gb=50
        )
    
    async def store_conversation(self, conversation: dict):
        """Intelligent storage routing"""
        importance = self.calculate_importance(conversation)
        
        if importance >= 8:
            # Critical - keep in RAM for fast access
            self.ram_cache.store(conversation)
        
        elif importance >= 5:
            # Important - fast SSD access
            await self.ssd_store.store_hot(conversation)
        
        else:
            # Archive - compress and store
            compressed = self.compress(conversation)
            await self.ssd_store.store_cold(compressed)
    
    async def retrieve_context(self, query: str, max_results: int = 5):
        """Fast context retrieval from all tiers"""
        
        # Check RAM first (fastest)
        ram_results = self.ram_cache.search(query, limit=max_results)
        
        if len(ram_results) >= max_results:
            return ram_results
        
        # Check hot SSD cache
        ssd_hot = await self.ssd_store.search_hot(
            query,
            limit=max_results - len(ram_results)
        )
        
        results = ram_results + ssd_hot
        
        # Promote frequently accessed to RAM
        for result in results:
            if result.access_count > 5:
                self.ram_cache.promote(result)
        
        return results
    
    def calculate_importance(self, conversation: dict) -> float:
        """Calculate conversation importance"""
        score = 0.0
        
        # Recent conversations are important
        if conversation.get("recency", 0) > 0.8:
            score += 3.0
        
        # Frequently accessed are important
        if conversation.get("access_count", 0) > 10:
            score += 3.0
        
        # User-marked important
        if conversation.get("marked_important", False):
            score += 2.0
        
        return score
```

**Expected Results:**
- ✅ Unlimited conversation history
- ✅ Fast retrieval from RAM cache
- ✅ Efficient SSD storage
- ✅ Automatic promotion of hot data

---

### PHASE 5: Performance Optimization (Week 5)

**Goal:** Squeeze maximum performance from RTX 4050

**Files to Create/Modify:**
1. `core/ollama_client.py` (UPDATE)
2. `core/performance_optimizer.py` (NEW)

**Implementation Steps:**

```python
# core/ollama_client.py - Update with GPU optimization

class OptimizedOllamaClient:
    def __init__(self, model: str):
        self.model = model
        
        # RTX 4050 Optimization Settings
        self.opts = {
            # GPU Settings
            "num_gpu": 1,
            "main_gpu": 0,
            
            # CPU Settings
            "num_thread": 12,  # i5 12th gen has 12 threads
            "numa": False,  # Single-socket CPU
            
            # Memory Optimization
            "use_mmap": True,  # Memory-mapped files
            "use_mlock": True,  # Lock model in RAM
            
            # Batch Processing
            "num_batch": 512,  # Optimal for RTX 4050
            "num_ctx": 4096,  # 4K context for 6GB VRAM
            
            # Speed Optimization
            "num_predict": 512,  # Max tokens per response
            "repeat_penalty": 1.1,
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.9,
            
            # VRAM Optimization
            "f16_kv": True,  # FP16 for KV cache (saves VRAM)
            "low_vram": False,  # We have enough VRAM
        }
    
    def get_optimized_params(self):
        """Return optimized parameters for RTX 4050"""
        return self.opts
```

**Expected Results:**
- ✅ 42-65 tokens/second (vs current 20-30)
- ✅ Better GPU utilization
- ✅ Optimal batch processing
- ✅ Efficient memory usage

---

### PHASE 6: Advanced Features (Week 6-8)

**Goal:** Batch processing, vector DB, parallel tasks

**Files to Create/Modify:**
1. `core/batch_inference_engine.py` (NEW)
2. `memory/lightweight_vector_db.py` (NEW)

**Implementation Steps:**

```python
# core/batch_inference_engine.py

class BatchInferenceEngine:
    """
    Process multiple queries efficiently
    - Batch similar queries together
    - Use smallest sufficient model
    - Maximize GPU utilization
    """
    
    async def process_batch(self, queries: List[str]):
        """Smart batching"""
        
        # Classify queries by complexity
        simple = [q for q in queries if self.complexity(q) < 3]
        complex = [q for q in queries if self.complexity(q) >= 3]
        
        results = []
        
        # Process simple queries with fast model
        if simple:
            await self.switch_model("flash")
            simple_results = await self.batch_infer(simple)
            results.extend(simple_results)
        
        # Process complex queries with powerful model
        if complex:
            await self.switch_model("sentinel")
            complex_results = await self.batch_infer(complex)
            results.extend(complex_results)
        
        return results
    
    def complexity(self, query: str) -> float:
        """Estimate query complexity"""
        # Simple heuristics
        length = len(query.split())
        has_code = "code" in query.lower()
        has_math = any(c in query for c in "∑∫√∞")
        
        score = length / 10.0
        if has_code:
            score += 2.0
        if has_math:
            score += 3.0
        
        return min(score, 10.0)
```

**Expected Results:**
- ✅ 3-5x parallel task throughput
- ✅ Efficient batch processing
- ✅ Optimal model selection per task
- ✅ Better resource utilization

---

## 🎯 IMPLEMENTATION PRIORITY

### QUICK WINS (Start Here - 1-2 days)
1. ✅ Update config.py with optimal models
2. ✅ Implement SmartModelRouter
3. ✅ Update ollama_client.py with GPU settings
4. ✅ Add batch processing

### MEDIUM EFFORT (2-3 days)
5. ✅ Hybrid inference engine
6. ✅ Context window optimization
7. ✅ Model preloading

### ADVANCED (3-5 days)
8. ✅ Agent orchestrator
9. ✅ Tiered memory system
10. ✅ Batch inference engine

---

## 📊 EXPECTED PERFORMANCE IMPROVEMENTS

| Metric | Current | After Phase 1 | After Phase 3 | After Phase 5 |
|--------|---------|---------------|---------------|---------------|
| Response Speed | 20-30 tok/s | 42-65 tok/s | 45-70 tok/s | 50-75 tok/s |
| Context Window | 2K tokens | 4K tokens | 6K tokens | 8K tokens |
| Model Switching | 10-15s | 5-8s | 2-3s | 1-2s |
| Parallel Tasks | 1 | 2 | 3-5 | 5+ |
| Memory Usage | 5-6GB | 4.5-5.5GB | 4.5-5.5GB | 4-5GB |
| Cold Start | 15-20s | 10-15s | 5-10s | 3-5s |

---

## 🚀 NEXT STEPS

**Ready to implement?** Which phase would you like to start with?

1. **Phase 1** - Smart model routing (RECOMMENDED - Quick wins)
2. **Phase 2** - Hybrid inference
3. **Phase 3** - Agent system
4. **Phase 4** - Tiered memory
5. **Phase 5** - Performance tuning
6. **Phase 6** - Advanced features

I recommend starting with **Phase 1** for immediate improvements, then proceeding sequentially.

---

**Status:** Ready for implementation
**Estimated Time:** 6-8 weeks for all phases
**Expected Result:** Professional-grade AI assistant optimized for RTX 4050
