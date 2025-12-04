"""
Ananta Rebirth - Stunning Main Window
Showcasing ALL of Ananta's powers with a beautiful, modern interface
"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, List, Any
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

# Import Ananta components
from core.controller import AnantaController
from ui.emotional_avatar import EmotionalAvatar, EmotionalState

class ModernMessageBox(QWidget):
    """Modern message bubble with typing indicator"""
    
    def __init__(self, message: str, is_user: bool = False, parent=None):
        super().__init__(parent)
        self.message = message
        self.is_user = is_user
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        
        # Avatar
        avatar_size = 36
        if self.is_user:
            avatar = QLabel("👤")
        else:
            avatar = QLabel("🤖")
        
        avatar.setFixedSize(avatar_size, avatar_size)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(f"""
            QLabel {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: {avatar_size//2}px;
                color: white;
                font-size: 18px;
            }}
        """)
        
        # Message content
        content_layout = QVBoxLayout()
        
        # Message text
        msg_label = QLabel(self.message)
        msg_label.setWordWrap(True)
        msg_label.setTextFormat(Qt.TextFormat.MarkdownText)
        msg_label.setStyleSheet("""
            QLabel {
                color: #2d3748;
                font-size: 14px;
                line-height: 1.4;
                padding: 12px 16px;
                background: #f7fafc;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        # Timestamp
        time_label = QLabel(datetime.now().strftime("%H:%M"))
        time_label.setStyleSheet("color: #718096; font-size: 11px;")
        
        content_layout.addWidget(msg_label)
        content_layout.addWidget(time_label)
        
        if self.is_user:
            layout.addStretch()
            layout.addLayout(content_layout)
            layout.addWidget(avatar)
        else:
            layout.addWidget(avatar)
            layout.addLayout(content_layout)
            layout.addStretch()

class PowerCard(QFrame):
    """Card showcasing Ananta's powers"""
    
    power_activated = pyqtSignal(str)
    
    def __init__(self, title: str, description: str, icon: str, color: str, power_id: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        self.icon = icon
        self.color = color
        self.power_id = power_id
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedSize(200, 120)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 12px;
                border: 2px solid {self.color};
                margin: 5px;
            }}
            QFrame:hover {{
                background: {self.color}20;
                border: 2px solid {self.color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icon
        icon_label = QLabel(self.icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"font-size: 32px; color: {self.color};")
        
        # Title
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2d3748;")
        
        # Description
        desc_label = QLabel(self.description)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 11px; color: #718096;")
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
    
    def mousePressEvent(self, event):
        self.power_activated.emit(self.power_id)
        super().mousePressEvent(event)

class StatusIndicator(QLabel):
    """Real-time status indicator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status = "ready"
        self.setup_ui()
        self.update_status()
    
    def setup_ui(self):
        self.setFixedSize(12, 12)
        self.setStyleSheet("""
            QLabel {
                border-radius: 6px;
            }
        """)
    
    def update_status(self, status: str = None):
        if status:
            self.status = status
        
        colors = {
            "ready": "#48bb78",
            "thinking": "#ed8936", 
            "processing": "#4299e1",
            "error": "#f56565",
            "offline": "#718096"
        }
        
        color = colors.get(self.status, "#718096")
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border-radius: 6px;
            }}
        """)

class AnantaMainWindow(QMainWindow):
    """Stunning main window showcasing all Ananta powers"""
    
    def __init__(self):
        super().__init__()
        self.controller = None
        self.thread_pool = ThreadPoolExecutor(max_workers=2)
        self.setup_ui()
        self.initialize_ananta()
    
    def setup_ui(self):
        self.setWindowTitle("🤖 Ananta Rebirth - AI Assistant")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set modern stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left panel - Avatar & Powers
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Center panel - Chat
        center_panel = self.create_center_panel()
        main_layout.addWidget(center_panel, 2)
        
        # Right panel - Status & Info
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
    
    def create_left_panel(self) -> QWidget:
        """Create left panel with avatar and power cards"""
        panel = QWidget()
        panel.setFixedWidth(300)
        layout = QVBoxLayout(panel)
        
        # Avatar Section
        avatar_container = QFrame()
        avatar_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Avatar
        self.avatar = EmotionalAvatar()
        self.avatar.setFixedSize(200, 200)
        avatar_layout.addWidget(self.avatar)
        
        # Status indicator
        status_layout = QHBoxLayout()
        self.status_indicator = StatusIndicator()
        status_layout.addWidget(self.status_indicator)
        status_layout.addWidget(QLabel("Ananta"))
        status_layout.addStretch()
        avatar_layout.addLayout(status_layout)
        
        layout.addWidget(avatar_container)
        
        # Power Cards Section
        powers_label = QLabel("🌟 Ananta's Powers")
        powers_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(powers_label)
        
        # Create power cards
        powers_scroll = QScrollArea()
        powers_scroll.setWidgetResizable(True)
        powers_scroll.setStyleSheet("QScrollArea { background: transparent; }")
        
        powers_widget = QWidget()
        powers_layout = QGridLayout(powers_widget)
        
        self.power_cards = {}
        powers = [
            ("🧠 Intelligence", "Advanced reasoning & context", "#4299e1", "intelligence"),
            ("👁️ Vision", "Analyze images & screenshots", "#9f7aea", "vision"),
            ("🤖 Automation", "Smart workflows & tasks", "#48bb78", "automation"),
            ("💬 Voice", "Talk with Ananta", "#ed8936", "voice"),
            ("⚡ Code", "Execute & analyze code", "#f56565", "code"),
            ("🧠 Memory", "Personal knowledge base", "#38b2ac", "memory"),
            ("😊 Emotion", "Emotional awareness", "#d69e2e", "emotion"),
            ("🔍 Context", "Real-time awareness", "#805ad5", "context"),
        ]
        
        for i, (title, desc, color, power_id) in enumerate(powers):
            card = PowerCard(title, desc, "🌟", color, power_id)
            card.power_activated.connect(self.activate_power)
            self.power_cards[power_id] = card
            powers_layout.addWidget(card, i // 2, i % 2)
        
        powers_scroll.setWidget(powers_widget)
        layout.addWidget(powers_scroll)
        
        return panel
    
    def create_center_panel(self) -> QWidget:
        """Create center chat panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Chat header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px 15px 0 0;
                padding: 15px;
            }
        """)
        header_layout = QHBoxLayout(header)
        
        title = QLabel("💬 Chat with Ananta")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Quick actions
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                color: white;
            }
            QPushButton:hover { background: rgba(255, 255, 255, 0.3); }
        """)
        clear_btn.clicked.connect(self.clear_chat)
        header_layout.addWidget(clear_btn)
        
        layout.addWidget(header)
        
        # Chat messages area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setStyleSheet("""
            QScrollArea {
                background: white;
                border: none;
            }
        """)
        
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.addStretch()
        self.chat_scroll.setWidget(self.chat_widget)
        layout.addWidget(self.chat_scroll)
        
        # Input area
        input_container = QFrame()
        input_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 0 0 15px 15px;
                padding: 15px;
            }
        """)
        input_layout = QHBoxLayout(input_container)
        
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(80)
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.9);
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
            }
        """)
        self.input_field.keyPressEvent = self.handle_key_press
        
        send_btn = QPushButton("📤")
        send_btn.setFixedSize(50, 50)
        send_btn.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 25px;
                font-size: 20px;
                color: white;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #48bb78, stop:1 #38a169);
                border: 2px solid #2f855a;
            }
        """)
        send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field, 4)
        input_layout.addWidget(send_btn)
        
        layout.addWidget(input_container)
        
        return panel
    
    def create_right_panel(self) -> QWidget:
        """Create right panel with status and info"""
        panel = QWidget()
        panel.setFixedWidth(300)
        layout = QVBoxLayout(panel)
        
        # System Status
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        status_layout = QVBoxLayout(status_frame)
        
        status_title = QLabel("📊 System Status")
        status_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        status_layout.addWidget(status_title)
        
        # Status items
        self.status_labels = {}
        status_items = [
            ("model", "🧠 Model", "qwen2.5:7b"),
            ("memory", "💾 Memory", "0 items"),
            ("gpu", "🔥 GPU", "RTX 4050"),
            ("uptime", "⏰ Uptime", "0m"),
        ]
        
        for key, label, value in status_items:
            item_layout = QHBoxLayout()
            item_label = QLabel(label)
            item_label.setStyleSheet("color: white; font-size: 12px;")
            value_label = QLabel(value)
            value_label.setStyleSheet("color: #cbd5e0; font-size: 12px;")
            self.status_labels[key] = value_label
            
            item_layout.addWidget(item_label)
            item_layout.addStretch()
            item_layout.addWidget(value_label)
            status_layout.addLayout(item_layout)
        
        layout.addWidget(status_frame)
        
        # Active Features
        features_frame = QFrame()
        features_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        features_layout = QVBoxLayout(features_frame)
        
        features_title = QLabel("⚡ Active Features")
        features_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        features_layout.addWidget(features_title)
        
        self.feature_labels = {}
        features = [
            ("vision", "👁️ Vision Analysis"),
            ("automation", "🤖 Smart Automation"),
            ("emotion", "😊 Emotional Intelligence"),
            ("context", "🔍 Context Awareness"),
            ("memory", "🧠 Adaptive Memory"),
            ("code", "⚡ Code Execution"),
        ]
        
        for key, label in features:
            check_label = QLabel(f"✅ {label}")
            check_label.setStyleSheet("color: #48bb78; font-size: 12px;")
            self.feature_labels[key] = check_label
            features_layout.addWidget(check_label)
        
        layout.addWidget(features_frame)
        
        # Quick Commands
        commands_frame = QFrame()
        commands_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        commands_layout = QVBoxLayout(commands_frame)
        
        commands_title = QLabel("🎯 Quick Commands")
        commands_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        commands_layout.addWidget(commands_title)
        
        commands = [
            ("Analyze this image", "vision"),
            ("Execute Python code", "code"),
            ("Check system status", "status"),
            ("Show my memories", "memory"),
        ]
        
        for cmd_text, cmd_type in commands:
            btn = QPushButton(cmd_text)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.2);
                    border: none;
                    padding: 8px;
                    border-radius: 8px;
                    color: white;
                    font-size: 11px;
                }
                QPushButton:hover { background: rgba(255, 255, 255, 0.3); }
            """)
            btn.clicked.connect(lambda checked, t=cmd_type: self.quick_command(t))
            commands_layout.addWidget(btn)
        
        layout.addWidget(commands_frame)
        layout.addStretch()
        
        return panel
    
    def initialize_ananta(self):
        """Initialize Ananta controller"""
        try:
            self.controller = AnantaController()
            self.add_message("🎉 Ananta is ready! I'm here to help with all your tasks.", is_user=False)
            self.update_system_status()
        except Exception as e:
            self.add_message(f"❌ Error initializing Ananta: {e}", is_user=False)
    
    def handle_key_press(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                # Add new line
                cursor = self.input_field.textCursor()
                cursor.insertText("\n")
            else:
                # Send message
                self.send_message()
        else:
            super().keyPressEvent(event)
    
    def send_message(self):
        """Send message to Ananta"""
        message = self.input_field.toPlainText().strip()
        if not message:
            return
        
        # Add user message
        self.add_message(message, is_user=True)
        self.input_field.clear()
        
        # Update status
        self.status_indicator.update_status("thinking")
        
        # Process in background
        self.thread_pool.submit(self.process_message, message)
    
    def process_message(self, message: str):
        """Process message with Ananta"""
        try:
            if self.controller:
                response = self.controller.query(message)
                response_text = response.get('response', 'Sorry, I could not process that.')
                
                # Add response in main thread
                QTimer.singleShot(0, lambda: self.add_message(response_text, is_user=False))
            else:
                QTimer.singleShot(0, lambda: self.add_message("Ananta is not initialized.", is_user=False))
        except Exception as e:
            QTimer.singleShot(0, lambda: self.add_message(f"Error: {str(e)}", is_user=False))
        finally:
            QTimer.singleShot(0, lambda: self.status_indicator.update_status("ready"))
    
    def add_message(self, message: str, is_user: bool = False):
        """Add message to chat"""
        msg_widget = ModernMessageBox(message, is_user)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, msg_widget)
        
        # Make avatar react to message
        self.avatar.react_to_message(message, is_user)
        
        # Scroll to bottom
        QTimer.singleShot(100, lambda: self.chat_scroll.ensureWidgetVisible(msg_widget))
    
    def clear_chat(self):
        """Clear chat messages"""
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def activate_power(self, power_id: str):
        """Activate a specific power"""
        power_messages = {
            "intelligence": "🧠 Activating advanced reasoning and context analysis...",
            "vision": "👁️ Vision analysis ready! Please share an image to analyze.",
            "automation": "🤖 Smart automation engine activated. What would you like to automate?",
            "voice": "💬 Voice interface ready! Click the microphone to start talking.",
            "code": "⚡ Code execution environment ready! Share your code to run or analyze.",
            "memory": "🧠 Memory system active! I can remember and recall our conversations.",
            "emotion": "😊 Emotional intelligence enabled! I'll be more aware of your feelings.",
            "context": "🔍 Context awareness active! I'm monitoring your environment and patterns."
        }
        
        message = power_messages.get(power_id, "Power activated!")
        self.add_message(message, is_user=False)
        
        # Highlight the activated card
        if power_id in self.power_cards:
            card = self.power_cards[power_id]
            card.setStyleSheet(card.styleSheet() + """
                QFrame {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: 3px solid #4c51bf;
                }
            """)
    
    def quick_command(self, command_type: str):
        """Execute quick command"""
        commands = {
            "vision": "Show me your vision analysis capabilities",
            "code": "Execute: print('Hello from Ananta!')",
            "status": "What is your current system status?",
            "memory": "What do you remember about me?"
        }
        
        message = commands.get(command_type, "Quick command")
        self.input_field.setPlainText(message)
        self.send_message()
    
    def update_system_status(self):
        """Update system status display"""
        if self.controller:
            try:
                # Update model
                model = self.controller.model
                self.status_labels["model"].setText(model)
                
                # Update memory count
                memory_stats = self.controller.get_memory_stats()
                total_mem = memory_stats.get("personal_count", 0) + memory_stats.get("knowledge_count", 0)
                self.status_labels["memory"].setText(f"{total_mem} items")
                
                # Update uptime (simplified)
                uptime = "5m"  # Would calculate actual uptime
                self.status_labels["uptime"].setText(uptime)
                
            except Exception as e:
                print(f"Error updating status: {e}")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application icon and properties
    app.setApplicationName("Ananta Rebirth")
    app.setApplicationVersion("2.0")
    
    window = AnantaMainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
