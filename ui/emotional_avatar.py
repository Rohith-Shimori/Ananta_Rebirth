"""
Emotional Avatar System
Dynamic avatar that responds to emotions, context, and interactions
"""

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
    """Emotional states for avatar"""
    HAPPY = "happy"
    CURIOUS = "curious"
    THINKING = "thinking"
    EXCITED = "excited"
    CALM = "calm"
    CONFUSED = "confused"
    EMPATHETIC = "empathetic"
    FOCUSED = "focused"

class Particle:
    """Individual particle in the avatar system"""
    
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.vz = random.uniform(-0.5, 0.5)
        self.life = 1.0
        self.max_life = 1.0
        self.size = random.uniform(2, 5)
        self.color = [1.0, 1.0, 1.0]
        self.energy = random.uniform(0.5, 1.0)
    
    def update(self, dt: float, emotion: EmotionalState):
        """Update particle based on emotion and physics"""
        # Emotion-based movement patterns
        if emotion == EmotionalState.HAPPY:
            # Bouncy, energetic movement
            self.vy += random.uniform(-0.1, 0.2)
            self.vx *= 0.98
            self.vy *= 0.98
            self.color = [1.0, 0.8, 0.2]  # Golden yellow
            
        elif emotion == EmotionalState.THINKING:
            # Slow, circular movement
            angle = dt * 0.5
            self.vx = math.cos(angle) * 0.3
            self.vy = math.sin(angle) * 0.3
            self.color = [0.2, 0.8, 1.0]  # Blue
            
        elif emotion == EmotionalState.EXCITED:
            # Fast, erratic movement
            self.vx += random.uniform(-0.3, 0.3)
            self.vy += random.uniform(-0.3, 0.3)
            self.color = [1.0, 0.2, 0.5]  # Pink/red
            
        elif emotion == EmotionalState.CALM:
            # Gentle floating
            self.vy += 0.05
            self.vx *= 0.95
            self.color = [0.5, 1.0, 0.5]  # Green
            
        elif emotion == EmotionalState.CURIOUS:
            # Exploratory movement
            self.vx += random.uniform(-0.1, 0.1)
            self.vy += random.uniform(-0.1, 0.1)
            self.color = [0.8, 0.5, 1.0]  # Purple
            
        elif emotion == EmotionalState.CONFUSED:
            # Erratic, uncertain movement
            self.vx += random.uniform(-0.4, 0.4)
            self.vy += random.uniform(-0.4, 0.4)
            self.color = [0.8, 0.6, 0.2]  # Orange
            
        elif emotion == EmotionalState.EMPATHETIC:
            # Flowing, wave-like movement
            wave = math.sin(dt * 2) * 0.2
            self.vx = wave
            self.vy = math.cos(dt * 2) * 0.1
            self.color = [1.0, 0.6, 0.8]  # Light pink
            
        elif emotion == EmotionalState.FOCUSED:
            # Concentric movement
            center_x, center_y = 0, 0
            dx = self.x - center_x
            dy = self.y - center_y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0.1:
                self.vx = -dx / dist * 0.2
                self.vy = -dy / dist * 0.2
            self.color = [0.2, 0.9, 0.8]  # Cyan
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt
        
        # Apply boundaries
        boundary = 2.0
        if abs(self.x) > boundary:
            self.vx *= -0.8
            self.x = max(-boundary, min(boundary, self.x))
        if abs(self.y) > boundary:
            self.vy *= -0.8
            self.y = max(-boundary, min(boundary, self.y))
        if abs(self.z) > boundary:
            self.vz *= -0.8
            self.z = max(-boundary, min(boundary, self.z))
        
        # Update life
        self.life -= dt * 0.1
        if self.life <= 0:
            self.respawn()
    
    def respawn(self):
        """Respawn particle at random position"""
        self.x = random.uniform(-1.5, 1.5)
        self.y = random.uniform(-1.5, 1.5)
        self.z = random.uniform(-1.5, 1.5)
        self.life = 1.0
        self.energy = random.uniform(0.5, 1.0)

