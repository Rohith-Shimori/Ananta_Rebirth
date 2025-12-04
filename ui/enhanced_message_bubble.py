"""
Enhanced Message Bubble Component
Better visibility and styling for chat messages
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import time

class EnhancedMessageBubble(QWidget):
    """Enhanced message bubble with better styling and animations"""
    
    def __init__(self, text: str, is_user: bool = False, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.text = text
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Message container
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(15, 12, 15, 12)
        
        # Message text
        self.message_label = QLabel(self.text)
        self.message_label.setWordWrap(True)
        self.message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        if self.is_user:
            # User message styling
            container.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(0, 245, 255, 0.3), stop:1 rgba(0, 128, 255, 0.3));
                    border: 2px solid rgba(0, 245, 255, 0.5);
                    border-radius: 18px;
                    color: white;
                }
            """)
            self.message_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 13px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    line-height: 1.4;
                }
            """)
        else:
            # AI message styling
            container.setStyleSheet("""
                QWidget {
                    background-color: rgba(28, 35, 51, 0.9);
                    border: 2px solid rgba(138, 216, 255, 0.3);
                    border-radius: 18px;
                    color: white;
                }
            """)
            self.message_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 13px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    line-height: 1.4;
                }
            """)
            
        container_layout.addWidget(self.message_label)
        layout.addWidget(container)
        
        # Set maximum width for better readability
        self.setMaximumWidth(600)
        
    def sizeHint(self):
        """Calculate optimal size"""
        hint = super().sizeHint()
        hint.setWidth(min(600, hint.width()))
        return hint

# Update the original MessageBubble to use the enhanced version
class MessageBubble(EnhancedMessageBubble):
    """Backward compatible MessageBubble"""
    pass
