"""
Test Suite for Optimization Integration
Tests all Phase 2-6 components
"""

import asyncio
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from core.batch_inference_engine import BatchInferenceEngine
from core.lightweight_agent_orchestrator import LightweightAgentOrchestrator
from memory.lightweight_vector_db import LightweightVectorDB
from core.context_window_manager import ContextWindowManager
from core.usage_pattern_tracker import UsagePatternTracker
from core.intelligent_preloader import IntelligentPreloader


async def test_batch_inference_engine():
    """Test batch inference engine"""
    print("\n" + "="*70)
    print("🧪 TEST 1: BATCH INFERENCE ENGINE")
    print("="*70)
    
    engine = BatchInferenceEngine()
    
    test_queries = [
        "What is Python?",
        "Explain machine learning",
        "How do I write a function?",
        "What is quantum computing?",
        "Prove that P=NP",
        "Write a hello world program",
    ]
    
    results = await engine.process_batch(test_queries)
    
    print(f"\n✅ Processed {len(results)} queries")
    engine.print_batch_stats()
    
    return True


async def test_agent_orchestrator():
    """Test lightweight agent orchestrator"""
    print("\n" + "="*70)
    print("🧪 TEST 2: LIGHTWEIGHT AGENT ORCHESTRATOR")
    print("="*70)
    
    orchestrator = LightweightAgentOrchestrator()
    
    result = await orchestrator.execute_complex_task(
        "Build a Python web scraper with error handling and data storage"
    )
    
    print(f"\n✅ Complex task completed")
    print(f"   Main Task: {result['main_task']}")
    print(f"   Status: {result['status']}")
    print(f"   Total Steps: {result['total_steps']}")
    
    orchestrator.print_orchestrator_info()
    
    return True


def test_vector_db():
    """Test lightweight vector database"""
    print("\n" + "="*70)
    print("🧪 TEST 3: LIGHTWEIGHT VECTOR DATABASE")
    print("="*70)
    
    db = LightweightVectorDB()
    
    documents = [
        ("Python is a programming language", {"category": "programming", "importance": 8}),
        ("Machine learning is a subset of AI", {"category": "ai", "importance": 9}),
        ("Neural networks are inspired by biology", {"category": "ai", "importance": 7}),
        ("Data science involves statistics", {"category": "data", "importance": 6}),
        ("Web development uses HTML and CSS", {"category": "web", "importance": 5}),
    ]
    
    print("\n📝 Storing documents:")
    for text, metadata in documents:
        vector_id = db.store_and_index(text, metadata)
        print(f"  [{vector_id}] {text[:40]}...")
    
    print("\n🔍 Searching:")
    query = "programming languages"
    results = db.search(query, k=3)
    print(f"Query: '{query}'")
    for result in results:
        print(f"  Distance: {result['distance']:.3f} | {result['metadata']}")
    
    db.print_stats()
    
    return True


def test_context_window_manager():
    """Test context window manager"""
    print("\n" + "="*70)
    print("🧪 TEST 4: CONTEXT WINDOW MANAGER")
    print("="*70)
    
    manager = ContextWindowManager()
    
    manager.print_window_info()
    
    # Test compression
    test_context = """
    Important: The system must handle 6GB VRAM efficiently.
    Key: Use quantized models for better performance.
    Note: Context windows should be optimized per model.
    
    The architecture includes multiple components.
    Each component has specific responsibilities.
    The system is designed for RTX 4050 hardware.
    
    Critical: Always preserve important facts during compression.
    Remember: Compression ratio should be tracked.
    """
    
    print("\n📊 Testing context compression:")
    print(f"Original length: {len(test_context.split())} tokens")
    
    compressed, ratio = manager.compress_context(test_context, "sentinel")
    print(f"Compressed length: {len(compressed.split())} tokens")
    print(f"Compression ratio: {ratio:.2f}")
    
    manager.print_compression_stats()
    
    return True


