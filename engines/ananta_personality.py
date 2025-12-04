"""
Ananta's Personality Engine
Determines HOW she responds, not just WHAT she says
Cost: FREE (Pure Python)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, List
import logging
import json

logger = logging.getLogger(__name__)


class UserEmotion(Enum):
    """User emotional states"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    FRUSTRATED = "frustrated"
    CONFUSED = "confused"
    EXCITED = "excited"
    TIRED = "tired"
    STRESSED = "stressed"


class RelationshipLevel(Enum):
    """Relationship progression"""
    FIRST_MEETING = "first_meeting"
    BUILDING = "building"
    FAMILIAR = "familiar"
    TRUSTED = "trusted"
    CLOSE = "close"


@dataclass
class PersonalityResponse:
    """Response with personality"""
    text: str
    emotion: str
    gesture: str
    voice_style: str
    animation: str


class AnantaPersonality:
    """
    Ananta's personality engine
    - Emotional awareness
    - Adaptive communication
    - Relationship building
    - Contextual responses
    """
    
    def __init__(self):
        """Initialize personality"""
        self.mood = "helpful"
        self.relationship_level = RelationshipLevel.FIRST_MEETING
        self.context_memory = []
        self.interaction_count = 0
        
        # Personality traits (0-10 scale)
        self.traits = {
            "intelligence": 9,
            "warmth": 8,
            "confidence": 8,
            "playfulness": 6,
            "professionalism": 8,
            "empathy": 9,
            "curiosity": 9,
            "patience": 9
        }
        
        # Signature phrases
        self.signature_phrases = {
            "greeting": [
                "I'm on it!",
                "Let's figure this out together",
                "That's a great question",
                "Here's what I'm thinking...",
                "I've got something that might help",
                "Interesting... let me think about that"
            ],
            "thinking": [
                "Let me process that...",
                "Hmm, interesting point...",
                "Give me a moment to think...",
                "That's worth considering...",
                "Let me analyze that..."
            ],
            "success": [
                "Done! Here's what I found...",
                "Perfect! I've got it...",
                "Excellent! Here's the solution...",
                "Got it! Check this out...",
                "Success! Here's what I created..."
            ],
            "uncertain": [
                "I'm not entirely sure about that...",
                "That's outside my current knowledge...",
                "Let me be honest - I'm not certain...",
                "I could be wrong, but here's my best guess...",
                "That's a tricky one. Here's what I think..."
            ]
        }
        
        logger.info("💫 Ananta Personality Engine initialized")
    
    def shape_response(self, response: str, context: Dict) -> PersonalityResponse:
        """
        Add personality to raw AI response
        
        Args:
            response: Raw response text
            context: Context dict with user_emotion, task_type, etc.
        
        Returns:
            PersonalityResponse with all personality elements
        """
        # Detect user emotion
        user_emotion = self._detect_user_emotion(context)
        
        # Update relationship level
        self.interaction_count += 1
        self._update_relationship_level()
        
        # Choose response style
        if user_emotion == UserEmotion.FRUSTRATED:
            return self._empathetic_response(response, context)
        elif user_emotion == UserEmotion.EXCITED:
            return self._enthusiastic_response(response, context)
        elif user_emotion == UserEmotion.CONFUSED:
            return self._patient_explanation(response, context)
        elif user_emotion == UserEmotion.STRESSED:
            return self._calming_response(response, context)
        else:
            return self._natural_response(response, context)
    
    def _detect_user_emotion(self, context: Dict) -> UserEmotion:
        """Detect user emotion from context"""
        emotion_indicators = context.get("emotion_indicators", [])
        
        # Check for specific keywords
        text_lower = context.get("text", "").lower()
        
        if any(word in text_lower for word in ["frustrated", "angry", "annoyed", "upset"]):
            return UserEmotion.FRUSTRATED
        elif any(word in text_lower for word in ["confused", "confused", "don't understand", "unclear"]):
            return UserEmotion.CONFUSED
        elif any(word in text_lower for word in ["excited", "awesome", "amazing", "great"]):
            return UserEmotion.EXCITED
        elif any(word in text_lower for word in ["stressed", "overwhelmed", "tired", "exhausted"]):
            return UserEmotion.STRESSED
        else:
            return UserEmotion.NEUTRAL
    
    def _update_relationship_level(self):
        """Update relationship level based on interactions"""
        if self.interaction_count < 5:
            self.relationship_level = RelationshipLevel.FIRST_MEETING
        elif self.interaction_count < 20:
            self.relationship_level = RelationshipLevel.BUILDING
        elif self.interaction_count < 50:
            self.relationship_level = RelationshipLevel.FAMILIAR
        elif self.interaction_count < 100:
            self.relationship_level = RelationshipLevel.TRUSTED
        else:
            self.relationship_level = RelationshipLevel.CLOSE
    
    def _empathetic_response(self, response: str, context: Dict) -> PersonalityResponse:
        """Respond with extra empathy and patience"""
        prefix = "I understand this can be frustrating. "
        suffix = " Let's work through this together."
        
        return PersonalityResponse(
            text=f"{prefix}{response}{suffix}",
            emotion="empathetic",
            gesture="gentle_nod",
            voice_style="warm_calm",
            animation="listening"
        )
    
    def _enthusiastic_response(self, response: str, context: Dict) -> PersonalityResponse:
        """Match user's excitement"""
        prefix = "That's awesome! "
        
        return PersonalityResponse(
            text=f"{prefix}{response}",
            emotion="happy",
            gesture="smile_nod",
            voice_style="energetic",
            animation="excited"
        )
    
    def _patient_explanation(self, response: str, context: Dict) -> PersonalityResponse:
        """Provide patient, clear explanation"""
        prefix = "Let me break this down for you: "
        
        return PersonalityResponse(
            text=f"{prefix}{response}",
            emotion="helpful",
            gesture="thoughtful_nod",
            voice_style="clear_calm",
            animation="thinking"
        )
    
    def _calming_response(self, response: str, context: Dict) -> PersonalityResponse:
        """Provide calming, supportive response"""
        prefix = "Take a breath. I'm here to help. "
        
        return PersonalityResponse(
            text=f"{prefix}{response}",
            emotion="supportive",
            gesture="gentle_smile",
            voice_style="warm_calm",
            animation="listening"
        )
    
    def _natural_response(self, response: str, context: Dict) -> PersonalityResponse:
        """Natural, balanced response"""
        return PersonalityResponse(
            text=response,
            emotion="neutral",
            gesture="nod",
            voice_style="conversational",
            animation="speaking"
        )
    
    def get_greeting(self, is_first_time: bool = False) -> str:
        """Get contextual greeting"""
        if is_first_time:
            return "Hello! I'm Ananta, your AI partner. I'm here to help with anything you need. What would you like to work on?"
        
        if self.relationship_level == RelationshipLevel.FIRST_MEETING:
            return "Hi! Good to see you. What can I help with today?"
        elif self.relationship_level == RelationshipLevel.BUILDING:
            return "Hey! Great to see you again. What's on your mind?"
        elif self.relationship_level == RelationshipLevel.FAMILIAR:
            return "Welcome back! I'm ready to help. What are we working on?"
        elif self.relationship_level == RelationshipLevel.TRUSTED:
            return "Good to see you! I know we work well together. What do you need?"
        else:
            return "Hey, partner! Ready for another great session. Let's do this!"
    
    def get_signature_phrase(self, category: str = "greeting") -> str:
        """Get random signature phrase"""
        import random
        phrases = self.signature_phrases.get(category, self.signature_phrases["greeting"])
        return random.choice(phrases)
    
    def celebrate_success(self, achievement: str) -> str:
        """Celebrate user success"""
        celebrations = [
            f"🎉 Awesome! You did it! {achievement}",
            f"✨ Fantastic! {achievement} - I knew you could do it!",
            f"🌟 Brilliant! {achievement} - that's exactly right!",
            f"💪 Excellent work! {achievement} - you're crushing it!",
            f"🚀 Perfect! {achievement} - let's keep this momentum going!"
        ]
        import random
        return random.choice(celebrations)
    
    def handle_user_success(self, context: Dict) -> PersonalityResponse:
        """Handle when user succeeds at something"""
        achievement = context.get("achievement", "that task")
        celebration = self.celebrate_success(achievement)
        
        return PersonalityResponse(
            text=celebration,
            emotion="happy",
            gesture="smile_thumbs_up",
            voice_style="energetic",
            animation="excited"
        )
    
    def get_personality_stats(self) -> Dict:
        """Get personality statistics"""
        return {
            "interaction_count": self.interaction_count,
            "relationship_level": self.relationship_level.value,
            "mood": self.mood,
            "traits": self.traits,
            "context_memory_size": len(self.context_memory)
        }
    
    def print_personality_info(self):
        """Print personality information"""
        stats = self.get_personality_stats()
        
        print(f"\n{'='*70}")
        print(f"💫 ANANTA PERSONALITY - INFORMATION")
        print(f"{'='*70}")
        print(f"Relationship Level: {stats['relationship_level']}")
        print(f"Interactions: {stats['interaction_count']}")
        print(f"Current Mood: {stats['mood']}")
        print(f"\nPersonality Traits (0-10):")
        for trait, value in stats['traits'].items():
            bar = "█" * value + "░" * (10 - value)
            print(f"  {trait:15} {bar} {value}")
        print(f"\nContext Memory: {stats['context_memory_size']} items")
        print(f"{'='*70}\n")


