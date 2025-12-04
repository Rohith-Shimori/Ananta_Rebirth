"""
Ananta Rebirth - Professional AI Interface
Inspired by ChatGPT, Claude, and TypingMind - Clean, Professional, Minimalist
"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, List, Any
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ui.enhanced_message_bubble import MessageBubble
from ui.advanced_avatar import LivingConstellationAvatar
from core.controller import AnantaController

class ProfessionalChatPanel(QWidget):
    """Professional chat interface inspired by ChatGPT/Claude"""
    
    message_sent = pyqtSignal(str, dict)
    
    def __init__(self, controller: AnantaController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.messages = []
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header - Clean and Minimal
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QWidget {
                background-color: #171717;
                border-bottom: 1px solid #2d2d2d;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # Avatar with clean styling
        self.avatar = LivingConstellationAvatar(40)
        self.avatar.setFixedSize(40, 40)
        header_layout.addWidget(self.avatar)
        
        # Title area
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(12, 0, 0, 0)
        title_layout.setSpacing(2)
        
        title = QLabel("Ananta")
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
        """)
        
        subtitle = QLabel("Advanced AI Assistant")
        subtitle.setStyleSheet("""
            QLabel {
                color: #a0a0a0;
                font-size: 12px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        header_layout.addWidget(title_widget)
        header_layout.addStretch()
        
        # Model indicator
        model_label = QLabel(f"🧠 {self.controller.model}")
        model_label.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                color: #a0a0a0;
                padding: 6px 12px;
                border-radius: 12px;
                font-size: 11px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
        """)
        header_layout.addWidget(model_label)
        
        layout.addWidget(header)
        
        # Messages area - Clean scrollable area
        self.messages_container = QWidget()
        self.messages_container.setStyleSheet("""
            QWidget {
                background-color: #171717;
            }
        """)
        
        messages_layout = QVBoxLayout(self.messages_container)
        messages_layout.setContentsMargins(0, 0, 0, 0)
        messages_layout.setSpacing(0)
        
        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.messages_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #171717;
            }
            QScrollBar:vertical {
                width: 8px;
                background-color: transparent;
            }
            QScrollBar::handle:vertical {
                background-color: #3a3a3a;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #4a4a4a;
            }
        """)
        
        layout.addWidget(self.scroll_area, 1)
        
        # Welcome message
        welcome_msg = QWidget()
        welcome_layout = QVBoxLayout(welcome_msg)
        welcome_layout.setContentsMargins(20, 40, 20, 40)
        
        welcome_title = QLabel("Welcome to Ananta")
        welcome_title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: 600;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin-bottom: 8px;
            }
        """)
        welcome_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        welcome_subtitle = QLabel("How can I help you today?")
        welcome_subtitle.setStyleSheet("""
            QLabel {
                color: #a0a0a0;
                font-size: 14px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
        """)
        welcome_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_subtitle)
        
        # Suggested prompts
        suggestions_layout = QHBoxLayout()
        suggestions_layout.setContentsMargins(0, 30, 0, 0)
        
        suggestions = [
            "Help me write code",
            "Explain a concept",
            "Brainstorm ideas",
            "Review my work"
        ]
        
        for suggestion in suggestions:
            btn = QPushButton(suggestion)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: 1px solid #3a3a3a;
                    border-radius: 18px;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                    border-color: #4a4a4a;
                }
            """)
            btn.clicked.connect(lambda checked, text=suggestion: self.set_input_text(text))
            suggestions_layout.addWidget(btn)
            
        suggestions_layout.addStretch()
        welcome_layout.addLayout(suggestions_layout)
        welcome_layout.addStretch()
        
        messages_layout.addWidget(welcome_msg)
        
        # Input area - Clean and focused
        input_container = QWidget()
        input_container.setFixedHeight(80)
        input_container.setStyleSheet("""
            QWidget {
                background-color: #171717;
                border-top: 1px solid #2d2d2d;
            }
        """)
        
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(20, 15, 20, 15)
        
        # Text input
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(50)
        self.input_field.setPlaceholderText("Message Ananta...")
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                border: 1px solid #3a3a3a;
                border-radius: 20px;
                padding: 12px 16px;
                color: #ffffff;
                font-size: 14px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border: 1px solid #4a9eff;
                background-color: #333333;
            }
        """)
        
        # Send button
        self.send_button = QPushButton("➤")
        self.send_button.setFixedSize(40, 40)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                border: none;
                border-radius: 20px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5aa8ff;
            }
            QPushButton:pressed {
                background-color: #3a8eef;
            }
            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #6a6a6a;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field, 1)
        input_layout.addWidget(self.send_button)
        
        layout.addWidget(input_container)
        
        # Connect signals
        self.input_field.textChanged.connect(self.on_text_changed)
        
        # Setup keyboard handling
        self.input_field.keyPressEvent = self.handle_key_press
        
    def set_input_text(self, text: str):
        """Set input text and focus"""
        self.input_field.setText(text)
        self.input_field.moveCursor(QTextCursor.MoveOperation.End)
        
    def on_text_changed(self):
        """Handle text change"""
        text = self.input_field.toPlainText().strip()
        self.send_button.setEnabled(bool(text))
        
    def handle_key_press(self, event):
        """Handle keyboard input"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                # Shift+Enter for new line
                cursor = self.input_field.textCursor()
                cursor.insertText('\n')
            else:
                # Enter to send
                if self.send_button.isEnabled():
                    self.send_message()
        else:
            super().keyPressEvent(event)
            
    def send_message(self):
        """Send message"""
        text = self.input_field.toPlainText().strip()
        if not text:
            return
            
        # Remove welcome message if present
        if len(self.messages) == 0:
            welcome = self.messages_container.findChild(QWidget)
            if welcome and welcome != self.messages_container:
                welcome.deleteLater()
                
        # Add user message
        self.add_message(text, is_user=True)
        
        # Clear input
        self.input_field.clear()
        self.send_button.setEnabled(False)
        
        # Set avatar to thinking
        self.avatar.set_emotion("thinking")
        
        # Process in background
        def process():
            try:
                response = self.controller.query(text, use_memory=True)
                QTimer.singleShot(0, lambda: self.handle_response(response))
            except Exception as e:
                error_response = f"Sorry, I encountered an error: {str(e)}"
                QTimer.singleShot(0, lambda: self.handle_response({'response': error_response}))
                
        self.thread_pool = ThreadPoolExecutor(max_workers=1)
        self.thread_pool.submit(process)
        
    def handle_response(self, response: dict):
        """Handle AI response"""
        response_text = response.get('response', '')
        self.add_message(response_text, is_user=False)
        
        # Update avatar emotion
        if any(word in response_text.lower() for word in ['great', 'wonderful', 'fantastic', 'amazing']):
            self.avatar.set_emotion('joy')
        elif any(word in response_text.lower() for word in ['powerful', 'strong', 'capable']):
            self.avatar.set_emotion('power')
        else:
            self.avatar.set_emotion('neutral')
            
    def add_message(self, text: str, is_user: bool = False):
        """Add message with clean styling"""
        message_widget = QWidget()
        message_widget.setStyleSheet("background-color: transparent;")
        
        message_layout = QVBoxLayout(message_widget)
        message_layout.setContentsMargins(20, 12, 20, 12)
        
        if is_user:
            # User message - right aligned
            container = QWidget()
            container_layout = QHBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.addStretch()
            
            bubble = QWidget()
            bubble.setStyleSheet("""
                QWidget {
                    background-color: #4a9eff;
                    border-radius: 18px;
                    max-width: 600px;
                }
            """)
            
            bubble_layout = QVBoxLayout(bubble)
            bubble_layout.setContentsMargins(16, 12, 16, 12)
            
            text_label = QLabel(text)
            text_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 14px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.4;
                }
            """)
            text_label.setWordWrap(True)
            
            bubble_layout.addWidget(text_label)
            container_layout.addWidget(bubble)
            
        else:
            # AI message - left aligned
            container = QWidget()
            container_layout = QHBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            
            # Avatar for AI messages
            ai_avatar = LivingConstellationAvatar(24)
            ai_avatar.setFixedSize(24, 24)
            container_layout.addWidget(ai_avatar)
            container_layout.addSpacing(12)
            
            bubble = QWidget()
            bubble.setStyleSheet("""
                QWidget {
                    background-color: #2d2d2d;
                    border: 1px solid #3a3a3a;
                    border-radius: 18px;
                    max-width: 600px;
                }
            """)
            
            bubble_layout = QVBoxLayout(bubble)
            bubble_layout.setContentsMargins(16, 12, 16, 12)
            
            text_label = QLabel(text)
            text_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 14px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.4;
                }
            """)
            text_label.setWordWrap(True)
            
            bubble_layout.addWidget(text_label)
            container_layout.addWidget(bubble)
            container_layout.addStretch()
            
        message_layout.addWidget(container)
        
        # Add to messages container
        self.messages_container.layout().addWidget(message_widget)
        self.messages.append({'text': text, 'is_user': is_user})
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def scroll_to_bottom(self):
        """Scroll to bottom"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

