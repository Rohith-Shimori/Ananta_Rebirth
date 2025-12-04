"""
Ananta Rebirth - Ultimate PyQt6 Interface
Based on Flutter frontend analysis with enhanced features
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Optional, Dict, List, Any

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

import OpenGL.GL as gl
from OpenGL.arrays import vbo
import numpy as np

# Import Ananta core
from core.controller import AnantaController

class AnantaOpenGLWidget(QOpenGLWidget):
    """OpenGL widget for particle effects and visualizations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.time = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(16)  # 60 FPS
        
    def initializeGL(self):
        gl.glClearColor(0.01, 0.02, 0.04, 1.0)  # Deep space background
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # Initialize particles
        self.init_particles()
        
    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, w, h, 0, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        
    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        # Draw particles
        self.draw_particles()
        
        # Draw neural network visualization
        self.draw_neural_network()
        
    def init_particles(self):
        """Initialize floating particles"""
        for _ in range(50):
            self.particles.append({
                'x': np.random.random(),
                'y': np.random.random(),
                'vx': (np.random.random() - 0.5) * 0.001,
                'vy': (np.random.random() - 0.5) * 0.001,
                'size': np.random.random() * 3 + 1,
                'alpha': np.random.random() * 0.5 + 0.1
            })
            
    def update_animation(self):
        self.time += 0.016
        # Update particle positions
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Wrap around edges
            if p['x'] < 0: p['x'] = 1
            if p['x'] > 1: p['x'] = 0
            if p['y'] < 0: p['y'] = 1
            if p['y'] > 1: p['y'] = 0
            
        self.update()
        
    def draw_particles(self):
        """Draw floating particles"""
        gl.glPointSize(2.0)
        gl.glBegin(gl.GL_POINTS)
        
        for p in self.particles:
            # Pulsing alpha
            alpha = p['alpha'] * (0.5 + 0.5 * np.sin(self.time * 2 + p['x'] * 10))
            gl.glColor4f(0.0, 0.96, 1.0, alpha)  # Cyan color
            
            x = p['x'] * self.width()
            y = p['y'] * self.height()
            gl.glVertex2f(x, y)
            
        gl.glEnd()
        
    def draw_neural_network(self):
        """Draw animated neural network connections"""
        gl.glLineWidth(1.0)
        gl.glBegin(gl.GL_LINES)
        
        # Draw connections between particles
        for i, p1 in enumerate(self.particles[:20]):  # Limit for performance
            for p2 in self.particles[:20]:
                dist = np.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)
                if dist < 0.2 and dist > 0.01:
                    alpha = (0.2 - dist) / 0.2 * 0.3
                    gl.glColor4f(0.0, 0.5, 1.0, alpha * (0.5 + 0.5 * np.sin(self.time * 3)))
                    
                    x1 = p1['x'] * self.width()
                    y1 = p1['y'] * self.height()
                    x2 = p2['x'] * self.width()
                    y2 = p2['y'] * self.height()
                    
                    gl.glVertex2f(x1, y1)
                    gl.glVertex2f(x2, y2)
                    
        gl.glEnd()

class GlassPanel(QFrame):
    """Glass morphism panel with blur effect"""
    
    def __init__(self, parent=None, border_radius=15):
        super().__init__(parent)
        self.border_radius = border_radius
        self.setStyleSheet("""
            GlassPanel {
                background-color: rgba(16, 19, 32, 0.85);
                border: 1px solid rgba(138, 216, 255, 0.3);
                border-radius: %dpx;
            }
        """ % border_radius)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create glass effect
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.border_radius, self.border_radius)
        
        # Gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(16, 19, 32, 200))  # Semi-transparent surface
        gradient.setColorAt(1, QColor(28, 35, 51, 200))  # Lighter surface
        painter.fillPath(path, gradient)
        
        # Glow effect
        painter.setPen(QPen(QColor(0, 245, 255, 100), 2))
        painter.drawPath(path)

class AnantaAvatar(QLabel):
    """Animated Ananta avatar with glow effects"""
    
    def __init__(self, size=60, parent=None):
        super().__init__(parent)
        self.size = size
        self.glow_animation = 0
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_glow)
        self.timer.start(50)
        
    def update_glow(self):
        self.glow_animation += 0.1
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = self.width() // 2
        radius = self.size // 2 - 5
        
        # Animated glow
        glow_intensity = 0.5 + 0.3 * np.sin(self.glow_animation)
        
        # Outer glow
        for i in range(5):
            alpha = int(255 * glow_intensity * (0.2 - i * 0.04))
            painter.setPen(QPen(QColor(0, 245, 255, alpha), 2))
            painter.drawEllipse(center, center, radius + i * 3, radius + i * 3)
        
        # Main gradient circle
        gradient = QRadialGradient(center, center, radius)
        gradient.setColorAt(0, QColor(0, 245, 255))  # Cyan
        gradient.setColorAt(1, QColor(0, 128, 255))  # Blue
        
        painter.setPen(QPen(gradient, 3))
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(center, center, radius, radius)
        
        # "A" text
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        font = QFont("Arial", int(self.size * 0.4), QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "A")

