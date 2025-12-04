"""
Advanced Emotional Intelligence System
Real emotional understanding using AI models and context analysis
"""

import json
import time
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger("ananta.emotion")

class EmotionType(Enum):
    """Comprehensive emotion types"""
    JOY = "joy"
    EXCITEMENT = "excitement"
    CURIOSITY = "curiosity"
    EMPATHY = "empathy"
    ENCOURAGEMENT = "encouragement"
    CALM = "calm"
    FOCUS = "focus"
    HUMOR = "humor"
    WISDOM = "wisdom"
    CONFUSION = "confusion"
    FRUSTRATION = "frustration"
    ANXIETY = "anxiety"
    SATISFACTION = "satisfaction"
    SURPRISE = "surprise"
    INTEREST = "interest"

@dataclass
class EmotionalState:
    """Rich emotional state representation"""
    primary_emotion: EmotionType
    secondary_emotion: Optional[EmotionType]
    intensity: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    context: str
    timestamp: datetime
    triggers: List[str]
    physiological_indicators: Dict[str, float]
    cognitive_load: float  # 0.0 to 1.0

@dataclass
class EmotionalProfile:
    """User's emotional profile and patterns"""
    baseline_emotions: Dict[str, float]
    emotional_triggers: Dict[str, List[str]]
    response_patterns: Dict[str, str]
    emotional_history: List[EmotionalState]
    personality_traits: Dict[str, float]
    adaptation_rate: float

