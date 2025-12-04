"""
Ananta Rebirth - Main Window
Complete PyQt6 interface with all features
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

from ui.components import (
    GlassPanel, VoiceVisualizer, 
    MessageBubble, SystemMonitor, TypingIndicator,
    AnantaOpenGLWidget
)
from ui.advanced_avatar import LivingConstellationAvatar
from core.controller import AnantaController

class ChatPanel(QWidget):
    """Main chat interface with message history"""
    
    message_sent = pyqtSignal(str, dict)  # message, options
    
    def __init__(self, controller: AnantaController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.messages = []
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Header with avatar
        header = QHBoxLayout()
        # Avatar with advanced constellation
        self.avatar = LivingConstellationAvatar(50)
        header.addWidget(self.avatar)
        
        title_layout = QVBoxLayout()
        title = QLabel("Ananta AI")
        title.setStyleSheet("color: #00F5FF; font-size: 18px; font-weight: bold;")
        subtitle = QLabel("Your Advanced AI Partner")
        subtitle.setStyleSheet("color: #B0C3FF; font-size: 12px;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header.addLayout(title_layout)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Message area
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
                background-color: rgba(16, 19, 32, 0.5);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(0, 245, 255, 0.3);
                border-radius: 4px;
            }
        """)
        layout.addWidget(scroll, 1)
        
        # Typing indicator
        self.typing_indicator = TypingIndicator()
        self.typing_indicator.hide()
        layout.addWidget(self.typing_indicator)
        
        # Input area
        input_panel = GlassPanel(border_radius=10)
        input_layout = QHBoxLayout(input_panel)
        input_layout.setContentsMargins(15, 10, 15, 10)
        
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(80)
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 13px;
            }
            QTextEdit:focus {
                outline: none;
            }
        """)
        
        send_button = QPushButton("🚀")
        send_button.setFixedSize(40, 40)
        send_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 245, 255, 0.2);
                border: 1px solid rgba(0, 245, 255, 0.5);
                border-radius: 20px;
                color: #00F5FF;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0, 245, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(0, 245, 255, 0.4);
            }
        """)
        send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field, 1)
        input_layout.addWidget(send_button)
        layout.addWidget(input_panel)
        
        self.setLayout(layout)
        
        # Connect enter key
        self.input_field.keyPressEvent = self.handle_key_press
        
    def handle_key_press(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                # Shift+Enter for new line
                super().keyPressEvent(event)
            else:
                # Enter to send
                self.send_message()
        else:
            super().keyPressEvent(event)
            
    def send_message(self):
        text = self.input_field.toPlainText().strip()
        if not text:
            return
            
        # Add user message
        self.add_message(text, is_user=True)
        
        # Clear input
        self.input_field.clear()
        
        # Show typing indicator
        self.typing_indicator.show()
        
        # Get options (simplified for now)
        options = {
            'use_memory': True,
            'reasoning_mode': 'off'
        }
        
        # Emit signal for async processing
        self.message_sent.emit(text, options)
        
    def add_message(self, text: str, is_user: bool = False):
        """Add message to chat"""
        bubble = MessageBubble(text, is_user)
        
        # Add to layout
        if is_user:
            # User messages align right
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addStretch()
            layout.addWidget(bubble)
            layout.setStretchFactor(bubble, 0)  # Don't stretch bubble
            self.message_layout.insertWidget(self.message_layout.count() - 1, container)
        else:
            # AI messages align left
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(bubble)
            layout.addStretch()
            layout.setStretchFactor(bubble, 0)
            self.message_layout.insertWidget(self.message_layout.count() - 1, container)
            
        self.messages.append({'text': text, 'is_user': is_user})
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def scroll_to_bottom(self):
        """Scroll message area to bottom"""
        scrollbar = self.parent().findChild(QScrollArea).verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def show_typing(self, show: bool):
        """Show/hide typing indicator"""
        self.typing_indicator.setVisible(show)

class VoicePanel(QWidget):
    """Voice interaction panel"""
    
    def __init__(self, controller: AnantaController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.is_listening = False
        self.is_speaking = False
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Voice visualizer
        visualizer_container = QWidget()
        visualizer_layout = QVBoxLayout(visualizer_container)
        visualizer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.visualizer = VoiceVisualizer()
        visualizer_layout.addWidget(self.visualizer)
        
        self.voice_status = QLabel("🎤 Tap to start speaking")
        self.voice_status.setStyleSheet("color: #B0C3FF; font-size: 14px;")
        self.voice_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        visualizer_layout.addWidget(self.voice_status)
        
        layout.addWidget(visualizer_container)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.listen_button = QPushButton("🎤 Listen")
        self.listen_button.setFixedHeight(50)
        self.listen_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 245, 255, 0.2);
                border: 1px solid rgba(0, 245, 255, 0.5);
                border-radius: 25px;
                color: #00F5FF;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 245, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(0, 245, 255, 0.4);
            }
        """)
        self.listen_button.clicked.connect(self.toggle_listening)
        
        self.speak_button = QPushButton("🔊 Speak")
        self.speak_button.setFixedHeight(50)
        self.speak_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(155, 93, 255, 0.2);
                border: 1px solid rgba(155, 93, 255, 0.5);
                border-radius: 25px;
                color: #9B5DFF;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(155, 93, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(155, 93, 255, 0.4);
            }
        """)
        self.speak_button.clicked.connect(self.toggle_speaking)
        
        button_layout.addWidget(self.listen_button)
        button_layout.addWidget(self.speak_button)
        layout.addLayout(button_layout)
        
        # Transcription display
        self.transcription = QLabel("")
        self.transcription.setWordWrap(True)
        self.transcription.setStyleSheet("""
            QLabel {
                background-color: rgba(28, 35, 51, 0.5);
                border: 1px solid rgba(138, 216, 255, 0.2);
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-size: 13px;
                min-height: 100px;
            }
        """)
        layout.addWidget(self.transcription)
        
        self.setLayout(layout)
        
    def toggle_listening(self):
        """Toggle voice listening"""
        self.is_listening = not self.is_listening
        self.visualizer.set_active(self.is_listening)
        
        if self.is_listening:
            self.listen_button.setText("⏹️ Stop")
            self.voice_status.setText("🎤 Listening...")
            self.transcription.setText("Listening for your voice...")
        else:
            self.listen_button.setText("🎤 Listen")
            self.voice_status.setText("🎤 Tap to start speaking")
            
    def toggle_speaking(self):
        """Toggle voice speaking"""
        self.is_speaking = not self.is_speaking
        
        if self.is_speaking:
            self.speak_button.setText("⏹️ Stop")
            self.voice_status.setText("🔊 Speaking...")
        else:
            self.speak_button.setText("🔊 Speak")
            self.voice_status.setText("🎤 Tap to start speaking")

