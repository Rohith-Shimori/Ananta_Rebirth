"""
Context Window Manager - Claude's Optimization Plan
Optimizes context windows per model for maximum efficiency
- Calculate optimal context per model
- Smart context compression
- Preserve important facts
- Dynamic window sizing
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import config


@dataclass
class ContextWindow:
    """Represents a context window configuration"""
    model: str
    max_tokens: int
    reserved_for_response: int
    available_for_context: int
    compression_ratio: float = 1.0


class ContextWindowManager:
    """
    Manages optimal context windows for each model
    Based on VRAM usage and model capabilities
    """
    
    def __init__(self):
        """Initialize context window manager"""
        self.windows = self._initialize_windows()
        self.compression_stats = {
            "total_compressions": 0,
            "avg_compression_ratio": 1.0,
            "facts_preserved": 0,
            "tokens_saved": 0
        }
    
    def _initialize_windows(self) -> Dict[str, ContextWindow]:
        """Initialize optimal context windows per model"""
        windows = {}
        
        # Get model configs from config.py
        models = config.OPTIMAL_MODELS
        
        for model_name, model_info in models.items():
            vram = model_info.get("vram", 4.0)
            
            # Calculate optimal context based on VRAM
            # Formula: More VRAM = larger context window
            if vram >= 4.5:
                max_tokens = 8192  # 8K for large models
                reserved = 2048    # Reserve 2K for response
            elif vram >= 4.0:
                max_tokens = 6144  # 6K for medium models
                reserved = 1536    # Reserve 1.5K for response
            elif vram >= 3.5:
                max_tokens = 4096  # 4K for smaller models
                reserved = 1024    # Reserve 1K for response
            else:
                max_tokens = 2048  # 2K for tiny models
                reserved = 512     # Reserve 512 for response
            
            available = max_tokens - reserved
            
            windows[model_name] = ContextWindow(
                model=model_name,
                max_tokens=max_tokens,
                reserved_for_response=reserved,
                available_for_context=available,
                compression_ratio=1.0
            )
        
        return windows
    
    def get_optimal_context_size(self, model: str) -> int:
        """Get optimal context size for a model"""
        if model not in self.windows:
            return config.CONTEXT_WINDOW
        
        return self.windows[model].available_for_context
    
    def compress_context(self, context: str, model: str, target_ratio: float = 0.7) -> Tuple[str, float]:
        """
        Compress context while preserving important facts
        
        Args:
            context: Full context text
            model: Model name
            target_ratio: Target compression ratio (0.7 = 30% reduction)
        
        Returns:
            Tuple of (compressed_context, actual_ratio)
        """
        if not context:
            return "", 1.0
        
        original_tokens = len(context.split())
        
        # Extract important sentences (those with key markers)
        important_markers = ["important", "key", "critical", "must", "note", "remember"]
        lines = context.split('\n')
        
        important_lines = []
        other_lines = []
        
        for line in lines:
            if any(marker in line.lower() for marker in important_markers):
                important_lines.append(line)
            else:
                other_lines.append(line)
        
        # Keep all important lines, sample others
        target_tokens = int(original_tokens * target_ratio)
        important_tokens = len(' '.join(important_lines).split())
        
        remaining_tokens = target_tokens - important_tokens
        if remaining_tokens > 0 and other_lines:
            # Sample other lines proportionally
            sample_size = max(1, int(len(other_lines) * (remaining_tokens / len(' '.join(other_lines).split()))))
            sampled_lines = other_lines[:sample_size]
        else:
            sampled_lines = []
        
        # Combine
        compressed = '\n'.join(important_lines + sampled_lines)
        
        # Calculate actual ratio
        compressed_tokens = len(compressed.split())
        actual_ratio = compressed_tokens / original_tokens if original_tokens > 0 else 1.0
        
        # Update stats
        self.compression_stats["total_compressions"] += 1
        self.compression_stats["tokens_saved"] += original_tokens - compressed_tokens
        self.compression_stats["facts_preserved"] += len(important_lines)
        
        # Update average ratio
        old_avg = self.compression_stats["avg_compression_ratio"]
        n = self.compression_stats["total_compressions"]
        self.compression_stats["avg_compression_ratio"] = (
            (old_avg * (n - 1) + actual_ratio) / n
        )
        
        return compressed, actual_ratio
    
    def should_compress_context(self, context_tokens: int, model: str) -> bool:
        """Determine if context should be compressed"""
        if model not in self.windows:
            return False
        
        available = self.windows[model].available_for_context
        return context_tokens > available * 0.8  # Compress if >80% full
    
    def fit_context_to_model(self, context: str, model: str) -> str:
        """
        Fit context to model's optimal window
        Automatically compresses if needed
        """
        context_tokens = len(context.split())
        available = self.get_optimal_context_size(model)
        
        if context_tokens <= available:
            return context
        
        # Need to compress
        target_ratio = available / context_tokens
        compressed, _ = self.compress_context(context, model, target_ratio)
        
        return compressed
    
    def get_window_info(self, model: str) -> Dict:
        """Get detailed window information"""
        if model not in self.windows:
            return {}
        
        window = self.windows[model]
        return {
            "model": model,
            "max_tokens": window.max_tokens,
            "reserved_for_response": window.reserved_for_response,
            "available_for_context": window.available_for_context,
            "compression_ratio": window.compression_ratio,
            "utilization_percent": 0  # Will be updated dynamically
        }
    
    def get_all_windows(self) -> Dict[str, Dict]:
        """Get all window configurations"""
        return {
            model: self.get_window_info(model)
            for model in self.windows.keys()
        }
    
    def get_compression_stats(self) -> Dict:
        """Get compression statistics"""
        return {
            "total_compressions": self.compression_stats["total_compressions"],
            "avg_compression_ratio": self.compression_stats["avg_compression_ratio"],
            "facts_preserved": self.compression_stats["facts_preserved"],
            "tokens_saved": self.compression_stats["tokens_saved"],
            "avg_tokens_saved_per_compression": (
                self.compression_stats["tokens_saved"] / 
                max(self.compression_stats["total_compressions"], 1)
            )
        }
    
    def print_window_info(self):
        """Print context window information"""
        print(f"\n{'='*70}")
        print(f"📊 CONTEXT WINDOW MANAGER - CONFIGURATION")
        print(f"{'='*70}")
        
        for model_name, window in self.windows.items():
            print(f"\n{model_name.upper()}:")
            print(f"  Max Tokens: {window.max_tokens}")
            print(f"  Available for Context: {window.available_for_context}")
            print(f"  Reserved for Response: {window.reserved_for_response}")
        
        print(f"\n{'='*70}\n")
    
    def print_compression_stats(self):
        """Print compression statistics"""
        stats = self.get_compression_stats()
        
        print(f"\n{'='*70}")
        print(f"📈 CONTEXT COMPRESSION - STATISTICS")
        print(f"{'='*70}")
        print(f"Total Compressions: {stats['total_compressions']}")
        print(f"Avg Compression Ratio: {stats['avg_compression_ratio']:.2f}")
        print(f"Facts Preserved: {stats['facts_preserved']}")
        print(f"Total Tokens Saved: {stats['tokens_saved']}")
        print(f"Avg Tokens Saved/Compression: {stats['avg_tokens_saved_per_compression']:.1f}")
        print(f"{'='*70}\n")


# Example usage
if __name__ == "__main__":
    manager = ContextWindowManager()
    
    # Print window info
    manager.print_window_info()
    
    # Test compression
    test_context = """
    Important: The system must handle 6GB VRAM efficiently.
    Key: Use quantized models for better performance.
    Note: Context windows should be optimized per model.
    
    The architecture includes multiple components.
    Each component has specific responsibilities.
    The system is designed for RTX 4050 hardware.
    
    Critical: Always preserve important facts during compression.
    Remember: Compression ratio should be tracked.
    """
    
    print("Original context length:", len(test_context.split()))
    compressed, ratio = manager.compress_context(test_context, "sentinel")
    print(f"Compressed context length: {len(compressed.split())}")
    print(f"Compression ratio: {ratio:.2f}")
    
    # Print stats
    manager.print_compression_stats()
