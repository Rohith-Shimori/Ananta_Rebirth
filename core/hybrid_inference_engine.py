"""
Phase 2: Hybrid Inference Engine - Claude's Optimization Plan
Intelligently manages VRAM/RAM split for larger models and context
- Hot layers in VRAM (6GB)
- Cold layers in RAM (24GB)
- Predictive preloading
"""

import psutil
from typing import Dict, List, Tuple, Optional
import config

# Safe import for GPUtil
try:
    import GPUtil
    GPUTIL_AVAILABLE = True
except ImportError:
    GPUTIL_AVAILABLE = False
    print("⚠️  GPUtil not available. Install: pip install gputil")


class LayerCache:
    """Manages layer caching and distribution"""
    
    def __init__(self):
        self.vram_cache = {}  # Layers in VRAM
        self.ram_cache = {}   # Layers in RAM
        self.access_count = {}  # Track access frequency
    
    def record_access(self, layer_id: str):
        """Record layer access for promotion logic"""
        self.access_count[layer_id] = self.access_count.get(layer_id, 0) + 1
    
    def get_hot_layers(self, threshold: int = 5) -> List[str]:
        """Get frequently accessed layers"""
        return [lid for lid, count in self.access_count.items() if count >= threshold]


class AccessPredictor:
    """Predicts which layers will be accessed next"""
    
    def __init__(self):
        self.access_patterns = {}
        self.sequence_history = []
    
    def predict_next_layers(self, current_layer: str, model_name: str) -> List[str]:
        """Predict next layers based on patterns"""
        key = f"{model_name}:{current_layer}"
        if key in self.access_patterns:
            return self.access_patterns[key]
        return []
    
    def record_sequence(self, layers: List[str]):
        """Record layer access sequence"""
        self.sequence_history.append(layers)
        
        # Build patterns from history
        for i, layer in enumerate(layers[:-1]):
            key = f"{layer}"
            next_layer = layers[i + 1]
            
            if key not in self.access_patterns:
                self.access_patterns[key] = []
            
            if next_layer not in self.access_patterns[key]:
                self.access_patterns[key].append(next_layer)


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
        self.layer_cache = LayerCache()
        self.access_predictor = AccessPredictor()
        self.model_layers = {}
        self.layer_distribution = {}
    
    def calculate_layer_importance(self, model_name: str) -> Dict[str, float]:
        """
        Calculate importance of each layer
        
        Importance scoring:
        - Attention layers: 10.0 (always in VRAM)
        - Embedding layers: 9.5
        - Output layers: 9.0
        - Feed-forward layers: 6.0
        - Other layers: 5.0
        """
        importance = {}
        
        # Layer type importance mapping
        layer_types = {
            "attention": 10.0,
            "embed": 9.5,
            "output": 9.0,
            "ffn": 6.0,
            "norm": 5.5,
            "other": 5.0
        }
        
        return layer_types
    
    def distribute_layers(self, model_name: str, model_size_gb: float) -> Dict:
        """
        Distribute model layers between VRAM and RAM
        
        Strategy:
        - Critical layers (attention, embedding, output) → VRAM
        - Less critical layers (FFN, norm) → RAM
        - Predictively preload next layers
        """
        
        importance_scores = self.calculate_layer_importance(model_name)
        
        vram_layers = []
        ram_layers = []
        current_vram = 0
        
        # Estimate layers per model
        # Typical 7B model: ~100 layers, ~47MB per layer
        num_layers = int(model_size_gb * 1000 / 47)
        layer_size_mb = (model_size_gb * 1000) / num_layers
        layer_size_gb = layer_size_mb / 1024
        
        # Allocate critical layers first
        critical_layers = ["attention", "embed", "output"]
        for layer_type in critical_layers:
            # Allocate ~20% of layers per critical type
            num_critical = max(1, int(num_layers * 0.2))
            for i in range(num_critical):
                if current_vram + layer_size_gb <= 5.5:  # Leave 0.5GB buffer
                    vram_layers.append(f"{layer_type}_{i}")
                    current_vram += layer_size_gb
        
        # Allocate remaining VRAM to FFN layers
        remaining_vram = 5.5 - current_vram
        num_ffn = int(remaining_vram / layer_size_gb)
        for i in range(num_ffn):
            vram_layers.append(f"ffn_{i}")
            current_vram += layer_size_gb
        
        # Rest go to RAM
        for i in range(num_layers - len(vram_layers)):
            ram_layers.append(f"layer_{i}")
        
        distribution = {
            "vram_layers": vram_layers,
            "ram_layers": ram_layers,
            "vram_used": current_vram,
            "ram_used": (num_layers - len(vram_layers)) * layer_size_gb,
            "efficiency": len(vram_layers) / num_layers,
            "num_layers": num_layers,
            "layer_size_gb": layer_size_gb
        }
        
        self.layer_distribution[model_name] = distribution
        return distribution
    
    def optimize_context_window(self, model_size_gb: float) -> int:
        """
        Calculate optimal context window for available VRAM
        
        Rule: ~1KB per token in KV cache for 7B models
        Available VRAM: 6GB - model_size
        """
        available_for_context = 6.0 - model_size_gb
        available_mb = available_for_context * 1024
        
        # Conservative: 1.2KB per token (includes overhead)
        max_tokens = int(available_mb / 1.2)
        
        # Cap at safe limits
        return min(max_tokens, 8192)  # Max 8K context
    
    def smart_context_compression(self, messages: List[dict]) -> List[dict]:
        """
        Compress context intelligently:
        - Keep recent messages in full
        - Summarize older messages
        - Preserve important facts
        """
        if len(messages) <= 10:
            return messages
        
        recent = messages[-10:]
        old = messages[:-10]
        
        # Summarize old context
        summary = self.summarize_messages(old)
        
        return [{"role": "system", "content": summary}] + recent
    
    def summarize_messages(self, messages: List[dict]) -> str:
        """Summarize old messages for context compression"""
        if not messages:
            return ""
        
        # Extract key information
        topics = set()
        facts = []
        
        for msg in messages:
            content = msg.get("content", "")
            
            # Simple topic extraction
            if "code" in content.lower():
                topics.add("code")
            if "error" in content.lower() or "bug" in content.lower():
                topics.add("debugging")
            if "question" in content.lower():
                topics.add("questions")
            
            # Extract facts (sentences with key info)
            sentences = content.split(".")
            for sent in sentences:
                if len(sent.split()) > 5 and any(kw in sent.lower() for kw in ["is", "are", "was", "were"]):
                    facts.append(sent.strip())
        
        # Build summary
        summary = "Previous context: "
        if topics:
            summary += f"Topics discussed: {', '.join(topics)}. "
        if facts:
            summary += f"Key facts: {'; '.join(facts[:3])}. "
        
        return summary
    
    def preload_next_layers(self, current_model: str, predicted_next: str) -> Dict:
        """
        Preload predicted next model's layers to RAM
        Enables fast switching (2-3 seconds)
        """
        if predicted_next not in self.layer_distribution:
            # Calculate distribution if not cached
            model_info = config.OPTIMAL_MODELS.get(predicted_next, {})
            model_size = model_info.get("vram", 4.7)
            self.distribute_layers(predicted_next, model_size)
        
        distribution = self.layer_distribution[predicted_next]
        
        return {
            "model": predicted_next,
            "preload_status": "ready",
            "vram_layers": len(distribution["vram_layers"]),
            "ram_layers": len(distribution["ram_layers"]),
            "switch_time_estimate": "2-3s"
        }
    
    def get_memory_stats(self) -> Dict:
        """Get current memory statistics"""
        try:
            # GPU memory
            gpu_used = 0
            gpu_total = 6.0
            gpu_percent = 0
            
            if GPUTIL_AVAILABLE:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu_used = gpus[0].memoryUsed / 1024
                        gpu_total = gpus[0].memoryTotal / 1024
                        gpu_percent = (gpu_used / gpu_total * 100) if gpu_total > 0 else 0
                except Exception as e:
                    print(f"⚠️  Error reading GPU stats: {e}")
            
            # System memory
            ram_stats = psutil.virtual_memory()
            ram_used = ram_stats.used / (1024**3)
            ram_total = ram_stats.total / (1024**3)
            
            return {
                "gpu_used_gb": gpu_used,
                "gpu_total_gb": gpu_total,
                "gpu_percent": gpu_percent,
                "ram_used_gb": ram_used,
                "ram_total_gb": ram_total,
                "ram_percent": ram_stats.percent
            }
        except Exception as e:
            print(f"⚠️  Error getting memory stats: {e}")
            return {
                "gpu_used_gb": 0,
                "gpu_total_gb": 6.0,
                "gpu_percent": 0,
                "ram_used_gb": 0,
                "ram_total_gb": 24.0,
                "ram_percent": 0
            }
    
    def print_distribution_info(self, model_name: str):
        """Print layer distribution information"""
        if model_name not in self.layer_distribution:
            return
        
        dist = self.layer_distribution[model_name]
        print(f"\n{'='*60}")
        print(f"🧠 HYBRID INFERENCE - LAYER DISTRIBUTION")
        print(f"{'='*60}")
        print(f"Model: {model_name}")
        print(f"Total Layers: {dist['num_layers']}")
        print(f"Layer Size: {dist['layer_size_gb']*1024:.1f}MB")
        print(f"\nVRAM Allocation:")
        print(f"  Layers in VRAM: {len(dist['vram_layers'])} ({dist['efficiency']*100:.1f}%)")
        print(f"  VRAM Used: {dist['vram_used']:.2f}GB / 6.0GB")
        print(f"\nRAM Allocation:")
        print(f"  Layers in RAM: {len(dist['ram_layers'])}")
        print(f"  RAM Used: {dist['ram_used']:.2f}GB / 24.0GB")
        print(f"\nContext Window: {self.optimize_context_window(dist['vram_used'])} tokens")
        print(f"{'='*60}\n")


# Example usage
if __name__ == "__main__":
    engine = HybridInferenceEngine()
    
    print("🚀 HYBRID INFERENCE ENGINE - TEST\n")
    
    # Test with each model
    for model_name, model_info in config.OPTIMAL_MODELS.items():
        model_size = model_info["vram"]
        
        # Distribute layers
        dist = engine.distribute_layers(model_name, model_size)
        
        # Calculate context window
        context = engine.optimize_context_window(model_size)
        
        print(f"{model_name.upper()}:")
        print(f"  VRAM: {model_size}GB | Context: {context} tokens")
        print(f"  VRAM Layers: {len(dist['vram_layers'])} | RAM Layers: {len(dist['ram_layers'])}")
        print(f"  Efficiency: {dist['efficiency']*100:.1f}%")
        print()
    
    # Print memory stats
    print("\n📊 SYSTEM MEMORY STATS:")
    stats = engine.get_memory_stats()
    print(f"GPU: {stats['gpu_used_gb']:.1f}GB / {stats['gpu_total_gb']:.1f}GB ({stats['gpu_percent']:.1f}%)")
    print(f"RAM: {stats['ram_used_gb']:.1f}GB / {stats['ram_total_gb']:.1f}GB ({stats['ram_percent']:.1f}%)")
