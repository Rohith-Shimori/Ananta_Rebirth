"""
Ananta Rebirth - Living Constellation Morphing Entity Avatar
Advanced 3D OpenGL avatar with emotion-responsive morphing
"""

import sys
import math
import random
from typing import List, Tuple, Dict
from enum import Enum

import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

import OpenGL.GL as gl
from OpenGL.arrays import vbo
import OpenGL.GL.shaders as shaders

class EmotionalState(Enum):
    """Ananta's emotional states"""
    JOY = "joy"
    THINKING = "thinking"
    POWER = "power"
    EMPATHETIC = "empathetic"
    QUANTUM = "quantum"
    NEUTRAL = "neutral"

class ConstellationNode:
    """Individual star node in the constellation"""
    
    def __init__(self, x: float, y: float, z: float):
        self.base_position = np.array([x, y, z], dtype=np.float32)
        self.position = self.base_position.copy()
        self.velocity = np.random.randn(3) * 0.001
        self.phase = random.random() * 2 * math.pi
        self.frequency = random.uniform(0.5, 2.0)
        self.amplitude = random.uniform(0.1, 0.3)
        self.brightness = random.uniform(0.3, 1.0)
        self.size = random.uniform(2, 5)
        self.connections = []  # Connected nodes
        
    def update(self, time: float, emotion: EmotionalState, morph_factor: float):
        """Update node position based on emotion and time"""
        # Base orbital motion
        angle = self.phase + time * self.frequency
        
        # Emotion-based movement patterns
        if emotion == EmotionalState.JOY:
            # Expanding, celebratory motion
            expansion = math.sin(time * 2) * 0.1
            self.position = self.base_position * (1 + expansion * morph_factor)
            self.position[1] += math.sin(angle) * self.amplitude * 0.5
            
        elif emotion == EmotionalState.THINKING:
            # Concentrated, organized motion
            contraction = 0.8 + 0.2 * math.sin(time * 3)
            self.position = self.base_position * contraction
            self.position[2] += math.cos(angle * 2) * 0.05
            
        elif emotion == EmotionalState.POWER:
            # Explosive, energetic motion
            pulse = (math.sin(time * 4) + 1) * 0.5
            self.position = self.base_position * (1 + pulse * 0.3 * morph_factor)
            self.position += np.random.randn(3) * 0.02 * pulse
            
        elif emotion == EmotionalState.EMPATHETIC:
            # Gentle, flowing motion
            wave = math.sin(time + self.phase) * 0.1
            self.position = self.base_position + np.array([wave, wave * 0.5, 0])
            
        elif emotion == EmotionalState.QUANTUM:
            # Multi-dimensional shifting
            shift = math.sin(time * 5 + self.phase) * 0.2
            self.position = self.base_position + np.array([shift, -shift, shift * 0.5])
            
        else:  # NEUTRAL
            # Calm, stable motion
            self.position = self.base_position + np.array([
                math.sin(angle) * self.amplitude * 0.3,
                math.cos(angle * 1.5) * self.amplitude * 0.3,
                math.sin(angle * 0.7) * self.amplitude * 0.1
            ])
            
        # Update brightness based on emotion
        self.update_brightness(emotion, time)
        
    def update_brightness(self, emotion: EmotionalState, time: float):
        """Update node brightness based on emotional state"""
        base_brightness = self.brightness
        
        if emotion == EmotionalState.JOY:
            self.brightness = base_brightness * (0.8 + 0.2 * math.sin(time * 3))
        elif emotion == EmotionalState.POWER:
            self.brightness = base_brightness * (0.7 + 0.3 * abs(math.sin(time * 6)))
        elif emotion == EmotionalState.EMPATHETIC:
            self.brightness = base_brightness * (0.6 + 0.4 * math.sin(time * 2))
        else:
            self.brightness = base_brightness * (0.7 + 0.3 * math.sin(time + self.phase))

class DataStream:
    """Flowing data stream between nodes"""
    
    def __init__(self, node1: ConstellationNode, node2: ConstellationNode):
        self.node1 = node1
        self.node2 = node2
        self.flow_phase = random.random() * 2 * math.pi
        self.flow_speed = random.uniform(2, 4)
        self.particle_positions = np.random.random(5)  # 5 particles per stream
        
    def update(self, time: float):
        """Update data stream flow"""
        self.flow_phase = (self.flow_phase + self.flow_speed * 0.016) % (2 * math.pi)
        
        # Update particle positions along the stream
        for i in range(len(self.particle_positions)):
            self.particle_positions[i] = (self.particle_positions[i] + 0.02) % 1.0

