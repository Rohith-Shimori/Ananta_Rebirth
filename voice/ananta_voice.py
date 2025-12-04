"""
Ananta's Voice System - XTTS-v2 Based
Realistic voice cloning with emotion support
Cost: FREE (Open-source)
"""

import numpy as np
import torch
from pathlib import Path
from typing import Optional, Dict, Tuple
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class VoiceConfig:
    """Voice configuration"""
    speed: float = 1.0
    pitch: float = 1.0
    emotion: str = "neutral"
    style: str = "conversational"
    language: str = "en"


class AnantaVoice:
    """
    Ananta's unique voice identity using XTTS-v2
    - Voice cloning from reference sample
    - Emotion and style transfer
    - Multi-language support
    - Real-time synthesis
    """
    
    def __init__(self, device: Optional[str] = None, skip_license: bool = True):
        """
        Initialize Ananta's voice system
        
        Args:
            device: "cuda" or "cpu" (auto-detected if None)
            skip_license: Skip license confirmation (for non-commercial use)
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"🎤 Initializing Ananta Voice on {self.device}")
        
        # Voice reference path (will be created/used) - MUST be before TTS init
        self.voice_dir = Path(__file__).parent / "voice_samples"
        self.voice_dir.mkdir(parents=True, exist_ok=True)
        self.voice_reference = self.voice_dir / "ananta_voice_reference.wav"
        
        # Try to import TTS
        try:
            from TTS.api import TTS
            self.TTS = TTS
        except ImportError:
            logger.error("❌ TTS not installed. Install with: pip install TTS")
            raise
        
        # Initialize XTTS-v2 model
        try:
            import os
            import warnings
            
            # Suppress deprecation warning
            warnings.filterwarnings('ignore', category=UserWarning)
            
            # Set environment variable to skip license confirmation
            if skip_license:
                os.environ['TTS_HOME'] = str(self.voice_dir)
            
            # Initialize with new API (avoiding deprecated gpu parameter)
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", 
                          gpu=(self.device == "cuda"))
            
            # Move to device using new API
            self.tts = self.tts.to(self.device)
            
            logger.info("✅ XTTS-v2 model loaded successfully")
        except KeyboardInterrupt:
            logger.warning("⚠️  License confirmation cancelled by user")
            logger.info("💡 To accept the license automatically, use: AnantaVoice(skip_license=True)")
            raise
        except Exception as e:
            logger.error(f"❌ Error loading XTTS-v2: {e}")
            logger.info("💡 Note: First run downloads the model (~1.5GB)")
            logger.info("   You may need to accept the license terms")
            logger.info("   Or use: AnantaVoice(skip_license=True)")
            raise
        
        # Voice characteristics
        self.voice_config = VoiceConfig()
        
        # Statistics
        self.stats = {
            "total_generations": 0,
            "total_duration": 0.0,
            "avg_generation_time": 0.0
        }
        
        # Create default voice reference if doesn't exist
        self._ensure_voice_reference()
    
    def _ensure_voice_reference(self):
        """Ensure voice reference exists"""
        if not self.voice_reference.exists():
            logger.warning(f"⚠️  Voice reference not found at {self.voice_reference}")
            logger.info("📝 To use custom voice:")
            logger.info(f"   1. Record 6-10 seconds of audio")
            logger.info(f"   2. Save as: {self.voice_reference}")
            logger.info(f"   3. Supported formats: WAV, MP3, OGG")
            logger.info("\n   For now, using default voice...")
    
    def speak(self, text: str, emotion: str = "neutral", 
              output_path: Optional[str] = None) -> np.ndarray:
        """
        Generate speech with Ananta's voice
        
        Args:
            text: Text to speak
            emotion: Emotion to convey (neutral, happy, excited, concerned, empathetic, confident)
            output_path: Optional path to save audio file
        
        Returns:
            Audio as numpy array
        """
        import time
        start_time = time.time()
        
        try:
            # Add emotional markers to text
            emotional_text = self._add_emotional_markers(text, emotion)
            
            # Generate speech
            if self.voice_reference.exists():
                # Use custom voice reference
                wav = self.tts.tts(
                    text=emotional_text,
                    speaker_wav=str(self.voice_reference),
                    language=self.voice_config.language
                )
            else:
                # Use default speaker
                wav = self.tts.tts(
                    text=emotional_text,
                    language=self.voice_config.language
                )
            
            # Save if path provided
            if output_path:
                self.tts.tts_to_file(
                    text=emotional_text,
                    speaker_wav=str(self.voice_reference) if self.voice_reference.exists() else None,
                    language=self.voice_config.language,
                    file_path=output_path
                )
                logger.info(f"💾 Audio saved to {output_path}")
            
            # Update statistics
            generation_time = time.time() - start_time
            self.stats["total_generations"] += 1
            self.stats["total_duration"] += generation_time
            self.stats["avg_generation_time"] = (
                self.stats["total_duration"] / self.stats["total_generations"]
            )
            
            logger.info(f"✅ Generated speech in {generation_time:.2f}s")
            
            return wav
        
        except Exception as e:
            logger.error(f"❌ Error generating speech: {e}")
            raise
    
    def speak_with_emotion(self, text: str, emotion: str) -> np.ndarray:
        """
        Speak with specific emotional tone
        
        Emotions:
        - neutral: Normal, informative tone
        - happy: Bright, cheerful tone
        - excited: Energetic, enthusiastic tone
        - concerned: Gentle, caring tone
        - empathetic: Warm, understanding tone
        - confident: Assured, capable tone
        """
        return self.speak(text, emotion=emotion)
    
    def _add_emotional_markers(self, text: str, emotion: str) -> str:
        """Add prosody markers for emotion"""
        markers = {
            "happy": "*with warm enthusiasm*",
            "excited": "*energetically*",
            "concerned": "*with gentle concern*",
            "empathetic": "*warmly and supportively*",
            "confident": "*with quiet confidence*",
            "neutral": ""
        }
        
        marker = markers.get(emotion, "")
        if marker:
            return f"{marker} {text}"
        return text
    
    def set_voice_config(self, config: VoiceConfig):
        """Update voice configuration"""
        self.voice_config = config
        logger.info(f"🎵 Voice config updated: {config}")
    
    def get_voice_stats(self) -> Dict:
        """Get voice generation statistics"""
        return {
            "total_generations": self.stats["total_generations"],
            "total_duration": self.stats["total_duration"],
            "avg_generation_time": self.stats["avg_generation_time"],
            "device": self.device,
            "voice_reference": str(self.voice_reference),
            "voice_exists": self.voice_reference.exists()
        }
    
    def print_voice_info(self):
        """Print voice system information"""
        stats = self.get_voice_stats()
        
        print(f"\n{'='*70}")
        print(f"🎤 ANANTA VOICE SYSTEM - INFORMATION")
        print(f"{'='*70}")
        print(f"Device: {stats['device']}")
        print(f"Model: XTTS-v2 (Multilingual)")
        print(f"Voice Reference: {stats['voice_reference']}")
        print(f"Voice Exists: {'✅ Yes' if stats['voice_exists'] else '❌ No'}")
        print(f"\nStatistics:")
        print(f"  Total Generations: {stats['total_generations']}")
        print(f"  Total Duration: {stats['total_duration']:.2f}s")
        print(f"  Avg Generation Time: {stats['avg_generation_time']:.2f}s")
        print(f"{'='*70}\n")


# Example usage and testing
if __name__ == "__main__":
    import time
    
    print("🚀 ANANTA VOICE SYSTEM - TEST\n")
    
    # Initialize voice
    voice = AnantaVoice()
    
    # Test different emotions
    test_phrases = [
        ("Hello! I'm Ananta, your AI partner.", "happy"),
        ("Let me think about that for a moment.", "neutral"),
        ("That's an amazing idea! Let's do it!", "excited"),
        ("I understand this can be frustrating. Let's work through it together.", "empathetic"),
        ("I've got this. Here's what I found.", "confident"),
    ]
    
    print("🎤 Testing different emotions:\n")
    
    for text, emotion in test_phrases:
        print(f"📝 {emotion.upper()}: {text}")
        try:
            output_file = f"ananta_{emotion}.wav"
            audio = voice.speak_with_emotion(text, emotion)
            print(f"   ✅ Generated {len(audio)} samples\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
    
    # Print stats
    voice.print_voice_info()
