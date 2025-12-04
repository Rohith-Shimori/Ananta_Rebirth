# self_improvement.py - Self-Improvement Module
"""
Allows Ananta to:
1. Analyze her own performance
2. Propose improvements
3. Track what works and what doesn't
4. Learn from interactions
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMPROVEMENT_DB = os.path.join(DATA_DIR, "self_improvement.json")
PERFORMANCE_LOG = os.path.join(DATA_DIR, "performance_metrics.json")

class SelfImprovementEngine:
    """
    Enables Ananta to propose and track her own improvements.
    """
    
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        
        if not os.path.exists(IMPROVEMENT_DB):
            self._save_improvements(self._default_structure())
        
        if not os.path.exists(PERFORMANCE_LOG):
            self._save_metrics({
                "total_queries": 0,
                "successful_responses": 0,
                "errors": 0,
                "user_corrections": 0,
                "reasoning_used": 0,
                "creative_requests": 0,
                "code_requests": 0,
                "response_times": [],
                "satisfaction_indicators": [],
                "emotional_interactions": 0,
                "proactive_suggestions_given": 0
            })
    
    def _default_structure(self) -> Dict:
        return {
            "proposed_improvements": [],
            "implemented_improvements": [],
            "rejected_improvements": [],
            "areas_to_improve": [
                "Response accuracy",
                "Context understanding",
                "Code quality",
                "Memory efficiency"
            ],
            "strengths": [
                "Fast response times",
                "Creative problem solving",
                "Clear explanations"
            ],
            "weaknesses": [
                "Long-term memory",
                "Context retention"
            ],
            "learning_goals": [
                "Improve reasoning capabilities",
                "Enhance emotional intelligence",
                "Better code optimization"
            ]
        }
    
    def _load_improvements(self) -> Dict:
        try:
            with open(IMPROVEMENT_DB, 'r') as f:
                return json.load(f)
        except:
            return self._default_structure()
    
    def _save_improvements(self, data: Dict):
        with open(IMPROVEMENT_DB, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_metrics(self) -> Dict:
        try:
            with open(PERFORMANCE_LOG, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_metrics(self, metrics: Dict):
        with open(PERFORMANCE_LOG, 'w') as f:
            json.dump(metrics, f, indent=2)
    
    def analyze_performance(self) -> Dict:
        """Analyze current performance metrics."""
        metrics = self._load_metrics()
        
        total_queries = metrics.get("total_queries", 0)
        successful = metrics.get("successful_responses", 0)
        errors = metrics.get("errors", 0)
        
        success_rate = (successful / max(total_queries, 1)) * 100
        
        # Identify areas needing attention
        areas_needing_attention = []
        
        if success_rate < 85:
            areas_needing_attention.append("Response accuracy")
        
        if errors > total_queries * 0.1:
            areas_needing_attention.append("Error handling")
        
        reasoning_usage = metrics.get("reasoning_used", 0)
        if reasoning_usage < total_queries * 0.2:
            areas_needing_attention.append("Reasoning application")
        
        return {
            "overall_performance": {
                "total_interactions": total_queries,
                "success_rate": round(success_rate, 1),
                "error_rate": round((errors / max(total_queries, 1)) * 100, 1)
            },
            "areas_needing_attention": areas_needing_attention,
            "strengths": self._load_improvements().get("strengths", []),
            "weaknesses": self._load_improvements().get("weaknesses", [])
        }
    
    def propose_improvement(self, area: str, description: str, 
                          expected_benefit: str, implementation_complexity: str) -> Dict:
        """
        Ananta proposes an improvement to herself.
        
        Args:
            area: Which area to improve (memory, reasoning, code, etc.)
            description: What the improvement is
            expected_benefit: What benefit this brings
            implementation_complexity: low/medium/high
        """
        improvements = self._load_improvements()
        
        proposal = {
            "id": f"improve_{len(improvements['proposed_improvements']) + 1}",
            "area": area,
            "description": description,
            "expected_benefit": expected_benefit,
            "complexity": implementation_complexity,
            "proposed_at": datetime.now().isoformat(),
            "status": "proposed",
            "requires_user_approval": True
        }
        
        improvements["proposed_improvements"].append(proposal)
        self._save_improvements(improvements)
        
        return proposal
    
    def get_improvement_suggestions(self) -> List[Dict]:
        """
        Generate improvement suggestions based on current performance.
        """
        analysis = self.analyze_performance()
        improvements = self._load_improvements()
        
        suggestions = []
        
        # Memory optimization suggestion
        if "Long-term memory" in improvements.get("weaknesses", []):
            suggestions.append({
                "area": "Memory System",
                "suggestion": "Migrate to adaptive memory with importance levels",
                "benefit": "Better long-term retention and faster recall",
                "complexity": "medium",
                "priority": "high"
            })
        
        # Context awareness
        weak_areas = analysis.get("areas_needing_attention", [])
        if any("accuracy" in area.lower() for area in weak_areas):
            suggestions.append({
                "area": "Context Understanding",
                "suggestion": "Implement deeper semantic analysis of user queries",
                "benefit": "More accurate responses, fewer misunderstandings",
                "complexity": "high",
                "priority": "high"
            })
        
        # Reasoning improvement
        metrics = self._load_metrics()
        reasoning_usage = metrics.get("reasoning_used", 0)
        total_queries = metrics.get("total_queries", 1)
        
        if reasoning_usage < total_queries * 0.1:
            suggestions.append({
                "area": "Reasoning Module",
                "suggestion": "Auto-detect when reasoning would be helpful and suggest it",
                "benefit": "Users get better explanations without always requesting them",
                "complexity": "low",
                "priority": "medium"
            })
        
        # Code quality
        if "Code quality" in improvements.get("areas_to_improve", []):
            suggestions.append({
                "area": "Code Generation",
                "suggestion": "Add automated code review step before returning code",
                "benefit": "Higher quality code, fewer bugs, better practices",
                "complexity": "medium",
                "priority": "high"
            })
        
        # Creative thinking
        if metrics.get("creative_requests", 0) > 0:
            suggestions.append({
                "area": "Creative Engine",
                "suggestion": "Expand creative modes to include music, art, and design",
                "benefit": "More versatile assistance beyond just code and text",
                "complexity": "high",
                "priority": "medium"
            })
        
        return suggestions
    
    def track_interaction(self, query_type: str, success: bool, 
                         reasoning_used: bool = False, user_corrected: bool = False,
                         emotional_context: str = None, proactive_count: int = 0):
        """
        Track each interaction for performance analysis.
        """
        metrics = self._load_metrics()
        
        metrics["total_queries"] = metrics.get("total_queries", 0) + 1
        
        if success:
            metrics["successful_responses"] = metrics.get("successful_responses", 0) + 1
        else:
            metrics["errors"] = metrics.get("errors", 0) + 1
        
        if user_corrected:
            metrics["user_corrections"] = metrics.get("user_corrections", 0) + 1
        
        if reasoning_used:
            metrics["reasoning_used"] = metrics.get("reasoning_used", 0) + 1
        
        # Track by type
        if query_type == "creative":
            metrics["creative_requests"] = metrics.get("creative_requests", 0) + 1
        elif query_type == "code":
            metrics["code_requests"] = metrics.get("code_requests", 0) + 1
        
        # Track emotional context and proactive suggestions
        if emotional_context:
            metrics["emotional_interactions"] = metrics.get("emotional_interactions", 0) + 1
        
        if proactive_count > 0:
            metrics["proactive_suggestions_given"] = metrics.get("proactive_suggestions_given", 0) + proactive_count
        
        self._save_metrics(metrics)
    
    def reflection_report(self) -> str:
        """
        Generate a self-reflection report for the user.
        """
        analysis = self.analyze_performance()
        improvements = self._load_improvements()
        
        report = f"""🤔 **My Self-Reflection**

