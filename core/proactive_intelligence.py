"""
Proactive Intelligence Engine
Anticipates user needs and provides intelligent assistance
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger("ananta.proactive")

class ProactiveAction(Enum):
    SUGGEST_BREAK = "suggest_break"
    OFFER_HELP = "offer_help"
    REMINDER = "reminder"
    OPTIMIZATION_TIP = "optimization_tip"
    CONTEXTUAL_ASSISTANCE = "contextual_assistance"
    SYSTEM_MONITORING = "system_monitoring"
    WORKFLOW_SUGGESTION = "workflow_suggestion"

@dataclass
class ProactiveSuggestion:
    action: ProactiveAction
    priority: float  # 0.0 to 1.0
    message: str
    context: Dict[str, Any]
    timestamp: datetime
    expires_at: datetime

class ProactiveIntelligence:
    """Advanced proactive intelligence that anticipates user needs"""
    
    def __init__(self):
        self.active_suggestions = []
        self.user_patterns = {}
        self.interaction_history = []
        self.system_baseline = {}
        self.last_proactive_check = time.time()
        self.proactive_settings = {
            'enabled': True,
            'frequency_minutes': 30,
            'intrusiveness_level': 0.3,  # 0.0 = minimal, 1.0 = very proactive
            'learning_enabled': True
        }
        self._initialize_baseline()
    
    def _initialize_baseline(self):
        """Initialize system baseline for monitoring"""
        try:
            import psutil
            self.system_baseline = {
                'cpu_avg': psutil.cpu_percent(interval=1),
                'memory_avg': psutil.virtual_memory().percent,
                'process_count': len(list(psutil.process_iter())),
                'timestamp': datetime.now()
            }
        except Exception as e:
            logger.error(f"Failed to initialize baseline: {e}")
            self.system_baseline = {'cpu_avg': 50, 'memory_avg': 50, 'process_count': 50}
    
    def analyze_and_suggest(self, context: Dict[str, Any], recent_interactions: List[Dict]) -> List[ProactiveSuggestion]:
        """Analyze context and generate proactive suggestions"""
        
        current_time = datetime.now()
        suggestions = []
        
        # Clean expired suggestions
        self.active_suggestions = [s for s in self.active_suggestions if s.expires_at > current_time]
        
        # Check if enough time has passed for proactive analysis
        if not self._should_check_proactive():
            return []
        
        # Generate suggestions based on different factors
        suggestions.extend(self._analyze_work_patterns(context, recent_interactions))
        suggestions.extend(self._analyze_system_health(context))
        suggestions.extend(self._analyze_time_context(context))
        suggestions.extend(self._analyze_development_context(context))
        suggestions.extend(self._analyze_user_behavior(context, recent_interactions))
        
        # Prioritize and filter suggestions
        filtered_suggestions = self._prioritize_and_filter(suggestions)
        
        # Add to active suggestions
        self.active_suggestions.extend(filtered_suggestions)
        
        self.last_proactive_check = time.time()
        return filtered_suggestions
    
    def _analyze_work_patterns(self, context: Dict, interactions: List[Dict]) -> List[ProactiveSuggestion]:
        """Analyze work patterns and suggest improvements"""
        suggestions = []
        
        # Check for long work sessions
        if context.get('user', {}).get('work_hours', False):
            last_break = self._get_last_break_time()
            if last_break and (datetime.now() - last_break) > timedelta(hours=2):
                suggestions.append(ProactiveSuggestion(
                    action=ProactiveAction.SUGGEST_BREAK,
                    priority=0.7,
                    message="You've been working for a while. Consider taking a short break to refresh your mind. 🧘‍♂️",
                    context={'reason': 'long_work_session', 'duration': '2+ hours'},
                    timestamp=datetime.now(),
                    expires_at=datetime.now() + timedelta(minutes=30)
                ))
        
        # Check for repetitive tasks
        if len(interactions) > 5:
            recent_queries = [i.get('text', '') for i in interactions[-5:]]
            if len(set(recent_queries)) < 3:  # High repetition
                suggestions.append(ProactiveSuggestion(
                    action=ProactiveAction.OPTIMIZATION_TIP,
                    priority=0.6,
                    message="I notice you're working on similar tasks. Would you like me to help automate or streamline this process?",
                    context={'reason': 'repetitive_tasks', 'patterns': list(set(recent_queries))},
                    timestamp=datetime.now(),
                    expires_at=datetime.now() + timedelta(hours=1)
                ))
        
        return suggestions
    
    def _analyze_system_health(self, context: Dict) -> List[ProactiveSuggestion]:
        """Analyze system health and performance"""
        suggestions = []
        
        try:
            import psutil
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            
            # High CPU usage
            if cpu_usage > 80:
                suggestions.append(ProactiveSuggestion(
                    action=ProactiveAction.SYSTEM_MONITORING,
                    priority=0.8,
                    message=f"Your CPU usage is high ({cpu_usage:.1f}%). Consider closing unnecessary applications.",
                    context={'metric': 'cpu', 'value': cpu_usage, 'threshold': 80},
                    timestamp=datetime.now(),
                    expires_at=datetime.now() + timedelta(minutes=15)
                ))
            
            # High memory usage
            if memory_usage > 85:
                suggestions.append(ProactiveSuggestion(
                    action=ProactiveAction.SYSTEM_MONITORING,
                    priority=0.8,
                    message=f"Memory usage is at {memory_usage:.1f}%. A system restart might help performance.",
                    context={'metric': 'memory', 'value': memory_usage, 'threshold': 85},
                    timestamp=datetime.now(),
                    expires_at=datetime.now() + timedelta(minutes=20)
                ))
            
            # Battery monitoring
            try:
                battery = psutil.sensors_battery()
                if battery and battery.percent < 20 and not battery.power_plugged:
                    suggestions.append(ProactiveSuggestion(
                        action=ProactiveAction.SYSTEM_MONITORING,
                        priority=0.9,
                        message=f"Low battery warning: {battery.percent:.0f}% remaining. Consider connecting to power.",
                        context={'metric': 'battery', 'value': battery.percent, 'plugged': False},
                        timestamp=datetime.now(),
                        expires_at=datetime.now() + timedelta(minutes=10)
                    ))
            except:
                pass
                
        except Exception as e:
            logger.error(f"System health analysis error: {e}")
        
        return suggestions
    
    def _analyze_time_context(self, context: Dict) -> List[ProactiveSuggestion]:
        """Analyze time-based context for suggestions"""
        suggestions = []
        
        user_context = context.get('user', {})
        time_of_day = user_context.get('time_of_day', '')
        work_hours = user_context.get('work_hours', False)
        
        # Morning productivity boost
        if time_of_day == 'morning' and work_hours:
            suggestions.append(ProactiveSuggestion(
                action=ProactiveAction.CONTEXTUAL_ASSISTANCE,
                priority=0.5,
                message="Good morning! Ready to tackle today's challenges? I can help prioritize your tasks. ☀️",
                context={'time': 'morning', 'type': 'productivity_boost'},
                timestamp=datetime.now(),
                expires_at=datetime.now() + timedelta(hours=2)
            ))
        
        # End of day wrap-up
        if time_of_day == 'evening' and work_hours:
            suggestions.append(ProactiveSuggestion(
                action=ProactiveAction.WORKFLOW_SUGGESTION,
                priority=0.6,
                message="Work day ending soon. Would you like me to help summarize today's progress or plan tomorrow's tasks?",
                context={'time': 'evening_wrap', 'type': 'daily_summary'},
                timestamp=datetime.now(),
                expires_at=datetime.now() + timedelta(hours=1)
            ))
        
        # Late night reminder
        if time_of_day == 'night' and not work_hours:
            suggestions.append(ProactiveSuggestion(
                action=ProactiveAction.SUGGEST_BREAK,
                priority=0.4,
                message="It's getting late. Remember to rest well for optimal performance tomorrow. 🌙",
                context={'time': 'late_night', 'type': 'health_reminder'},
                timestamp=datetime.now(),
                expires_at=datetime.now() + timedelta(minutes=30)
            ))
        
        return suggestions
    
    def _analyze_development_context(self, context: Dict) -> List[ProactiveSuggestion]:
        """Analyze development-specific context"""
        suggestions = []
        
        env_context = context.get('environment', {})
        
        if env_context.get('development_mode', False):
            # Check for common development patterns
            running_apps = env_context.get('running_applications', [])
            
            # Git operations suggestion
            if any('git' in app.lower() for app in running_apps):
                suggestions.append(ProactiveSuggestion(
                    action=ProactiveAction.CONTEXTUAL_ASSISTANCE,
                    priority=0.6,
                    message="I see you're using Git. Need help with commit messages, branch management, or conflict resolution?",
                    context={'development': 'git_operations'},
                    timestamp=datetime.now(),
                    expires_at=datetime.now() + timedelta(minutes=45)
                ))
            
            # Code optimization suggestion
            system_load = env_context.get('system_load', '')
            if system_load == 'high':
                suggestions.append(ProactiveSuggestion(
                    action=ProactiveAction.OPTIMIZATION_TIP,
                    priority=0.7,
                    message="High system load detected. Consider optimizing your development environment or checking for resource leaks.",
                    context={'development': 'performance_optimization'},
                    timestamp=datetime.now(),
                    expires_at=datetime.now() + timedelta(hours=1)
                ))
        
        return suggestions
    
    def _analyze_user_behavior(self, context: Dict, interactions: List[Dict]) -> List[ProactiveSuggestion]:
        """Analyze user behavior patterns for personalized suggestions"""
        suggestions = []
        
        if not interactions:
            return suggestions
        
        # Analyze interaction patterns
        recent_interactions = interactions[-10:]
        
        # Check for frustration indicators
        frustration_keywords = ['error', 'wrong', 'not working', 'confused', 'help']
        frustration_count = sum(1 for i in recent_interactions 
                               if any(keyword in i.get('text', '').lower() for keyword in frustration_keywords))
        
        if frustration_count >= 3:
            suggestions.append(ProactiveSuggestion(
                action=ProactiveAction.OFFER_HELP,
                priority=0.8,
                message="I sense some frustration. Let me help you more directly. What specific challenge are you facing?",
                context={'analysis': 'frustration_detected', 'count': frustration_count},
                timestamp=datetime.now(),
                expires_at=datetime.now() + timedelta(minutes=20)
            ))
        
        # Check for learning patterns
        question_patterns = ['how to', 'what is', 'why does', 'explain']
        question_count = sum(1 for i in recent_interactions 
                           if any(pattern in i.get('text', '').lower() for pattern in question_patterns))
        
        if question_count >= 5:
            suggestions.append(ProactiveSuggestion(
                action=ProactiveAction.CONTEXTUAL_ASSISTANCE,
                priority=0.5,
                message="You're exploring many concepts! Would you like me to create a structured learning path or provide deeper explanations?",
                context={'analysis': 'learning_pattern', 'count': question_count},
                timestamp=datetime.now(),
                expires_at=datetime.now() + timedelta(hours=2)
            ))
        
        return suggestions
    
    def _should_check_proactive(self) -> bool:
        """Check if enough time has passed for proactive analysis"""
        if not self.proactive_settings['enabled']:
            return False
        
        time_since_last = time.time() - self.last_proactive_check
        min_interval = self.proactive_settings['frequency_minutes'] * 60
        
        return time_since_last >= min_interval
    
    def _prioritize_and_filter(self, suggestions: List[ProactiveSuggestion]) -> List[ProactiveSuggestion]:
        """Prioritize and filter suggestions based on settings"""
        
        # Sort by priority
        suggestions.sort(key=lambda x: x.priority, reverse=True)
        
        # Filter based on intrusiveness level
        max_suggestions = int(5 * (1 - self.proactive_settings['intrusiveness_level']) + 2)
        max_suggestions = max(1, min(5, max_suggestions))
        
        # Filter by minimum priority threshold
        min_priority = 0.3 * (1 - self.proactive_settings['intrusiveness_level'])
        
        filtered = [s for s in suggestions if s.priority >= min_priority][:max_suggestions]
        
        return filtered
    
    def _get_last_break_time(self) -> Optional[datetime]:
        """Get timestamp of last detected break"""
        # This would track break patterns
        # Simplified implementation
        return datetime.now() - timedelta(hours=3)
    
    def get_proactive_summary(self) -> Dict[str, Any]:
        """Get summary of proactive intelligence status"""
        
        active_count = len(self.active_suggestions)
        priority_distribution = {'high': 0, 'medium': 0, 'low': 0}
        
        for suggestion in self.active_suggestions:
            if suggestion.priority >= 0.7:
                priority_distribution['high'] += 1
            elif suggestion.priority >= 0.5:
                priority_distribution['medium'] += 1
            else:
                priority_distribution['low'] += 1
        
        return {
            'active_suggestions': active_count,
            'priority_distribution': priority_distribution,
            'last_check': self.last_proactive_check,
            'settings': self.proactive_settings,
            'learning_patterns': len(self.user_patterns)
        }
    
    def update_settings(self, new_settings: Dict[str, Any]):
        """Update proactive intelligence settings"""
        self.proactive_settings.update(new_settings)
    
    def dismiss_suggestion(self, suggestion_id: str):
        """Dismiss a specific suggestion"""
        self.active_suggestions = [s for s in self.active_suggestions 
                                  if s.timestamp.isoformat() != suggestion_id]
    
    def learn_from_feedback(self, suggestion_id: str, feedback: str):
        """Learn from user feedback on suggestions"""
        if not self.proactive_settings['learning_enabled']:
            return
        
        feedback_lower = feedback.lower()
        
        # Analyze feedback
        positive_feedback = ['helpful', 'good', 'useful', 'thanks', 'great']
        negative_feedback = ['not helpful', 'annoying', 'wrong', 'bad', 'stop']
        
        if any(word in feedback_lower for word in positive_feedback):
            # Reinforce this type of suggestion
            self._reinforce_suggestion_type(suggestion_id)
        elif any(word in feedback_lower for word in negative_feedback):
            # Reduce this type of suggestion
            self._reduce_suggestion_type(suggestion_id)
    
    def _reinforce_suggestion_type(self, suggestion_id: str):
        """Reinforce a specific type of suggestion"""
        # Find the suggestion and learn from it
        for suggestion in self.active_suggestions:
            if suggestion.timestamp.isoformat() == suggestion_id:
                action_type = suggestion.action.value
                self.user_patterns[action_type] = self.user_patterns.get(action_type, 0) + 1
                break
    
    def _reduce_suggestion_type(self, suggestion_id: str):
        """Reduce frequency of a specific type of suggestion"""
        for suggestion in self.active_suggestions:
            if suggestion.timestamp.isoformat() == suggestion_id:
                action_type = suggestion.action.value
                self.user_patterns[action_type] = self.user_patterns.get(action_type, 0) - 1
                break
