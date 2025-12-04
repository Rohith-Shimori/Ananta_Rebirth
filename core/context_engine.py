"""
Real-Time Context Engine - Advanced Environmental Awareness
Makes Ananta truly aware of user context, time, location, activity patterns
"""

import psutil
import platform
import subprocess
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger("ananta.context")

@dataclass
class SystemContext:
    cpu_usage: float
    memory_usage: float
    active_processes: List[str]
    network_status: bool
    battery_level: Optional[float]
    power_source: Optional[str]

@dataclass
class UserContext:
    current_time: datetime
    day_part: str  # morning, afternoon, evening, night
    work_hours: bool
    weekend: bool
    estimated_activity: str
    focus_level: str
    recent_patterns: List[str]

@dataclass
class EnvironmentContext:
    installed_apps: List[str]
    running_apps: List[str]
    recent_files: List[str]
    development_environment: bool
    ai_model_loaded: bool
    system_load: str

class RealTimeContextEngine:
    """Advanced context awareness for JARVIS-like intelligence"""
    
    def __init__(self):
        self.context_history = []
        self.user_patterns = {}
        self.last_update = time.time()
        self._init_user_patterns()
    
    def _init_user_patterns(self):
        """Initialize user behavior patterns"""
        self.user_patterns = {
            'work_hours': (9, 17),  # Default 9-5
            'peak_productivity': [10, 14, 16],  # 10AM, 2PM, 4PM
            'break_times': [12, 15, 18],  # Lunch, afternoon break, evening
            'sleep_hours': (22, 7),  # 10PM - 7AM
            'preferred_apps': [],
            'development_keywords': ['code', 'programming', 'debug', 'test']
        }
    
    def get_system_context(self) -> SystemContext:
        """Get real-time system information"""
        try:
            # CPU and Memory
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Active processes
            active_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    active_processes.append(proc.info['name'])
                except:
                    continue
            
            # Network status
            network_status = psutil.net_if_stats().get('Ethernet', 
                                psutil.net_if_stats().get('Wi-Fi', None)) is not None
            
            # Battery (if available)
            battery = None
            power_source = None
            try:
                battery_obj = psutil.sensors_battery()
                if battery_obj:
                    battery = battery_obj.percent
                    power_source = "battery" if not battery_obj.power_plugged else "plugged"
            except:
                pass
            
            return SystemContext(
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                active_processes=active_processes[:10],  # Top 10
                network_status=network_status,
                battery_level=battery,
                power_source=power_source
            )
        except Exception as e:
            logger.error(f"System context error: {e}")
            return SystemContext(0, 0, [], False, None, None)
    
    def get_user_context(self) -> UserContext:
        """Get intelligent user context"""
        now = datetime.now()
        
        # Time-based context
        hour = now.hour
        if 6 <= hour < 12:
            day_part = "morning"
        elif 12 <= hour < 17:
            day_part = "afternoon"
        elif 17 <= hour < 22:
            day_part = "evening"
        else:
            day_part = "night"
        
        # Work hours detection
        work_start, work_end = self.user_patterns['work_hours']
        work_hours = work_start <= hour <= work_end
        
        # Weekend detection
        weekend = now.weekday() >= 5
        
        # Activity estimation based on time and patterns
        estimated_activity = self._estimate_activity(now, day_part, work_hours, weekend)
        
        # Focus level based on system usage and time
        focus_level = self._calculate_focus_level(now, work_hours)
        
        # Recent patterns from history
        recent_patterns = self._get_recent_patterns()
        
        return UserContext(
            current_time=now,
            day_part=day_part,
            work_hours=work_hours,
            weekend=weekend,
            estimated_activity=estimated_activity,
            focus_level=focus_level,
            recent_patterns=recent_patterns
        )
    
    def get_environment_context(self) -> EnvironmentContext:
        """Get development and application context"""
        try:
            # Installed applications (Windows)
            installed_apps = []
            running_apps = []
            
            if platform.system() == "Windows":
                try:
                    # Get running applications
                    result = subprocess.run(['tasklist', '/fo', 'csv'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')[1:]  # Skip header
                        for line in lines[:20]:  # Top 20
                            if line.strip():
                                parts = line.split(',')
                                if len(parts) > 0:
                                    app_name = parts[0].strip('"')
                                    running_apps.append(app_name)
                except:
                    pass
            
            # Recent files (simplified)
            recent_files = self._get_recent_files()
            
            # Development environment detection
            development_environment = self._is_development_environment(running_apps)
            
            # AI model status (simplified check)
            ai_model_loaded = self._check_ai_model_status()
            
            # System load classification
            system_load = self._classify_system_load()
            
            return EnvironmentContext(
                installed_apps=installed_apps,
                running_apps=running_apps,
                recent_files=recent_files,
                development_environment=development_environment,
                ai_model_loaded=ai_model_loaded,
                system_load=system_load
            )
        except Exception as e:
            logger.error(f"Environment context error: {e}")
            return EnvironmentContext([], [], [], False, False, "unknown")
    
    def get_full_context(self) -> Dict[str, Any]:
        """Get comprehensive real-time context"""
        system_ctx = self.get_system_context()
        user_ctx = self.get_user_context()
        env_ctx = self.get_environment_context()
        
        full_context = {
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_usage": system_ctx.cpu_usage,
                "memory_usage": system_ctx.memory_usage,
                "battery_level": system_ctx.battery_level,
                "power_source": system_ctx.power_source,
                "network_status": system_ctx.network_status
            },
            "user": {
                "time_of_day": user_ctx.day_part,
                "work_hours": user_ctx.work_hours,
                "weekend": user_ctx.weekend,
                "estimated_activity": user_ctx.estimated_activity,
                "focus_level": user_ctx.focus_level,
                "current_time": user_ctx.current_time.strftime("%I:%M %p")
            },
            "environment": {
                "development_mode": env_ctx.development_environment,
                "running_applications": env_ctx.running_apps[:5],
                "ai_model_ready": env_ctx.ai_model_loaded,
                "system_load": env_ctx.system_load
            },
            "insights": self._generate_context_insights(system_ctx, user_ctx, env_ctx)
        }
        
        # Store in history
        self.context_history.append(full_context)
        if len(self.context_history) > 100:  # Keep last 100 entries
            self.context_history.pop(0)
        
        self.last_update = time.time()
        return full_context
    
    def _estimate_activity(self, now: datetime, day_part: str, work_hours: bool, weekend: bool) -> str:
        """Estimate user's current activity"""
        if weekend:
            if day_part in ["morning", "afternoon"]:
                return "leisure"
            else:
                return "relaxation"
        
        if work_hours:
            if day_part == "morning":
                return "starting_work"
            elif day_part == "afternoon":
                return "deep_work"
            else:
                return "wrapping_up"
        
        if day_part == "evening":
            return "personal_time"
        elif day_part == "night":
            return "late_work" if work_hours else "rest"
        
        return "general"
    
    def _calculate_focus_level(self, now: datetime, work_hours: bool) -> str:
        """Calculate user's likely focus level"""
        if not work_hours:
            return "low"
        
        hour = now.hour
        if hour in [10, 14, 16]:  # Peak productivity times
            return "high"
        elif hour in [11, 13, 15, 17]:  # Good productivity
            return "medium"
        else:
            return "low"
    
    def _get_recent_patterns(self) -> List[str]:
        """Extract recent patterns from context history"""
        if len(self.context_history) < 3:
            return ["insufficient_data"]
        
        recent = self.context_history[-3:]
        patterns = []
        
        # Check for consistent patterns
        activities = [ctx.get("user", {}).get("estimated_activity", "") for ctx in recent]
        if len(set(activities)) == 1:
            patterns.append(f"consistent_{activities[0]}")
        
        # Check work pattern
        work_periods = [ctx.get("user", {}).get("work_hours", False) for ctx in recent]
        if all(work_periods):
            patterns.append("work_focused")
        
        return patterns
    
    def _get_recent_files(self) -> List[str]:
        """Get recent files (simplified implementation)"""
        # This would need platform-specific implementation
        return ["recent_file_1", "recent_file_2"]
    
    def _is_development_environment(self, running_apps: List[str]) -> bool:
        """Check if user is in development environment"""
        dev_keywords = ['code', 'visual studio', 'intellij', 'pycharm', 'vscode', 
                       'git', 'docker', 'terminal', 'powershell', 'cmd']
        
        running_lower = [app.lower() for app in running_apps]
        return any(keyword in ' '.join(running_lower) for keyword in dev_keywords)
    
    def _check_ai_model_status(self) -> bool:
        """Check if AI model is loaded and ready"""
        # Simplified check - would integrate with actual model status
        return True
    
    def _classify_system_load(self) -> str:
        """Classify overall system load"""
        try:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            
            if cpu > 80 or memory > 80:
                return "high"
            elif cpu > 50 or memory > 50:
                return "medium"
            else:
                return "low"
        except:
            return "unknown"
    
    def _generate_context_insights(self, system: SystemContext, user: UserContext, env: EnvironmentContext) -> List[str]:
        """Generate intelligent insights from context"""
        insights = []
        
        # Battery insights
        if system.battery_level and system.battery_level < 20:
            if system.power_source != "plugged":
                insights.append("low_battery_warning")
        
        # Work-life balance insights
        if user.work_hours and user.focus_level == "low":
            insights.append("consider_break")
        
        # Development environment insights
        if env.development_environment and system.system_load == "high":
            insights.append("optimize_performance")
        
        # Time-based suggestions
        if user.day_part == "evening" and user.work_hours:
            insights.append("wrap_up_suggestion")
        
        return insights
    
    def learn_user_pattern(self, pattern_type: str, data: Dict[str, Any]):
        """Learn and adapt to user patterns"""
        if pattern_type not in self.user_patterns:
            self.user_patterns[pattern_type] = []
        
        self.user_patterns[pattern_type].append({
            'timestamp': datetime.now().isoformat(),
            'data': data
        })
        
        # Keep only recent patterns
        if len(self.user_patterns[pattern_type]) > 50:
            self.user_patterns[pattern_type] = self.user_patterns[pattern_type][-30:]
