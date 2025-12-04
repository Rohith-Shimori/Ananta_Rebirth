# backend/features/proactive_assistant.py
"""
Proactive Assistant for Ananta
Checks in on user, reminds about tasks, suggests breaks
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os

class ProactiveAssistant:
    """
    Makes Ananta proactive - checks in, reminds, suggests
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.schedule_file = os.path.join(data_dir, "proactive_schedule.json")
        self.enabled = True
        self.last_checkin = None
        self.work_session_start = None
        
        # Load or create schedule
        self.schedule_data = self._load_schedule()
    
    def _load_schedule(self) -> Dict:
        """Load proactive schedule"""
        try:
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        except:
            return {
                "preferences": {
                    "work_duration": 90,  # minutes before break reminder
                    "checkin_frequency": 180,  # minutes between check-ins
                    "quiet_hours": {
                        "enabled": True,
                        "start": "22:00",
                        "end": "08:00"
                    }
                },
                "reminders": [],
                "achievements": []
            }
    
    def _save_schedule(self):
        """Save schedule"""
        with open(self.schedule_file, 'w') as f:
            json.dump(self.schedule_data, f, indent=2)
    
    def is_quiet_hours(self) -> bool:
        """Check if current time is in quiet hours"""
        if not self.schedule_data["preferences"]["quiet_hours"]["enabled"]:
            return False
        
        now = datetime.now().time()
        quiet = self.schedule_data["preferences"]["quiet_hours"]
        
        start = datetime.strptime(quiet["start"], "%H:%M").time()
        end = datetime.strptime(quiet["end"], "%H:%M").time()
        
        if start < end:
            return start <= now <= end
        else:  # Crosses midnight
            return now >= start or now <= end
    
    def should_check_in(self) -> bool:
        """Determine if should check in with user"""
        if self.is_quiet_hours():
            return False
        
        if self.last_checkin is None:
            return True
        
        minutes_since = (datetime.now() - self.last_checkin).total_seconds() / 60
        checkin_freq = self.schedule_data["preferences"]["checkin_frequency"]
        
        return minutes_since >= checkin_freq
    
    def get_checkin_message(self, context: Dict) -> str:
        """
        Generate contextual check-in message
        
        Args:
            context: User context (tasks, recent activity)
        
        Returns:
            Check-in message
        """
        user_name = context.get("user_name", "")
        pending_tasks = context.get("pending_tasks", [])
        recent_topic = context.get("recent_topic", "")
        time_of_day = datetime.now().hour
        
        # Greeting based on time
        if 5 <= time_of_day < 12:
            greeting = f"Good morning{' ' + user_name if user_name else ''}!"
        elif 12 <= time_of_day < 17:
            greeting = f"Hey{' ' + user_name if user_name else ''}!"
        elif 17 <= time_of_day < 22:
            greeting = f"Good evening{' ' + user_name if user_name else ''}!"
        else:
            greeting = f"Hey{' ' + user_name if user_name else ''}, still working?"
        
        # Build message
        messages = [greeting]
        
        # Check on recent work
        if recent_topic:
            messages.append(f"How's {recent_topic} going?")
        
        # Remind about tasks
        if pending_tasks and len(pending_tasks) > 0:
            if len(pending_tasks) == 1:
                messages.append(f"Don't forget about: {pending_tasks[0]['title']}")
            else:
                messages.append(f"You have {len(pending_tasks)} pending tasks. Need help prioritizing?")
        
        # Random helpful suggestions
        if len(messages) == 1:  # Only greeting so far
            suggestions = [
                "What are you working on?",
                "Need help with anything?",
                "Want to brainstorm some ideas?",
                "How about we tackle something new?"
            ]
            import random
            messages.append(random.choice(suggestions))
        
        return " ".join(messages)
    
    def suggest_break(self) -> str:
        """Suggest a break to user"""
        if self.work_session_start is None:
            return ""
        
        minutes_working = (datetime.now() - self.work_session_start).total_seconds() / 60
        work_duration = self.schedule_data["preferences"]["work_duration"]
        
        if minutes_working >= work_duration:
            suggestions = [
                "You've been working for a while. Time for a quick break? 🧘",
                "Great focus! How about stretching for 5 minutes?",
                "Your eyes might need a break. Look away from the screen for a bit? 👀",
                "Coffee break? Your brain will thank you! ☕"
            ]
            import random
            return random.choice(suggestions)
        
        return ""
    
    def start_work_session(self):
        """Mark start of work session"""
        self.work_session_start = datetime.now()
    
    def end_work_session(self):
        """Mark end of work session"""
        if self.work_session_start:
            duration = (datetime.now() - self.work_session_start).total_seconds() / 60
            
            # Track achievement
            self.schedule_data["achievements"].append({
                "date": datetime.now().isoformat(),
                "type": "work_session",
                "duration_minutes": int(duration)
            })
            self._save_schedule()
            
            self.work_session_start = None
            
            return f"Great work! You focused for {int(duration)} minutes. 🎉"
        return ""
    
    def add_reminder(self, title: str, time_str: str, recurrence: str = "once"):
        """
        Add a proactive reminder
        
        Args:
            title: Reminder title
            time_str: Time string (e.g., "14:30", "tomorrow 10:00")
            recurrence: once, daily, weekly
        """
        reminder = {
            "id": len(self.schedule_data["reminders"]) + 1,
            "title": title,
            "time": time_str,
            "recurrence": recurrence,
            "created": datetime.now().isoformat(),
            "active": True
        }
        
        self.schedule_data["reminders"].append(reminder)
        self._save_schedule()
        
        return f"✅ Reminder set: {title} at {time_str}"
    
    def check_reminders(self) -> List[str]:
        """Check if any reminders are due"""
        due_reminders = []
        now = datetime.now()
        
        for reminder in self.schedule_data["reminders"]:
            if not reminder["active"]:
                continue
            
            # Simple time matching (can be enhanced)
            reminder_time = reminder["time"]
            # match exact HH:MM strings; if reminder_time contains additional words
            # (e.g., 'tomorrow 10:00') this simple matcher will not trigger.
            if reminder_time == now.strftime("%H:%M"):
                due_reminders.append(f"⏰ Reminder: {reminder['title']}")
                
                # Disable if once
                if reminder["recurrence"] == "once":
                    reminder["active"] = False
        
        if due_reminders:
            self._save_schedule()
        
        return due_reminders
    
    def get_daily_summary(self, stats: Dict) -> str:
        """
        Generate end-of-day summary
        
        Args:
            stats: User statistics
        
        Returns:
            Summary message
        """
        achievements = self.schedule_data["achievements"]
        today = datetime.now().date()
        
        # Filter today's achievements
        today_achievements = [
            a for a in achievements
            if datetime.fromisoformat(a["date"]).date() == today
        ]
        
        if not today_achievements:
            return "You didn't track any sessions today. Tomorrow is a new day! 💪"
        
        # Calculate totals
        total_minutes = sum(a.get("duration_minutes", 0) for a in today_achievements)
        session_count = len(today_achievements)
        
        summary = f"🎉 Daily Summary:\n"
        summary += f"• {session_count} focused session{'s' if session_count > 1 else ''}\n"
        summary += f"• {total_minutes} minutes of productive work\n"
        
        # Add stats if available
        if stats:
            interactions = stats.get("total_interactions", 0)
            if interactions > 0:
                summary += f"• {interactions} conversations with me\n"
        
        summary += "\nGreat job today! 🌟"
        
        return summary
    
    def suggest_next_action(self, context: Dict) -> Optional[str]:
        """
        Suggest what user should work on next
        
        Args:
            context: User context
        
        Returns:
            Suggestion or None
        """
        pending_tasks = context.get("pending_tasks", [])
        recent_activity = context.get("recent_activity", "")
        
        if not pending_tasks:
            return "You're all caught up! Want to start something new?"
        
        # Suggest highest priority task
        high_priority = [t for t in pending_tasks if t.get("priority") == "high"]
        
        if high_priority:
            task = high_priority[0]
            return f"💡 Suggestion: Let's tackle '{task['title']}' next? It's high priority."
        
        # Suggest oldest task
        if pending_tasks:
            task = pending_tasks[0]
            return f"How about we work on '{task['title']}'?"
        
        return None
    
    def celebrate_achievement(self, achievement_type: str) -> str:
        """Generate celebration message"""
        celebrations = {
            "task_completed": [
                "🎉 Awesome! Another one done!",
                "💪 You're on fire!",
                "✅ That's what I call progress!",
                "🌟 Great work! What's next?"
            ],
            "streak": [
                "🔥 You're on a streak!",
                "💯 Consistency is key!",
                "⚡ Momentum building!"
            ],
            "milestone": [
                "🏆 Milestone reached!",
                "🎊 This is huge!",
                "🌈 You've come so far!"
            ]
        }
        
        import random
        messages = celebrations.get(achievement_type, ["Great job!"])
        return random.choice(messages)
    
    async def run_background(self, controller):
        """
        Run proactive features in background
        Should be called in a separate thread/process
        """
        print("🤖 Proactive Assistant started!")
        
        while self.enabled:
            try:
                # Check reminders
                reminders = self.check_reminders()
                for reminder in reminders:
                    print(f"[Proactive] {reminder}")
                
                # Check if should suggest break
                if self.work_session_start:
                    break_msg = self.suggest_break()
                    if break_msg:
                        print(f"[Proactive] {break_msg}")
                
                # Sleep for a minute
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"Proactive Assistant Error: {e}")
                await asyncio.sleep(60)
    
    def get_settings(self) -> Dict:
        """Get current settings"""
        return self.schedule_data["preferences"]
    
    def update_settings(self, settings: Dict):
        """Update settings"""
        self.schedule_data["preferences"].update(settings)
        self._save_schedule()