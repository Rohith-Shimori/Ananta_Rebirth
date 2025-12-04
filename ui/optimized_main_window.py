"""
Ananta Rebirth - Optimized Main Window
Professional, responsive, and user-friendly interface
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
from ui.components import (
    GlassPanel, VoiceVisualizer, 
    SystemMonitor, TypingIndicator,
    AnantaOpenGLWidget
)
from ui.advanced_avatar import LivingConstellationAvatar
from core.controller import AnantaController

class OptimizedChatPanel(QWidget):
    """Optimized chat interface with visible typing and better feedback"""
    
    message_sent = pyqtSignal(str, dict)
    
    def __init__(self, controller: AnantaController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.messages = []
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Header with avatar and status
        header = GlassPanel(border_radius=12)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Avatar with status indicator
        avatar_container = QWidget()
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        
        self.avatar = LivingConstellationAvatar(60)
        avatar_layout.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Status indicator
        self.status_indicator = QLabel("🟢 Online")
        self.status_indicator.setStyleSheet("""
            QLabel {
                background-color: rgba(76, 175, 80, 0.2);
                border: 1px solid rgba(76, 175, 80, 0.5);
                border-radius: 10px;
                padding: 4px 8px;
                color: #4CAF50;
                font-size: 10px;
                font-weight: bold;
            }
        """)
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_layout.addWidget(self.status_indicator)
        
        header_layout.addWidget(avatar_container)
        
        # Title and info
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Ananta AI")
        title.setStyleSheet("color: #00F5FF; font-size: 20px; font-weight: bold;")
        subtitle = QLabel("Advanced AI Partner • Vision + Automation")
        subtitle.setStyleSheet("color: #B0C3FF; font-size: 12px;")
        
        # Model info
        self.model_info = QLabel(f"🧠 {self.controller.model}")
        self.model_info.setStyleSheet("color: #6E7CA3; font-size: 10px;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        title_layout.addWidget(self.model_info)
        title_layout.addStretch()
        
        header_layout.addWidget(title_container)
        header_layout.addStretch()
        
        layout.addWidget(header)
        
        # Message area with better styling
        message_container = GlassPanel(border_radius=12)
        message_layout = QVBoxLayout(message_container)
        message_layout.setContentsMargins(20, 20, 20, 20)
        
        # Message title
        msg_title = QLabel("💬 Conversation")
        msg_title.setStyleSheet("color: #00F5FF; font-size: 14px; font-weight: bold;")
        message_layout.addWidget(msg_title)
        
        # Scrollable message area
        self.message_area = QWidget()
        self.message_layout = QVBoxLayout(self.message_area)
        self.message_layout.addStretch()
        
        scroll = QScrollArea()
        scroll.setWidget(self.message_area)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: rgba(16, 19, 32, 0.3);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(0, 245, 255, 0.4);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(0, 245, 255, 0.6);
            }
        """)
        message_layout.addWidget(scroll, 1)
        
        layout.addWidget(message_container, 1)
        
        # Typing indicator
        typing_container = QWidget()
        typing_layout = QHBoxLayout(typing_container)
        typing_layout.setContentsMargins(20, 0, 20, 0)
        
        self.typing_indicator = TypingIndicator()
        typing_layout.addWidget(self.typing_indicator)
        
        self.typing_text = QLabel("Ananta is thinking...")
        self.typing_text.setStyleSheet("color: #B0C3FF; font-size: 12px; font-style: italic;")
        typing_layout.addWidget(self.typing_text)
        typing_layout.addStretch()
        
        self.typing_widget = QWidget()
        self.typing_widget.setLayout(typing_layout)
        self.typing_widget.hide()
        layout.addWidget(self.typing_widget)
        
        # Enhanced input area
        input_container = GlassPanel(border_radius=12)
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(20, 20, 20, 20)
        input_layout.setSpacing(10)
        
        # Input title
        input_title = QLabel("✍️ Type your message")
        input_title.setStyleSheet("color: #00F5FF; font-size: 12px; font-weight: bold;")
        input_layout.addWidget(input_title)
        
        # Text input with better visibility
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(100)
        self.input_field.setPlaceholderText("Type your message here... (Press Enter to send, Shift+Enter for new line)")
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: rgba(28, 35, 51, 0.8);
                border: 2px solid rgba(138, 216, 255, 0.3);
                border-radius: 8px;
                padding: 12px;
                color: white;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                selection-background-color: rgba(0, 245, 255, 0.3);
            }
            QTextEdit:focus {
                border: 2px solid rgba(0, 245, 255, 0.6);
                background-color: rgba(28, 35, 51, 0.9);
                outline: none;
            }
        """)
        
        # Character counter
        char_counter_layout = QHBoxLayout()
        char_counter_layout.addStretch()
        
        self.char_counter = QLabel("0 / 1000")
        self.char_counter.setStyleSheet("color: #6E7CA3; font-size: 10px;")
        char_counter_layout.addWidget(self.char_counter)
        
        input_layout.addWidget(self.input_field)
        input_layout.addLayout(char_counter_layout)
        
        # Button row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Send button
        self.send_button = QPushButton("🚀 Send Message")
        self.send_button.setFixedHeight(45)
        self.send_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 245, 255, 0.8), stop:1 rgba(0, 128, 255, 0.8));
                border: 2px solid rgba(0, 245, 255, 0.6);
                border-radius: 22px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 245, 255, 1.0), stop:1 rgba(0, 128, 255, 1.0));
                border: 2px solid rgba(0, 245, 255, 0.8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 245, 255, 0.6), stop:1 rgba(0, 128, 255, 0.6));
            }
            QPushButton:disabled {
                background-color: rgba(128, 128, 128, 0.5);
                border: 2px solid rgba(128, 128, 128, 0.3);
                color: rgba(255, 255, 255, 0.5);
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        
        # Clear button
        self.clear_button = QPushButton("🗑️ Clear")
        self.clear_button.setFixedHeight(45)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(244, 67, 54, 0.2);
                border: 2px solid rgba(244, 67, 54, 0.5);
                border-radius: 22px;
                color: #F44336;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: rgba(244, 67, 54, 0.3);
                border: 2px solid rgba(244, 67, 54, 0.7);
            }
        """)
        self.clear_button.clicked.connect(self.clear_chat)
        
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        button_layout.addWidget(self.send_button)
        
        input_layout.addLayout(button_layout)
        layout.addWidget(input_container)
        
        self.setLayout(layout)
        
        # Connect signals
        self.input_field.textChanged.connect(self.update_char_counter)
        self.input_field.textChanged.connect(self.on_text_changed)
        
        # Initial state
        self.update_send_button_state()
        
    def on_text_changed(self):
        """Handle text change for visual feedback"""
        self.update_send_button_state()
        
    def update_char_counter(self):
        """Update character counter"""
        text = self.input_field.toPlainText()
        char_count = len(text)
        self.char_counter.setText(f"{char_count} / 1000")
        
        # Change color based on count
        if char_count > 900:
            self.char_counter.setStyleSheet("color: #F44336; font-size: 10px; font-weight: bold;")
        elif char_count > 700:
            self.char_counter.setStyleSheet("color: #FF9800; font-size: 10px;")
        else:
            self.char_counter.setStyleSheet("color: #6E7CA3; font-size: 10px;")
            
    def update_send_button_state(self):
        """Update send button state"""
        text = self.input_field.toPlainText().strip()
        self.send_button.setEnabled(bool(text))
        
    def handle_key_press(self, event):
        """Handle keyboard input"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                # Shift+Enter for new line
                return False  # Let default handler handle it
            else:
                # Enter to send
                if self.send_button.isEnabled():
                    self.send_message()
                return True
        return False
        
    def send_message(self):
        """Send message with better feedback"""
        text = self.input_field.toPlainText().strip()
        if not text:
            return
            
        # Add user message immediately
        self.add_message(text, is_user=True)
        
        # Clear input and update UI
        self.input_field.clear()
        self.update_char_counter()
        self.update_send_button_state()
        
        # Show typing indicator
        self.show_typing(True)
        
        # Update status
        self.status_indicator.setText("🤔 Thinking...")
        self.status_indicator.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 152, 0, 0.2);
                border: 1px solid rgba(255, 152, 0, 0.5);
                border-radius: 10px;
                padding: 4px 8px;
                color: #FF9800;
                font-size: 10px;
                font-weight: bold;
            }
        """)
        
        # Set avatar to thinking mode
        self.avatar.set_emotion("thinking")
        
        # Get options
        options = {
            'use_memory': True,
            'reasoning_mode': 'off'
        }
        
        # Emit signal for async processing
        self.message_sent.emit(text, options)
        
    def add_message(self, text: str, is_user: bool = False):
        """Add message with better styling"""
        bubble = MessageBubble(text, is_user)
        
        # Add timestamp
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        
        # Create message container
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 5, 0, 5)
        
        # Add message
        if is_user:
            # User messages align right
            msg_wrapper = QWidget()
            msg_layout = QHBoxLayout(msg_wrapper)
            msg_layout.setContentsMargins(0, 0, 0, 0)
            msg_layout.addStretch()
            msg_layout.addWidget(bubble)
            msg_layout.setStretchFactor(bubble, 0)
            
            # Timestamp
            time_label = QLabel(timestamp)
            time_label.setStyleSheet("color: #6E7CA3; font-size: 9px;")
            time_layout = QHBoxLayout()
            time_layout.addStretch()
            time_layout.addWidget(time_label)
            time_layout.setContentsMargins(0, 0, 50, 0)
            
            container_layout.addWidget(msg_wrapper)
            container_layout.addLayout(time_layout)
        else:
            # AI messages align left
            msg_wrapper = QWidget()
            msg_layout = QHBoxLayout(msg_wrapper)
            msg_layout.setContentsMargins(0, 0, 0, 0)
            msg_layout.addWidget(bubble)
            msg_layout.addStretch()
            msg_layout.setStretchFactor(bubble, 0)
            
            # Timestamp
            time_label = QLabel(timestamp)
            time_label.setStyleSheet("color: #6E7CA3; font-size: 9px;")
            time_layout = QHBoxLayout()
            time_layout.addWidget(time_label)
            time_layout.addStretch()
            time_layout.setContentsMargins(50, 0, 0, 0)
            
            container_layout.addWidget(msg_wrapper)
            container_layout.addLayout(time_layout)
            
        self.message_layout.insertWidget(self.message_layout.count() - 1, container)
        self.messages.append({'text': text, 'is_user': is_user, 'timestamp': timestamp})
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def clear_chat(self):
        """Clear chat history"""
        # Clear messages
        self.messages.clear()
        
        # Clear UI
        while self.message_layout.count() > 1:  # Keep stretch
            item = self.message_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Add clear message
        self.add_message("Chat cleared. How can I help you?", is_user=False)
        
    def show_typing(self, show: bool):
        """Show/hide typing indicator"""
        self.typing_widget.setVisible(show)
        
    def scroll_to_bottom(self):
        """Scroll message area to bottom"""
        scrollbar = self.message_area.parent().findChild(QScrollArea).verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def set_status(self, status: str, color: str = "#4CAF50"):
        """Update status indicator"""
        self.status_indicator.setText(status)
        self.status_indicator.setStyleSheet(f"""
            QLabel {{
                background-color: rgba({color}, 0.2);
                border: 1px solid rgba({color}, 0.5);
                border-radius: 10px;
                padding: 4px 8px;
                color: {color};
                font-size: 10px;
                font-weight: bold;
            }}
        """)

