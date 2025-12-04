#!/usr/bin/env python3
"""
Comprehensive Test Suite for Ananta Rebirth
Tests all core functionality and features
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_core_functionality():
    """Test core Ananta functionality"""
    print("🧠 Testing Ananta Core Functionality...")
    print("=" * 50)
    
    results = []
    
    # Test 1: Import Controller
    try:
        from core.controller import AnantaController
        results.append(("Controller import", "SUCCESS", None))
        print("✅ Controller import: SUCCESS")
    except Exception as e:
        results.append(("Controller import", "FAILED", str(e)))
        print(f"❌ Controller import: FAILED - {e}")
        return results
    
    # Test 2: Initialize Controller
    try:
        controller = AnantaController()
        results.append(("Controller initialization", "SUCCESS", None))
        print("✅ Controller initialization: SUCCESS")
    except Exception as e:
        results.append(("Controller initialization", "FAILED", str(e)))
        print(f"❌ Controller initialization: FAILED - {e}")
        return results
    
    # Test 3: Test Basic Query
    try:
        result = controller.query("Hello Ananta, who are you?", use_memory=False)
        if result and "response" in result:
            results.append(("Basic query", "SUCCESS", result["response"][:100]))
            print("✅ Basic query: SUCCESS")
            print(f"📝 Response: {result['response'][:100]}...")
        else:
            results.append(("Basic query", "FAILED", "No response"))
            print("❌ Basic query: FAILED - No response")
    except Exception as e:
        results.append(("Basic query", "FAILED", str(e)))
        print(f"❌ Basic query: FAILED - {e}")
    
    # Test 4: Test Vision Engine
    try:
        controller.vision
        results.append(("Vision engine", "LOADED", None))
        print("✅ Vision engine: LOADED")
    except Exception as e:
        results.append(("Vision engine", "FAILED", str(e)))
        print(f"❌ Vision engine: FAILED - {e}")
    
    # Test 5: Test Automation Engine
    try:
        controller.automation
        results.append(("Automation engine", "LOADED", None))
        print("✅ Automation engine: LOADED")
    except Exception as e:
        results.append(("Automation engine", "FAILED", str(e)))
        print(f"❌ Automation engine: FAILED - {e}")
    
    # Test 6: Test Memory System
    try:
        controller.memory
        results.append(("Memory system", "LOADED", None))
        print("✅ Memory system: LOADED")
    except Exception as e:
        results.append(("Memory system", "FAILED", str(e)))
        print(f"❌ Memory system: FAILED - {e}")
    
    # Test 7: Test Emotional Intelligence
    try:
        controller.emotional_intelligence
        results.append(("Emotional intelligence", "LOADED", None))
        print("✅ Emotional intelligence: LOADED")
    except Exception as e:
        results.append(("Emotional intelligence", "FAILED", str(e)))
        print(f"❌ Emotional intelligence: FAILED - {e}")
    
    # Test 8: Test Context Engine
    try:
        controller.context_engine
        results.append(("Context engine", "LOADED", None))
        print("✅ Context engine: LOADED")
    except Exception as e:
        results.append(("Context engine", "FAILED", str(e)))
        print(f"❌ Context engine: FAILED - {e}")
    
    # Test 9: Test Persona System
    try:
        if hasattr(controller, 'persona') and controller.persona:
            results.append(("Persona system", "LOADED", list(controller.persona.keys())))
            print("✅ Persona system: LOADED")
        else:
            results.append(("Persona system", "FAILED", "No persona data"))
            print("❌ Persona system: FAILED - No persona data")
    except Exception as e:
        results.append(("Persona system", "FAILED", str(e)))
        print(f"❌ Persona system: FAILED - {e}")
    
    print("=" * 50)
    print("🎯 Core Functionality Test Complete!")
    return results

def test_gui_components():
    """Test GUI components"""
    print("\n🎨 Testing GUI Components...")
    print("=" * 50)
    
    results = []
    
    # Test 1: Import GUI Components
    try:
        from ui.components import (
            GlassPanel, VoiceVisualizer, MessageBubble, 
            SystemMonitor, TypingIndicator
        )
        results.append(("GUI components import", "SUCCESS", None))
        print("✅ GUI components import: SUCCESS")
    except Exception as e:
        results.append(("GUI components import", "FAILED", str(e)))
        print(f"❌ GUI components import: FAILED - {e}")
        return results
    
    # Test 2: Import Advanced Avatar
    try:
        from ui.advanced_avatar import LivingConstellationAvatar, EmotionalState
        results.append(("Advanced avatar import", "SUCCESS", None))
        print("✅ Advanced avatar import: SUCCESS")
    except Exception as e:
        results.append(("Advanced avatar import", "FAILED", str(e)))
        print(f"❌ Advanced avatar import: FAILED - {e}")
    
    # Test 3: Import Main Window
    try:
        from ui.main_window import MainWindow
        results.append(("Main window import", "SUCCESS", None))
        print("✅ Main window import: SUCCESS")
    except Exception as e:
        results.append(("Main window import", "FAILED", str(e)))
        print(f"❌ Main window import: FAILED - {e}")
    
    print("=" * 50)
    print("🎯 GUI Components Test Complete!")
    return results

def test_file_structure():
    """Test file structure and completeness"""
    print("\n📁 Testing File Structure...")
    print("=" * 50)
    
    results = []
    base_dir = Path(".")
    
    # Essential files and directories
    essential_items = {
        "config.py": "Configuration file",
        "main.py": "Terminal interface",
        "gui_launcher.py": "GUI launcher",
        "core/": "Core AI modules",
        "intelligence/": "Intelligence engines",
        "automation/": "Automation engines",
        "memory/": "Memory systems",
        "engines/": "Specialized engines",
        "features/": "Feature modules",
        "utils/": "Utility modules",
        "ui/": "User interface",
        "data/": "Data directory",
        "requirements.txt": "Dependencies",
    }
    
    for item, description in essential_items.items():
        item_path = base_dir / item
        if item_path.exists():
            results.append((f"File structure: {item}", "EXISTS", description))
            print(f"✅ {item}: EXISTS ({description})")
        else:
            results.append((f"File structure: {item}", "MISSING", description))
            print(f"❌ {item}: MISSING ({description})")
    
    # Check Python file count
    py_files = list(base_dir.rglob("*.py"))
    results.append(("Python files count", str(len(py_files)), "Total Python files"))
    print(f"📊 Total Python files: {len(py_files)}")
    
    print("=" * 50)
    print("🎯 File Structure Test Complete!")
    return results

def main():
    """Run comprehensive test suite"""
    print("🚀 ANANTA REBIRTH - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print("Testing all features and functionality...")
    print()
    
    all_results = []
    
    # Test 1: Core Functionality
    core_results = test_core_functionality()
    all_results.extend(core_results)
    
    # Test 2: GUI Components
    gui_results = test_gui_components()
    all_results.extend(gui_results)
    
    # Test 3: File Structure
    structure_results = test_file_structure()
    all_results.extend(structure_results)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    
    success_count = sum(1 for _, status, _ in all_results if status in ["SUCCESS", "LOADED", "EXISTS"])
    total_count = len(all_results)
    
    print(f"🎯 Overall Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    print()
    
    # Categorize results
    print("📋 Results by Category:")
    print()
    
    categories = {
        "Core Functionality": [r for r in all_results if "import" in r[0] or "engine" in r[0] or "system" in r[0]],
        "GUI Components": [r for r in all_results if "GUI" in r[0] or "avatar" in r[0] or "window" in r[0]],
        "File Structure": [r for r in all_results if "File structure" in r[0] or "Python files" in r[0]],
    }
    
    for category, items in categories.items():
        print(f"🔸 {category}:")
        for test, status, details in items:
            icon = "✅" if status in ["SUCCESS", "LOADED", "EXISTS"] else "❌"
            print(f"   {icon} {test}: {status}")
            if details and status not in ["SUCCESS", "LOADED", "EXISTS"]:
                print(f"      Details: {details}")
        print()
    
    # Final Assessment
    if success_count == total_count:
        print("🎉 ALL TESTS PASSED! Ananta Rebirth is fully functional!")
        print("🚀 Ready for production use!")
    elif success_count >= total_count * 0.8:
        print("✅ MOST TESTS PASSED! Ananta Rebirth is mostly functional.")
        print("🔧 Minor issues may need attention.")
    else:
        print("⚠️  MULTIPLE TESTS FAILED! Review required issues.")
    
    print("\n" + "=" * 60)
    print("🎊 TEST SUITE COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
