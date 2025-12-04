"""
Smart Model Router - Phase 1 of Claude's Optimization Plan
Intelligently routes queries to optimal model based on:
- Query complexity
- Current VRAM usage
- Response time requirements
- Task type
"""

import re
import psutil
from typing import Dict, Tuple, Optional
import config

# Safe import for GPUtil
try:
    import GPUtil
    GPUTIL_AVAILABLE = True
except ImportError:
    GPUTIL_AVAILABLE = False
    print("⚠️  GPUtil not available. Install: pip install gputil")


class QueryComplexityAnalyzer:
    """Analyzes query complexity to determine optimal model"""
    
    def __init__(self):
        self.complexity_keywords = {
            "high": ["prove", "derive", "theorem", "algorithm", "architecture", "design pattern"],
            "medium": ["explain", "analyze", "compare", "implement", "debug"],
            "low": ["what", "how", "when", "where", "who", "list", "define"]
        }
    
    def analyze(self, query: str) -> float:
        """
        Analyze query complexity (0-10 scale)
        0-3: Simple (use FLASH)
        3-7: Medium (use SENTINEL)
        7-10: Complex (use ORACLE)
        """
        query_lower = query.lower()
        
        # Length-based scoring
        words = query_lower.split()
        length_score = min(len(words) / 20.0, 3.0)  # Max 3.0 from length
        
        # Keyword-based scoring
        keyword_score = 0.0
        for keyword in self.complexity_keywords["high"]:
            if keyword in query_lower:
                keyword_score += 3.0
        
        for keyword in self.complexity_keywords["medium"]:
            if keyword in query_lower:
                keyword_score += 1.5
        
        for keyword in self.complexity_keywords["low"]:
            if keyword in query_lower:
                keyword_score += 0.5
        
        # Code detection
        code_score = 0.0
        if any(pattern in query_lower for pattern in ["def ", "class ", "import ", "function", "code"]):
            code_score += 2.0
        if "```" in query:
            code_score += 1.0
        
        # Math/reasoning detection
        math_score = 0.0
        if any(c in query for c in "∑∫√∞±×÷"):
            math_score += 3.0
        if any(word in query_lower for word in ["equation", "solve", "calculate", "derive"]):
            math_score += 2.0
        
        # Total complexity
        total = length_score + keyword_score + code_score + math_score
        return min(total, 10.0)


