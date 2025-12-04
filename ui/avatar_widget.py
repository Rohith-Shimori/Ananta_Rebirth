"""
PyQt Avatar Widget
Displays Ananta's 2D avatar in PyQt window with real-time emotion updates
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pathlib import Path
import logging

from ui.ananta_avatar import AnantaAvatar
from ui.holographic_ui import HolographicUI

logger = logging.getLogger(__name__)


class AvatarWidget(QWidget):
    """
    PyQt widget displaying Ananta's animated 2D avatar
    
    Features:
    - Real-time emotion switching
    - Speaking animation
    - Holographic styling
    - Smooth animations
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create avatar and UI systems
        self.avatar = AnantaAvatar()
        self.holographic_ui = HolographicUI()
        
        # Current state
        self.current_emotion = "neutral"
        self.is_speaking = False
        self.animation_frame = 0
        
        # Setup UI
        self.init_ui()
        
        # Animation timer for smooth updates
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(100)  # Update every 100ms
        
        logger.info("✅ Avatar Widget initialized")
    
    def init_ui(self):
        """Initialize UI elements"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Avatar display (using QWebEngineView for HTML/SVG)
        self.web_view = QWebEngineView()
        self.web_view.setMinimumSize(350, 450)
        self.web_view.setMaximumSize(350, 450)
        self.web_view.setStyleSheet("background-color: #0A0E1A; border: 2px solid #00F0FF;")
        
        # Update avatar display
        self.update_avatar_display()
        
        layout.addWidget(self.web_view, alignment=Qt.AlignCenter)
        
        # Status label
        self.status_label = QLabel(f"Emotion: {self.current_emotion.capitalize()}")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #00F0FF;
                font-size: 14px;
                font-weight: bold;
                text-shadow: 0 0 10px #00F0FF;
                padding: 5px;
            }
        """)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #0A0E1A;")
    
    def update_avatar_display(self):
        """Update the avatar display with current emotion and speaking state"""
        try:
            # Get SVG from avatar system
            svg = self.avatar.get_svg_avatar(self.current_emotion, self.is_speaking)
            
            # Wrap in full HTML document with holographic styling
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    
                    body {{
                        background: linear-gradient(135deg, #0A0E1A 0%, #0F1A2E 100%);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        font-family: 'Courier New', monospace;
                        overflow: hidden;
                    }}
                    
                    .avatar-container {{
                        position: relative;
                        width: 300px;
                        height: 400px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }}
                    
                    .avatar-box {{
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(135deg, rgba(0,240,255,0.1) 0%, rgba(189,0,255,0.1) 100%);
                        border: 2px solid #00F0FF;
                        border-radius: 20px;
                        box-shadow: 0 0 30px rgba(0,240,255,0.3), 
                                    inset 0 0 30px rgba(189,0,255,0.1),
                                    0 0 60px rgba(189,0,255,0.2);
                        position: relative;
                        overflow: hidden;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }}
                    
                    /* Scan lines effect */
                    .avatar-box::before {{
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
                        z-index: 1;
                    }}
                    
                    /* Glow effect */
                    .avatar-box::after {{
                        content: '';
                        position: absolute;
                        top: -50%;
                        left: -50%;
                        width: 200%;
                        height: 200%;
                        background: radial-gradient(circle, rgba(0,240,255,0.1) 0%, transparent 70%);
                        animation: glow-pulse 3s ease-in-out infinite;
                        z-index: 0;
                    }}
                    
                    svg {{
                        position: relative;
                        z-index: 2;
                        filter: drop-shadow(0 0 20px rgba(0,240,255,0.3));
                    }}
                    
                    @keyframes scan-lines {{
                        0% {{ transform: translateY(0); }}
                        100% {{ transform: translateY(10px); }}
                    }}
                    
                    @keyframes glow-pulse {{
                        0%, 100% {{ 
                            filter: drop-shadow(0 0 10px #00F0FF) drop-shadow(0 0 20px #BD00FF);
                        }}
                        50% {{ 
                            filter: drop-shadow(0 0 20px #00F0FF) drop-shadow(0 0 30px #BD00FF);
                        }}
                    }}
                    
                    @keyframes breathing {{
                        0%, 100% {{ transform: scale(1); }}
                        50% {{ transform: scale(1.02); }}
                    }}
                    
                    @keyframes blink {{
                        0%, 90%, 100% {{ opacity: 1; }}
                        95% {{ opacity: 0; }}
                    }}
                    
                    .avatar-body {{ animation: breathing 3s ease-in-out infinite; }}
                    .avatar-eyes {{ animation: blink 4s ease-in-out infinite; }}
                </style>
            </head>
            <body>
                <div class="avatar-container">
                    <div class="avatar-box">
                        {svg}
                    </div>
                </div>
            </body>
            </html>
            """
            
            self.web_view.setHtml(full_html)
            
        except Exception as e:
            logger.error(f"❌ Error updating avatar display: {e}")
            self.web_view.setHtml(f"<html><body style='background: #0A0E1A; color: #FF006E;'><p>Error: {e}</p></body></html>")
    
    def set_emotion(self, emotion: str):
        """
        Set avatar emotion
        
        Args:
            emotion: One of 'neutral', 'happy', 'thinking', 'concerned', 'excited'
        """
        if emotion not in ["neutral", "happy", "thinking", "concerned", "excited"]:
            logger.warning(f"⚠️  Unknown emotion: {emotion}. Using neutral.")
            emotion = "neutral"
        
        self.current_emotion = emotion
        self.avatar.set_emotion(emotion)
        self.update_avatar_display()
        self.status_label.setText(f"Emotion: {emotion.capitalize()}")
        logger.info(f"😊 Avatar emotion set to: {emotion}")
    
    def set_speaking(self, speaking: bool):
        """
        Set speaking state (shows mouth animation)
        
        Args:
            speaking: True if speaking, False otherwise
        """
        self.is_speaking = speaking
        self.update_avatar_display()
        logger.info(f"🎤 Avatar speaking: {speaking}")
    
    def update_animation(self):
        """Update animation frame - called by timer"""
        self.animation_frame += 1
        # Could be used for more complex animations in future
    
    def get_current_emotion(self) -> str:
        """Get current emotion"""
        return self.current_emotion
    
    def get_speaking_state(self) -> bool:
        """Get current speaking state"""
        return self.is_speaking


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    app = QApplication(sys.argv)
    
    # Create test window
    window = QMainWindow()
    window.setWindowTitle("Ananta Avatar - Test")
    window.setStyleSheet("background-color: #0A0E1A;")
    window.setGeometry(100, 100, 800, 600)
    
    # Central widget
    central_widget = QWidget()
    layout = QVBoxLayout()
    
    # Add avatar
    avatar_widget = AvatarWidget()
    layout.addWidget(avatar_widget, alignment=Qt.AlignCenter)
    
    # Add control buttons
    button_layout = QHBoxLayout()
    
    emotions = ["neutral", "happy", "thinking", "concerned", "excited"]
    for emotion in emotions:
        btn = QPushButton(emotion.capitalize())
        btn.clicked.connect(lambda checked, e=emotion: avatar_widget.set_emotion(e))
        btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #00F0FF, stop:1 #BD00FF);
                color: #0A0E1A;
                border: 1px solid #00F0FF;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #BD00FF, stop:1 #00F0FF);
                box-shadow: 0 0 20px #00F0FF;
            }
            QPushButton:pressed {
                padding: 12px 18px;
            }
        """)
        button_layout.addWidget(btn)
    
    # Speaking button
    speak_btn = QPushButton("🎤 Speaking")
    speak_btn.setCheckable(True)
    speak_btn.clicked.connect(lambda checked: avatar_widget.set_speaking(checked))
    speak_btn.setStyleSheet("""
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #FFD700, stop:1 #FF8C00);
            color: #0A0E1A;
            border: 1px solid #FFD700;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 12px;
            min-width: 100px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #FF8C00, stop:1 #FFD700);
        }
        QPushButton:checked {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #00FF88, stop:1 #00DD66);
        }
    """)
    button_layout.addWidget(speak_btn)
    
    layout.addLayout(button_layout)
    
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    window.show()
    
    print("\n" + "="*60)
    print("🎨 ANANTA AVATAR WIDGET - TEST MODE")
    print("="*60)
    print("\n✅ Avatar widget loaded successfully!")
    print("\n📝 Controls:")
    print("  • Click emotion buttons to change avatar emotion")
    print("  • Click 'Speaking' button to toggle mouth animation")
    print("\n🎯 Emotions available:")
    for emotion in emotions:
        print(f"  • {emotion.capitalize()}")
    print("\n" + "="*60 + "\n")
    
    sys.exit(app.exec_())
