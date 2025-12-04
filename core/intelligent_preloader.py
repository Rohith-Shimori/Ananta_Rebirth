"""
Intelligent Preloader - Claude's Optimization Plan
Predictive model preloading for fast switching
- Learn user patterns
- Preload likely next model
- Minimize switching time (2-3s goal)
- Background preloading
"""

import asyncio
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
import time
import config


@dataclass
class PreloadTask:
    """Represents a model preload task"""
    model: str
    priority: int
    scheduled_time: float
    status: str = "pending"  # pending, loading, completed, failed


class IntelligentPreloader:
    """
    Predictive model preloading system
    Learns patterns and preloads models before they're needed
    """
    
    def __init__(self, usage_tracker=None):
        """
        Initialize intelligent preloader
        
        Args:
            usage_tracker: Optional UsagePatternTracker instance
        """
        self.usage_tracker = usage_tracker
        self.preload_queue: List[PreloadTask] = []
        self.loaded_models: Set[str] = set()
        self.preload_history: List[Dict] = []
        self.stats = {
            "total_preloads": 0,
            "successful_preloads": 0,
            "failed_preloads": 0,
            "avg_preload_time": 0.0,
            "time_saved_by_preloading": 0.0,
            "preload_accuracy": 0.0
        }
        
        # Preloading configuration
        self.max_preload_queue = 3
        self.preload_timeout = 30  # seconds
        self.min_preload_interval = 5  # seconds between preloads
        self.last_preload_time = 0
    
    def predict_next_models(self, k: int = 3) -> List[Tuple[str, float]]:
        """
        Predict next k models to be used
        Returns list of (model, confidence) tuples
        """
        if not self.usage_tracker:
            # Default prediction if no tracker
            return [
                ("sentinel", 0.8),
                ("architect", 0.6),
                ("flash", 0.5)
            ]
        
        # Get prediction from tracker
        next_model = self.usage_tracker.predict_next_model()
        
        if not next_model:
            return [
                ("sentinel", 0.8),
                ("architect", 0.6),
                ("flash", 0.5)
            ]
        
        # Build confidence scores based on patterns
        predictions = []
        
        # Primary prediction (high confidence)
        predictions.append((next_model, 0.9))
        
        # Secondary predictions (medium confidence)
        # Get models that frequently follow the current model
        for (from_model, to_model), transition in self.usage_tracker.transitions.items():
            if from_model == next_model and to_model not in [p[0] for p in predictions]:
                confidence = min(0.7, transition.frequency / 10.0)
                predictions.append((to_model, confidence))
        
        # Tertiary predictions (low confidence)
        # Add other models that are commonly used
        for model_name in config.OPTIMAL_MODELS.keys():
            if model_name not in [p[0] for p in predictions]:
                predictions.append((model_name, 0.3))
        
        # Sort by confidence and return top k
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:k]
    
    def schedule_preload(self, model: str, priority: int = 5, 
                        delay: float = 0.0) -> Optional[PreloadTask]:
        """
        Schedule a model for preloading
        
        Args:
            model: Model name to preload
            priority: Priority (1-10, higher = more important)
            delay: Delay before preloading (seconds)
        
        Returns:
            PreloadTask if scheduled, None if queue full
        """
        # Check if already loaded
        if model in self.loaded_models:
            return None
        
        # Check queue size
        if len(self.preload_queue) >= self.max_preload_queue:
            # Remove lowest priority task
            self.preload_queue.sort(key=lambda x: x.priority)
            if self.preload_queue[0].priority < priority:
                self.preload_queue.pop(0)
            else:
                return None
        
        # Create task
        task = PreloadTask(
            model=model,
            priority=priority,
            scheduled_time=time.time() + delay
        )
        
        self.preload_queue.append(task)
        self.preload_queue.sort(key=lambda x: x.priority, reverse=True)
        
        return task
    
    async def preload_model(self, model: str) -> bool:
        """
        Preload a model (simulated)
        In real implementation, would load model into VRAM
        
        Args:
            model: Model name to preload
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check rate limiting
            current_time = time.time()
            if current_time - self.last_preload_time < self.min_preload_interval:
                await asyncio.sleep(self.min_preload_interval)
            
            self.last_preload_time = time.time()
            
            # Simulate preloading
            preload_start = time.time()
            
            # In real implementation:
            # - Load model weights into VRAM
            # - Prepare model for inference
            # - Verify model is ready
            await asyncio.sleep(0.5)  # Simulate loading time
            
            preload_time = time.time() - preload_start
            
            # Update stats
            self.stats["total_preloads"] += 1
            self.stats["successful_preloads"] += 1
            
            old_avg = self.stats["avg_preload_time"]
            n = self.stats["total_preloads"]
            self.stats["avg_preload_time"] = (
                (old_avg * (n - 1) + preload_time) / n
            )
            
            self.loaded_models.add(model)
            
            # Record in history
            self.preload_history.append({
                "model": model,
                "preload_time": preload_time,
                "status": "success",
                "timestamp": time.time()
            })
            
            return True
        
        except Exception as e:
            print(f"⚠️  Error preloading model {model}: {e}")
            self.stats["failed_preloads"] += 1
            
            self.preload_history.append({
                "model": model,
                "status": "failed",
                "error": str(e),
                "timestamp": time.time()
            })
            
            return False
    
    async def process_preload_queue(self):
        """Process preload queue asynchronously"""
        while True:
            try:
                # Find tasks ready to preload
                current_time = time.time()
                ready_tasks = [
                    t for t in self.preload_queue
                    if t.scheduled_time <= current_time and t.status == "pending"
                ]
                
                # Process ready tasks
                for task in ready_tasks:
                    task.status = "loading"
                    success = await self.preload_model(task.model)
                    task.status = "completed" if success else "failed"
                
                # Remove completed tasks
                self.preload_queue = [
                    t for t in self.preload_queue
                    if t.status == "pending" or t.status == "loading"
                ]
                
                # Wait before next check
                await asyncio.sleep(1)
            
            except Exception as e:
                print(f"⚠️  Error in preload queue processing: {e}")
                await asyncio.sleep(1)
    
    async def predictive_preload(self):
        """
        Continuously predict and preload likely next models
        Should run in background
        """
        while True:
            try:
                # Get next likely models
                predictions = self.predict_next_models(k=3)
                
                # Schedule preloads
                for i, (model, confidence) in enumerate(predictions):
                    if model not in self.loaded_models:
                        # Higher confidence = higher priority and earlier scheduling
                        priority = int(confidence * 10)
                        delay = i * 2  # Stagger preloads
                        
                        self.schedule_preload(model, priority=priority, delay=delay)
                
                # Wait before next prediction
                await asyncio.sleep(10)
            
            except Exception as e:
                print(f"⚠️  Error in predictive preload: {e}")
                await asyncio.sleep(10)
    
    def get_preload_stats(self) -> Dict:
        """Get preloading statistics"""
        total = self.stats["total_preloads"]
        successful = self.stats["successful_preloads"]
        
        accuracy = (successful / total * 100) if total > 0 else 0
        
        return {
            "total_preloads": total,
            "successful_preloads": successful,
            "failed_preloads": self.stats["failed_preloads"],
            "success_rate": accuracy,
            "avg_preload_time": self.stats["avg_preload_time"],
            "loaded_models": len(self.loaded_models),
            "queue_size": len(self.preload_queue),
            "time_saved": self.stats["time_saved_by_preloading"]
        }
    
    def unload_model(self, model: str):
        """Unload a model from memory"""
        if model in self.loaded_models:
            self.loaded_models.remove(model)
    
    def clear_loaded_models(self):
        """Clear all loaded models"""
        self.loaded_models.clear()
    
    def print_preload_stats(self):
        """Print preloading statistics"""
        stats = self.get_preload_stats()
        
        print(f"\n{'='*70}")
        print(f"📦 INTELLIGENT PRELOADER - STATISTICS")
        print(f"{'='*70}")
        print(f"Total Preloads: {stats['total_preloads']}")
        print(f"Successful: {stats['successful_preloads']}")
        print(f"Failed: {stats['failed_preloads']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Avg Preload Time: {stats['avg_preload_time']:.2f}s")
        print(f"Loaded Models: {stats['loaded_models']}")
        print(f"Queue Size: {stats['queue_size']}")
        print(f"Time Saved: {stats['time_saved']:.1f}s")
        print(f"{'='*70}\n")


# Example usage
if __name__ == "__main__":
    async def main():
        preloader = IntelligentPreloader()
        
        print("🚀 INTELLIGENT PRELOADER - TEST\n")
        
        # Predict next models
        predictions = preloader.predict_next_models(k=3)
        print("📊 Next Model Predictions:")
        for model, confidence in predictions:
            print(f"  {model}: {confidence:.1%}")
        
        # Schedule preloads
        print("\n📦 Scheduling Preloads:")
        for model, confidence in predictions:
            task = preloader.schedule_preload(model, priority=int(confidence * 10))
            if task:
                print(f"  Scheduled {model} with priority {task.priority}")
        
        # Process queue
        print("\n⏳ Processing Preload Queue:")
        for task in preloader.preload_queue:
            success = await preloader.preload_model(task.model)
            print(f"  {task.model}: {'✅ Success' if success else '❌ Failed'}")
        
        # Print stats
        preloader.print_preload_stats()
    
    asyncio.run(main())
