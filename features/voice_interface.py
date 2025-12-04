# backend/features/voice_interface.py
"""
Voice Interface for Ananta
Speech-to-Text and Text-to-Speech with emotion
"""

import os
import tempfile
from typing import Optional, Tuple

class VoiceInterface:
    """
    Handles voice input/output with emotion detection
    """
    
    def __init__(self):
        self.tts_available = self._check_tts()
        self.stt_available = self._check_stt()
        self.voice_personality = {
            "rate": 175,  # Words per minute
            "pitch": 1.0,  # Voice pitch
            "emotion": "friendly"  # Default emotion
        }
    
    def _check_tts(self) -> bool:
        """Check if TTS is available"""
        try:
            import pyttsx3
            return True
        except ImportError:
            return False
    
    def _check_stt(self) -> bool:
        """Check if STT is available"""
        try:
            import speech_recognition as sr
            return True
        except ImportError:
            return False
    
    def speak(self, text: str, emotion: str = "friendly") -> bool:
        """
        Convert text to speech with emotion
        
        Args:
            text: Text to speak
            emotion: Emotion tone (friendly, excited, calm, serious)
        
        Returns:
            Success status
        """
        if not self.tts_available:
            return False
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            # Adjust voice based on emotion
            rate, pitch = self._get_voice_params(emotion)
            engine.setProperty('rate', rate)
            
            # Get available voices
            voices = engine.getProperty('voices')
            
            # Try to use a female voice (more friendly)
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            engine.say(text)
            engine.runAndWait()
            return True
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
    
    def _get_voice_params(self, emotion: str) -> Tuple[int, float]:
        """Get voice parameters based on emotion"""
        params = {
            "friendly": (175, 1.0),
            "excited": (200, 1.2),
            "calm": (150, 0.9),
            "serious": (160, 0.8),
            "encouraging": (180, 1.1)
        }
        return params.get(emotion, (175, 1.0))
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen to user's voice input
        
        Args:
            timeout: Seconds to wait for speech start
            phrase_time_limit: Max seconds for the phrase
        
        Returns:
            Transcribed text or None
        """
        if not self.stt_available:
            return None
        
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎤 Listening...")
                
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen
                audio = recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("🔄 Processing...")
                
                # Transcribe using Google Speech Recognition (free)
                text = recognizer.recognize_google(audio)
                
                print(f"✅ Heard: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("⏰ No speech detected")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except Exception as e:
            print(f"STT Error: {e}")
            return None
    
    def detect_emotion_from_text(self, text: str) -> str:
        """
        Detect emotion from text content
        Simple rule-based detection
        
        Args:
            text: User's message
        
        Returns:
            Detected emotion
        """
        text_lower = text.lower()
        
        # Frustration indicators
        frustration_words = ['stuck', 'confused', 'error', 'bug', 'wrong', 'not working']
        if any(word in text_lower for word in frustration_words):
            return "frustrated"
        
        # Excitement indicators
        excitement_words = ['awesome', 'great', 'amazing', 'love', 'excited', '!']
        if any(word in text_lower for word in excitement_words):
            return "excited"
        
        # Question indicators
        if '?' in text or any(word in text_lower for word in ['how', 'what', 'why', 'when']):
            return "curious"
        
        # Default
        return "neutral"
    
    def get_response_emotion(self, user_emotion: str, context: str) -> str:
        """
        Determine Ananta's response emotion based on user's emotion
        
        Args:
            user_emotion: User's detected emotion
            context: Context of conversation
        
        Returns:
            Ananta's response emotion
        """
        emotion_map = {
            "frustrated": "calm",      # Be calming when user is frustrated
            "excited": "excited",      # Match excitement
            "curious": "friendly",     # Be friendly for questions
            "neutral": "friendly"      # Default friendly
        }
        
        return emotion_map.get(user_emotion, "friendly")
    
    def conversation_mode(self, controller, use_voice_output: bool = True):
        """
        Start continuous voice conversation mode
        
        Args:
            controller: AnantaController instance
            use_voice_output: Whether to speak responses
        """
        print("🎤 Voice conversation mode activated!")
        print("Say 'exit' or 'stop' to end conversation\n")
        
        while True:
            # Listen
            user_input = self.listen(timeout=10)
            
            if user_input is None:
                continue
            
            # Check for exit
            if any(word in user_input.lower() for word in ['exit', 'stop', 'quit', 'goodbye']):
                farewell = "Goodbye! Talk to you later!"
                print(f"Ananta: {farewell}")
                if use_voice_output:
                    self.speak(farewell, emotion="friendly")
                break
            
            # Detect user emotion
            user_emotion = self.detect_emotion_from_text(user_input)
            
            # Get response from Ananta
            response = controller.query(
                user_input,
                use_memory=True,
                reasoning_mode="off"  # Voice mode: quick responses
            )
            
            ananta_text = response.get("response", "I didn't understand that.")
            
            # Determine response emotion
            response_emotion = self.get_response_emotion(user_emotion, ananta_text)
            
            # Display
            print(f"You: {user_input}")
            print(f"Ananta: {ananta_text}\n")
            
            # Speak response
            if use_voice_output:
                self.speak(ananta_text, emotion=response_emotion)
    
    def get_capabilities(self) -> dict:
        """Get current capabilities"""
        return {
            "text_to_speech": self.tts_available,
            "speech_to_text": self.stt_available,
            "emotions": ["friendly", "excited", "calm", "serious", "encouraging"],
            "status": "ready" if (self.tts_available and self.stt_available) else "limited"
        }


# Install instructions
"""
To enable voice features:

pip install pyttsx3 speechrecognition pyaudio

On Windows, PyAudio might need:
pip install pipwin
pipwin install pyaudio

On Linux:
sudo apt-get install portaudio19-dev python3-pyaudio

On Mac:
brew install portaudio
pip install pyaudio
"""