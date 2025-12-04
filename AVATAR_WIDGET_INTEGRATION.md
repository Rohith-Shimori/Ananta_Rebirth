# 🎨 AVATAR WIDGET INTEGRATION GUIDE

**Status:** ✅ **CREATED & READY**  
**File:** `ui/avatar_widget.py`  
**Framework:** PyQt5 + QWebEngineView  
**Features:** Real-time emotion switching, speaking animation, holographic effects

---

## 🚀 QUICK START

### **1. Install Dependencies**

```bash
pip install PyQt5 PyQtWebEngine
```

### **2. Test Standalone Widget**

```bash
python ui/avatar_widget.py
```

This opens a test window with:
- Ananta's 2D avatar
- 5 emotion buttons (Neutral, Happy, Thinking, Concerned, Excited)
- Speaking toggle button
- Real-time animation

### **3. Integrate Into Your Main Window**

```python
from ui.avatar_widget import AvatarWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create avatar widget
        self.avatar_widget = AvatarWidget()
        
        # Add to layout
        self.main_layout.addWidget(self.avatar_widget, 0, 0)
```

---

## 📋 AVATAR WIDGET API

### **Constructor**

```python
avatar_widget = AvatarWidget(parent=None)
```

### **Methods**

#### **set_emotion(emotion: str)**
Set avatar emotion

```python
avatar_widget.set_emotion("happy")
# Options: "neutral", "happy", "thinking", "concerned", "excited"
```

#### **set_speaking(speaking: bool)**
Toggle speaking animation

```python
avatar_widget.set_speaking(True)   # Show speaking
avatar_widget.set_speaking(False)  # Stop speaking
```

#### **get_current_emotion() -> str**
Get current emotion

```python
emotion = avatar_widget.get_current_emotion()
print(emotion)  # "happy"
```

#### **get_speaking_state() -> bool**
Get speaking state

```python
is_speaking = avatar_widget.get_speaking_state()
print(is_speaking)  # True/False
```

---

## 🎯 INTEGRATION EXAMPLES

### **Example 1: Basic Integration**

```python
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.avatar_widget import AvatarWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Ananta - AI Assistant")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Add avatar
        self.avatar_widget = AvatarWidget()
        layout.addWidget(self.avatar_widget)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
```

### **Example 2: Connect to Chat**

```python
from ui.avatar_widget import AvatarWidget
from engines.ananta_personality import AnantaPersonality

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.avatar_widget = AvatarWidget()
        self.personality = AnantaPersonality()
        
        # Connect signals
        self.chat_input.returnPressed.connect(self.on_message_sent)
    
    def on_message_sent(self, message):
        """When user sends message"""
        # Set avatar to listening
        self.avatar_widget.set_emotion("thinking")
        
        # Process message
        response = self.personality.shape_response(
            "Processing...",
            {"text": message}
        )
        
        # Update avatar with response emotion
        self.avatar_widget.set_emotion(response.emotion)
        
        # Show speaking
        self.avatar_widget.set_speaking(True)
        
        # Display response
        self.chat_output.append(response.text)
        
        # Stop speaking after 2 seconds
        QTimer.singleShot(2000, lambda: self.avatar_widget.set_speaking(False))
```

### **Example 3: Full Workflow with Voice**

```python
from ui.avatar_widget import AvatarWidget
from voice.ananta_voice import AnantaVoice
from engines.ananta_personality import AnantaPersonality

class FullAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.avatar_widget = AvatarWidget()
        self.voice = AnantaVoice(skip_license=True)
        self.personality = AnantaPersonality()
    
    def respond_to_user(self, user_input):
        """Full response workflow"""
        # 1. Detect emotion and shape response
        context = {"text": user_input}
        response = self.personality.shape_response(
            "Here's my response",
            context
        )
        
        # 2. Update avatar emotion
        self.avatar_widget.set_emotion(response.emotion)
        
        # 3. Show speaking
        self.avatar_widget.set_speaking(True)
        
        # 4. Generate speech
        audio = self.voice.speak_with_emotion(
            response.text,
            emotion=response.emotion
        )
        
        # 5. Play audio (you'll need audio playback library)
        # self.play_audio(audio)
        
        # 6. Stop speaking after audio finishes
        QTimer.singleShot(3000, lambda: self.avatar_widget.set_speaking(False))
        
        return response
```

---

## 🎨 FEATURES

### **Emotions Supported**

1. **Neutral** 😐
   - Default calm expression
   - Used for listening/waiting

2. **Happy** 😊
   - Bright smile
   - Used for positive responses

