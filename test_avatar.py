"""
Test the Living Constellation Morphing Entity Avatar
"""

import sys
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from ui.advanced_avatar import LivingConstellationAvatar, EmotionalState

class AvatarTestWindow(QWidget):
    """Test window for the advanced avatar"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌌 Living Constellation Avatar Test")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #02040A;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🌌 Living Constellation")
        title.setStyleSheet("color: #00F5FF; font-size: 16px; font-weight: bold; text-align: center;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Morphing Entity Avatar")
        subtitle.setStyleSheet("color: #B0C3FF; font-size: 12px; text-align: center;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Avatar
        avatar_container = QWidget()
        avatar_container.setFixedSize(200, 200)
        avatar_container.setStyleSheet("background-color: rgba(2, 4, 10, 0.8); border-radius: 10px;")
        
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.avatar = LivingConstellationAvatar(150)
        avatar_layout.addWidget(self.avatar)
        
        layout.addWidget(avatar_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Emotion controls
        emotions_layout = QVBoxLayout()
        emotions_title = QLabel("🎭 Emotional States:")
        emotions_title.setStyleSheet("color: #00F5FF; font-size: 14px; font-weight: bold;")
        emotions_layout.addWidget(emotions_title)
        
        # Emotion buttons
        emotions = [
            ("😊 Joy", "joy"),
            ("🤔 Thinking", "thinking"), 
            ("⚡ Power", "power"),
            ("❤️ Empathetic", "empathetic"),
            ("🔮 Quantum", "quantum"),
            ("😌 Neutral", "neutral")
        ]
        
        for display_name, emotion_name in emotions:
            btn = QPushButton(display_name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(28, 35, 51, 0.8);
                    border: 1px solid rgba(138, 216, 255, 0.3);
                    border-radius: 20px;
                    color: white;
                    padding: 8px 16px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 245, 255, 0.2);
                    border: 1px solid rgba(0, 245, 255, 0.5);
                }
            """)
            btn.clicked.connect(lambda checked, e=emotion_name: self.avatar.set_emotion(e))
            emotions_layout.addWidget(btn)
            
        layout.addLayout(emotions_layout)
        
        # Auto-cycle checkbox
        self.auto_cycle = QCheckBox("🔄 Auto-cycle emotions")
        self.auto_cycle.setStyleSheet("color: #B0C3FF; font-size: 12px;")
        self.auto_cycle.stateChanged.connect(self.toggle_auto_cycle)
        layout.addWidget(self.auto_cycle)
        
        # Auto-cycle timer
        self.cycle_timer = QTimer()
        self.cycle_timer.timeout.connect(self.cycle_emotion)
        self.current_emotion_index = 0
        self.emotion_list = ["joy", "thinking", "power", "empathetic", "quantum", "neutral"]
        
    def toggle_auto_cycle(self, state):
        """Toggle auto-cycling of emotions"""
        if state == 2:  # Checked
            self.cycle_timer.start(3000)  # Change every 3 seconds
        else:
            self.cycle_timer.stop()
            
    def cycle_emotion(self):
        """Cycle to next emotion"""
        emotion = self.emotion_list[self.current_emotion_index]
        self.avatar.set_emotion(emotion)
        self.current_emotion_index = (self.current_emotion_index + 1) % len(self.emotion_list)

def main():
    app = QApplication(sys.argv)
    
    # Set dark style
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(2, 4, 10))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(palette)
    
    window = AvatarTestWindow()
    window.show()
    
    # Start with joy emotion
    window.avatar.set_emotion("joy")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    print("🌌 Testing Living Constellation Morphing Entity Avatar...")
    print("🎭 Features:")
    print("  ✅ 60+ animated star nodes")
    print("  ✅ Dynamic data streams")
    print("  ✅ 6 emotional states")
    print("  ✅ Smooth morphing transitions")
    print("  ✅ Mouse interaction")
    print("  ✅ GPU-accelerated rendering")
    print("🚀 Launching test window...")
    main()
