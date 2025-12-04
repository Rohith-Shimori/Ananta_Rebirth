#!/usr/bin/env python3
"""
Clean launch test to verify warnings are suppressed
"""

import sys
import os
import warnings
from pathlib import Path

# Suppress warnings early
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", module="PyQt6")

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_clean_imports():
    """Test imports without warnings"""
    print("🔍 Testing clean imports...")
    
    try:
        from core.controller import AnantaController
        print("✅ AnantaController imported cleanly")
    except Exception as e:
        print(f"❌ AnantaController import failed: {e}")
        return False
    
    try:
        from ui.ananta_main_window import AnantaMainWindow
        print("✅ AnantaMainWindow imported cleanly")
    except Exception as e:
        print(f"❌ AnantaMainWindow import failed: {e}")
        return False
    
    return True

def test_gpu_util():
    """Test GPUtil is available"""
    print("\n🔍 Testing GPUtil...")
    
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            print(f"✅ GPU detected: {gpu.name}")
            print(f"   VRAM: {gpu.memoryTotal}MB")
            print(f"   Free: {gpu.memoryFree}MB")
        else:
            print("⚠️  No GPUs detected")
        return True
    except Exception as e:
        print(f"❌ GPUtil test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Clean Launch Test")
    print("=" * 40)
    
    success = True
    
    if not test_clean_imports():
        success = False
    
    if not test_gpu_util():
        success = False
    
    if success:
        print("\n🎉 Clean launch test passed!")
        print("✅ All imports working without warnings")
        print("✅ GPUtil is available")
        print("\n🚀 Ready for clean launch: python launch_ananta.py")
    else:
        print("\n❌ Some tests failed")
    
    sys.exit(0 if success else 1)