def test_usage_pattern_tracker():
    """Test usage pattern tracker"""
    print("\n" + "="*70)
    print("🧪 TEST 5: USAGE PATTERN TRACKER")
    print("="*70)
    
    tracker = UsagePatternTracker()
    
    # Simulate usage
    print("\n📊 Simulating usage patterns:")
    tracker.track_query("sentinel", 2.5, success=True, query_type="general")
    tracker.track_query("architect", 3.1, success=True, query_type="code")
    tracker.track_query("flash", 1.2, success=True, query_type="quick")
    tracker.track_query("sentinel", 2.3, success=True, query_type="general")
    tracker.track_query("oracle", 4.2, success=True, query_type="reasoning")
    
    # Track model switches
    tracker.track_model_switch("sentinel", "architect", 2.5, "code task detected")
    tracker.track_model_switch("architect", "sentinel", 2.3, "back to general")
    tracker.track_model_switch("sentinel", "oracle", 3.1, "complex reasoning needed")
    
    tracker.print_statistics()
    
    # Predict next model
    next_model = tracker.predict_next_model()
    print(f"Predicted next model: {next_model}\n")
    
    return True


async def test_intelligent_preloader():
    """Test intelligent preloader"""
    print("\n" + "="*70)
    print("🧪 TEST 6: INTELLIGENT PRELOADER")
    print("="*70)
    
    tracker = UsagePatternTracker()
    preloader = IntelligentPreloader(usage_tracker=tracker)
    
    # Simulate some usage
    tracker.track_query("sentinel", 2.5, success=True)
    tracker.track_query("architect", 3.1, success=True)
    tracker.track_query("flash", 1.2, success=True)
    
    # Predict and schedule preloads
    print("\n📦 Predicting next models:")
    predictions = preloader.predict_next_models(k=3)
    for model, confidence in predictions:
        print(f"  {model}: {confidence:.1%}")
    
    print("\n📦 Scheduling preloads:")
    for model, confidence in predictions:
        task = preloader.schedule_preload(model, priority=int(confidence * 10))
        if task:
            print(f"  Scheduled {model} with priority {task.priority}")
    
    print("\n⏳ Processing preload queue:")
    for task in preloader.preload_queue:
        success = await preloader.preload_model(task.model)
        print(f"  {task.model}: {'✅ Success' if success else '❌ Failed'}")
    
    preloader.print_preload_stats()
    
    return True


async def test_integration():
    """Test all components together"""
    print("\n" + "="*70)
    print("🧪 TEST 7: FULL INTEGRATION")
    print("="*70)
    
    print("\n🔄 Initializing all components...")
    
    batch_engine = BatchInferenceEngine()
    orchestrator = LightweightAgentOrchestrator()
    vector_db = LightweightVectorDB()
    context_mgr = ContextWindowManager()
    tracker = UsagePatternTracker()
    preloader = IntelligentPreloader(usage_tracker=tracker)
    
    print("✅ All components initialized successfully")
    
    # Simulate a workflow
    print("\n🔄 Simulating workflow:")
    
    # 1. Track usage
    print("  1️⃣  Tracking usage patterns...")
    tracker.track_query("sentinel", 2.5, success=True, query_type="general")
    tracker.track_query("architect", 3.1, success=True, query_type="code")
    
    # 2. Predict and preload
    print("  2️⃣  Predicting and preloading next models...")
    predictions = preloader.predict_next_models(k=2)
    for model, confidence in predictions:
        preloader.schedule_preload(model, priority=int(confidence * 10))
    
    # 3. Store in vector DB
    print("  3️⃣  Storing context in vector database...")
    vector_db.store_and_index("User query about Python", {"importance": 8})
    
    # 4. Optimize context window
    print("  4️⃣  Optimizing context window...")
    optimal_size = context_mgr.get_optimal_context_size("sentinel")
    print(f"     Optimal context for sentinel: {optimal_size} tokens")
    
    print("\n✅ Workflow completed successfully")
    
    return True


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 ANANTA REBIRTH - OPTIMIZATION INTEGRATION TEST SUITE")
    print("="*70)
    print(f"Testing Phases 2-6 of Claude's Optimization Plan")
    print(f"Hardware: {config.GPU_SETTINGS['num_gpu']}x GPU, {config.GPU_SETTINGS['num_thread']} threads")
    
    tests = [
        ("Batch Inference Engine", test_batch_inference_engine),
        ("Agent Orchestrator", test_agent_orchestrator),
        ("Vector Database", test_vector_db),
        ("Context Window Manager", test_context_window_manager),
        ("Usage Pattern Tracker", test_usage_pattern_tracker),
        ("Intelligent Preloader", test_intelligent_preloader),
        ("Full Integration", test_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, "✅ PASSED"))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, f"❌ FAILED: {str(e)[:50]}"))
    
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
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