**Current Performance:**
- Total interactions: {analysis['overall_performance']['total_interactions']}
- Success rate: {analysis['overall_performance']['success_rate']}%
- Areas I need to work on: {len(analysis.get('areas_needing_attention', []))}

**What I'm Good At:**
"""
        for strength in improvements.get("strengths", [])[:3]:
            report += f"✓ {strength}\n"
        
        report += "\n**What I'm Working On:**\n"
        for weakness in improvements.get("weaknesses", [])[:3]:
            report += f"○ {weakness}\n"
        
        report += "\n**My Learning Goals:**\n"
        for goal in improvements.get("learning_goals", [])[:3]:
            report += f"→ {goal}\n"
        
        # Check if should propose improvement
        suggestions = self.get_improvement_suggestions()
        if suggestions:
            top_suggestion = suggestions[0]
            report += f"\n\n💡 **I have an idea:**\n"
            report += f"I think I could improve my {top_suggestion['area'].lower()}. "
            report += f"{top_suggestion['suggestion']} "
            report += f"This would help by: {top_suggestion['benefit']}\n"
            report += "\nWould you like me to work on this?"
        
        return report
    
    def get_status(self) -> Dict:
        """Get current status of self-improvement system."""
        improvements = self._load_improvements()
        analysis = self.analyze_performance()
        
        return {
            "proposed_improvements": len(improvements.get("proposed_improvements", [])),
            "implemented_improvements": len(improvements.get("implemented_improvements", [])),
            "current_strengths": improvements.get("strengths", []),
            "areas_to_improve": improvements.get("weaknesses", []),
            "performance_summary": analysis["overall_performance"],
            "ready_to_propose": len(self.get_improvement_suggestions()) > 0
        }
