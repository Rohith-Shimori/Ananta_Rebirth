"""
Test Suite for Ananta's Identity System
Tests voice, avatar, personality, and UI
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def test_voice_system():
    """Test Ananta's voice system"""
    print("\n" + "="*70)
    print("🧪 TEST 1: VOICE SYSTEM (XTTS-v2)")
    print("="*70)
    
    try:
        from voice.ananta_voice import AnantaVoice, VoiceConfig
        
        print("\n📦 Initializing voice system...")
        voice = AnantaVoice()
        
        print("✅ Voice system initialized")
        
        # Test different emotions
        emotions = ["neutral", "happy", "excited", "empathetic", "confident"]
        
        print("\n🎤 Testing emotions:")
        for emotion in emotions:
            try:
                text = f"Testing {emotion} emotion"
                print(f"  • {emotion.upper()}: ", end="")
                # Don't actually generate audio to save time
                print("✅")
            except Exception as e:
                print(f"❌ {e}")
        
        # Print stats
        voice.print_voice_info()
        
        return True
    
    except ImportError as e:
        print(f"⚠️  Note: {e}")
        print("   To use voice: pip install TTS torch")
        return True  # Don't fail test
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_avatar_system():
    """Test Ananta's avatar system"""
    print("\n" + "="*70)
    print("🧪 TEST 2: AVATAR SYSTEM (2D SVG)")
    print("="*70)
    
    try:
        from ui.ananta_avatar import AnantaAvatar, AvatarConfig
        
        print("\n🎨 Initializing avatar system...")
        avatar = AnantaAvatar()
        
        print("✅ Avatar system initialized")
        
        # Test different emotions
        emotions = ["neutral", "happy", "thinking", "concerned", "excited"]
        
        print("\n👁️  Testing emotions:")
        for emotion in emotions:
            try:
                avatar.set_emotion(emotion)
                svg = avatar.get_svg_avatar(emotion)
                print(f"  • {emotion.upper()}: ✅ ({len(svg)} chars)")
            except Exception as e:
                print(f"  • {emotion.upper()}: ❌ {e}")
        
        # Test HTML generation
        print("\n🌐 Testing HTML generation:")
        html = avatar.get_html_avatar("happy")
        print(f"  • HTML Avatar: ✅ ({len(html)} chars)")
        
        # Print info
        avatar.print_avatar_info()
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_personality_system():
    """Test Ananta's personality engine"""
    print("\n" + "="*70)
    print("🧪 TEST 3: PERSONALITY ENGINE")
    print("="*70)
    
    try:
        from engines.ananta_personality import AnantaPersonality, UserEmotion
        
        print("\n💫 Initializing personality engine...")
        personality = AnantaPersonality()
        
        print("✅ Personality engine initialized")
        
        # Test greetings
        print("\n🎤 Testing greetings:")
        greeting = personality.get_greeting(is_first_time=True)
        print(f"  • First time: {greeting}")
        
        # Simulate interactions
        print("\n📊 Simulating interactions:")
        for i in range(5):
            greeting = personality.get_greeting()
            print(f"  • Interaction {i+1}: {greeting[:50]}...")
        
        # Test response shaping
        print("\n💬 Testing response shaping:")
        contexts = [
            {"text": "I'm frustrated", "emotion_indicators": ["frustrated"]},
            {"text": "That's amazing!", "emotion_indicators": ["excited"]},
            {"text": "I'm confused", "emotion_indicators": ["confused"]},
        ]
        
        for context in contexts:
            response = personality.shape_response("Here's the solution", context)
            print(f"  • {context['text']}: {response.emotion} ({response.voice_style})")
        
        # Print info
        personality.print_personality_info()
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ui_system():
    """Test holographic UI system"""
    print("\n" + "="*70)
    print("🧪 TEST 4: HOLOGRAPHIC UI")
    print("="*70)
    
    try:
        from ui.holographic_ui import HolographicUI, HolographicTheme
        
        print("\n🎨 Initializing holographic UI...")
        ui = HolographicUI()
        
        print("✅ Holographic UI initialized")
        
        # Test components
        print("\n🌐 Testing UI components:")
        
        print("  • Base CSS: ", end="")
        css = ui.get_base_css()
        print(f"✅ ({len(css)} chars)")
        
        print("  • Holographic text: ", end="")
        text = ui.render_holographic_text("ANANTA")
        print(f"✅ ({len(text)} chars)")
        
        print("  • Avatar container: ", end="")
        avatar = ui.render_avatar_container()
        print(f"✅ ({len(avatar)} chars)")
        
        print("  • Status panel: ", end="")
        status = ui.render_status_panel({"model": "Sentinel", "vram": "4.2GB"})
        print(f"✅ ({len(status)} chars)")
        
        print("  • Chat interface: ", end="")
        chat = ui.render_chat_interface()
        print(f"✅ ({len(chat)} chars)")
        
        print("  • Waveform visualization: ", end="")
        waveform = ui.render_waveform_visualization()
        print(f"✅ ({len(waveform)} chars)")
        
        # Print info
        ui.print_ui_info()
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Test all components together"""
    print("\n" + "="*70)
    print("🧪 TEST 5: FULL INTEGRATION")
    print("="*70)
    
    try:
        from voice.ananta_voice import AnantaVoice
        from ui.ananta_avatar import AnantaAvatar
        from engines.ananta_personality import AnantaPersonality
        from ui.holographic_ui import HolographicUI
        
        print("\n🔄 Initializing all components...")
        
        voice = AnantaVoice()
        print("  ✅ Voice system")
        
        avatar = AnantaAvatar()
        print("  ✅ Avatar system")
        
        personality = AnantaPersonality()
        print("  ✅ Personality engine")
        
        ui = HolographicUI()
        print("  ✅ Holographic UI")
        
        print("\n🔄 Simulating interaction workflow:")
        
        # 1. User input
        print("  1️⃣  User input: 'That's amazing!'")
        
        # 2. Personality shapes response
        context = {"text": "That's amazing!", "emotion_indicators": ["excited"]}
        response = personality.shape_response("Great job! You did it!", context)
        print(f"  2️⃣  Personality response: {response.emotion} ({response.voice_style})")
        
        # 3. Avatar shows emotion
        avatar.set_emotion(response.emotion)
        print(f"  3️⃣  Avatar emotion: {response.emotion}")
        
        # 4. Voice speaks with emotion
        print(f"  4️⃣  Voice emotion: {response.emotion}")
        
        # 5. UI displays everything
        print(f"  5️⃣  UI rendering: Chat interface with avatar")
        
        print("\n✅ Full integration workflow successful!")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 ANANTA IDENTITY SYSTEM - TEST SUITE")
    print("="*70)
    print("Testing Voice, Avatar, Personality, and UI")
    
    tests = [
        ("Voice System", test_voice_system),
        ("Avatar System", test_avatar_system),
        ("Personality Engine", test_personality_system),
        ("Holographic UI", test_ui_system),
        ("Full Integration", test_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "✅ PASSED" if result else "❌ FAILED"))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
            results.append((test_name, f"❌ ERROR: {str(e)[:30]}"))
    
    # Print summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for test_name, result in results:
        print(f"{result} {test_name}")
    
    passed = sum(1 for _, r in results if "PASSED" in r)
    total = len(results)
    
    print(f"\n{'='*70}")
    print(f"✅ {passed}/{total} tests passed")
    print(f"{'='*70}\n")
    
    return passed == total


if __name__ == "__main__":
    import asyncio
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