class ProfessionalMainWindow(QMainWindow):
    """Professional main window inspired by top AI interfaces"""
    
    def __init__(self):
        super().__init__()
        self.controller = None
        self.setup_window()
        self.setup_ui()
        self.setup_controller()
        
    def setup_window(self):
        """Setup window properties"""
        self.setWindowTitle("Ananta - Professional AI Assistant")
        self.setGeometry(200, 100, 1200, 800)
        
        # Set window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Window
        )
        
        # Custom title bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
            QWidget {
                background-color: #0a0a0a;
            }
        """)
        
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        
        # Window controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(0)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(46, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e81123;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        # Minimize button
        minimize_btn = QPushButton("─")
        minimize_btn.setFixedSize(46, 40)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        
        # Maximize button
        maximize_btn = QPushButton("□")
        maximize_btn.setFixedSize(46, 40)
        maximize_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        maximize_btn.clicked.connect(self.toggle_maximize)
        
        controls_layout.addWidget(minimize_btn)
        controls_layout.addWidget(maximize_btn)
        controls_layout.addWidget(close_btn)
        
        title_layout.addStretch()
        title_layout.addLayout(controls_layout)
        
        # Enable window dragging
        self.title_bar.mousePressEvent = self.start_drag
        self.title_bar.mouseMoveEvent = self.perform_drag
        
    def setup_ui(self):
        """Setup main UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add title bar
        main_layout.addWidget(self.title_bar)
        
        # Chat panel
        self.chat_panel = QWidget()
        self.chat_panel.setStyleSheet("""
            QWidget {
                background-color: #171717;
                border-radius: 8px;
            }
        """)
        main_layout.addWidget(self.chat_panel, 1)
        
        # Create panels
        self.panels = {}
        
    def setup_controller(self):
        """Setup Ananta controller"""
        try:
            self.controller = AnantaController()
            
            # Create professional chat panel
            self.panels['chat'] = ProfessionalChatPanel(self.controller)
            
            # Add to chat panel
            layout = QVBoxLayout(self.chat_panel)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.panels['chat'])
            
            # Connect signals
            self.panels['chat'].message_sent.connect(self.process_message)
            
            print("✅ Professional Ananta interface initialized successfully!")
            
        except Exception as e:
            print(f"❌ Failed to initialize controller: {e}")
            
    def process_message(self, message: str, options: dict):
        """Process message (already handled in panel)"""
        pass
        
    def toggle_maximize(self):
        """Toggle window maximization"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
            
    def start_drag(self, event):
        """Start window dragging"""
        self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        
    def perform_drag(self, event):
        """Perform window dragging"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            
    def closeEvent(self, event):
        """Handle window close"""
        if hasattr(self, 'thread_pool'):
            self.thread_pool.shutdown(wait=False)
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set dark theme
    app.setStyle('Fusion')
    
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(10, 10, 10))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(palette)
    
    # Create and show main window
    window = ProfessionalMainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