class AdvancedEmotionalIntelligence:
    """Advanced emotional intelligence using real AI analysis"""
    
    def __init__(self, use_ai_analysis: bool = True):
        self.use_ai_analysis = use_ai_analysis
        self.thread_pool = ThreadPoolExecutor(max_workers=2)
        
        # Emotional state tracking
        self.current_state = EmotionalState(
            primary_emotion=EmotionType.CALM,
            secondary_emotion=None,
            intensity=0.5,
            confidence=0.8,
            context="initialization",
            timestamp=datetime.now(),
            triggers=[],
            physiological_indicators={},
            cognitive_load=0.3
        )
        
        # User emotional profile
        self.user_profile = EmotionalProfile(
            baseline_emotions={e.value: 0.5 for e in EmotionType},
            emotional_triggers={e.value: [] for e in EmotionType},
            response_patterns={},
            emotional_history=[],
            personality_traits={
                'empathy_level': 0.8,
                'enthusiasm': 0.7,
                'wisdom': 0.9,
                'humor': 0.6,
                'encouragement': 0.8,
                'sensitivity': 0.7
            },
            adaptation_rate=0.1
        )
        
        # Conversation context
        self.conversation_history = []
        self.emotional_transitions = []
        self.context_window = []
        
        # Emotion analysis models
        self.emotion_keywords = self._build_emotion_keywords()
        self.emotion_weights = self._build_emotion_weights()
        
        # Physiological simulation (would integrate with real sensors)
        self.physio_baseline = {
            'heart_rate': 70,
            'breathing_rate': 16,
            'stress_level': 0.2,
            'engagement': 0.5
        }
    
    def _build_emotion_keywords(self) -> Dict[EmotionType, List[str]]:
        """Build comprehensive emotion keyword mappings"""
        return {
            EmotionType.JOY: [
                'happy', 'excited', 'great', 'awesome', 'wonderful', 'amazing', 'love',
                'fantastic', 'brilliant', 'excellent', 'perfect', 'delighted', 'pleased'
            ],
            EmotionType.EMPATHY: [
                'sad', 'depressed', 'upset', 'frustrated', 'angry', 'worried', 'stressed',
                'hurt', 'pain', 'difficult', 'struggling', 'overwhelmed', 'exhausted'
            ],
            EmotionType.CURIOSITY: [
                'curious', 'interested', 'wonder', 'how', 'why', 'what if', 'explore',
                'discover', 'learn', 'understand', 'explain', 'curiosity', 'fascinated'
            ],
            EmotionType.ENCOURAGEMENT: [
                'tired', 'exhausted', 'giving up', 'can\'t', 'difficult', 'hard',
                'stuck', 'need help', 'challenge', 'overwhelmed', 'discouraged'
            ],
            EmotionType.HUMOR: [
                'funny', 'haha', 'lol', 'joke', 'kidding', 'humorous', 'laugh',
                'amusing', 'entertaining', 'playful', 'witty'
            ],
            EmotionType.CONFUSION: [
                'confused', 'unclear', 'don\'t understand', 'lost', 'puzzled',
                'uncertain', 'mixed up', 'complicated', 'difficult to follow'
            ],
            EmotionType.FRUSTRATION: [
                'frustrated', 'annoyed', 'irritated', 'angry', 'upset', 'mad',
                'not working', 'broken', 'stuck', 'problem', 'issue'
            ],
            EmotionType.ANXIETY: [
                'anxious', 'nervous', 'worried', 'afraid', 'scared', 'tense',
                'uneasy', 'concerned', 'apprehensive', 'stressful'
            ],
            EmotionType.SATISFACTION: [
                'satisfied', 'accomplished', 'proud', 'successful', 'achieved',
                'completed', 'done', 'finished', 'resolved', 'working well'
            ],
            EmotionType.SURPRISE: [
                'surprised', 'shocked', 'amazed', 'astonished', 'unexpected',
                'wow', 'whoa', 'incredible', 'unbelievable'
            ],
            EmotionType.INTEREST: [
                'interested', 'engaged', 'attentive', 'focused', 'curious',
                'want to know', 'tell me more', 'fascinating', 'intriguing'
            ],
            EmotionType.CALM: [
                'calm', 'relaxed', 'peaceful', 'serene', 'tranquil', 'quiet',
                'comfortable', 'at ease', 'restful', 'balanced'
            ],
            EmotionType.FOCUS: [
                'focus', 'concentrate', 'attention', 'dedicated', 'working',
                'task', 'project', 'goal', 'objective', 'productive'
            ],
            EmotionType.WISDOM: [
                'wisdom', 'insight', 'understanding', 'knowledge', 'experience',
                'deep', 'profound', 'meaningful', 'thoughtful', 'reflective'
            ],
            EmotionType.EXCITEMENT: [
                'excited', 'thrilled', 'enthusiastic', 'eager', 'passionate',
                'energetic', 'vibrant', 'dynamic', 'animated', 'lively'
            ]
        }
    
    def _build_emotion_weights(self) -> Dict[EmotionType, Dict[str, float]]:
        """Build emotion analysis weights"""
        return {
            EmotionType.JOY: {'positivity': 0.9, 'energy': 0.7, 'intensity': 0.8},
            EmotionType.EMPATHY: {'negativity': 0.6, 'concern': 0.9, 'intensity': 0.7},
            EmotionType.CURIOSITY: {'exploration': 0.9, 'questions': 0.8, 'interest': 0.7},
            EmotionType.ENCOURAGEMENT: {'support': 0.9, 'motivation': 0.8, 'care': 0.7},
            EmotionType.HUMOR: {'playfulness': 0.9, 'surprise': 0.6, 'positivity': 0.7},
            EmotionType.CONFUSION: {'uncertainty': 0.9, 'complexity': 0.7, 'need_clarity': 0.8},
            EmotionType.FRUSTRATION: {'negativity': 0.8, 'intensity': 0.9, 'blockage': 0.7},
            EmotionType.ANXIETY: {'fear': 0.8, 'uncertainty': 0.7, 'tension': 0.9},
            EmotionType.SATISFACTION: {'positivity': 0.8, 'accomplishment': 0.9, 'calm': 0.7},
            EmotionType.SURPRISE: {'unexpected': 0.9, 'novelty': 0.8, 'intensity': 0.7},
            EmotionType.INTEREST: {'engagement': 0.9, 'attention': 0.8, 'curiosity': 0.7},
            EmotionType.CALM: {'peace': 0.9, 'stability': 0.8, 'balance': 0.7},
            EmotionType.FOCUS: {'concentration': 0.9, 'productivity': 0.8, 'clarity': 0.7},
            EmotionType.WISDOM: {'depth': 0.9, 'insight': 0.8, 'reflection': 0.7},
            EmotionType.EXCITEMENT: {'energy': 0.9, 'anticipation': 0.8, 'positivity': 0.7}
        }
    
    def analyze_text_emotion(self, text: str, context: Dict[str, Any] = None) -> EmotionalState:
        """Analyze text emotion using multiple methods"""
        context = context or {}
        
        # Method 1: Keyword analysis
        keyword_scores = self._analyze_keywords(text)
        
        # Method 2: Linguistic patterns
        linguistic_scores = self._analyze_linguistic_patterns(text)
        
        # Method 3: Contextual analysis
        contextual_scores = self._analyze_context(text, context)
        
        # Method 4: AI analysis (if available)
        ai_scores = {}
        if self.use_ai_analysis:
            ai_scores = self._ai_emotion_analysis(text)
        
        # Combine all scores
        combined_scores = self._combine_emotion_scores(
            keyword_scores, linguistic_scores, contextual_scores, ai_scores
        )
        
        # Determine primary and secondary emotions
        sorted_emotions = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        primary_emotion = sorted_emotions[0][0] if sorted_emotions else EmotionType.CALM
        secondary_emotion = sorted_emotions[1][0] if len(sorted_emotions) > 1 else None
        
        intensity = combined_scores.get(primary_emotion, 0.5)
        confidence = min(0.95, 0.5 + (sorted_emotions[0][1] - sorted_emotions[1][1] if len(sorted_emotions) > 1 else 0.3))
        
        # Extract triggers
        triggers = self._extract_triggers(text, primary_emotion)
        
        # Simulate physiological indicators
        physio_indicators = self._simulate_physiological_indicators(primary_emotion, intensity)
        
        # Calculate cognitive load
        cognitive_load = self._calculate_cognitive_load(text, context)
        
        # Create emotional state
        state = EmotionalState(
            primary_emotion=primary_emotion,
            secondary_emotion=secondary_emotion,
            intensity=min(1.0, intensity),
            confidence=min(1.0, confidence),
            context=f"conversation_{len(self.conversation_history)}",
            timestamp=datetime.now(),
            triggers=triggers,
            physiological_indicators=physio_indicators,
            cognitive_load=cognitive_load
        )
        
        # Update current state and history
        self.current_state = state
        self.user_profile.emotional_history.append(state)
        
        # Keep history manageable
        if len(self.user_profile.emotional_history) > 100:
            self.user_profile.emotional_history = self.user_profile.emotional_history[-50:]
        
        return state
    
    def _analyze_keywords(self, text: str) -> Dict[EmotionType, float]:
        """Analyze emotion based on keyword matching"""
        text_lower = text.lower()
        scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Weight by keyword importance
                    weight = 1.0
                    if keyword in ['love', 'hate', 'amazing', 'terrible']:  # Strong words
                        weight = 1.5
                    score += weight
            
            # Normalize by text length
            scores[emotion] = min(1.0, score / (len(text.split()) * 0.3))
        
        return scores
    
    def _analyze_linguistic_patterns(self, text: str) -> Dict[EmotionType, float]:
        """Analyze linguistic patterns for emotion"""
        scores = {}
        
        # Punctuation patterns
        exclamation_count = text.count('!')
        question_count = text.count('?')
        ellipsis_count = text.count('...')
        
        # Capitalization
        all_caps = sum(1 for word in text.split() if word.isupper())
        
        # Sentence length
        sentences = text.split('.')
        avg_sentence_length = sum(len(s.strip().split()) for s in sentences) / max(len(sentences), 1)
        
        # Pattern-based emotion detection
        if exclamation_count > 2:
            scores[EmotionType.EXCITEMENT] = 0.8
            scores[EmotionType.JOY] = 0.6
        elif question_count > 2:
            scores[EmotionType.CURIOSITY] = 0.8
            scores[EmotionType.CONFUSION] = 0.4
        elif ellipsis_count > 0:
            scores[EmotionType.CONFUSION] = 0.5
            scores[EmotionType.UNCERTAINTY] = 0.3
        elif all_caps > 1:
            scores[EmotionType.FRUSTRATION] = 0.7
            scores[EmotionType.EXCITEMENT] = 0.5
        
        # Sentence complexity
        if avg_sentence_length > 20:
            scores[EmotionType.WISDOM] = 0.6
            scores[EmotionType.FOCUS] = 0.4
        elif avg_sentence_length < 8:
            scores[EmotionType.EXCITEMENT] = 0.5
            scores[EmotionType.JOY] = 0.3
        
        return scores
    
    def _analyze_context(self, text: str, context: Dict[str, Any]) -> Dict[EmotionType, float]:
        """Analyze emotion based on context"""
        scores = {}
        
        # Time of day
        hour = datetime.now().hour
        if 6 <= hour < 12:  # Morning
            scores[EmotionType.EXCITEMENT] = 0.7
            scores[EmotionType.FOCUS] = 0.6
        elif 12 <= hour < 17:  # Afternoon
            scores[EmotionType.FOCUS] = 0.7
            scores[EmotionType.INTEREST] = 0.5
        elif 17 <= hour < 22:  # Evening
            scores[EmotionType.CALM] = 0.7
            scores[EmotionType.JOY] = 0.6
        else:  # Night
            scores[EmotionType.CALM] = 0.6
            scores[EmotionType.WISDOM] = 0.5
        
        # Conversation history context
        if len(self.conversation_history) > 0:
            last_state = self.user_profile.emotional_history[-1] if self.user_profile.emotional_history else None
            
            if last_state:
                # Emotional inertia - emotions tend to persist
                scores[last_state.primary_emotion] = 0.3
                
                # Emotional transitions
                if last_state.primary_emotion == EmotionType.FRUSTRATION:
                    if 'help' in text.lower() or 'solution' in text.lower():
                        scores[EmotionType.ENCOURAGEMENT] = 0.6
                        scores[EmotionType.EMPATHY] = 0.5
        
        # Task context
        if context.get('is_work_related', False):
            scores[EmotionType.FOCUS] = 0.6
            scores[EmotionType.INTEREST] = 0.5
        
        if context.get('is_learning', False):
            scores[EmotionType.CURIOSITY] = 0.7
            scores[EmotionType.INTEREST] = 0.6
        
        return scores
    
    def _ai_emotion_analysis(self, text: str) -> Dict[EmotionType, float]:
        """Use AI model for emotion analysis"""
        scores = {}
        
        try:
            # This would use a real AI model for emotion analysis
            # For now, we'll simulate with a more sophisticated approach
            
            # Create emotion analysis prompt
            prompt = f"""
Analyze the emotional content of this text and provide emotion scores (0-1) for each emotion type:

Text: "{text}"

Provide scores for: joy, sadness, anger, fear, surprise, disgust, interest, confusion
Return as JSON format.
"""
            
            # In real implementation, this would call an AI model
            # For now, return empty scores (will be handled by other methods)
            pass
            
        except Exception as e:
            logger.error(f"AI emotion analysis failed: {e}")
        
        return scores
    
    def _combine_emotion_scores(self, *score_dicts) -> Dict[EmotionType, float]:
        """Combine emotion scores from multiple methods"""
        combined = {}
        
        for score_dict in score_dicts:
            if score_dict:
                for emotion, score in score_dict.items():
                    if emotion not in combined:
                        combined[emotion] = 0
                    combined[emotion] += score
        
        # Normalize and apply weighting
        num_methods = len([d for d in score_dicts if d])
        if num_methods > 0:
            for emotion in combined:
                combined[emotion] = min(1.0, combined[emotion] / num_methods)
        
        return combined
    
    def _extract_triggers(self, text: str, emotion: EmotionType) -> List[str]:
        """Extract emotional triggers from text"""
        triggers = []
        
        # Extract keywords that triggered the emotion
        if emotion in self.emotion_keywords:
            for keyword in self.emotion_keywords[emotion]:
                if keyword in text.lower():
                    triggers.append(keyword)
        
        # Extract phrases
        if '!' in text and emotion in [EmotionType.EXCITEMENT, EmotionType.JOY]:
            triggers.append('exclamation')
        
        if '?' in text and emotion == EmotionType.CURIOSITY:
            triggers.append('question')
        
        return triggers[:5]  # Limit to top 5 triggers
    
    def _simulate_physiological_indicators(self, emotion: EmotionType, intensity: float) -> Dict[str, float]:
        """Simulate physiological indicators based on emotion"""
        indicators = {}
        
        # Base values
        heart_rate = self.physio_baseline['heart_rate']
        breathing_rate = self.physio_baseline['breathing_rate']
        stress_level = self.physio_baseline['stress_level']
        engagement = self.physio_baseline['engagement']
        
        # Emotion-based modifications
        if emotion in [EmotionType.EXCITEMENT, EmotionType.JOY]:
            heart_rate += 20 * intensity
            breathing_rate += 4 * intensity
            engagement += 0.3 * intensity
            
        elif emotion in [EmotionType.ANXIETY, EmotionType.FRUSTRATION]:
            heart_rate += 15 * intensity
            breathing_rate += 6 * intensity
            stress_level += 0.4 * intensity
            
        elif emotion in [EmotionType.CALM, EmotionType.SATISFACTION]:
            heart_rate -= 5 * intensity
            breathing_rate -= 2 * intensity
            stress_level -= 0.3 * intensity
            
        elif emotion in [EmotionType.FOCUS, EmotionType.INTEREST]:
            engagement += 0.5 * intensity
            stress_level += 0.1 * intensity
        
        # Ensure values stay in reasonable ranges
        indicators = {
            'heart_rate': max(50, min(120, heart_rate)),
            'breathing_rate': max(10, min(30, breathing_rate)),
            'stress_level': max(0.0, min(1.0, stress_level)),
            'engagement': max(0.0, min(1.0, engagement))
        }
        
        return indicators
    
    def _calculate_cognitive_load(self, text: str, context: Dict[str, Any]) -> float:
        """Calculate cognitive load based on text complexity and context"""
        load = 0.3  # Base load
        
        # Text complexity factors
        word_count = len(text.split())
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        
        # Complexity indicators
        if avg_words_per_sentence > 15:
            load += 0.2
        if word_count > 50:
            load += 0.1
        if any(word in text.lower() for word in ['complex', 'difficult', 'complicated']):
            load += 0.2
        
        # Context factors
        if context.get('is_technical', False):
            load += 0.2
        if context.get('requires_reasoning', False):
            load += 0.3
        
        return min(1.0, load)
    
    def determine_response_emotion(self, user_emotion: EmotionalState, context: Dict[str, Any]) -> EmotionalState:
        """Determine appropriate emotional response"""
        
        # Response mapping based on user emotion
        response_mapping = {
            EmotionType.JOY: EmotionType.JOY,
            EmotionType.EMPATHY: EmotionType.EMPATHY,
            EmotionType.CURIOSITY: EmotionType.CURIOSITY,
            EmotionType.ENCOURAGEMENT: EmotionType.ENCOURAGEMENT,
            EmotionType.HUMOR: EmotionType.HUMOR,
            EmotionType.CONFUSION: EmotionType.CURIOSITY,
            EmotionType.FRUSTRATION: EmotionType.EMPATHY,
            EmotionType.ANXIETY: EmotionType.CALM,
            EmotionType.SATISFACTION: EmotionType.JOY,
            EmotionType.SURPRISE: EmotionType.CURIOSITY,
            EmotionType.INTEREST: EmotionType.INTEREST,
            EmotionType.CALM: EmotionType.CALM,
            EmotionType.FOCUS: EmotionType.FOCUS,
            EmotionType.WISDOM: EmotionType.WISDOM,
            EmotionType.EXCITEMENT: EmotionType.EXCITEMENT
        }
        
        # Get base response emotion
        primary_response = response_mapping.get(user_emotion.primary_emotion, EmotionType.CALM)
        
        # Adjust intensity based on user's intensity
        response_intensity = min(1.0, user_emotion.intensity * 0.8)
        
        # Add wisdom and empathy for complex emotions
        secondary_response = None
        if user_emotion.intensity > 0.7:
            secondary_response = EmotionType.WISDOM
        
        if user_emotion.primary_emotion in [EmotionType.FRUSTRATION, EmotionType.ANXIETY]:
            secondary_response = EmotionType.EMPATHY
        
        # Calculate confidence based on clarity of user emotion
        response_confidence = user_emotion.confidence * 0.9
        
        # Create response state
        response_state = EmotionalState(
            primary_emotion=primary_response,
            secondary_emotion=secondary_response,
            intensity=response_intensity,
            confidence=response_confidence,
            context=f"response_to_{user_emotion.primary_emotion.value}",
            timestamp=datetime.now(),
            triggers=user_emotion.triggers,
            physiological_indicators=self._simulate_physiological_indicators(primary_response, response_intensity),
            cognitive_load=0.4  # Responses require moderate cognitive load
        )
        
        return response_state
    
    def generate_emotional_response(self, emotional_state: EmotionalState, user_input: str, context: Dict[str, Any]) -> str:
        """Generate emotionally appropriate response using AI"""
        
        # Build response prompt based on emotional state
        emotion_descriptors = {
            EmotionType.JOY: "warm, enthusiastic, and positive",
            EmotionType.EMPATHY: "understanding, supportive, and caring",
            EmotionType.CURIOSITY: "inquisitive, interested, and engaging",
            EmotionType.ENCOURAGEMENT: "motivating, supportive, and uplifting",
            EmotionType.HUMOR: "playful, witty, and light-hearted",
            EmotionType.CONFUSION: "clarifying, patient, and helpful",
            EmotionType.FRUSTRATION: "calm, understanding, and solution-oriented",
            EmotionType.ANXIETY: "reassuring, calm, and grounding",
            EmotionType.SATISFACTION: "affirming, positive, and congratulatory",
            EmotionType.SURPRISE: "engaged, interested, and responsive",
            EmotionType.INTEREST: "attentive, engaged, and responsive",
            EmotionType.CALM: "balanced, thoughtful, and peaceful",
            EmotionType.FOCUS: "clear, direct, and productive",
            EmotionType.WISDOM: "insightful, thoughtful, and deep",
            EmotionType.EXCITEMENT: "energetic, enthusiastic, and engaging"
        }
        
        descriptor = emotion_descriptors.get(emotional_state.primary_emotion, "balanced and appropriate")
        
        response_prompt = f"""
You are an AI assistant with advanced emotional intelligence. Respond to the user with a {descriptor} tone.

User's emotional state: {emotional_state.primary_emotion.value} (intensity: {emotional_state.intensity:.2f})
User said: "{user_input}"

Generate a response that:
1. Matches the emotional tone appropriately
2. Addresses the user's needs and emotions
3. Is helpful and constructive
4. Feels natural and authentic
5. Incorporates your personality traits (empathy: {self.user_profile.personality_traits['empathy_level']}, wisdom: {self.user_profile.personality_traits['wisdom']})

Response:
"""
        
        try:
            # Use AI model to generate response
            from core.ollama_client import OllamaClient
            ollama = OllamaClient(model="qwen2.5:7b-instruct-q4_K_M")
            
            response = ollama.generate(response_prompt, max_tokens=300, temperature=0.7)
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate emotional response: {e}")
            
            # Fallback to template responses
            return self._generate_fallback_response(emotional_state, user_input)
    
    def _generate_fallback_response(self, emotional_state: EmotionalState, user_input: str) -> str:
        """Generate fallback response when AI is unavailable"""
        
        fallback_responses = {
            EmotionType.JOY: [
                "That's wonderful! I'm happy to hear that! 🌟",
                "Fantastic! Your enthusiasm is contagious! ✨",
                "That sounds amazing! I'm excited for you! 🎉"
            ],
            EmotionType.EMPATHY: [
                "I understand how you feel. I'm here to support you. 💙",
                "That sounds challenging. Let me help you through this. 🤗",
                "I can sense this is important to you. I'm listening. 👂"
            ],
            EmotionType.CURIOSITY: [
                "That's fascinating! Tell me more about it. 🤔",
                "Interesting! I'd love to explore that further. 🔍",
                "That sparks my curiosity! What else can you share? ✨"
            ],
            EmotionType.ENCOURAGEMENT: [
                "You've got this! I believe in you! 💪",
                "Keep going! You're doing great! 🌟",
                "Don't give up! You're stronger than you think! 🦾"
            ],
            EmotionType.CALM: [
                "Let's approach this thoughtfully and calmly. 🧘",
                "Take a moment. We'll work through this together. 🌸",
                "Peace and clarity will guide us. 🕊️"
            ]
        }
        
        responses = fallback_responses.get(emotional_state.primary_emotion, [
            "I understand. How can I help you with this? 🤔",
            "Thank you for sharing that with me. 💭",
            "Let's work on this together. 🤝"
        ])
        
        return random.choice(responses)
    
    def update_user_profile(self, interaction_data: Dict[str, Any]):
        """Update user emotional profile based on interactions"""
        
        # Update baseline emotions
        if self.user_profile.emotional_history:
            recent_emotions = self.user_profile.emotional_history[-20:]  # Last 20 interactions
            emotion_counts = {}
            
            for state in recent_emotions:
                emotion = state.primary_emotion.value
                if emotion not in emotion_counts:
                    emotion_counts[emotion] = 0
                emotion_counts[emotion] += 1
            
            # Update baseline with smoothing
            for emotion, count in emotion_counts.items():
                frequency = count / len(recent_emotions)
                current_baseline = self.user_profile.baseline_emotions.get(emotion, 0.5)
                new_baseline = current_baseline * 0.9 + frequency * 0.1  # Smooth adaptation
                self.user_profile.baseline_emotions[emotion] = new_baseline
        
        # Update emotional triggers
        if 'triggers' in interaction_data:
            emotion = interaction_data.get('emotion')
            triggers = interaction_data.get('triggers', [])
            
            if emotion and triggers:
                if emotion not in self.user_profile.emotional_triggers:
                    self.user_profile.emotional_triggers[emotion] = []
                
                for trigger in triggers:
                    if trigger not in self.user_profile.emotional_triggers[emotion]:
                        self.user_profile.emotional_triggers[emotion].append(trigger)
        
        # Update personality traits (very slow adaptation)
        if 'feedback' in interaction_data:
            feedback = interaction_data['feedback']
            if feedback == 'positive':
                self.user_profile.personality_traits['empathy_level'] = min(1.0, 
                    self.user_profile.personality_traits['empathy_level'] + 0.01)
            elif feedback == 'negative':
                self.user_profile.personality_traits['empathy_level'] = max(0.3, 
                    self.user_profile.personality_traits['empathy_level'] - 0.01)
    
    def get_emotional_insights(self) -> Dict[str, Any]:
        """Get insights about user's emotional patterns"""
        
        if not self.user_profile.emotional_history:
            return {"message": "Not enough data for emotional insights"}
        
        # Analyze emotional patterns
        recent_emotions = self.user_profile.emotional_history[-50:]
        
        # Most common emotions
        emotion_counts = {}
        for state in recent_emotions:
            emotion = state.primary_emotion.value
            if emotion not in emotion_counts:
                emotion_counts[emotion] = 0
            emotion_counts[emotion] += 1
        
        most_common = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Emotional intensity trends
        intensities = [state.intensity for state in recent_emotions]
        avg_intensity = sum(intensities) / len(intensities)
        
        # Cognitive load patterns
        cognitive_loads = [state.cognitive_load for state in recent_emotions]
        avg_cognitive_load = sum(cognitive_loads) / len(cognitive_loads)
        
        # Emotional triggers
        common_triggers = {}
        for state in recent_emotions:
            for trigger in state.triggers:
                if trigger not in common_triggers:
                    common_triggers[trigger] = 0
                common_triggers[trigger] += 1
        
        top_triggers = sorted(common_triggers.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "most_common_emotions": most_common,
            "average_intensity": avg_intensity,
            "average_cognitive_load": avg_cognitive_load,
            "top_triggers": top_triggers,
            "personality_traits": self.user_profile.personality_traits,
            "emotional_stability": 1.0 - (max(intensities) - min(intensities)),
            "total_interactions": len(self.user_profile.emotional_history)
        }