class VoiceVisualizer(QWidget):
    """5-bar voice visualization widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(150, 60)
        self.animation_time = 0
        self.is_active = False
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)
        
    def set_active(self, active):
        self.is_active = active
        
    def update_animation(self):
        self.animation_time += 0.1
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        bar_width = 20
        bar_spacing = 30
        start_x = (self.width() - (5 * bar_width + 4 * bar_spacing)) // 2
        
        for i in range(5):
            if self.is_active:
                # Animated height when active
                delay = i * 0.2
                height = 10 + abs(np.sin(self.animation_time - delay) * 25)
            else:
                # Static height when inactive
                height = 10
                
            x = start_x + i * (bar_width + bar_spacing)
            y = (self.height() - height) // 2
            
            # Bar gradient
            gradient = QLinearGradient(x, y + height, x, y)
            gradient.setColorAt(0, QColor(0, 245, 255, 100))
            gradient.setColorAt(1, QColor(0, 245, 255, 255))
            
            painter.fillRect(x, y, bar_width, height, gradient)
            
            # Glow effect
            if self.is_active:
                painter.setPen(QPen(QColor(0, 245, 255, 50), 2))
                painter.drawRect(x - 1, y - 1, bar_width + 2, height + 2)

class MessageBubble(QLabel):
    """Animated message bubble with typing effect"""
    
    def __init__(self, text="", is_user=False, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.setWordWrap(True)
        self.setText(text)
        
        if is_user:
            self.setStyleSheet("""
                MessageBubble {
                    background-color: rgba(0, 245, 255, 0.2);
                    border: 1px solid rgba(0, 245, 255, 0.5);
                    border-radius: 15px;
                    padding: 10px;
                    color: white;
                    font-size: 12px;
                }
            """)
        else:
            self.setStyleSheet("""
                MessageBubble {
                    background-color: rgba(28, 35, 51, 0.9);
                    border: 1px solid rgba(138, 216, 255, 0.3);
                    border-radius: 15px;
                    padding: 10px;
                    color: white;
                    font-size: 12px;
                }
            """)

class SystemMonitor(QWidget):
    """Real-time system monitoring widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = None
        self.setup_ui()
        
        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)  # Update every second
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Title
        title = QLabel("🧠 System Status")
        title.setStyleSheet("color: #00F5FF; font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Stats labels
        self.cpu_label = QLabel("CPU: --%")
        self.memory_label = QLabel("Memory: --%")
        self.gpu_label = QLabel("GPU: Active")
        self.model_label = QLabel("Model: --")
        
        for label in [self.cpu_label, self.memory_label, self.gpu_label, self.model_label]:
            label.setStyleSheet("color: #B0C3FF; font-size: 11px;")
            layout.addWidget(label)
            
        self.setLayout(layout)
        
    def set_controller(self, controller):
        self.controller = controller
        
    def update_stats(self):
        if self.controller:
            # Get context from controller
            try:
                context = self.controller.context_engine.get_full_context()
                system = context.get('system', {})
                
                self.cpu_label.setText(f"CPU: {system.get('cpu_usage', 0):.1f}%")
                self.memory_label.setText(f"Memory: {system.get('memory_usage', 0):.1f}%")
                self.gpu_label.setText(f"GPU: {'Active' if system.get('gpu_available') else 'Inactive'}")
                self.model_label.setText(f"Model: {self.controller.model}")
                
            except:
                pass

class TypingIndicator(QWidget):
    """Animated typing indicator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 20)
        self.animation_time = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(200)
        
    def update_animation(self):
        self.animation_time += 1
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        dot_size = 6
        spacing = 15
        start_x = (self.width() - (3 * dot_size + 2 * spacing)) // 2
        
        for i in range(3):
            # Animated opacity
            phase = (self.animation_time + i * 2) % 6
            if phase < 3:
                alpha = int(255 * (phase / 3))
            else:
                alpha = int(255 * (1 - (phase - 3) / 3))
                
            x = start_x + i * (dot_size + spacing)
            y = (self.height() - dot_size) // 2
            
            painter.setBrush(QBrush(QColor(0, 245, 255, alpha)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x, y, dot_size, dot_size)

# Continue with main window and complete interface...
if __name__ == "__main__":
    print("🎨 Ananta PyQt6 Interface Components Ready!")
    print("📋 Components created:")
    print("  ✅ OpenGLWidget - Particle effects")
    print("  ✅ GlassPanel - Glass morphism")
    print("  ✅ VoiceVisualizer - Voice bars")
    print("  ✅ MessageBubble - Chat bubbles")
    print("  ✅ SystemMonitor - Live stats")
    print("  ✅ TypingIndicator - Animated dots")