class LivingConstellationAvatar(QOpenGLWidget):
    """Living Constellation Morphing Entity Avatar"""
    
    emotion_changed = pyqtSignal(str)
    
    def __init__(self, size: int = 150, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        
        # Avatar properties
        self.size = size
        self.time = 0
        self.current_emotion = EmotionalState.NEUTRAL
        self.morph_factor = 0.0  # Morphing transition factor
        self.target_emotion = EmotionalState.NEUTRAL
        
        # Constellation components
        self.nodes: List[ConstellationNode] = []
        self.data_streams: List[DataStream] = []
        self.core_particles: List[np.ndarray] = []
        
        # Animation
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(16)  # 60 FPS
        
        # Mouse interaction
        self.mouse_position = np.array([0.5, 0.5])
        self.is_mouse_over = False
        self.setMouseTracking(True)
        
        # Initialize constellation
        self.initialize_constellation()
        
    def initialize_constellation(self):
        """Initialize the constellation structure"""
        # Create central core nodes
        core_radius = 0.15
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            x = math.cos(angle) * core_radius
            y = math.sin(angle) * core_radius
            z = random.uniform(-0.05, 0.05)
            self.nodes.append(ConstellationNode(x, y, z))
            
        # Create orbital rings
        for ring in range(3):
            radius = 0.3 + ring * 0.2
            nodes_in_ring = 12 + ring * 4
            
            for i in range(nodes_in_ring):
                angle = (i / nodes_in_ring) * 2 * math.pi
                x = math.cos(angle) * radius
                y = math.sin(angle) * radius
                z = random.uniform(-0.1, 0.1)
                self.nodes.append(ConstellationNode(x, y, z))
                
        # Create outer constellation nodes
        for _ in range(20):
            # Spherical distribution
            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)
            r = random.uniform(0.6, 0.8)
            
            x = r * math.sin(phi) * math.cos(theta)
            y = r * math.sin(phi) * math.sin(theta)
            z = r * math.cos(phi)
            
            self.nodes.append(ConstellationNode(x, y, z))
            
        # Create connections (data streams)
        self.create_connections()
        
        # Create core particles
        for _ in range(50):
            pos = np.random.randn(3) * 0.05
            self.core_particles.append(pos)
            
    def create_connections(self):
        """Create data stream connections between nodes"""
        # Connect nearby nodes
        for i, node1 in enumerate(self.nodes):
            for j, node2 in enumerate(self.nodes[i+1:], i+1):
                distance = np.linalg.norm(node1.base_position - node2.base_position)
                
                # Connect if within threshold
                if distance < 0.3 and random.random() < 0.7:
                    self.data_streams.append(DataStream(node1, node2))
                    node1.connections.append(node2)
                    node2.connections.append(node1)
                    
    def initializeGL(self):
        """Initialize OpenGL context"""
        gl.glClearColor(0.01, 0.02, 0.04, 1.0)  # Deep space background
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_POINT_SMOOTH)
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glHint(gl.GL_POINT_SMOOTH_HINT, gl.GL_NICEST)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
        
    def resizeGL(self, w: int, h: int):
        """Handle widget resize"""
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-1, 1, -1, 1, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        
    def paintGL(self):
        """Render the avatar"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glLoadIdentity()
        
        # Apply mouse interaction
        if self.is_mouse_over:
            gl.glTranslatef(
                (self.mouse_position[0] - 0.5) * 0.1,
                (self.mouse_position[1] - 0.5) * 0.1,
                0
            )
            
        # Draw core energy
        self.draw_core_energy()
        
        # Draw data streams
        self.draw_data_streams()
        
        # Draw constellation nodes
        self.draw_constellation_nodes()
        
        # Draw morphing tendrils
        self.draw_morphing_tendrils()
        
        # Draw energy field
        self.draw_energy_field()
        
    def draw_core_energy(self):
        """Draw central energy core"""
        gl.glPointSize(8.0)
        gl.glBegin(gl.GL_POINTS)
        
        # Pulsing core
        pulse = (math.sin(self.time * 3) + 1) * 0.5
        core_color = self.get_emotion_color(self.current_emotion, pulse)
        
        for particle in self.core_particles:
            # Animate particles
            particle[0] += math.sin(self.time * 2 + particle[1]) * 0.001
            particle[1] += math.cos(self.time * 2 + particle[0]) * 0.001
            particle[2] += math.sin(self.time * 3) * 0.001
            
            # Keep particles bounded
            for i in range(3):
                if abs(particle[i]) > 0.1:
                    particle[i] *= 0.95
                    
            gl.glColor4f(*core_color)
            gl.glVertex3f(*particle)
            
        gl.glEnd()
        
    def draw_data_streams(self):
        """Draw flowing data streams"""
        gl.glLineWidth(1.5)
        gl.glBegin(gl.GL_LINES)
        
        stream_color = self.get_emotion_color(self.current_emotion, 0.6)
        gl.glColor4f(*stream_color)
        
        for stream in self.data_streams:
            # Draw base connection
            gl.glVertex3f(*stream.node1.position)
            gl.glVertex3f(*stream.node2.position)
            
        gl.glEnd()
        
        # Draw flowing particles along streams
        gl.glPointSize(3.0)
        gl.glBegin(gl.GL_POINTS)
        
        for stream in self.data_streams:
            for particle_pos in stream.particle_positions:
                # Interpolate position along stream
                pos = stream.node1.position * (1 - particle_pos) + stream.node2.position * particle_pos
                
                # Add wave motion
                wave = math.sin(stream.flow_phase + particle_pos * 10) * 0.02
                pos[1] += wave
                
                gl.glColor4f(*stream_color)
                gl.glVertex3f(*pos)
                
        gl.glEnd()
        
    def draw_constellation_nodes(self):
        """Draw constellation nodes"""
        gl.glPointSize(4.0)
        gl.glBegin(gl.GL_POINTS)
        
        for node in self.nodes:
            # Node color based on emotion and brightness
            color = self.get_emotion_color(self.current_emotion, node.brightness)
            gl.glColor4f(*color)
            gl.glVertex3f(*node.position)
            
        gl.glEnd()
        
    def draw_morphing_tendrils(self):
        """Draw morphing energy tendrils"""
        if self.morph_factor > 0.1:
            gl.glLineWidth(2.0)
            gl.glBegin(gl.GL_LINES)
            
            # Create dynamic tendrils from outer nodes
            for node in self.nodes[:10]:  # Limit for performance
                if np.linalg.norm(node.position) > 0.5:
                    # Create tendril endpoints
                    for angle in range(0, 360, 45):
                        rad = math.radians(angle + self.time * 50)
                        end_x = node.position[0] + math.cos(rad) * 0.2 * self.morph_factor
                        end_y = node.position[1] + math.sin(rad) * 0.2 * self.morph_factor
                        end_z = node.position[2] + math.sin(self.time * 3) * 0.1 * self.morph_factor
                        
                        tendril_color = self.get_emotion_color(self.current_emotion, 0.3 * self.morph_factor)
                        gl.glColor4f(*tendril_color)
                        
                        gl.glVertex3f(*node.position)
                        gl.glVertex3f(end_x, end_y, end_z)
                        
            gl.glEnd()
            
    def draw_energy_field(self):
        """Draw surrounding energy field"""
        gl.glLineWidth(1.0)
        gl.glBegin(gl.GL_LINE_LOOP)
        
        # Rotating energy ring
        segments = 32
        field_color = self.get_emotion_color(self.current_emotion, 0.2)
        gl.glColor4f(*field_color)
        
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi + self.time
            radius = 0.9 + 0.05 * math.sin(self.time * 2)
            
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = math.sin(angle * 2) * 0.1
            
            gl.glVertex3f(x, y, z)
            
        gl.glEnd()
        
    def get_emotion_color(self, emotion: EmotionalState, intensity: float) -> Tuple[float, float, float, float]:
        """Get color based on emotional state"""
        colors = {
            EmotionalState.JOY: (1.0, 0.8, 0.2, intensity),      # Gold
            EmotionalState.THINKING: (0.2, 0.6, 1.0, intensity),  # Blue
            EmotionalState.POWER: (0.8, 0.2, 1.0, intensity),    # Purple
            EmotionalState.EMPATHETIC: (1.0, 0.4, 0.8, intensity), # Pink
            EmotionalState.QUANTUM: (0.2, 1.0, 0.8, intensity),  # Cyan
            EmotionalState.NEUTRAL: (0.0, 0.96, 1.0, intensity)  # Cyan
        }
        return colors.get(emotion, colors[EmotionalState.NEUTRAL])
        
    def update_animation(self):
        """Update animation frame"""
        self.time += 0.016  # 60 FPS
        
        # Update morphing transition
        if self.morph_factor < 1.0 and self.target_emotion != self.current_emotion:
            self.morph_factor = min(1.0, self.morph_factor + 0.02)
            if self.morph_factor >= 1.0:
                self.current_emotion = self.target_emotion
                self.morph_factor = 0.0
                
        # Update nodes
        for node in self.nodes:
            node.update(self.time, self.current_emotion, self.morph_factor)
            
        # Update data streams
        for stream in self.data_streams:
            stream.update(self.time)
            
        self.update()
        
    def set_emotion(self, emotion: str):
        """Set emotional state"""
        try:
            new_emotion = EmotionalState(emotion.lower())
            if new_emotion != self.current_emotion:
                self.target_emotion = new_emotion
                self.morph_factor = 0.0
                self.emotion_changed.emit(emotion)
        except ValueError:
            pass
            
    def enterEvent(self, event):
        """Handle mouse enter"""
        self.is_mouse_over = True
        
    def leaveEvent(self, event):
        """Handle mouse leave"""
        self.is_mouse_over = False
        
    def mouseMoveEvent(self, event):
        """Handle mouse movement"""
        if self.is_mouse_over:
            self.mouse_position[0] = event.position().x() / self.width()
            self.mouse_position[1] = event.position().y() / self.height()

# Test the avatar
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("Living Constellation Avatar Test")
    window.setFixedSize(200, 200)
    
    layout = QVBoxLayout(window)
    
    avatar = LivingConstellationAvatar(150)
    layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignCenter)
    
    # Emotion control
    emotions = ["joy", "thinking", "power", "empathetic", "quantum", "neutral"]
    emotion_combo = QComboBox()
    emotion_combo.addItems(emotions)
    emotion_combo.currentTextChanged.connect(avatar.set_emotion)
    layout.addWidget(emotion_combo)
    
    window.show()
    sys.exit(app.exec())
