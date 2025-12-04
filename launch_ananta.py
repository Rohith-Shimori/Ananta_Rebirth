#!/usr/bin/env python3
"""
Ananta Rebirth Launcher
Launches the new, stunning UI with all real features
"""

import sys
import os
import warnings
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", module="PyQt6")

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main launcher function"""
    try:
        # Import after path setup
        from PyQt6.QtWidgets import QApplication
        from ui.ananta_main_window import AnantaMainWindow
        
        # Create application
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # Set application properties
        app.setApplicationName("Ananta Rebirth")
        app.setApplicationVersion("2.0")
        app.setOrganizationName("Ananta AI")
        
        # Create and show main window
        window = AnantaMainWindow()
        window.show()
        
        # Start event loop
        return app.exec()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install PyQt6 pyopengl numpy")
        return 1
    except Exception as e:
        print(f"❌ Error launching Ananta: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
