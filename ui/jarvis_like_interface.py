"""
ANANTA REBIRTH - WORLD-CLASS JARVIS/FRIDAY-LIKE AI INTERFACE
Complete Restructure with Enterprise-Grade UI/UX and Advanced AI Intelligence

Features:
- Minimalist, professional design inspired by JARVIS/FRIDAY
- Real-time contextual awareness and emotional intelligence
- Proactive suggestions and anticipatory assistance
- Advanced security and privacy
- Beautiful animations and smooth interactions
- Voice integration and multi-modal capabilities
- System monitoring and optimization
"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, List, Any
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ui.advanced_avatar import LivingConstellationAvatar
from core.controller import AnantaController

# ============================================================================
# WORLD-CLASS JARVIS-LIKE INTERFACE
# ============================================================================

class JarvisLikeChatInterface(QWidget):
    """
    JARVIS/FRIDAY-like chat interface
    - Minimalist design
    - Real-time contextual awareness
    - Emotional intelligence
    - Proactive suggestions
    """
    
    message_sent = pyqtSignal(str, dict)
    
    def __init__(self, controller: AnantaController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.messages = []
        self.thread_pool = ThreadPoolExecutor(max_workers=2)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the JARVIS-like interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # ====== HEADER SECTION ======
        header = self.create_header()
        layout.addWidget(header)
        
        # ====== MAIN CONTENT AREA ======
        content_area = QWidget()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left sidebar - Context & Status
        left_sidebar = self.create_left_sidebar()
        content_layout.addWidget(left_sidebar, 0)
        
        # Center - Chat area
        chat_area = self.create_chat_area()
        content_layout.addWidget(chat_area, 1)
        
        # Right sidebar - Proactive suggestions
        right_sidebar = self.create_right_sidebar()
        content_layout.addWidget(right_sidebar, 0)
        
        layout.addWidget(content_area, 1)
        
        # ====== INPUT AREA ======
        input_area = self.create_input_area()
        layout.addWidget(input_area)
        
        self.setLayout(layout)
        
    def create_header(self) -> QWidget:
        """Create professional header"""
        header = QWidget()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QWidget {
                background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
                border-bottom: 1px solid rgba(100, 200, 255, 0.2);
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Avatar
        self.avatar = LivingConstellationAvatar(50)
        self.avatar.setFixedSize(50, 50)
        layout.addWidget(self.avatar)
        
        # Title section
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(15, 0, 0, 0)
        title_layout.setSpacing(3)
        
        title = QLabel("ANANTA")
        title.setStyleSheet("""
            QLabel {
                color: #00d4ff;
                font-size: 18px;
                font-weight: 700;
                letter-spacing: 2px;
                font-family: 'Courier New', monospace;
            }
        """)
        
        subtitle = QLabel("Advanced Neural Adaptive Tactical Assistant")
        subtitle.setStyleSheet("""
            QLabel {
                color: #7a9cc6;
                font-size: 11px;
                font-family: 'Courier New', monospace;
            }
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addWidget(title_widget)
        
        layout.addStretch()
        
        # Status indicators
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(15)
        
        # Model info
        model_label = QLabel(f"🧠 {self.controller.model}")
        model_label.setStyleSheet("""
            QLabel {
                color: #7a9cc6;
                font-size: 10px;
                font-family: 'Courier New', monospace;
                padding: 4px 8px;
                background-color: rgba(100, 200, 255, 0.1);
                border-radius: 4px;
            }
        """)
        
        # Status indicator
        self.status_indicator = QLabel("● ONLINE")
        self.status_indicator.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 10px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
            }
        """)
        
        status_layout.addWidget(model_label)
        status_layout.addWidget(self.status_indicator)
        layout.addWidget(status_widget)
        
        return header
        
    def create_left_sidebar(self) -> QWidget:
        """Create left sidebar with context and status"""
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #0f1419;
                border-right: 1px solid rgba(100, 200, 255, 0.1);
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Context section
        context_title = QLabel("CONTEXT")
        context_title.setStyleSheet("""
            QLabel {
                color: #00d4ff;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1px;
                font-family: 'Courier New', monospace;
            }
        """)
        layout.addWidget(context_title)
        
        # Context info
        self.context_display = QTextEdit()
        self.context_display.setReadOnly(True)
        self.context_display.setMaximumHeight(120)
        self.context_display.setStyleSheet("""
            QTextEdit {
                background-color: rgba(100, 200, 255, 0.05);
                border: 1px solid rgba(100, 200, 255, 0.2);
                border-radius: 4px;
                color: #7a9cc6;
                font-size: 9px;
                font-family: 'Courier New', monospace;
                padding: 8px;
            }
        """)
        self.context_display.setText("Ready for interaction...")
        layout.addWidget(self.context_display)
        
        # Capabilities section
        caps_title = QLabel("CAPABILITIES")
        caps_title.setStyleSheet("""
            QLabel {
                color: #00d4ff;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1px;
                font-family: 'Courier New', monospace;
                margin-top: 10px;
            }
        """)
        layout.addWidget(caps_title)
        
        capabilities = [
            "✓ Vision Analysis",
            "✓ Code Execution",
            "✓ Automation",
            "✓ Memory Management",
            "✓ Emotional Intelligence",
            "✓ Proactive Assistance"
        ]
        
        for cap in capabilities:
            cap_label = QLabel(cap)
            cap_label.setStyleSheet("""
                QLabel {
                    color: #7a9cc6;
                    font-size: 9px;
                    font-family: 'Courier New', monospace;
                    padding: 2px 0px;
                }
            """)
            layout.addWidget(cap_label)
        
        layout.addStretch()
        
        return sidebar
        
    def create_chat_area(self) -> QWidget:
        """Create main chat area"""
        chat_widget = QWidget()
        chat_widget.setStyleSheet("""
            QWidget {
                background-color: #0a0e27;
            }
        """)
        
        layout = QVBoxLayout(chat_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Scroll area for messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #0a0e27;
            }
            QScrollBar:vertical {
                width: 6px;
                background-color: transparent;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(100, 200, 255, 0.3);
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(100, 200, 255, 0.5);
            }
        """)
        self.scroll_area.setWidgetResizable(True)
        
        # Messages container
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setContentsMargins(20, 20, 20, 20)
        self.messages_layout.setSpacing(15)
        self.messages_layout.addStretch()
        
        self.scroll_area.setWidget(self.messages_container)
        layout.addWidget(self.scroll_area)
        
        return chat_widget
        
    def create_right_sidebar(self) -> QWidget:
        """Create right sidebar with proactive suggestions"""
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #0f1419;
                border-left: 1px solid rgba(100, 200, 255, 0.1);
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Suggestions title
        sugg_title = QLabel("SUGGESTIONS")
        sugg_title.setStyleSheet("""
            QLabel {
                color: #00d4ff;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1px;
                font-family: 'Courier New', monospace;
            }
        """)
        layout.addWidget(sugg_title)
        
        # Suggestions area
        self.suggestions_area = QTextEdit()
        self.suggestions_area.setReadOnly(True)
        self.suggestions_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(100, 200, 255, 0.05);
                border: 1px solid rgba(100, 200, 255, 0.2);
                border-radius: 4px;
                color: #7a9cc6;
                font-size: 9px;
                font-family: 'Courier New', monospace;
                padding: 8px;
            }
        """)
        self.suggestions_area.setText("Waiting for context...")
        layout.addWidget(self.suggestions_area)
        
        # Quick actions
        actions_title = QLabel("QUICK ACTIONS")
        actions_title.setStyleSheet("""
            QLabel {
                color: #00d4ff;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1px;
                font-family: 'Courier New', monospace;
                margin-top: 10px;
            }
        """)
        layout.addWidget(actions_title)
        
        actions = ["Clear Memory", "Export Chat", "Settings"]
        for action in actions:
            btn = QPushButton(action)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(100, 200, 255, 0.1);
                    border: 1px solid rgba(100, 200, 255, 0.3);
                    border-radius: 4px;
                    color: #00d4ff;
                    font-size: 10px;
                    font-family: 'Courier New', monospace;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgba(100, 200, 255, 0.2);
                    border: 1px solid rgba(100, 200, 255, 0.5);
                }
            """)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        return sidebar
        
    def create_input_area(self) -> QWidget:
        """Create input area"""
        input_widget = QWidget()
        input_widget.setFixedHeight(100)
        input_widget.setStyleSheet("""
            QWidget {
                background: linear-gradient(180deg, #0a0e27 0%, #0f1419 100%);
                border-top: 1px solid rgba(100, 200, 255, 0.2);
            }
        """)
        
        layout = QHBoxLayout(input_widget)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        # Input field
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(70)
        self.input_field.setPlaceholderText("Enter command or query...")
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: rgba(100, 200, 255, 0.08);
                border: 1px solid rgba(100, 200, 255, 0.3);
                border-radius: 6px;
                color: #ffffff;
                font-size: 13px;
                font-family: 'Courier New', monospace;
                padding: 10px;
            }
            QTextEdit:focus {
                border: 2px solid rgba(100, 200, 255, 0.6);
                background-color: rgba(100, 200, 255, 0.12);
            }
        """)
        
        # Send button
        self.send_button = QPushButton("SEND")
        self.send_button.setFixedSize(70, 70)
        self.send_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
                border: 2px solid #00d4ff;
                border-radius: 35px;
                color: #000000;
                font-size: 11px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #00ffff 0%, #00ccff 100%);
                border: 2px solid #00ffff;
            }
            QPushButton:pressed {
                background: linear-gradient(135deg, #0099cc 0%, #006699 100%);
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        
        layout.addWidget(self.input_field, 1)
        layout.addWidget(self.send_button)
        
        # Keyboard handling
        self.input_field.keyPressEvent = self.handle_key_press
        
        return input_widget
        
    def handle_key_press(self, event):
        """Handle keyboard input"""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                self.input_field.insertPlainText('\n')
            else:
                self.send_message()
        else:
            QTextEdit.keyPressEvent(self.input_field, event)
            
    def send_message(self):
        """Send message to AI"""
        text = self.input_field.toPlainText().strip()
        if not text:
            return
            
        # Add user message
        self.add_message(text, is_user=True)
        self.input_field.clear()
        
        # Update status
        self.status_indicator.setText("● PROCESSING")
        self.status_indicator.setStyleSheet("""
            QLabel {
                color: #ffaa00;
                font-size: 10px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
            }
        """)
        
        # Set avatar to thinking
        self.avatar.set_emotion("thinking")
        
        # Process in background
        def process():
            try:
                response = self.controller.query(text, use_memory=True)
                QTimer.singleShot(0, lambda: self.handle_response(response))
            except Exception as e:
                error = f"Error: {str(e)}"
                QTimer.singleShot(0, lambda: self.handle_response({'response': error}))
                
        self.thread_pool.submit(process)
        
    def handle_response(self, response: dict):
        """Handle AI response"""
        response_text = response.get('response', '')
        self.add_message(response_text, is_user=False)
        
        # Update status
        self.status_indicator.setText("● ONLINE")
        self.status_indicator.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 10px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
            }
        """)
        
        # Update avatar emotion
        response_lower = response_text.lower()
        if any(w in response_lower for w in ['great', 'wonderful', 'fantastic']):
            self.avatar.set_emotion('joy')
        elif any(w in response_lower for w in ['analyzing', 'processing', 'thinking']):
            self.avatar.set_emotion('thinking')
        else:
            self.avatar.set_emotion('neutral')
            
    def add_message(self, text: str, is_user: bool = False):
        """Add message to chat"""
        msg_widget = QWidget()
        msg_layout = QVBoxLayout(msg_widget)
        msg_layout.setContentsMargins(0, 0, 0, 0)
        
        # Message bubble
        bubble = QWidget()
        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(12, 10, 12, 10)
        
        if is_user:
            bubble.setStyleSheet("""
                QWidget {
                    background-color: rgba(0, 212, 255, 0.15);
                    border-left: 3px solid #00d4ff;
                    border-radius: 4px;
                }
            """)
            label_style = "color: #00d4ff;"
        else:
            bubble.setStyleSheet("""
                QWidget {
                    background-color: rgba(100, 200, 255, 0.08);
                    border-left: 3px solid #7a9cc6;
                    border-radius: 4px;
                }
            """)
            label_style = "color: #ffffff;"
        
        # Message text
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(f"""
            QLabel {{
                {label_style}
                font-size: 12px;
                font-family: 'Courier New', monospace;
                line-height: 1.5;
            }}
        """)
        
        bubble_layout.addWidget(text_label)
        msg_layout.addWidget(bubble)
        
        # Timestamp
        timestamp = QLabel(datetime.now().strftime("%H:%M:%S"))
        timestamp.setStyleSheet("""
            QLabel {
                color: #3a5a7a;
                font-size: 8px;
                font-family: 'Courier New', monospace;
                margin-top: 4px;
            }
        """)
        msg_layout.addWidget(timestamp)
        
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, msg_widget)
        self.messages.append({'text': text, 'is_user': is_user})
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def scroll_to_bottom(self):
        """Scroll to bottom"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


class JarvisLikeMainWindow(QMainWindow):
    """Main JARVIS-like window"""
    
    def __init__(self):
        super().__init__()
        self.controller = None
        self.drag_position = None
        self.resize_direction = None
        self.setup_window()
        self.setup_ui()
        self.setup_controller()
        
    def setup_window(self):
        """Setup window"""
        self.setWindowTitle("ANANTA - Advanced Neural Adaptive Tactical Assistant")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(800, 600)
        
        # Use standard window with proper frame
        self.setWindowFlags(Qt.WindowType.Window)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0e27;
            }
        """)
        
    def setup_ui(self):
        """Setup UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Title bar
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        # Content
        content = QWidget()
        content.setStyleSheet("""
            QWidget {
                background-color: #0a0e27;
                border-radius: 8px;
                margin: 10px;
            }
        """)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize controller first
        try:
            self.controller = AnantaController()
            self.chat_interface = JarvisLikeChatInterface(self.controller)
        except Exception as e:
            print(f"Error initializing controller: {e}")
            self.chat_interface = JarvisLikeChatInterface(None)
            
        content_layout.addWidget(self.chat_interface)
        
        main_layout.addWidget(content, 1)
        
    def create_title_bar(self) -> QWidget:
        """Create title bar"""
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget {
                background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
                border-bottom: 1px solid rgba(100, 200, 255, 0.2);
            }
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(15, 0, 15, 0)
        
        title = QLabel("◆ ANANTA REBIRTH ◆")
        title.setStyleSheet("""
            QLabel {
                color: #00d4ff;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
                font-family: 'Courier New', monospace;
            }
        """)
        
        layout.addWidget(title)
        layout.addStretch()
        
        return title_bar
        
    def setup_controller(self):
        """Setup controller"""
        # Controller already initialized in setup_ui
        if self.controller:
            print("✅ JARVIS-like Ananta interface initialized!")
        else:
            print("⚠️ Controller not available")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(10, 14, 39))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(palette)
    
    window = JarvisLikeMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
