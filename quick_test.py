#!/usr/bin/env python3
"""
Quick Test Script - Fast verification of Ananta Rebirth
Run this to quickly verify all features are working
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def quick_test():
    """Run quick tests"""
    print_header("🚀 ANANTA REBIRTH - QUICK TEST")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Retriever
    print("\n1️⃣ Testing Retriever...")
    try:
        from core.retriever import Retriever
        r = Retriever()
        r.add_documents(["id1"], [{"type": "test"}], ["Test document"])
        results = r.query("test", top_k=1)
        if results:
            print("   ✅ Retriever: OK")
            tests_passed += 1
        else:
            print("   ❌ Retriever: No results")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Retriever: {e}")
        tests_failed += 1
    
    # Test 2: Emotional Intelligence
    print("\n2️⃣ Testing Emotional Intelligence...")
    try:
        from core.emotional_intelligence import EmotionalIntelligence
        ei = EmotionalIntelligence()
        emotion = ei.analyze_user_emotion("I am happy!", {})
        if emotion:
            print(f"   ✅ Emotional Intelligence: OK (emotion: {emotion.value})")
            tests_passed += 1
        else:
            print("   ❌ Emotional Intelligence: No emotion")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Emotional Intelligence: {e}")
        tests_failed += 1
    
    # Test 3: Context Engine
    print("\n3️⃣ Testing Context Engine...")
    try:
        from core.context_engine import RealTimeContextEngine
        ctx = RealTimeContextEngine()
        result = ctx.get_full_context()
        if result:
            print("   ✅ Context Engine: OK")
            tests_passed += 1
        else:
            print("   ❌ Context Engine: No result")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Context Engine: {e}")
        tests_failed += 1
    
    # Test 4: Security Engine
    print("\n4️⃣ Testing Security Engine...")
    try:
        from core.security_engine import AdvancedSecurityEngine
        sec = AdvancedSecurityEngine()
        result = sec.analyze_request({"ip_address": "127.0.0.1", "body": "test"})
        if result:
            print(f"   ✅ Security Engine: OK")
            tests_passed += 1
        else:
            print("   ❌ Security Engine: No result")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Security Engine: {e}")
        tests_failed += 1
    
    # Test 5: System Monitor
    print("\n5️⃣ Testing System Monitor...")
    try:
        from core.system_monitor import SystemMonitoringEngine
        monitor = SystemMonitoringEngine()
        stats = monitor._collect_all_metrics()
        if stats and "cpu_usage" in stats:
            print(f"   ✅ System Monitor: OK")
            tests_passed += 1
        else:
            print("   ❌ System Monitor: No stats")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ System Monitor: {e}")
        tests_failed += 1
    
    # Test 6: Memory System
    print("\n6️⃣ Testing Memory System...")
    try:
        from memory.adaptive_memory import AdaptiveMemory
        mem = AdaptiveMemory()
        mem_id = mem.add_memory("user", "test memory", "conversation")
        retrieved = mem.get_recent_memories(limit=1)
        if retrieved:
            print("   ✅ Memory System: OK")
            tests_passed += 1
        else:
            print("   ❌ Memory System: No retrieval")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Memory System: {e}")
        tests_failed += 1
    
    # Test 7: Code Executor
    print("\n7️⃣ Testing Code Executor...")
    try:
        from features.code_executor import CodeExecutor
        executor = CodeExecutor()
        result = executor.execute_code("print('test')", "python")
        if result and "success" in result:
            print("   ✅ Code Executor: OK")
            tests_passed += 1
        else:
            print("   ❌ Code Executor: No result")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Code Executor: {e}")
        tests_failed += 1
    
    # Test 8: Voice Interface
    print("\n8️⃣ Testing Voice Interface...")
    try:
        from features.voice_interface import VoiceInterface
        voice = VoiceInterface()
        print("   ✅ Voice Interface: OK (loaded)")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Voice Interface: {e}")
        tests_failed += 1
    
    # Test 9: Creative Engine
    print("\n9️⃣ Testing Creative Engine...")
    try:
        from engines.creative_engine import CreativeEngine
        creative = CreativeEngine()
        print("   ✅ Creative Engine: OK (loaded)")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Creative Engine: {e}")
        tests_failed += 1
    
    # Test 10: Ollama Client
    print("\n🔟 Testing Ollama Client...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("   ✅ Ollama: Running")
            tests_passed += 1
        else:
            print("   ⏭️ Ollama: Not responding")
    except:
        print("   ⏭️ Ollama: Not running (start with 'ollama serve')")
    
    # Summary
    print_header("📊 QUICK TEST RESULTS")
    
    total = tests_passed + tests_failed
    success_rate = (tests_passed / total * 100) if total > 0 else 0
    
    print(f"\n✅ Passed:  {tests_passed}")
    print(f"❌ Failed:  {tests_failed}")
    print(f"📊 Success: {success_rate:.1f}%")
    
    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED! Ananta is ready to use!")
        print("\nNext steps:")
        print("  1. Start Ollama: ollama serve")
        print("  2. Run terminal: python main.py")
        print("  3. Or run GUI: python gui_launcher.py")
        print("  4. Or run full tests: python run_tests.py")
    else:
        print(f"\n⚠️ {tests_failed} test(s) failed. Check errors above.")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        quick_test()
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
