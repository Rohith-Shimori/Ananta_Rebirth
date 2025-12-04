"""
Usage Pattern Tracker - Claude's Optimization Plan
Learns user patterns for predictive optimization
- Track which models are used when
- Learn time-of-day patterns
- Predict next model needed
- Enable smart preloading
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
from pathlib import Path
import config


@dataclass
class UsagePattern:
    """Represents a usage pattern"""
    model: str
    hour_of_day: int
    day_of_week: int
    frequency: int = 0
    avg_response_time: float = 0.0
    success_rate: float = 1.0
    last_used: Optional[datetime] = None


@dataclass
class ModelTransition:
    """Represents a transition between models"""
    from_model: str
    to_model: str
    frequency: int = 0
    avg_switch_time: float = 0.0
    context: str = ""  # What triggered the switch


class UsagePatternTracker:
    """
    Tracks usage patterns for predictive optimization
    Learns when and why models are used
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize usage pattern tracker"""
        self.db_path = Path(db_path or str(config.DATA_DIR / "usage_patterns.json"))
        self.patterns: Dict[str, UsagePattern] = {}
        self.transitions: Dict[Tuple[str, str], ModelTransition] = {}
        self.query_history: List[Dict] = []
        self.stats = {
            "total_queries": 0,
            "total_model_switches": 0,
            "avg_response_time": 0.0,
            "most_used_model": None,
            "peak_usage_hour": None
        }
        
        # Load existing patterns
        self._load_patterns()
    
    def _load_patterns(self):
        """Load patterns from disk"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    # Reconstruct patterns
                    for key, pattern_data in data.get("patterns", {}).items():
                        pattern = UsagePattern(
                            model=pattern_data["model"],
                            hour_of_day=pattern_data["hour_of_day"],
                            day_of_week=pattern_data["day_of_week"],
                            frequency=pattern_data["frequency"],
                            avg_response_time=pattern_data["avg_response_time"],
                            success_rate=pattern_data["success_rate"]
                        )
                        self.patterns[key] = pattern
                    
                    # Reconstruct transitions
                    for key, trans_data in data.get("transitions", {}).items():
                        from_model, to_model = key.split("->")
                        transition = ModelTransition(
                            from_model=from_model,
                            to_model=to_model,
                            frequency=trans_data["frequency"],
                            avg_switch_time=trans_data["avg_switch_time"],
                            context=trans_data.get("context", "")
                        )
                        self.transitions[(from_model, to_model)] = transition
                    
                    self.stats = data.get("stats", self.stats)
            except Exception as e:
                print(f"⚠️  Error loading patterns: {e}")
    
    def _save_patterns(self):
        """Save patterns to disk"""
        try:
            data = {
                "patterns": {
                    f"{p.model}_{p.hour_of_day}_{p.day_of_week}": {
                        "model": p.model,
                        "hour_of_day": p.hour_of_day,
                        "day_of_week": p.day_of_week,
                        "frequency": p.frequency,
                        "avg_response_time": p.avg_response_time,
                        "success_rate": p.success_rate
                    }
                    for p in self.patterns.values()
                },
                "transitions": {
                    f"{t.from_model}->{t.to_model}": {
                        "frequency": t.frequency,
                        "avg_switch_time": t.avg_switch_time,
                        "context": t.context
                    }
                    for t in self.transitions.values()
                },
                "stats": self.stats
            }
            
            with open(self.db_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving patterns: {e}")
    
    def track_query(self, model: str, response_time: float, success: bool = True, 
                   query_type: str = "general"):
        """Track a query execution"""
        now = datetime.now()
        hour = now.hour
        day = now.weekday()
        
        # Create pattern key
        pattern_key = f"{model}_{hour}_{day}"
        
        if pattern_key not in self.patterns:
            self.patterns[pattern_key] = UsagePattern(
                model=model,
                hour_of_day=hour,
                day_of_week=day
            )
        
        pattern = self.patterns[pattern_key]
        
        # Update pattern
        pattern.frequency += 1
        pattern.last_used = now
        
        # Update response time (exponential moving average)
        alpha = 0.3
        pattern.avg_response_time = (
            alpha * response_time + 
            (1 - alpha) * pattern.avg_response_time
        )
        
        # Update success rate
        if success:
            pattern.success_rate = (
                (pattern.success_rate * (pattern.frequency - 1) + 1) / 
                pattern.frequency
            )
        else:
            pattern.success_rate = (
                (pattern.success_rate * (pattern.frequency - 1)) / 
                pattern.frequency
            )
        
        # Update global stats
        self.stats["total_queries"] += 1
        old_avg = self.stats["avg_response_time"]
        n = self.stats["total_queries"]
        self.stats["avg_response_time"] = (
            (old_avg * (n - 1) + response_time) / n
        )
        
        # Track most used model
        model_counts = {}
        for p in self.patterns.values():
            model_counts[p.model] = model_counts.get(p.model, 0) + p.frequency
        self.stats["most_used_model"] = max(model_counts, key=model_counts.get)
        
        # Track peak usage hour
        hour_counts = {}
        for p in self.patterns.values():
            hour_counts[p.hour_of_day] = hour_counts.get(p.hour_of_day, 0) + p.frequency
        self.stats["peak_usage_hour"] = max(hour_counts, key=hour_counts.get)
        
        # Add to history
        self.query_history.append({
            "model": model,
            "response_time": response_time,
            "success": success,
            "query_type": query_type,
            "timestamp": now.isoformat()
        })
        
        # Keep only last 1000 queries
        if len(self.query_history) > 1000:
            self.query_history = self.query_history[-1000:]
    
    def track_model_switch(self, from_model: str, to_model: str, 
                          switch_time: float, context: str = ""):
        """Track a model switch"""
        key = (from_model, to_model)
        
        if key not in self.transitions:
            self.transitions[key] = ModelTransition(
                from_model=from_model,
                to_model=to_model,
                context=context
            )
        
        transition = self.transitions[key]
        transition.frequency += 1
        
        # Update switch time (exponential moving average)
        alpha = 0.3
        transition.avg_switch_time = (
            alpha * switch_time + 
            (1 - alpha) * transition.avg_switch_time
        )
        
        self.stats["total_model_switches"] += 1
    
    def predict_next_model(self) -> Optional[str]:
        """Predict the next model that will be used"""
        now = datetime.now()
        hour = now.hour
        day = now.weekday()
        
        # Find patterns for current time
        current_patterns = [
            p for p in self.patterns.values()
            if p.hour_of_day == hour and p.day_of_week == day
        ]
        
        if not current_patterns:
            # Fall back to current hour regardless of day
            current_patterns = [
                p for p in self.patterns.values()
                if p.hour_of_day == hour
            ]
        
        if not current_patterns:
            return None
        
        # Return most frequent model for this time
        return max(current_patterns, key=lambda p: p.frequency).model
    
    def get_pattern_for_time(self, hour: int, day: int) -> Optional[UsagePattern]:
        """Get usage pattern for specific time"""
        pattern_key = f"*_{hour}_{day}"
        
        for key, pattern in self.patterns.items():
            if pattern.hour_of_day == hour and pattern.day_of_week == day:
                return pattern
        
        return None
    
    def get_model_statistics(self, model: str) -> Dict:
        """Get statistics for a specific model"""
        model_patterns = [p for p in self.patterns.values() if p.model == model]
        
        if not model_patterns:
            return {}
        
        total_uses = sum(p.frequency for p in model_patterns)
        avg_response_time = sum(p.avg_response_time * p.frequency for p in model_patterns) / total_uses
        avg_success_rate = sum(p.success_rate * p.frequency for p in model_patterns) / total_uses
        
        # Find most common time
        most_common = max(model_patterns, key=lambda p: p.frequency)
        
        return {
            "model": model,
            "total_uses": total_uses,
            "avg_response_time": avg_response_time,
            "avg_success_rate": avg_success_rate,
            "most_common_hour": most_common.hour_of_day,
            "most_common_day": most_common.day_of_week,
            "patterns_count": len(model_patterns)
        }
    
    def get_all_statistics(self) -> Dict:
        """Get all statistics"""
        return {
            "total_queries": self.stats["total_queries"],
            "total_model_switches": self.stats["total_model_switches"],
            "avg_response_time": self.stats["avg_response_time"],
            "most_used_model": self.stats["most_used_model"],
            "peak_usage_hour": self.stats["peak_usage_hour"],
            "unique_patterns": len(self.patterns),
            "unique_transitions": len(self.transitions)
        }
    
    def print_statistics(self):
        """Print usage statistics"""
        stats = self.get_all_statistics()
        
        print(f"\n{'='*70}")
        print(f"📊 USAGE PATTERN TRACKER - STATISTICS")
        print(f"{'='*70}")
        print(f"Total Queries: {stats['total_queries']}")
        print(f"Total Model Switches: {stats['total_model_switches']}")
        print(f"Avg Response Time: {stats['avg_response_time']:.2f}s")
        print(f"Most Used Model: {stats['most_used_model']}")
        print(f"Peak Usage Hour: {stats['peak_usage_hour']}:00")
        print(f"Unique Patterns: {stats['unique_patterns']}")
        print(f"Unique Transitions: {stats['unique_transitions']}")
        print(f"{'='*70}\n")
    
    def print_model_statistics(self, model: str):
        """Print statistics for a specific model"""
        stats = self.get_model_statistics(model)
        
        if not stats:
            print(f"No statistics for model: {model}")
            return
        
        print(f"\n{'='*70}")
        print(f"📊 MODEL STATISTICS - {model.upper()}")
        print(f"{'='*70}")
        print(f"Total Uses: {stats['total_uses']}")
        print(f"Avg Response Time: {stats['avg_response_time']:.2f}s")
        print(f"Avg Success Rate: {stats['avg_success_rate']:.1%}")
        print(f"Most Common Hour: {stats['most_common_hour']}:00")
        print(f"Most Common Day: {stats['most_common_day']}")
        print(f"Patterns Count: {stats['patterns_count']}")
        print(f"{'='*70}\n")


# Example usage
if __name__ == "__main__":
    tracker = UsagePatternTracker()
    
    # Simulate some usage
    print("🚀 USAGE PATTERN TRACKER - TEST\n")
    
    # Track some queries
    tracker.track_query("sentinel", 2.5, success=True, query_type="general")
    tracker.track_query("architect", 3.1, success=True, query_type="code")
    tracker.track_query("flash", 1.2, success=True, query_type="quick")
    tracker.track_query("sentinel", 2.3, success=True, query_type="general")
    
    # Track model switches
    tracker.track_model_switch("sentinel", "architect", 2.5, "code task detected")
    tracker.track_model_switch("architect", "sentinel", 2.3, "back to general")
    
    # Print statistics
    tracker.print_statistics()
    
    # Predict next model
    next_model = tracker.predict_next_model()
    print(f"Predicted next model: {next_model}\n")
    
    # Save patterns
    tracker._save_patterns()
    print("✅ Patterns saved")
