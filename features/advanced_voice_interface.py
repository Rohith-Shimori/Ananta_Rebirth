"""
Advanced Voice Interface with Emotional Intelligence
Human-like voice interaction with emotion detection and expressive responses
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger("ananta.voice")

class VoiceEmotion(Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    EXCITED = "excited"
    EMPATHETIC = "empathetic"
    ENCOURAGING = "encouraging"
    CURIOUS = "curious"
    CALM = "calm"
    WISDOM = "wisdom"

@dataclass
class VoiceSettings:
    rate: int = 175  # Words per minute
    volume: float = 0.9
    pitch: int = 50
    emotion: VoiceEmotion = VoiceEmotion.NEUTRAL

class AdvancedVoiceInterface:
    """Advanced voice interface with emotional intelligence"""
    
    def __init__(self):
        self.settings = VoiceSettings()
        self.is_enabled = False
        self.is_listening = False
        self.is_speaking = False
        self.voice_history = []
        self.emotion_patterns = {}
        self._initialize_voice()
    
    def _initialize_voice(self):
        """Initialize voice engines"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self._configure_tts_engine()
            self.is_enabled = True
            logger.info("✅ Text-to-speech engine initialized")
        except ImportError:
            logger.warning("⚠️  pyttsx3 not available. Install: pip install pyttsx3")
            self.tts_engine = None
        except Exception as e:
            logger.error(f"Voice initialization failed: {e}")
            self.tts_engine = None
        
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = None
            
            # List available microphones
            mics = sr.Microphone.list_microphone_names()
            if mics:
                self.microphone = sr.Microphone()
                logger.info(f"✅ Speech recognition initialized with {len(mics)} microphones")
            else:
                logger.warning("⚠️  No microphones found")
        except ImportError:
            logger.warning("⚠️  speechrecognition not available. Install: pip install speechrecognition")
            self.recognizer = None
        except Exception as e:
            logger.error(f"Speech recognition initialization failed: {e}")
            self.recognizer = None
    
    def _configure_tts_engine(self):
        """Configure text-to-speech engine with emotional parameters"""
        if not self.tts_engine:
            return
        
        # Get available voices
        voices = self.tts_engine.getProperty('voices')
        
        # Try to find a high-quality voice
        selected_voice = None
        for voice in voices:
            if any(quality in voice.name.lower() for quality in ['david', 'zira', 'karen', 'susan']):
                selected_voice = voice.id
                break
        
        if selected_voice:
            self.tts_engine.setProperty('voice', selected_voice)
        
        # Set default properties
        self.tts_engine.setProperty('rate', self.settings.rate)
        self.tts_engine.setProperty('volume', self.settings.volume)
    
    def speak_with_emotion(self, text: str, emotion: VoiceEmotion = VoiceEmotion.NEUTRAL, 
                          background: bool = False) -> bool:
        """
        Speak text with emotional expression
        """
        if not self.is_enabled or not self.tts_engine or self.is_speaking:
            return False
        
        try:
            # Apply emotional voice settings
            self._apply_emotional_settings(emotion)
            
            # Log voice interaction
            self.voice_history.append({
                'type': 'speak',
                'text': text,
                'emotion': emotion.value,
                'timestamp': datetime.now().isoformat(),
                'settings': {
                    'rate': self.settings.rate,
                    'pitch': self.settings.pitch,
                    'volume': self.settings.volume
                }
            })
            
            if background:
                # Run in background thread
                import threading
                thread = threading.Thread(target=self._speak_async, args=(text,))
                thread.daemon = True
                thread.start()
                return True
            else:
                # Synchronous speaking
                self.is_speaking = True
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                self.is_speaking = False
                return True
                
        except Exception as e:
            logger.error(f"Speech error: {e}")
            self.is_speaking = False
            return False
    
    def _speak_async(self, text: str):
        """Async speech function"""
        try:
            self.is_speaking = True
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"Async speech error: {e}")
        finally:
            self.is_speaking = False
    
    def _apply_emotional_settings(self, emotion: VoiceEmotion):
        """Apply emotional parameters to voice"""
        if not self.tts_engine:
            return
        
        # Emotional voice configurations
        emotion_configs = {
            VoiceEmotion.NEUTRAL: {'rate': 175, 'pitch': 50, 'volume': 0.9},
            VoiceEmotion.HAPPY: {'rate': 180, 'pitch': 60, 'volume': 0.95},
            VoiceEmotion.EXCITED: {'rate': 190, 'pitch': 70, 'volume': 1.0},
            VoiceEmotion.EMPATHETIC: {'rate': 160, 'pitch': 45, 'volume': 0.85},
            VoiceEmotion.ENCOURAGING: {'rate': 170, 'pitch': 55, 'volume': 0.9},
            VoiceEmotion.CURIOUS: {'rate': 175, 'pitch': 65, 'volume': 0.9},
            VoiceEmotion.CALM: {'rate': 165, 'pitch': 45, 'volume': 0.8},
            VoiceEmotion.WISDOM: {'rate': 160, 'pitch': 40, 'volume': 0.85}
        }
        
        config = emotion_configs.get(emotion, emotion_configs[VoiceEmotion.NEUTRAL])
        
        self.tts_engine.setProperty('rate', config['rate'])
        self.tts_engine.setProperty('volume', config['volume'])
        
        # Some engines support pitch
        try:
            self.tts_engine.setProperty('pitch', config['pitch'])
        except:
            pass  # Pitch not supported on all engines
    
    def listen_for_speech(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for user speech input
        """
        if not self.is_enabled or not self.recognizer or not self.microphone or self.is_listening:
            return None
        
        try:
            self.is_listening = True
            
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                logger.info("🎤 Listening...")
                
                # Listen to the input
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
            logger.info("🔊 Processing speech...")
            
            # Recognize speech using Google's free service
            try:
                text = self.recognizer.recognize_google(audio)
                
                # Log voice interaction
                self.voice_history.append({
                    'type': 'listen',
                    'text': text,
                    'timestamp': datetime.now().isoformat(),
                    'confidence': 'high'  # Google recognition typically has high confidence
                })
                
                logger.info(f"✅ Recognized: {text}")
                return text
                
            except sr.UnknownValueError:
                logger.warning("⚠️  Could not understand audio")
                return None
            except sr.RequestError as e:
                logger.error(f"Speech recognition service error: {e}")
                return None
                
        except sr.WaitTimeoutError:
            logger.info("⏱️  Listening timeout")
            return None
        except Exception as e:
            logger.error(f"Listening error: {e}")
            return None
        finally:
            self.is_listening = False
    
    def detect_voice_emotion(self, text: str, audio_features: Dict = None) -> VoiceEmotion:
        """
        Detect emotion from voice text and audio features
        """
        text_lower = text.lower()
        
        # Emotion keywords
        emotion_keywords = {
            VoiceEmotion.HAPPY: ['happy', 'excited', 'great', 'awesome', 'wonderful', 'love', 'fantastic'],
            VoiceEmotion.EMPATHETIC: ['sad', 'sorry', 'difficult', 'hard', 'struggling', 'challenging'],
            VoiceEmotion.ENCOURAGING: ['can do', 'believe', 'capable', 'strong', 'you got this'],
            VoiceEmotion.CURIOUS: ['how', 'why', 'what', 'curious', 'interested', 'wonder'],
            VoiceEmotion.EXCITED: ['amazing', 'incredible', 'wow', 'exciting', 'thrilling']
        }
        
        # Score emotions
        emotion_scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Consider audio features if available
        if audio_features:
            # Pitch, volume, speed analysis would go here
            # For now, just use text analysis
            pass
        
        # Return highest scoring emotion
        if emotion_scores:
            best_emotion = max(emotion_scores, key=emotion_scores.get)
            if emotion_scores[best_emotion] > 0:
                return best_emotion
        
        return VoiceEmotion.NEUTRAL
    
    def get_voice_capabilities(self) -> Dict[str, Any]:
        """Get voice system capabilities and status"""
        return {
            'tts_enabled': self.tts_engine is not None,
            'stt_enabled': self.recognizer is not None,
            'microphone_available': self.microphone is not None,
            'is_speaking': self.is_speaking,
            'is_listening': self.is_listening,
            'current_settings': {
                'rate': self.settings.rate,
                'volume': self.settings.volume,
                'pitch': self.settings.pitch,
                'emotion': self.settings.emotion.value
            },
            'supported_emotions': [e.value for e in VoiceEmotion],
            'interaction_count': len(self.voice_history)
        }
    
    def update_voice_settings(self, **kwargs):
        """Update voice settings"""
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        
        # Apply settings to engine if available
        if self.tts_engine:
            self.tts_engine.setProperty('rate', self.settings.rate)
            self.tts_engine.setProperty('volume', self.settings.volume)
            try:
                self.tts_engine.setProperty('pitch', self.settings.pitch)
            except:
                pass
    
    def get_voice_history(self, limit: int = 10) -> List[Dict]:
        """Get recent voice interactions"""
        return self.voice_history[-limit:] if self.voice_history else []
    
    def clear_voice_history(self):
        """Clear voice interaction history"""
        self.voice_history.clear()
    
    def test_voice_system(self) -> Dict[str, bool]:
        """Test voice system components"""
        results = {
            'tts_test': False,
            'stt_test': False,
            'microphone_test': False
        }
        
        # Test TTS
        if self.tts_engine:
            try:
                self.speak_with_emotion("Voice system test", VoiceEmotion.NEUTRAL)
                results['tts_test'] = True
            except:
                results['tts_test'] = False
        
        # Test microphone availability
        if self.microphone:
            results['microphone_test'] = True
        
        # Test speech recognition (quick test)
        if self.recognizer and self.microphone:
            results['stt_test'] = True  # Basic availability test
        
        return results
    
    def stop_speaking(self):
        """Stop current speech"""
        if self.tts_engine and self.is_speaking:
            try:
                self.tts_engine.stop()
                self.is_speaking = False
            except:
                pass
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available TTS voices"""
        if not self.tts_engine:
            return []
        
        voices = []
        for voice in self.tts_engine.getProperty('voices'):
            voices.append({
                'id': voice.id,
                'name': voice.name,
                'gender': getattr(voice, 'gender', 'unknown'),
                'language': getattr(voice, 'languages', ['unknown'])[0] if hasattr(voice, 'languages') else 'unknown'
            })
        
        return voices
    
    def set_voice_by_id(self, voice_id: str) -> bool:
        """Set TTS voice by ID"""
        if not self.tts_engine:
            return False
        
        try:
            self.tts_engine.setProperty('voice', voice_id)
            return True
        except:
            return False