class OptimizedMainWindow(QMainWindow):
    """Optimized main window with better layout and performance"""
    
    def __init__(self):
        super().__init__()
        self.controller = None
        self.setup_window()
        self.setup_ui()
        self.setup_controller()
        
    def setup_window(self):
        """Setup window properties"""
        self.setWindowTitle("🚀 Ananta Rebirth - Advanced AI Partner")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Set window flags for borderless window
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Window
        )
        
        # Set transparent background
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Custom title bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(45)
        self.title_bar.setStyleSheet("""
            QWidget {
                background-color: rgba(16, 19, 32, 0.95);
                border-bottom: 2px solid rgba(0, 245, 255, 0.3);
            }
        """)
        
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        
        # Title with icon
        title_widget = QWidget()
        title_widget_layout = QHBoxLayout(title_widget)
        title_widget_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel("🚀")
        icon_label.setStyleSheet("font-size: 18px;")
        title_widget_layout.addWidget(icon_label)
        
        title = QLabel("Ananta Rebirth")
        title.setStyleSheet("color: #00F5FF; font-size: 16px; font-weight: bold;")
        title_widget_layout.addWidget(title)
        
        subtitle = QLabel("Advanced AI Partner")
        subtitle.setStyleSheet("color: #B0C3FF; font-size: 11px;")
        title_widget_layout.addWidget(subtitle)
        
        title_layout.addWidget(title_widget)
        title_layout.addStretch()
        
        # Window controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(5)
        
        minimize_btn = QPushButton("─")
        minimize_btn.setFixedSize(35, 35)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 193, 7, 0.2);
                border: 1px solid rgba(255, 193, 7, 0.5);
                border-radius: 17px;
                color: #FFC107;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 193, 7, 0.4);
                border: 1px solid rgba(255, 193, 7, 0.7);
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        
        maximize_btn = QPushButton("□")
        maximize_btn.setFixedSize(35, 35)
        maximize_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 245, 255, 0.2);
                border: 1px solid rgba(0, 245, 255, 0.5);
                border-radius: 17px;
                color: #00F5FF;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 245, 255, 0.4);
                border: 1px solid rgba(0, 245, 255, 0.7);
            }
        """)
        maximize_btn.clicked.connect(self.toggle_maximize)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(35, 35)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(244, 67, 54, 0.2);
                border: 1px solid rgba(244, 67, 54, 0.5);
                border-radius: 17px;
                color: #F44336;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(244, 67, 54, 0.4);
                border: 1px solid rgba(244, 67, 54, 0.7);
            }
        """)
        close_btn.clicked.connect(self.close)
        
        controls_layout.addWidget(minimize_btn)
        controls_layout.addWidget(maximize_btn)
        controls_layout.addWidget(close_btn)
        
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
        
        # Content area
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(2, 4, 10, 0.95);
                border-radius: 15px;
                margin: 10px;
            }
        """)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)
        
        # Navigation bar
        nav_bar = GlassPanel(border_radius=10)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(20, 15, 20, 15)
        
        # Navigation buttons with better styling
        self.nav_buttons = []
        nav_items = [
            ("💬 Chat", "chat", "Start conversation"),
            ("🎤 Voice", "voice", "Voice interaction"),
            ("👁️ Vision", "vision", "Analyze images"),
            ("🤖 Automation", "automation", "Manage workflows"),
            ("📊 Stats", "stats", "View statistics"),
            ("⚙️ Settings", "settings", "Configure preferences")
        ]
        
        for icon_text, name, tooltip in nav_items:
            btn = QPushButton(icon_text)
            btn.setFixedHeight(50)
            btn.setToolTip(tooltip)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(28, 35, 51, 0.6);
                    border: 2px solid rgba(138, 216, 255, 0.2);
                    border-radius: 25px;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    text-align: left;
                    padding-left: 20px;
                    padding-right: 20px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 245, 255, 0.2);
                    border: 2px solid rgba(0, 245, 255, 0.5);
                    color: #00F5FF;
                }
                QPushButton:checked {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(0, 245, 255, 0.4), stop:1 rgba(0, 128, 255, 0.4));
                    border: 2px solid rgba(0, 245, 255, 0.7);
                    color: white;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=name: self.switch_panel(n))
            nav_layout.addWidget(btn)
            self.nav_buttons.append((btn, name))
            
        nav_layout.addStretch()
        
        # System monitor mini
        self.system_monitor = SystemMonitor()
        self.system_monitor.setFixedWidth(200)
        nav_layout.addWidget(self.system_monitor)
        
        content_layout.addWidget(nav_bar)
        
        # Main content area
        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack, 1)
        
        main_layout.addWidget(content_widget)
        
        # Create panels
        self.panels = {}
        
    def setup_controller(self):
        """Setup Ananta controller and panels"""
        try:
            # Initialize controller
            self.controller = AnantaController()
            
            # Create optimized chat panel
            self.panels['chat'] = OptimizedChatPanel(self.controller)
            
            # Create other panels (simplified for now)
            self.panels['voice'] = QWidget()
            self.panels['vision'] = QWidget()
            self.panels['automation'] = QWidget()
            self.panels['stats'] = QWidget()
            self.panels['settings'] = QWidget()
            
            # Add panels to stack
            for name, panel in self.panels.items():
                self.content_stack.addWidget(panel)
                
            # Setup system monitor
            self.system_monitor.set_controller(self.controller)
            
            # Connect chat signals
            if 'chat' in self.panels:
                self.panels['chat'].message_sent.connect(self.process_message)
                
            # Select first panel
            self.nav_buttons[0][0].setChecked(True)
            
            print("✅ Optimized Ananta interface initialized successfully!")
            
        except Exception as e:
            print(f"❌ Failed to initialize controller: {e}")
            
    def switch_panel(self, panel_name: str):
        """Switch to specific panel"""
        if panel_name in self.panels:
            self.content_stack.setCurrentWidget(self.panels[panel_name])
            
            # Update button states
            for btn, name in self.nav_buttons:
                btn.setChecked(name == panel_name)
                
    def process_message(self, message: str, options: dict):
        """Process chat message asynchronously"""
        if not self.controller:
            return
            
        chat_panel = self.panels.get('chat')
        if not chat_panel:
            return
            
        # Run in thread to avoid blocking UI
        def process():
            try:
                response = self.controller.query(
                    message, 
                    use_memory=options.get('use_memory', True),
                    reasoning_mode=options.get('reasoning_mode', 'off')
                )
                
                # Update UI in main thread
                QTimer.singleShot(0, lambda: self._handle_response(response))
                
            except Exception as e:
                error_response = f"❌ Error processing message: {str(e)}"
                QTimer.singleShot(0, lambda: self._handle_response({'response': error_response}))
                
        # Hide typing indicator after delay
        QTimer.singleShot(1000, lambda: chat_panel.show_typing(False))
        
        # Start processing
        self.thread_pool = ThreadPoolExecutor(max_workers=1)
        self.thread_pool.submit(process)
        
    def _handle_response(self, response: dict):
        """Handle AI response"""
        chat_panel = self.panels.get('chat')
        if chat_panel:
            chat_panel.show_typing(False)
            chat_panel.add_message(response.get('response', ''), is_user=False)
            
            # Update status
            chat_panel.set_status("🟢 Online", "#4CAF50")
            
            # Update avatar emotion based on response
            if hasattr(chat_panel, 'avatar'):
                # Simple emotion detection based on response content
                response_text = response.get('response', '').lower()
                if any(word in response_text for word in ['great', 'wonderful', 'fantastic', 'amazing']):
                    chat_panel.avatar.set_emotion('joy')
                elif any(word in response_text for word in ['thinking', 'analyze', 'consider']):
                    chat_panel.avatar.set_emotion('thinking')
                elif any(word in response_text for word in ['powerful', 'strong', 'capable']):
                    chat_panel.avatar.set_emotion('power')
                else:
                    chat_panel.avatar.set_emotion('neutral')
                    
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
        # Cleanup
        if hasattr(self, 'thread_pool'):
            self.thread_pool.shutdown(wait=False)
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set dark palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(2, 4, 10))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(16, 19, 32))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(28, 35, 51))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(28, 35, 51))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(0, 245, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 245, 255, 100))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)
    
    # Create and show main window
    window = OptimizedMainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