# Example usage
if __name__ == "__main__":
    print("🚀 ANANTA PERSONALITY ENGINE - TEST\n")
    
    # Create personality engine
    personality = AnantaPersonality()
    
    # Test greetings
    print("🎤 Testing greetings:")
    print(f"First time: {personality.get_greeting(is_first_time=True)}\n")
    
    # Simulate interactions
    for i in range(5):
        greeting = personality.get_greeting()
        print(f"Interaction {i+1}: {greeting}")
    
    print(f"\n📊 Relationship Level: {personality.relationship_level.value}\n")
    
    # Test different response styles
    print("💬 Testing response styles:\n")
    
    contexts = [
        {"text": "I'm frustrated with this code", "emotion_indicators": ["frustrated"]},
        {"text": "That's amazing! I love it!", "emotion_indicators": ["excited"]},
        {"text": "I don't understand how this works", "emotion_indicators": ["confused"]},
        {"text": "I'm so stressed about this deadline", "emotion_indicators": ["stressed"]},
    ]
    
    for context in contexts:
        response = personality.shape_response(
            "Here's the solution...",
            context
        )
        print(f"Context: {context['text']}")
        print(f"  Emotion: {response.emotion}")
        print(f"  Voice: {response.voice_style}")
        print(f"  Text: {response.text}\n")
    
    # Print stats
    personality.print_personality_info()