class EmotionalAvatar(QOpenGLWidget):
    """Dynamic emotional avatar using OpenGL particles"""
    
    emotion_changed = pyqtSignal(EmotionalState)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_emotion = EmotionalState.CALM
        self.particles: List[Particle] = []
        self.time = 0
        self.rotation_x = 0
        self.rotation_y = 0
        self.energy_level = 0.5
        self.focus_point = [0, 0, 0]
        self.init_particles()
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS
        
    def init_particles(self):
        """Initialize particle system"""
        self.particles = []
        for _ in range(150):
            particle = Particle(
                random.uniform(-2, 2),
                random.uniform(-2, 2),
                random.uniform(-2, 2)
            )
            self.particles.append(particle)
    
    def set_emotion(self, emotion: EmotionalState):
        """Change emotional state"""
        if self.current_emotion != emotion:
            self.current_emotion = emotion
            self.emotion_changed.emit(emotion)
            
            # Boost energy on emotion change
            self.energy_level = min(1.0, self.energy_level + 0.3)
    
    def set_energy_level(self, level: float):
        """Set energy level (0.0 to 1.0)"""
        self.energy_level = max(0.0, min(1.0, level))
    
    def focus_on_point(self, x: float, y: float, z: float):
        """Make avatar focus on a specific point"""
        self.focus_point = [x, y, z]
    
    def initializeGL(self):
        """Initialize OpenGL"""
        gl.glClearColor(0.0, 0.0, 0.0, 0.0)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_POINT_SMOOTH)
        gl.glHint(gl.GL_POINT_SMOOTH_HINT, gl.GL_NICEST)
        
        # Setup shaders
        self.setup_shaders()
    
    def setup_shaders(self):
        """Setup vertex and fragment shaders"""
        vertex_shader = """
        #version 120
        attribute vec3 position;
        attribute vec3 color;
        attribute float size;
        attribute float alpha;
        
        uniform mat4 projection;
        uniform mat4 modelview;
        
        varying vec3 fragColor;
        varying float fragAlpha;
        
        void main() {
            gl_Position = projection * modelview * vec4(position, 1.0);
            gl_PointSize = size;
            fragColor = color;
            fragAlpha = alpha;
        }
        """
        
        fragment_shader = """
        #version 120
        varying vec3 fragColor;
        varying float fragAlpha;
        
        void main() {
            vec2 coord = gl_PointCoord - vec2(0.5);
            float dist = length(coord);
            
            if (dist > 0.5) {
                discard;
            }
            
            float alpha = (1.0 - dist * 2.0) * fragAlpha;
            gl_FragColor = vec4(fragColor, alpha);
        }
        """
        
        try:
            self.shader_program = shaders.compileProgram(
                shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
                shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
            )
        except:
            # Fallback to fixed pipeline if shaders fail
            self.shader_program = None
    
    def resizeGL(self, width: int, height: int):
        """Handle widget resize"""
        gl.glViewport(0, 0, width, height)
        aspect = width / height if height > 0 else 1
        
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # Use gluPerspective instead of deprecated glPerspective
        from OpenGL.GLU import gluPerspective
        gluPerspective(45, aspect, 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def paintGL(self):
        """Render the avatar"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        
        # Camera position
        gl.glTranslatef(0.0, 0.0, -8.0)
        gl.glRotatef(self.rotation_x, 1, 0, 0)
        gl.glRotatef(self.rotation_y, 0, 1, 0)
        
        if self.shader_program:
            self.render_with_shaders()
        else:
            self.render_fixed_function()
    
    def render_with_shaders(self):
        """Render using shader program"""
        gl.glUseProgram(self.shader_program)
        
        # Prepare vertex data
        vertices = []
        colors = []
        sizes = []
        alphas = []
        
        for particle in self.particles:
            vertices.extend([particle.x, particle.y, particle.z])
            colors.extend(particle.color)
            sizes.append(particle.size * particle.energy * self.energy_level)
            alphas.append(particle.life * 0.8)
        
        # Convert to numpy arrays
        vertices = np.array(vertices, dtype=np.float32)
        colors = np.array(colors, dtype=np.float32)
        sizes = np.array(sizes, dtype=np.float32)
        alphas = np.array(alphas, dtype=np.float32)
        
        # Set attributes
        position_loc = gl.glGetAttribLocation(self.shader_program, "position")
        color_loc = gl.glGetAttribLocation(self.shader_program, "color")
        size_loc = gl.glGetAttribLocation(self.shader_program, "size")
        alpha_loc = gl.glGetAttribLocation(self.shader_program, "alpha")
        
        gl.glEnableVertexAttribArray(position_loc)
        gl.glEnableVertexAttribArray(color_loc)
        gl.glEnableVertexAttribArray(size_loc)
        gl.glEnableVertexAttribArray(alpha_loc)
        
        gl.glVertexAttribPointer(position_loc, 3, gl.GL_FLOAT, False, 0, vertices)
        gl.glVertexAttribPointer(color_loc, 3, gl.GL_FLOAT, False, 0, colors)
        gl.glVertexAttribPointer(size_loc, 1, gl.GL_FLOAT, False, 0, sizes)
        gl.glVertexAttribPointer(alpha_loc, 1, gl.GL_FLOAT, False, 0, alphas)
        
        # Draw particles
        gl.glDrawArrays(gl.GL_POINTS, 0, len(self.particles))
        
        # Cleanup
        gl.glDisableVertexAttribArray(position_loc)
        gl.glDisableVertexAttribArray(color_loc)
        gl.glDisableVertexAttribArray(size_loc)
        gl.glDisableVertexAttribArray(alpha_loc)
        
        gl.glUseProgram(0)
    
    def render_fixed_function(self):
        """Fallback rendering with fixed function pipeline"""
        gl.glBegin(gl.GL_POINTS)
        
        for particle in self.particles:
            alpha = particle.life * 0.8
            size = particle.size * particle.energy * self.energy_level
            
            gl.glColor4f(particle.color[0], particle.color[1], particle.color[2], alpha)
            gl.glPointSize(size)
            gl.glVertex3f(particle.x, particle.y, particle.z)
        
        gl.glEnd()
    
    def update_animation(self):
        """Update animation frame"""
        dt = 0.016  # 16ms timestep
        
        self.time += dt
        
        # Slow rotation
        self.rotation_y += dt * 10
        
        # Update particles
        for particle in self.particles:
            particle.update(dt, self.current_emotion)
        
        # Decay energy level
        self.energy_level *= 0.995
        
        # Trigger redraw
        self.update()
    
    def analyze_text_emotion(self, text: str) -> EmotionalState:
        """Analyze text to determine appropriate emotion"""
        text_lower = text.lower()
        
        # Emotion keywords
        if any(word in text_lower for word in ["happy", "great", "awesome", "wonderful", "love"]):
            return EmotionalState.HAPPY
        elif any(word in text_lower for word in ["think", "wonder", "consider", "analyze"]):
            return EmotionalState.THINKING
        elif any(word in text_lower for word in ["excited", "amazing", "wow", "incredible"]):
            return EmotionalState.EXCITED
        elif any(word in text_lower for word in ["calm", "relax", "peace", "quiet"]):
            return EmotionalState.CALM
        elif any(word in text_lower for word in ["curious", "interested", "how", "why"]):
            return EmotionalState.CURIOUS
        elif any(word in text_lower for word in ["confused", "unclear", "don't understand"]):
            return EmotionalState.CONFUSED
        elif any(word in text_lower for word in ["sad", "upset", "worried", "stressed"]):
            return EmotionalState.EMPATHETIC
        elif any(word in text_lower for word in ["focus", "concentrate", "work", "task"]):
            return EmotionalState.FOCUSED
        else:
            return EmotionalState.CALM
    
    def react_to_message(self, message: str, is_user: bool = False):
        """React to a message with emotion and animation"""
        emotion = self.analyze_text_emotion(message)
        self.set_emotion(emotion)
        
        # Boost energy based on message
        self.energy_level = min(1.0, self.energy_level + 0.2)
        
        # Focus on user if they sent message
        if is_user:
            self.focus_on_point(0, -1, 0)
    
    def get_current_emotion(self) -> EmotionalState:
        """Get current emotional state"""
        return self.current_emotion
    
    def get_energy_level(self) -> float:
        """Get current energy level"""
        return self.energy_level

# Example usage
if __name__ == "__main__":
    app = QApplication([])
    
    window = QWidget()
    layout = QVBoxLayout(window)
    
    avatar = EmotionalAvatar()
    avatar.setFixedSize(400, 400)
    layout.addWidget(avatar)
    
    # Emotion controls
    emotions_layout = QHBoxLayout()
    for emotion in EmotionalState:
        btn = QPushButton(emotion.value.title())
        btn.clicked.connect(lambda checked, e=emotion: avatar.set_emotion(e))
        emotions_layout.addWidget(btn)
    
    layout.addLayout(emotions_layout)
    
    window.show()
    app.exec()
