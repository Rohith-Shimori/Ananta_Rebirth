"""
Ananta's 2D Avatar System
Animated avatar with emotional expressions
Cost: FREE (Custom SVG/Canvas based)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class EmotionState(Enum):
    """Avatar emotional states"""
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    HAPPY = "happy"
    CONCERNED = "concerned"
    EXCITED = "excited"


@dataclass
class AvatarConfig:
    """Avatar configuration"""
    style: str = "modern_professional"
    age: str = "25-30"
    hair: str = "long_flowing"
    eyes: str = "intelligent_warm"
    clothing: str = "futuristic_elegant"
    color_scheme: list = None
    
    def __post_init__(self):
        if self.color_scheme is None:
            self.color_scheme = ["#00F0FF", "#BD00FF", "#FFD700"]


class AnantaAvatar:
    """
    Ananta's 2D animated avatar
    - Emotional expressions
    - Idle animations
    - Lip-sync ready
    - Holographic styling
    """
    
    def __init__(self, config: Optional[AvatarConfig] = None):
        """Initialize avatar"""
        self.config = config or AvatarConfig()
        self.current_state = EmotionState.IDLE
        self.current_emotion = "neutral"
        self.animation_frame = 0
        
        logger.info("👁️  Ananta Avatar initialized")
    
    def get_svg_avatar(self, emotion: str = "neutral", 
                       speaking: bool = False) -> str:
        """
        Generate SVG representation of avatar
        
        Args:
            emotion: Current emotion (neutral, happy, thinking, concerned, excited)
            speaking: Whether avatar is speaking
        
        Returns:
            SVG string for rendering
        """
        colors = self.config.color_scheme
        primary = colors[0]  # Cyan
        secondary = colors[1]  # Purple
        
        # Base avatar SVG
        svg = f"""
        <svg viewBox="0 0 200 300" xmlns="http://www.w3.org/2000/svg">
            <!-- Define styles -->
            <defs>
                <style>
                    @keyframes breathing {{
                        0%, 100% {{ transform: scale(1); }}
                        50% {{ transform: scale(1.02); }}
                    }}
                    @keyframes blink {{
                        0%, 90%, 100% {{ opacity: 1; }}
                        95% {{ opacity: 0; }}
                    }}
                    @keyframes glow {{
                        0%, 100% {{ filter: drop-shadow(0 0 10px {primary}); }}
                        50% {{ filter: drop-shadow(0 0 20px {primary}); }}
                    }}
                    .avatar-body {{ animation: breathing 3s ease-in-out infinite; }}
                    .avatar-eyes {{ animation: blink 4s ease-in-out infinite; }}
                    .avatar-glow {{ animation: glow 2s ease-in-out infinite; }}
                </style>
                <radialGradient id="face-gradient">
                    <stop offset="0%" style="stop-color:{primary};stop-opacity:0.3" />
                    <stop offset="100%" style="stop-color:{secondary};stop-opacity:0.1" />
                </radialGradient>
            </defs>
            
            <!-- Glow effect -->
            <circle cx="100" cy="120" r="90" class="avatar-glow" 
                    fill="url(#face-gradient)" opacity="0.5"/>
            
            <!-- Head -->
            <g class="avatar-body">
                <!-- Face -->
                <circle cx="100" cy="100" r="50" fill="{primary}" opacity="0.2" stroke="{primary}" stroke-width="2"/>
                
                <!-- Hair -->
                <path d="M 50 70 Q 50 30 100 25 Q 150 30 150 70" 
                      fill="{secondary}" opacity="0.4" stroke="{primary}" stroke-width="1.5"/>
                
                <!-- Eyes container -->
                <g class="avatar-eyes">
                    {self._get_eyes_svg(emotion, primary, secondary)}
                </g>
                
                <!-- Mouth -->
                {self._get_mouth_svg(emotion, speaking, primary)}
                
                <!-- Particles (for thinking/excited) -->
                {self._get_particles_svg(emotion, primary, secondary)}
            </g>
            
            <!-- Body/Clothing -->
            <g class="avatar-body">
                <rect x="70" y="150" width="60" height="80" rx="10" 
                      fill="{secondary}" opacity="0.3" stroke="{primary}" stroke-width="1.5"/>
                
                <!-- Accent lines (futuristic) -->
                <line x1="70" y1="170" x2="130" y2="170" stroke="{primary}" stroke-width="1" opacity="0.5"/>
                <line x1="70" y1="190" x2="130" y2="190" stroke="{primary}" stroke-width="1" opacity="0.5"/>
            </g>
        </svg>
        """
        
        return svg
    
    def _get_eyes_svg(self, emotion: str, primary: str, secondary: str) -> str:
        """Generate eyes based on emotion"""
        if emotion == "happy":
            # Happy eyes - closed smile
            return f"""
            <circle cx="80" cy="90" r="8" fill="{primary}" opacity="0.6"/>
            <path d="M 75 92 Q 80 95 85 92" stroke="{primary}" stroke-width="1.5" fill="none"/>
            
            <circle cx="120" cy="90" r="8" fill="{primary}" opacity="0.6"/>
            <path d="M 115 92 Q 120 95 125 92" stroke="{primary}" stroke-width="1.5" fill="none"/>
            """
        elif emotion == "thinking":
            # Thinking eyes - looking up
            return f"""
            <circle cx="80" cy="85" r="8" fill="{primary}" opacity="0.6"/>
            <circle cx="78" cy="83" r="4" fill="{secondary}" opacity="0.8"/>
            
            <circle cx="120" cy="85" r="8" fill="{primary}" opacity="0.6"/>
            <circle cx="118" cy="83" r="4" fill="{secondary}" opacity="0.8"/>
            """
        elif emotion == "concerned":
            # Concerned eyes - worried
            return f"""
            <circle cx="80" cy="90" r="8" fill="{primary}" opacity="0.6"/>
            <circle cx="78" cy="88" r="4" fill="{secondary}" opacity="0.8"/>
            <path d="M 75 85 Q 80 83 85 85" stroke="{primary}" stroke-width="1" fill="none"/>
            
            <circle cx="120" cy="90" r="8" fill="{primary}" opacity="0.6"/>
            <circle cx="118" cy="88" r="4" fill="{secondary}" opacity="0.8"/>
            <path d="M 115 85 Q 120 83 125 85" stroke="{primary}" stroke-width="1" fill="none"/>
            """
        elif emotion == "excited":
            # Excited eyes - wide open
            return f"""
            <circle cx="80" cy="90" r="10" fill="{primary}" opacity="0.6"/>
            <circle cx="78" cy="90" r="5" fill="{secondary}" opacity="0.9"/>
            <circle cx="76" cy="88" r="2" fill="white" opacity="0.8"/>
            
            <circle cx="120" cy="90" r="10" fill="{primary}" opacity="0.6"/>
            <circle cx="118" cy="90" r="5" fill="{secondary}" opacity="0.9"/>
            <circle cx="116" cy="88" r="2" fill="white" opacity="0.8"/>
            """
        else:
            # Neutral eyes
            return f"""
            <circle cx="80" cy="90" r="8" fill="{primary}" opacity="0.6"/>
            <circle cx="78" cy="90" r="4" fill="{secondary}" opacity="0.8"/>
            
            <circle cx="120" cy="90" r="8" fill="{primary}" opacity="0.6"/>
            <circle cx="118" cy="90" r="4" fill="{secondary}" opacity="0.8"/>
            """
    
    def _get_mouth_svg(self, emotion: str, speaking: bool, primary: str) -> str:
        """Generate mouth based on emotion and speaking state"""
        if speaking:
            # Speaking - open mouth
            return f"""
            <ellipse cx="100" cy="115" rx="8" ry="10" fill="{primary}" opacity="0.4"/>
            <path d="M 92 115 Q 100 125 108 115" stroke="{primary}" stroke-width="1.5" fill="none"/>
            """
        elif emotion == "happy":
            # Happy - big smile
            return f"""
            <path d="M 90 110 Q 100 120 110 110" stroke="{primary}" stroke-width="2" fill="none" stroke-linecap="round"/>
            """
        elif emotion == "concerned":
            # Concerned - slight frown
            return f"""
            <path d="M 90 115 Q 100 110 110 115" stroke="{primary}" stroke-width="1.5" fill="none" stroke-linecap="round"/>
            """
        elif emotion == "excited":
            # Excited - wide smile
            return f"""
            <path d="M 85 110 Q 100 125 115 110" stroke="{primary}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            """
        else:
            # Neutral - straight line
            return f"""
            <line x1="90" y1="115" x2="110" y2="115" stroke="{primary}" stroke-width="1.5" stroke-linecap="round"/>
            """
    
    def _get_particles_svg(self, emotion: str, primary: str, secondary: str) -> str:
        """Generate particle effects for certain emotions"""
        if emotion == "thinking":
            return f"""
            <circle cx="140" cy="60" r="2" fill="{secondary}" opacity="0.6"/>
            <circle cx="150" cy="70" r="1.5" fill="{primary}" opacity="0.5"/>
            <circle cx="145" cy="75" r="1" fill="{secondary}" opacity="0.4"/>
            """
        elif emotion == "excited":
            return f"""
            <circle cx="60" cy="50" r="2" fill="{primary}" opacity="0.7"/>
            <circle cx="140" cy="50" r="2" fill="{primary}" opacity="0.7"/>
            <circle cx="50" cy="100" r="1.5" fill="{secondary}" opacity="0.6"/>
            <circle cx="150" cy="100" r="1.5" fill="{secondary}" opacity="0.6"/>
            """
        else:
            return ""
    
    def get_html_avatar(self, emotion: str = "neutral", 
                       speaking: bool = False) -> str:
        """
        Generate HTML/CSS representation of avatar
        
        Returns:
            HTML string with embedded CSS
        """
        svg = self.get_svg_avatar(emotion, speaking)
        
        html = f"""
        <div class="ananta-avatar-container">
            <style>
                .ananta-avatar-container {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 300px;
                    height: 400px;
                    background: linear-gradient(135deg, rgba(0,240,255,0.1) 0%, rgba(189,0,255,0.1) 100%);
                    border: 2px solid #00F0FF;
                    border-radius: 20px;
                    box-shadow: 0 0 30px rgba(0,240,255,0.3), inset 0 0 30px rgba(189,0,255,0.1);
                    position: relative;
                    overflow: hidden;
                }}
                
                .ananta-avatar-container::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: repeating-linear-gradient(
                        0deg,
                        rgba(0,240,255,0.03) 0px,
                        rgba(0,240,255,0.03) 1px,
                        transparent 1px,
                        transparent 2px
                    );
                    pointer-events: none;
                    animation: scan-lines 8s linear infinite;
                }}
                
                @keyframes scan-lines {{
                    0% {{ transform: translateY(0); }}
                    100% {{ transform: translateY(10px); }}
                }}
                
                .ananta-avatar-svg {{
                    width: 200px;
                    height: 300px;
                    z-index: 1;
                }}
            </style>
            
            <svg class="ananta-avatar-svg" viewBox="0 0 200 300" xmlns="http://www.w3.org/2000/svg">
                {svg}
            </svg>
        </div>
        """
        
        return html
    
    def set_emotion(self, emotion: str):
        """Set avatar emotion"""
        try:
            self.current_emotion = emotion
            self.current_state = EmotionState(emotion)
            logger.info(f"😊 Avatar emotion set to: {emotion}")
        except ValueError:
            logger.warning(f"⚠️  Unknown emotion: {emotion}")
    
    def get_animation_frame(self, frame_number: int = 0) -> str:
        """Get animation frame for given frame number"""
        self.animation_frame = frame_number
        return self.get_svg_avatar(self.current_emotion)
    
    def print_avatar_info(self):
        """Print avatar information"""
        print(f"\n{'='*70}")
        print(f"👁️  ANANTA AVATAR - INFORMATION")
        print(f"{'='*70}")
        print(f"Style: {self.config.style}")
        print(f"Age: {self.config.age}")
        print(f"Hair: {self.config.hair}")
        print(f"Eyes: {self.config.eyes}")
        print(f"Clothing: {self.config.clothing}")
        print(f"Color Scheme: {self.config.color_scheme}")
        print(f"\nCurrent State:")
        print(f"  Emotion: {self.current_emotion}")
        print(f"  Animation Frame: {self.animation_frame}")
        print(f"{'='*70}\n")


# Example usage
if __name__ == "__main__":
    print("🚀 ANANTA AVATAR SYSTEM - TEST\n")
    
    # Create avatar
    avatar = AnantaAvatar()
    
    # Test different emotions
    emotions = ["neutral", "happy", "thinking", "concerned", "excited"]
    
    print("🎨 Testing different emotions:\n")
    
    for emotion in emotions:
        avatar.set_emotion(emotion)
        svg = avatar.get_svg_avatar(emotion)
        print(f"✅ {emotion.upper()}: Generated SVG ({len(svg)} chars)")
    
    # Print info
    avatar.print_avatar_info()
    
    # Generate HTML
    html = avatar.get_html_avatar("happy")
    print(f"✅ Generated HTML avatar ({len(html)} chars)")