class VRAMMonitor:
    """Monitors GPU VRAM usage"""
    
    def __init__(self):
        self.max_vram = 6.0  # RTX 4050 has 6GB
    
    def get_available_vram(self) -> float:
        """Get available VRAM in GB"""
        if not GPUTIL_AVAILABLE:
            return self.max_vram
        
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                available = gpu.memoryTotal - gpu.memoryUsed
                return available / 1024.0  # Convert MB to GB
        except Exception as e:
            print(f"⚠️  Error reading VRAM: {e}")
        
        return self.max_vram  # Assume full if can't detect
    
    def get_used_vram(self) -> float:
        """Get used VRAM in GB"""
        if not GPUTIL_AVAILABLE:
            return 0.0
        
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                return gpu.memoryUsed / 1024.0  # Convert MB to GB
        except Exception as e:
            print(f"⚠️  Error reading VRAM: {e}")
        
        return 0.0
    
    def get_vram_percentage(self) -> float:
        """Get VRAM usage percentage"""
        if not GPUTIL_AVAILABLE:
            return 0.0
        
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                return gpu.load * 100  # Already in 0-1 range
        except Exception as e:
            print(f"⚠️  Error reading VRAM: {e}")
        
        return 0.0


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
        self.model_config = config.OPTIMAL_MODELS
        self.routing_stats = {
            "total_queries": 0,
            "model_usage": {model: 0 for model in self.model_config.keys()}
        }
    
    def detect_task_type(self, query: str) -> str:
        """
        Detect task type from query
        Returns: "code", "reasoning", "vision", "general"
        """
        query_lower = query.lower()
        
        # Code detection
        code_keywords = ["code", "function", "debug", "implement", "refactor", 
                        "syntax", "error", "bug", "def ", "class ", "import ",
                        "variable", "loop", "condition", "algorithm"]
        if any(kw in query_lower for kw in code_keywords):
            return "code"
        
        # Reasoning detection
        reasoning_keywords = ["analyze", "reason", "prove", "solve", "explain",
                             "why", "how", "logic", "math", "equation", "derive",
                             "theorem", "calculate", "compute"]
        if any(kw in query_lower for kw in reasoning_keywords):
            return "reasoning"
        
        # Vision detection
        vision_keywords = ["image", "picture", "screenshot", "photo", "visual",
                          "see", "look", "view", "display", "show", "diagram"]
        if any(kw in query_lower for kw in vision_keywords):
            return "vision"
        
        return "general"
    
    def route_query(self, query: str, context: Optional[Dict] = None) -> str:
        """
        Route query to optimal model
        Returns: model name (sentinel, architect, oracle, flash, vision, nano)
        """
        if context is None:
            context = {}
        
        # Analyze query
        task_type = self.detect_task_type(query)
        complexity = self.query_analyzer.analyze(query)
        urgency = context.get("urgency", "normal")
        
        # Check available VRAM
        available_vram = self.vram_monitor.get_available_vram()
        
        # Smart routing logic
        if task_type == "code":
            # Code tasks → ARCHITECT (deepseek-coder)
            model = "architect"
        
        elif task_type == "reasoning" and complexity > 7:
            # Complex reasoning → ORACLE (deepseek-r1)
            model = "oracle"
        
        elif task_type == "vision":
            # Vision tasks → VISION (llava-phi3)
            model = "vision"
        
        elif urgency == "high" or complexity < 3:
            # Urgent or simple → FLASH (phi-3-mini)
            model = "flash"
        
        elif available_vram < 5.0:
            # Low VRAM → NANO (gemma:2b)
            model = "nano"
        
        else:
            # Default → SENTINEL (qwen2.5)
            model = "sentinel"
        
        # Update stats
        self.current_model = model
        self.routing_stats["total_queries"] += 1
        self.routing_stats["model_usage"][model] += 1
        
        return model
    
    def get_model_info(self, model_name: str) -> Dict:
        """Get information about a model"""
        if model_name in self.model_config:
            return self.model_config[model_name]
        return self.model_config["sentinel"]  # Default
    
    def get_model_path(self, model_name: str) -> str:
        """Get Ollama model path"""
        model_info = self.get_model_info(model_name)
        return model_info["model"]
    
    def get_routing_stats(self) -> Dict:
        """Get routing statistics"""
        stats = self.routing_stats.copy()
        stats["current_model"] = self.current_model
        stats["available_vram"] = self.vram_monitor.get_available_vram()
        stats["used_vram"] = self.vram_monitor.get_used_vram()
        stats["vram_percentage"] = self.vram_monitor.get_vram_percentage()
        return stats
    
    def print_routing_info(self, query: str, model: str):
        """Print routing information for debugging"""
        model_info = self.get_model_info(model)
        print(f"\n{'='*60}")
        print(f"🎯 SMART ROUTING DECISION")
        print(f"{'='*60}")
        print(f"Query: {query[:80]}...")
        print(f"Task Type: {self.detect_task_type(query)}")
        print(f"Complexity: {self.query_analyzer.analyze(query):.1f}/10")
        print(f"Selected Model: {model.upper()} ({model_info['description']})")
        print(f"Model: {model_info['model']}")
        print(f"VRAM: {model_info['vram']}GB | Speed: {model_info['speed']} tok/s")
        print(f"Available VRAM: {self.vram_monitor.get_available_vram():.1f}GB")
        print(f"{'='*60}\n")


# Example usage
if __name__ == "__main__":
    router = SmartModelRouter()
    
    # Test queries
    test_queries = [
        ("Write a Python function to sort an array", "code"),
        ("Explain quantum entanglement", "reasoning"),
        ("Analyze this image", "vision"),
        ("What is the weather?", "general"),
        ("Debug this code: def foo(): return bar", "code"),
        ("Prove that P=NP", "reasoning"),
    ]
    
    print("🚀 SMART MODEL ROUTER - TEST RESULTS\n")
    
    for query, expected_type in test_queries:
        model = router.route_query(query)
        detected_type = router.detect_task_type(query)
        complexity = router.query_analyzer.analyze(query)
        
        print(f"Query: {query[:50]}...")
        print(f"  Expected: {expected_type} | Detected: {detected_type}")
        print(f"  Complexity: {complexity:.1f}/10 | Model: {model}")
        print()
    
    print("\n📊 ROUTING STATISTICS:")
    stats = router.get_routing_stats()
    print(f"Total Queries: {stats['total_queries']}")
    print(f"Model Usage: {stats['model_usage']}")
    print(f"Available VRAM: {stats['available_vram']:.1f}GB")
    print(f"VRAM Usage: {stats['vram_percentage']:.1f}%")
