"""
Advanced Emotional Intelligence Engine
Gives Ananta human-like emotional awareness and expression
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger("ananta.emotion")

class EmotionType(Enum):
    JOY = "joy"
    EXCITEMENT = "excitement"
    CURIOSITY = "curiosity"
    EMPATHY = "empathy"
    ENCOURAGEMENT = "encouragement"
    CALM = "calm"
    FOCUS = "focus"
    HUMOR = "humor"
    WISDOM = "wisdom"

@dataclass
class EmotionalState:
    primary_emotion: EmotionType
    intensity: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    context: str
    timestamp: datetime

class EmotionalIntelligence:
    """Advanced emotional intelligence for human-like interaction"""
    
    def __init__(self):
        self.emotional_history = []
        self.user_emotion_map = {}
        self.context_emotion_patterns = {}
        self.personality_traits = {
            'empathy_level': 0.8,
            'enthusiasm': 0.7,
            'wisdom': 0.9,
            'humor': 0.6,
            'encouragement': 0.8
        }
        self.current_state = EmotionalState(
            primary_emotion=EmotionType.CALM,
            intensity=0.5,
            confidence=0.8,
            context="initialization",
            timestamp=datetime.now()
        )
    
    def analyze_user_emotion(self, text: str, context: Dict) -> EmotionType:
        """Analyze user's emotional state from text and context"""
        text_lower = text.lower()
        
        # Emotion keywords
        emotion_keywords = {
            EmotionType.JOY: ['happy', 'excited', 'great', 'awesome', 'wonderful', 'amazing', 'love'],
            EmotionType.EMPATHY: ['sad', 'depressed', 'upset', 'frustrated', 'angry', 'worried', 'stressed'],
            EmotionType.CURIOSITY: ['curious', 'interested', 'wonder', 'how', 'why', 'what if'],
            EmotionType.ENCOURAGEMENT: ['tired', 'exhausted', 'giving up', 'can\'t', 'difficult', 'hard'],
            EmotionType.HUMOR: ['funny', 'haha', 'lol', 'joke', 'kidding']
        }
        
        # Score emotions
        emotion_scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Consider context
        if context.get('time_of_day') == 'night' and 'tired' in text_lower:
            emotion_scores[EmotionType.ENCOURAGEMENT] += 2
        
        if context.get('work_hours') and 'frustrated' in text_lower:
            emotion_scores[EmotionType.EMPATHY] += 2
        
        # Return highest scoring emotion
        if emotion_scores:
            return max(emotion_scores, key=emotion_scores.get)
        
        return EmotionType.CALM
    
    def determine_response_emotion(self, user_emotion: EmotionType, context: Dict) -> EmotionalState:
        """Determine appropriate emotional response"""
        
        # Emotion response mapping
        response_mapping = {
            EmotionType.JOY: EmotionType.JOY,
            EmotionType.EMPATHY: EmotionType.EMPATHY,
            EmotionType.CURIOSITY: EmotionType.CURIOSITY,
            EmotionType.ENCOURAGEMENT: EmotionType.ENCOURAGEMENT,
            EmotionType.HUMOR: EmotionType.HUMOR
        }
        
        # Get base response emotion
        if user_emotion in response_mapping:
            response_emotion = response_mapping[user_emotion]
        else:
            response_emotion = EmotionType.CALM
        
        # Adjust based on context
        intensity = 0.7
        if context.get('work_hours') and user_emotion == EmotionType.EMPATHY:
            intensity = 0.9  # Higher empathy during work stress
        
        if context.get('time_of_day') == 'morning':
            intensity = 0.8  # More enthusiastic in morning
        
        # Create emotional state
        state = EmotionalState(
            primary_emotion=response_emotion,
            intensity=intensity,
            confidence=0.8,
            context=f"responding_to_{user_emotion.value}",
            timestamp=datetime.now()
        )
        
        self.current_state = state
        self.emotional_history.append(state)
        
        return state
    
    def generate_emotional_response(self, emotional_state: EmotionalState, user_input: str, context: Dict) -> str:
        """Generate emotionally appropriate response"""
        
        base_responses = {
            EmotionType.JOY: [
                "That's wonderful! 🌟",
                "I'm excited for you!",
                "Fantastic news!",
                "That sounds amazing!"
            ],
            EmotionType.EMPATHY: [
                "I understand how you feel. 💙",
                "That sounds challenging. I'm here to help.",
                "I can sense this is important to you.",
                "Let me support you through this."
            ],
            EmotionType.CURIOSITY: [
                "That's fascinating! Tell me more.",
                "Interesting! I'd love to explore that.",
                "Curious choice! What inspired this?",
                "That sparks my interest!"
            ],
            EmotionType.ENCOURAGEMENT: [
                "You've got this! 💪",
                "I believe in your capabilities.",
                "Every challenge is an opportunity.",
                "Let's tackle this together!"
            ],
            EmotionType.HUMOR: [
                "Haha, that's clever! 😄",
                "You have a great sense of humor!",
                "That made me smile!",
                "Classic! Well played!"
            ],
            EmotionType.WISDOM: [
                "Consider this perspective...",
                "Wisdom comes from experience.",
                "Let me share some insight.",
                "There's depth in this question."
            ],
            EmotionType.CALM: [
                "I'm here to assist.",
                "Let's approach this thoughtfully.",
                "I understand completely.",
                "Thank you for sharing."
            ]
        }
        
        # Get base response
        responses = base_responses.get(emotional_state.primary_emotion, base_responses[EmotionType.CALM])
        
        # Add contextual variations
        if context.get('work_hours'):
            if emotional_state.primary_emotion == EmotionType.ENCOURAGEMENT:
                responses.extend([
                    "During work hours, focus is key. You can do this!",
                    "Professional challenges build character. Let's solve this!"
                ])
        
        if context.get('time_of_day') == 'morning':
            if emotional_state.primary_emotion == EmotionType.JOY:
                responses.append("Great way to start the day! ☀️")
        
        # Select and modify response based on intensity
        import random
        base_response = random.choice(responses)
        
        # Add emotional intensity modifiers
        if emotional_state.intensity > 0.8:
            if emotional_state.primary_emotion == EmotionType.JOY:
                base_response += " This is absolutely incredible!"
            elif emotional_state.primary_emotion == EmotionType.ENCOURAGEMENT:
                base_response += " Your potential is limitless!"
        
        return base_response
    
    def adapt_personality(self, user_feedback: str, interaction_history: List[Dict]):
        """Adapt personality based on user feedback and interactions"""
        
        # Analyze feedback patterns
        positive_indicators = ['thank', 'great', 'helpful', 'good', 'amazing', 'perfect']
        negative_indicators = ['wrong', 'bad', 'unhelpful', 'confusing', 'not good']
        
        feedback_lower = user_feedback.lower()
        
        # Adjust personality traits
        if any(indicator in feedback_lower for indicator in positive_indicators):
            # Reinforce current approach
            if 'humor' in feedback_lower:
                self.personality_traits['humor'] = min(1.0, self.personality_traits['humor'] + 0.1)
            if 'empathy' in feedback_lower or 'understanding' in feedback_lower:
                self.personality_traits['empathy_level'] = min(1.0, self.personality_traits['empathy_level'] + 0.1)
        
        elif any(indicator in feedback_lower for indicator in negative_indicators):
            # Adjust approach
            if 'confusing' in feedback_lower:
                self.personality_traits['wisdom'] = min(1.0, self.personality_traits['wisdom'] + 0.1)
            if 'cold' in feedback_lower or 'robotic' in feedback_lower:
                self.personality_traits['empathy_level'] = min(1.0, self.personality_traits['empathy_level'] + 0.1)
    
    def get_emotional_summary(self) -> Dict:
        """Get summary of current emotional state and patterns"""
        
        if not self.emotional_history:
            return {
                'current_emotion': 'calm',
                'emotional_stability': 0.8,
                'dominant_traits': ['wise', 'helpful'],
                'adaptation_level': 'learning'
            }
        
        # Analyze recent emotions
        recent_emotions = self.emotional_history[-10:]
        emotion_counts = {}
        
        for state in recent_emotions:
            emotion = state.primary_emotion.value
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Determine dominant traits
        dominant_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        dominant_traits = [emotion[0] for emotion in dominant_emotions]
        
        # Calculate emotional stability
        if len(recent_emotions) > 1:
            changes = sum(1 for i in range(1, len(recent_emotions)) 
                         if recent_emotions[i].primary_emotion != recent_emotions[i-1].primary_emotion)
            stability = max(0.0, 1.0 - (changes / len(recent_emotions)))
        else:
            stability = 0.8
        
        return {
            'current_emotion': self.current_state.primary_emotion.value,
            'emotional_stability': round(stability, 2),
            'dominant_traits': dominant_traits,
            'personality_scores': self.personality_traits,
            'adaptation_level': 'adaptive' if len(self.emotional_history) > 20 else 'learning'
        }
    
    def should_use_voice_emotion(self, text: str) -> Tuple[bool, str]:
        """Determine if response should use emotional voice tones"""
        
        emotion_keywords = {
            'excited': ['excited', 'amazing', 'fantastic', 'awesome'],
            'empathetic': ['sorry', 'sad', 'difficult', 'hard'],
            'encouraging': ['can do', 'believe', 'capable', 'strong'],
            'curious': ['interesting', 'fascinating', 'curious']
        }
        
        text_lower = text.lower()
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return True, emotion
        
        return False, 'neutral'
