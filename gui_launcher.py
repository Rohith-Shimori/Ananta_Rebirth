"""
Ananta Rebirth - GUI Launcher
Launch the PyQt6 interface
"""

import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from ui.jarvis_like_interface import main
    
    print("🚀 Starting Ananta Rebirth GUI...")
    print("🎨 PyQt6 Interface Loading...")
    print("🧠 Initializing AI Controller...")
    print("👁️ Vision Engine Ready...")
    print("🤖 Automation System Ready...")
    print("💫 Loading Interface...")
    
    main()
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\n📦 Required packages:")
    print("  pip install PyQt6 PyQt6-OpenGL PyOpenGL numpy")
    print("\n🔧 Or run:")
    print("  pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Error launching interface: {e}")
    input("Press Enter to exit...")