class VisionPanel(QWidget):
    """Vision analysis panel with drag & drop"""
    
    def __init__(self, controller: AnantaController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("👁️ Vision Analysis")
        title.setStyleSheet("color: #00F5FF; font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Drop area
        self.drop_area = GlassPanel()
        self.drop_area.setFixedHeight(200)
        self.drop_layout = QVBoxLayout(self.drop_area)
        self.drop_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        drop_icon = QLabel("📸")
        drop_icon.setStyleSheet("font-size: 48px;")
        drop_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_layout.addWidget(drop_icon)
        
        drop_text = QLabel("Drag & drop images here\nor click to browse")
        drop_text.setStyleSheet("color: #B0C3FF; font-size: 14px;")
        drop_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_layout.addWidget(drop_text)
        
        self.drop_area.mousePressEvent = self.browse_files
        layout.addWidget(self.drop_area)
        
        # Analysis results
        self.results_area = GlassPanel()
        self.results_layout = QVBoxLayout(self.results_area)
        
        results_title = QLabel("🔍 Analysis Results")
        results_title.setStyleSheet("color: #00F5FF; font-size: 14px; font-weight: bold;")
        self.results_layout.addWidget(results_title)
        
        self.results_text = QLabel("No image analyzed yet")
        self.results_text.setWordWrap(True)
        self.results_text.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
                padding: 10px;
                background-color: rgba(0, 0, 0, 0.3);
                border-radius: 5px;
            }
        """)
        self.results_layout.addWidget(self.results_text)
        
        layout.addWidget(self.results_area)
        
        self.setLayout(layout)
        
        # Enable drag & drop
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file_path in files:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                self.analyze_image(file_path)
                break
                
    def browse_files(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if file_path:
            self.analyze_image(file_path)
            
    def analyze_image(self, image_path: str):
        """Analyze image using vision engine"""
        self.results_text.setText("🔍 Analyzing image...")
        
        # Run analysis in thread
        QTimer.singleShot(100, lambda: self._perform_analysis(image_path))
        
    def _perform_analysis(self, image_path: str):
        """Perform actual vision analysis"""
        try:
            result = self.controller.analyze_code_image(image_path, "auto")
            
            if result.get("success"):
                analysis = result.get("analysis", "")
                if len(analysis) > 500:
                    analysis = analysis[:500] + "..."
                    
                self.results_text.setText(f"✅ Analysis Complete:\n\n{analysis}")
            else:
                self.results_text.setText(f"❌ Analysis Failed:\n\n{result.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.results_text.setText(f"❌ Error: {str(e)}")

class AutomationPanel(QWidget):
    """Automation workflow panel"""
    
    def __init__(self, controller: AnantaController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🤖 Automation Workflows")
        title.setStyleSheet("color: #00F5FF; font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Workflow list
        self.workflow_list = QListWidget()
        self.workflow_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(28, 35, 51, 0.5);
                border: 1px solid rgba(138, 216, 255, 0.2);
                border-radius: 10px;
                padding: 5px;
                color: white;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px;
                background-color: rgba(16, 19, 32, 0.5);
                border-radius: 5px;
            }
            QListWidget::item:selected {
                background-color: rgba(0, 245, 255, 0.2);
                border: 1px solid rgba(0, 245, 255, 0.5);
            }
        """)
        layout.addWidget(self.workflow_list)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        create_button = QPushButton("➕ Create")
        create_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 245, 255, 0.2);
                border: 1px solid rgba(0, 245, 255, 0.5);
                border-radius: 20px;
                color: #00F5FF;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(0, 245, 255, 0.3);
            }
        """)
        
        run_button = QPushButton("▶️ Run")
        run_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(76, 175, 80, 0.2);
                border: 1px solid rgba(76, 175, 80, 0.5);
                border-radius: 20px;
                color: #4CAF50;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(76, 175, 80, 0.3);
            }
        """)
        
        button_layout.addWidget(create_button)
        button_layout.addWidget(run_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Status display
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #B0C3FF; font-size: 11px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Load existing workflows
        self.load_workflows()
        
    def load_workflows(self):
        """Load existing automation workflows"""
        self.workflow_list.clear()
        
        # Add sample workflows
        sample_workflows = [
            "🔍 Code Analysis - Analyze uploaded code files",
            "📝 Document OCR - Extract text from images",
            "🎨 Design to Code - Convert mockups to HTML/CSS",
            "🐛 Error Detection - Find and fix code issues",
            "📊 System Monitor - Track performance metrics"
        ]
        
        for workflow in sample_workflows:
            self.workflow_list.addItem(workflow)

class MainWindow(QMainWindow):
    """Main Ananta Rebirth window"""
    
    def __init__(self):
        super().__init__()
        self.controller = None
        self.setup_window()
        self.setup_ui()
        self.setup_controller()
        
    def setup_window(self):
        """Setup window properties"""
        self.setWindowTitle("Ananta Rebirth - Advanced AI Partner")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set window flags for borderless window
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Window
        )
        
        # Set transparent background
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Custom title bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
            QWidget {
                background-color: rgba(16, 19, 32, 0.9);
                border-bottom: 1px solid rgba(138, 216, 255, 0.3);
            }
        """)
        
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        
        # Title
        title = QLabel("🚀 Ananta Rebirth")
        title.setStyleSheet("color: #00F5FF; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title)
        
        title_layout.addStretch()
        
        # Window controls
        minimize_btn = QPushButton("─")
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 193, 7, 0.2);
                border: 1px solid rgba(255, 193, 7, 0.5);
                border-radius: 15px;
                color: #FFC107;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 193, 7, 0.3);
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(244, 67, 54, 0.2);
                border: 1px solid rgba(244, 67, 54, 0.5);
                border-radius: 15px;
                color: #F44336;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(244, 67, 54, 0.3);
            }
        """)
        close_btn.clicked.connect(self.close)
        
        title_layout.addWidget(minimize_btn)
        title_layout.addWidget(close_btn)
        
        # Enable window dragging
        self.title_bar.mousePressEvent = self.start_drag
        self.title_bar.mouseMoveEvent = self.perform_drag
        
    def setup_ui(self):
        """Setup main UI"""
        # Central widget with OpenGL background
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add title bar
        main_layout.addWidget(self.title_bar)
        
        # Content area with tabs
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left sidebar - Navigation
        sidebar = GlassPanel()
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 15, 15, 15)
        sidebar_layout.setSpacing(15)
        
        # Navigation buttons
        self.nav_buttons = []
        nav_items = [
            ("💬 Chat", "chat"),
            ("🎤 Voice", "voice"),
            ("👁️ Vision", "vision"),
            ("🤖 Automation", "automation"),
            ("📊 Stats", "stats"),
            ("⚙️ Settings", "settings")
        ]
        
        for icon_text, name in nav_items:
            btn = QPushButton(icon_text)
            btn.setFixedHeight(45)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(28, 35, 51, 0.5);
                    border: 1px solid rgba(138, 216, 255, 0.2);
                    border-radius: 10px;
                    color: white;
                    font-size: 13px;
                    text-align: left;
                    padding-left: 15px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 245, 255, 0.2);
                    border: 1px solid rgba(0, 245, 255, 0.5);
                }
                QPushButton:checked {
                    background-color: rgba(0, 245, 255, 0.3);
                    border: 1px solid rgba(0, 245, 255, 0.7);
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=name: self.switch_panel(n))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append((btn, name))
            
        sidebar_layout.addStretch()
        
        # System monitor
        self.system_monitor = SystemMonitor()
        sidebar_layout.addWidget(self.system_monitor)
        
        content_layout.addWidget(sidebar)
        
        # Main content area
        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack, 1)
        
        main_layout.addLayout(content_layout)
        
        # Create panels (will be added after controller setup)
        self.panels = {}
        
    def setup_controller(self):
        """Setup Ananta controller and panels"""
        try:
            # Initialize controller
            self.controller = AnantaController()
            
            # Create panels
            self.panels['chat'] = ChatPanel(self.controller)
            self.panels['voice'] = VoicePanel(self.controller)
            self.panels['vision'] = VisionPanel(self.controller)
            self.panels['automation'] = AutomationPanel(self.controller)
            self.panels['stats'] = QWidget()  # TODO: Implement stats panel
            self.panels['settings'] = QWidget()  # TODO: Implement settings panel
            
            # Add panels to stack
            for name, panel in self.panels.items():
                self.content_stack.addWidget(panel)
                
            # Setup system monitor
            self.system_monitor.set_controller(self.controller)
            
            # Connect chat signals
            if 'chat' in self.panels:
                self.panels['chat'].message_sent.connect(self.process_message)
                
            # Connect avatar emotions to controller
            if hasattr(self, 'avatar') and self.controller:
                # Update avatar emotion based on AI responses
                self.avatar.emotion_changed.connect(self.on_emotion_changed)
                
            # Select first panel
            self.nav_buttons[0][0].setChecked(True)
            
            print("✅ Ananta interface initialized successfully!")
            
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
                
        # Hide typing indicator when done
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
            
            # Update avatar emotion based on response
            if hasattr(self, 'avatar') and 'emotional_state' in response:
                emotion = response.get('emotional_state', 'neutral')
                self.avatar.set_emotion(emotion)
                
    def on_emotion_changed(self, emotion: str):
        """Handle avatar emotion change"""
        print(f"🎭 Avatar emotion changed to: {emotion}")
        
    def set_avatar_emotion(self, emotion: str):
        """Set avatar emotion externally"""
        if hasattr(self, 'avatar'):
            self.avatar.set_emotion(emotion)
            
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
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
