"""
Holographic UI Effects - JARVIS-Like Interface
CSS/HTML based holographic styling
Cost: FREE (Pure CSS/HTML)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class HolographicTheme:
    """Holographic color theme"""
    primary: str = "#00F0FF"      # Cyan
    secondary: str = "#BD00FF"    # Purple
    accent: str = "#FFD700"       # Gold
    text: str = "#E0F7FF"         # Light cyan
    background: str = "#0A0E1A"   # Dark blue
    danger: str = "#FF006E"       # Pink/Red
    success: str = "#00FF88"      # Green


class HolographicUI:
    """
    JARVIS-like holographic interface effects
    - Glow effects
    - Particle systems
    - Scan lines
    - Smooth transitions
    """
    
    def __init__(self, theme: Optional[HolographicTheme] = None):
        """Initialize holographic UI"""
        self.theme = theme or HolographicTheme()
        self.effects_enabled = True
        
        logger.info("🎨 Holographic UI initialized")
    
    def get_base_css(self) -> str:
        """Get base CSS for holographic theme"""
        return f"""
        :root {{
            --primary: {self.theme.primary};
            --secondary: {self.theme.secondary};
            --accent: {self.theme.accent};
            --text: {self.theme.text};
            --background: {self.theme.background};
            --danger: {self.theme.danger};
            --success: {self.theme.success};
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: linear-gradient(135deg, {self.theme.background} 0%, #0F1A2E 100%);
            color: {self.theme.text};
            font-family: 'Courier New', monospace;
            overflow: hidden;
        }}
        
        /* Holographic text effect */
        .holographic-text {{
            position: relative;
            display: inline-block;
            font-weight: bold;
            letter-spacing: 2px;
        }}
        
        .holographic-text .text-glow {{
            text-shadow: 
                0 0 10px {self.theme.primary},
                0 0 20px {self.theme.secondary},
                0 0 30px {self.theme.primary},
                0 0 40px {self.theme.secondary};
            animation: text-flicker 3s ease-in-out infinite;
        }}
        
        @keyframes text-flicker {{
            0%, 100% {{
                text-shadow: 
                    0 0 10px {self.theme.primary},
                    0 0 20px {self.theme.secondary},
                    0 0 30px {self.theme.primary};
            }}
            50% {{
                text-shadow: 
                    0 0 20px {self.theme.primary},
                    0 0 30px {self.theme.secondary},
                    0 0 40px {self.theme.primary},
                    0 0 50px {self.theme.secondary};
            }}
        }}
        
        /* Scan lines effect */
        .scan-lines {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 240, 255, 0.03) 0px,
                rgba(0, 240, 255, 0.03) 1px,
                transparent 1px,
                transparent 2px
            );
            pointer-events: none;
            animation: scan-lines-move 8s linear infinite;
        }}
        
        @keyframes scan-lines-move {{
            0% {{ transform: translateY(0); }}
            100% {{ transform: translateY(10px); }}
        }}
        
        /* Glow effect */
        .glow {{
            box-shadow: 
                0 0 10px {self.theme.primary},
                0 0 20px {self.theme.secondary},
                inset 0 0 10px rgba(0, 240, 255, 0.1);
        }}
        
        /* Breathing animation */
        @keyframes breathing {{
            0%, 100% {{ opacity: 0.7; }}
            50% {{ opacity: 1; }}
        }}
        
        .breathing {{
            animation: breathing 2s ease-in-out infinite;
        }}
        
        /* Particle effect */
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) translateX(0px); }}
            25% {{ transform: translateY(-20px) translateX(10px); }}
            50% {{ transform: translateY(-40px) translateX(-10px); }}
            75% {{ transform: translateY(-20px) translateX(10px); }}
        }}
        
        .particle {{
            position: absolute;
            width: 4px;
            height: 4px;
            background: {self.theme.primary};
            border-radius: 50%;
            animation: float 4s ease-in-out infinite;
            opacity: 0.6;
        }}
        
        /* Holographic container */
        .holographic-container {{
            position: relative;
            border: 2px solid {self.theme.primary};
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.05) 0%, rgba(189, 0, 255, 0.05) 100%);
            box-shadow: 
                0 0 20px {self.theme.primary},
                inset 0 0 20px rgba(0, 240, 255, 0.1),
                0 0 40px {self.theme.secondary};
            border-radius: 10px;
            overflow: hidden;
        }}
        
        .holographic-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 240, 255, 0.03) 0px,
                rgba(0, 240, 255, 0.03) 1px,
                transparent 1px,
                transparent 2px
            );
            pointer-events: none;
            animation: scan-lines-move 8s linear infinite;
        }}
        
        /* Buttons */
        .holographic-button {{
            background: linear-gradient(135deg, {self.theme.primary} 0%, {self.theme.secondary} 100%);
            border: 1px solid {self.theme.primary};
            color: {self.theme.background};
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px {self.theme.primary};
        }}
        
        .holographic-button:hover {{
            box-shadow: 0 0 20px {self.theme.primary}, 0 0 30px {self.theme.secondary};
            transform: scale(1.05);
        }}
        
        .holographic-button:active {{
            transform: scale(0.95);
        }}
        
        /* Status indicator */
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s ease-in-out infinite;
        }}
        
        .status-indicator.active {{
            background: {self.theme.success};
            box-shadow: 0 0 10px {self.theme.success};
        }}
        
        .status-indicator.inactive {{
            background: {self.theme.danger};
            box-shadow: 0 0 10px {self.theme.danger};
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        /* Energy ring */
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .energy-ring {{
            position: absolute;
            border: 2px solid {self.theme.primary};
            border-radius: 50%;
            animation: spin 3s linear infinite;
            opacity: 0.5;
        }}
        """
    
    def render_holographic_text(self, text: str) -> str:
        """Render text with holographic effects"""
        return f"""
        <div class="holographic-text">
            <span class="text-glow">{text}</span>
            <div class="scan-lines"></div>
        </div>
        """
    
    def render_avatar_container(self) -> str:
        """Create container for 3D avatar with effects"""
        return f"""
        <div class="holographic-container" style="width: 300px; height: 400px; position: relative;">
            <div class="avatar-glow" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);"></div>
            <canvas id="avatar-canvas" class="avatar-3d" style="width: 100%; height: 100%;"></canvas>
            <div class="energy-ring" style="top: 10%; left: 10%; width: 80%; height: 80%;"></div>
            <div class="energy-ring" style="top: 20%; left: 20%; width: 60%; height: 60%; animation-direction: reverse;"></div>
        </div>
        """
    
    def render_status_panel(self, stats: Dict) -> str:
        """Render system status panel"""
        return f"""
        <div class="holographic-container" style="padding: 20px; margin: 10px;">
            <h3 class="holographic-text">
                <span class="text-glow">SYSTEM STATUS</span>
            </h3>
            <div style="margin-top: 15px;">
                <div style="margin: 10px 0;">
                    <span class="status-indicator active"></span>
                    <span>Model: {stats.get('model', 'Sentinel')}</span>
                </div>
                <div style="margin: 10px 0;">
                    <span class="status-indicator active"></span>
                    <span>VRAM: {stats.get('vram', '4.2GB')} / 6GB</span>
                </div>
                <div style="margin: 10px 0;">
                    <span class="status-indicator active"></span>
                    <span>Response: {stats.get('response_speed', '42')} tok/s</span>
                </div>
                <div style="margin: 10px 0;">
                    <span class="status-indicator active"></span>
                    <span>Context: {stats.get('context', '4.5K')} tokens</span>
                </div>
            </div>
        </div>
        """
    
    def render_chat_interface(self) -> str:
        """Render main chat interface"""
        return f"""
        <div style="width: 100%; height: 100vh; background: {self.theme.background}; display: flex; flex-direction: column;">
            <!-- Header -->
            <div class="holographic-container" style="padding: 20px; margin: 10px; flex: 0 0 auto;">
                <h1 class="holographic-text">
                    <span class="text-glow">⚡ ANANTA</span>
                </h1>
                <p style="margin-top: 10px; opacity: 0.8;">Your AI Partner</p>
            </div>
            
            <!-- Main content -->
            <div style="flex: 1; display: flex; gap: 10px; margin: 10px; overflow: hidden;">
                <!-- Avatar -->
                <div style="flex: 0 0 350px;">
                    {self.render_avatar_container()}
                </div>
                
                <!-- Chat area -->
                <div class="holographic-container" style="flex: 1; display: flex; flex-direction: column; padding: 20px;">
                    <div id="chat-messages" style="flex: 1; overflow-y: auto; margin-bottom: 20px;">
                        <div style="text-align: center; opacity: 0.7;">
                            <p>Ready to assist...</p>
                        </div>
                    </div>
                    
                    <!-- Input -->
                    <div style="display: flex; gap: 10px;">
                        <input type="text" id="user-input" placeholder="What can I help with?" 
                               style="flex: 1; padding: 10px; background: rgba(0, 240, 255, 0.1); 
                                      border: 1px solid {self.theme.primary}; color: {self.theme.text};
                                      border-radius: 5px; font-family: 'Courier New', monospace;">
                        <button class="holographic-button">Send</button>
                    </div>
                </div>
            </div>
            
            <!-- Footer with status -->
            <div class="holographic-container" style="padding: 15px; margin: 10px; flex: 0 0 auto;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="status-indicator active"></span>
                    <span>System Online • Ready for interaction</span>
                    <span class="breathing" style="font-size: 20px;">◆</span>
                </div>
            </div>
        </div>
        """
    
    def render_waveform_visualization(self, height: int = 100) -> str:
        """Render audio waveform visualization"""
        return f"""
        <div class="holographic-container" style="padding: 20px; height: {height}px; display: flex; align-items: center; justify-content: center;">
            <svg width="100%" height="100%" style="filter: drop-shadow(0 0 5px {self.theme.primary});">
                <defs>
                    <linearGradient id="waveform-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:{self.theme.primary};stop-opacity:1" />
                        <stop offset="50%" style="stop-color:{self.theme.secondary};stop-opacity:1" />
                        <stop offset="100%" style="stop-color:{self.theme.primary};stop-opacity:1" />
                    </linearGradient>
                </defs>
                <polyline points="0,50 10,30 20,40 30,20 40,35 50,15 60,40 70,25 80,45 90,10 100,50" 
                          fill="none" stroke="url(#waveform-gradient)" stroke-width="2" stroke-linecap="round"/>
            </svg>
        </div>
        """
    
    def get_theme_info(self) -> Dict:
        """Get theme information"""
        return {
            "primary": self.theme.primary,
            "secondary": self.theme.secondary,
            "accent": self.theme.accent,
            "text": self.theme.text,
            "background": self.theme.background,
            "danger": self.theme.danger,
            "success": self.theme.success
        }
    
    def print_ui_info(self):
        """Print UI information"""
        theme = self.get_theme_info()
        
        print(f"\n{'='*70}")
        print(f"🎨 HOLOGRAPHIC UI - INFORMATION")
        print(f"{'='*70}")
        print(f"Theme Colors:")
        for color_name, color_value in theme.items():
            print(f"  {color_name:12} {color_value}")
        print(f"\nEffects Enabled: {self.effects_enabled}")
        print(f"{'='*70}\n")


# Example usage
if __name__ == "__main__":
    print("🚀 HOLOGRAPHIC UI - TEST\n")
    
    # Create UI
    ui = HolographicUI()
    
    # Generate components
    print("✅ Generated holographic text")
    text = ui.render_holographic_text("ANANTA")
    
    print("✅ Generated avatar container")
    avatar = ui.render_avatar_container()
    
    print("✅ Generated status panel")
    status = ui.render_status_panel({"model": "Sentinel", "vram": "4.2GB"})
    
    print("✅ Generated chat interface")
    chat = ui.render_chat_interface()
    
    print("✅ Generated waveform visualization")
    waveform = ui.render_waveform_visualization()
    
    # Print info
    ui.print_ui_info()