3. **Thinking** 🤔
   - Thoughtful gaze
   - Particle effects
   - Used for processing

4. **Concerned** 😟
   - Gentle frown
   - Empathetic eyes
   - Used for warnings/concerns

5. **Excited** 🤩
   - Wide eyes
   - Particle effects
   - Used for celebrations

### **Visual Effects**

✅ **Holographic Glow** - Cyan/purple glow effect  
✅ **Scan Lines** - Animated scan lines overlay  
✅ **Breathing Animation** - Subtle breathing motion  
✅ **Blinking Eyes** - Natural eye blinking  
✅ **Speaking Animation** - Mouth animation when speaking  
✅ **Particle Effects** - For thinking and excited states  

---

## 🧪 TESTING

### **Test Standalone Widget**

```bash
python ui/avatar_widget.py
```

**What you'll see:**
- Ananta's 2D avatar in the center
- 5 emotion buttons below
- Speaking toggle button
- Real-time emotion changes
- Smooth animations

### **Test in Your Code**

```python
from ui.avatar_widget import AvatarWidget

widget = AvatarWidget()

# Test emotions
for emotion in ["neutral", "happy", "thinking", "concerned", "excited"]:
    widget.set_emotion(emotion)
    print(f"✅ {emotion}")

# Test speaking
widget.set_speaking(True)
print("🎤 Speaking")

widget.set_speaking(False)
print("🤐 Silent")
```

---

## 🔧 CUSTOMIZATION

### **Change Colors**

Edit the HTML in `update_avatar_display()`:

```python
# Change primary color
primary = '#FF1493'  # Hot pink instead of cyan

# Change secondary color
secondary = '#00BFFF'  # Deep sky blue instead of purple
```

### **Change Animation Speed**

```python
# In update_avatar_display(), modify CSS:
animation: breathing 2s ease-in-out infinite;  # Faster breathing
animation: scan-lines 4s linear infinite;      # Faster scan lines
```

### **Change Widget Size**

```python
self.web_view.setMinimumSize(400, 500)  # Larger
self.web_view.setMaximumSize(400, 500)
```

---

## 📦 DEPENDENCIES

```
PyQt5>=5.15.0
PyQtWebEngine>=5.15.0
```

Install with:
```bash
pip install PyQt5 PyQtWebEngine
```

---

## 🐛 TROUBLESHOOTING

### **Issue: "No module named 'PyQt5'"**

**Solution:**
```bash
pip install PyQt5 PyQtWebEngine
```

### **Issue: Avatar not displaying**

**Solution:**
- Check that `ui/ananta_avatar.py` exists
- Verify SVG generation is working
- Check browser console for errors

### **Issue: Emotions not changing**

**Solution:**
- Verify emotion names are correct
- Check that `set_emotion()` is being called
- Verify `update_avatar_display()` is working

### **Issue: Widget is too small/large**

**Solution:**
- Adjust `setMinimumSize()` and `setMaximumSize()`
- Modify SVG viewBox in avatar system

---

## 🚀 NEXT STEPS

### **Immediate (Today)**
- ✅ Install PyQt5
- ✅ Test standalone widget
- ✅ Verify all emotions work

### **Short Term (This Week)**
- [ ] Integrate into main window
- [ ] Connect to chat input
- [ ] Connect to voice system
- [ ] Add audio playback

### **Medium Term (This Month)**
- [ ] Add lip-sync animation
- [ ] Create more expressions
- [ ] Add custom animations
- [ ] Optimize performance

---

## 💡 TIPS

1. **Use QTimer for delayed actions**
   ```python
   QTimer.singleShot(2000, lambda: widget.set_speaking(False))
   ```

2. **Connect signals for real-time updates**
   ```python
   self.chat_input.returnPressed.connect(self.on_message)
   ```

3. **Keep animations smooth**
   - Update at 100ms intervals (10 FPS)
   - Use CSS animations for smoothness

4. **Test emotions frequently**
   - Each emotion should be visually distinct
   - Verify animations are smooth

---

## 📞 SUPPORT

**Questions?**
- Check the code comments in `avatar_widget.py`
- Review the integration examples above
- Test with `python ui/avatar_widget.py`

---

## ✨ SUMMARY

You now have:
- ✅ PyQt5 Avatar Widget
- ✅ 5 emotional expressions
- ✅ Speaking animation
- ✅ Holographic effects
- ✅ Real-time emotion switching
- ✅ Ready for integration

**Next:** Integrate into your main window and connect to chat! 🚀

---

**Ready to bring Ananta's face to life?** 🎨
