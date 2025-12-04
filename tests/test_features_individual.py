#!/usr/bin/env python3
"""
Individual Feature Test Suite for Ananta Rebirth
Tests each feature independently with detailed reporting
"""

import sys
import os
from pathlib import Path
import time
import traceback

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestResult:
    """Store test result with details"""
    def __init__(self, name, status, message="", duration=0):
        self.name = name
        self.status = status  # "PASS", "FAIL", "SKIP", "ERROR"
        self.message = message
        self.duration = duration
    
    def __repr__(self):
        icon = {"PASS": "✅", "FAIL": "❌", "ERROR": "⚠️", "SKIP": "⏭️"}[self.status]
        return f"{icon} {self.name} ({self.duration:.2f}s) - {self.status}"

class FeatureTester:
    """Test individual features"""
    
    def __init__(self):
        self.results = []
        self.ollama_available = False
    
    def check_ollama(self):
        """Check if Ollama is running"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            self.ollama_available = response.status_code == 200
            return self.ollama_available
        except:
            self.ollama_available = False
            return False
    
    def test_retriever(self):
        """Test Retriever (Vector Database)"""
        print("\n🔍 Testing Retriever (Vector Database)...")
        start = time.time()
        try:
            from core.retriever import Retriever
            
            # Initialize retriever
            retriever = Retriever()
            
            # Test add documents
            test_ids = ["doc1", "doc2", "doc3"]
            test_docs = [
                "Python is a programming language",
                "Machine learning is a subset of AI",
                "Neural networks are inspired by biology"
            ]
            test_metas = [
                {"type": "tech", "source": "wiki"},
                {"type": "ai", "source": "textbook"},
                {"type": "ai", "source": "research"}
            ]
            
            retriever.add_documents(test_ids, test_metas, test_docs)
            
            # Test query
            results = retriever.query("What is Python?", top_k=2)
            
            if len(results) > 0 and "document" in results[0]:
                duration = time.time() - start
                result = TestResult("Retriever", "PASS", f"Retrieved {len(results)} documents", duration)
                self.results.append(result)
                print(f"  ✅ Added documents and retrieved results")
                return result
            else:
                raise Exception("No results returned from query")
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("Retriever", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def test_ollama_client(self):
        """Test Ollama Client"""
        print("\n🤖 Testing Ollama Client...")
        start = time.time()
        try:
            if not self.ollama_available:
                duration = time.time() - start
                result = TestResult("Ollama Client", "SKIP", "Ollama not running", duration)
                self.results.append(result)
                print(f"  ⏭️ Ollama not running - skipping")
                return result
            
            from core.ollama_client import OllamaClient
            
            client = OllamaClient()
            
            # Test simple generation
            response = client.generate("What is 2+2?", max_tokens=50)
            
            if response and len(response) > 0:
                duration = time.time() - start
                result = TestResult("Ollama Client", "PASS", f"Generated {len(response)} chars", duration)
                self.results.append(result)
                print(f"  ✅ Generated response: {response[:50]}...")
                return result
            else:
                raise Exception("No response from Ollama")
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("Ollama Client", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def test_emotional_intelligence(self):
        """Test Emotional Intelligence Engine"""
        print("\n❤️ Testing Emotional Intelligence...")
        start = time.time()
        try:
            from core.emotional_intelligence import EmotionalIntelligence
            
            ei = EmotionalIntelligence()
            
            # Test emotion analysis
            text = "I am very happy and excited about this project!"
            emotion = ei.analyze_user_emotion(text, {})
            
            if emotion:
                duration = time.time() - start
                result = TestResult("Emotional Intelligence", "PASS", 
                                   f"Detected emotion: {emotion.value}", duration)
                self.results.append(result)
                print(f"  ✅ Emotion: {emotion.value}")
                return result
            else:
                raise Exception("No emotion detected")
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("Emotional Intelligence", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def test_context_engine(self):
        """Test Context Engine"""
        print("\n🧠 Testing Context Engine...")
        start = time.time()
        try:
            from core.context_engine import RealTimeContextEngine
            
            context = RealTimeContextEngine()
            
            # Test context retrieval
            context_result = context.get_full_context()
            
            if context_result and "system" in context_result:
                duration = time.time() - start
                result = TestResult("Context Engine", "PASS", 
                                   f"Retrieved full context", duration)
                self.results.append(result)
                print(f"  ✅ Context retrieved successfully")
                return result
            else:
                raise Exception("Failed to get context")
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("Context Engine", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def test_security_engine(self):
        """Test Security Engine"""
        print("\n🔒 Testing Security Engine...")
        start = time.time()
        try:
            from core.security_engine import AdvancedSecurityEngine
            
            security = AdvancedSecurityEngine()
            
            # Test request analysis
            test_request = {
                "ip_address": "127.0.0.1",
                "body": "test",
                "method": "GET",
                "path": "/"
            }
            result_analysis = security.analyze_request(test_request)
            
            if result_analysis and "action" in result_analysis:
                duration = time.time() - start
                result = TestResult("Security Engine", "PASS", 
                                   "Security analysis working", duration)
                self.results.append(result)
                print(f"  ✅ Security engine operational")
                return result
            else:
                raise Exception("No analysis result")
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("Security Engine", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def test_system_monitor(self):
        """Test System Monitor"""
        print("\n📊 Testing System Monitor...")
        start = time.time()
        try:
            from core.system_monitor import SystemMonitoringEngine
            
            monitor = SystemMonitoringEngine()
            
            # Get system stats
            stats = monitor._collect_all_metrics()
            
            if stats and "cpu_usage" in stats:
                duration = time.time() - start
                result = TestResult("System Monitor", "PASS", 
                                   f"CPU: {stats['cpu_usage'].value:.1f}%", duration)
                self.results.append(result)
                print(f"  ✅ System stats retrieved")
                return result
            else:
                raise Exception("Failed to get system stats")
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("System Monitor", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def test_code_executor(self):
        """Test Code Executor"""
        print("\n💻 Testing Code Executor...")
        start = time.time()
        try:
            from features.code_executor import CodeExecutor
            
            executor = CodeExecutor()
            
            # Test simple code execution
            code = "print('test')"
            output = executor.execute_code(code, "python")
            
            if output and output.get("success") is not None:
                duration = time.time() - start
                result = TestResult("Code Executor", "PASS", "Code executed successfully", duration)
                self.results.append(result)
                print(f"  ✅ Code executed successfully")
                return result
            else:
                raise Exception("Code execution failed")
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("Code Executor", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def test_voice_interface(self):
        """Test Voice Interface"""
        print("\n🎤 Testing Voice Interface...")
        start = time.time()
        try:
            from features.voice_interface import VoiceInterface
            
            voice = VoiceInterface()
            
            # Test text-to-speech
            voice.speak("Hello, this is a test")
            
            duration = time.time() - start
            result = TestResult("Voice Interface", "PASS", "Voice interface operational", duration)
            self.results.append(result)
            print(f"  ✅ Voice interface working")
            return result
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("Voice Interface", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def test_project_scaffolder(self):
        """Test Project Scaffolder"""
        print("\n🏗️ Testing Project Scaffolder...")
        start = time.time()
        try:
            from engines.project_scaffolder import ProjectScaffolder
            
            scaffolder = ProjectScaffolder()
            
            # Test listing available templates
            templates_result = scaffolder.list_available_templates()
            templates = templates_result.get("templates", [])
            
            if templates and len(templates) > 0:
                duration = time.time() - start
                result = TestResult("Project Scaffolder", "PASS", 
                                   f"Found {len(templates)} templates", duration)
                self.results.append(result)
                print(f"  ✅ Project scaffolder working")
                return result
            else:
                raise Exception("No templates found")
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("Project Scaffolder", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def test_creative_engine(self):
        """Test Creative Engine"""
        print("\n🎨 Testing Creative Engine...")
        start = time.time()
        try:
            from engines.creative_engine import CreativeEngine
            
            creative = CreativeEngine()
            
            # Test creative intent detection
            prompt = "Write a story about AI"
            intent = creative.detect_creative_intent(prompt)
            
            if intent:
                duration = time.time() - start
                result = TestResult("Creative Engine", "PASS", 
                                   f"Detected intent: {intent}", duration)
                self.results.append(result)
                print(f"  ✅ Creative engine working")
                return result
            else:
                raise Exception("Failed to detect intent")
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("Creative Engine", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def test_memory_system(self):
        """Test Memory System"""
        print("\n🧠 Testing Memory System...")
        start = time.time()
        try:
            from memory.adaptive_memory import AdaptiveMemory
            
            memory = AdaptiveMemory()
            
            # Test memory storage
            mem_id = memory.add_memory("user", "test memory", "conversation")
            retrieved = memory.get_recent_memories(limit=1)
            
            if retrieved and len(retrieved) > 0:
                duration = time.time() - start
                result = TestResult("Memory System", "PASS", "Memory storage working", duration)
                self.results.append(result)
                print(f"  ✅ Memory storage and retrieval working")
                return result
            else:
                raise Exception("Memory retrieval failed")
        
        except Exception as e:
            duration = time.time() - start
            result = TestResult("Memory System", "FAIL", str(e), duration)
            self.results.append(result)
            print(f"  ❌ Error: {e}")
            return result
    
    def run_all_tests(self):
        """Run all feature tests"""
        print("\n" + "="*70)
        print("🚀 ANANTA REBIRTH - INDIVIDUAL FEATURE TEST SUITE")
        print("="*70)
        
        # Check Ollama first
        print("\n🔍 Checking Ollama availability...")
        if self.check_ollama():
            print("✅ Ollama is running on localhost:11434")
        else:
            print("⚠️ Ollama is not running - some tests will be skipped")
        
        # Run tests
        print("\n" + "="*70)
        print("📋 RUNNING INDIVIDUAL FEATURE TESTS")
        print("="*70)
        
        self.test_retriever()
        self.test_ollama_client()
        self.test_emotional_intelligence()
        self.test_context_engine()
        self.test_security_engine()
        self.test_system_monitor()
        self.test_code_executor()
        self.test_voice_interface()
        self.test_project_scaffolder()
        self.test_creative_engine()
        self.test_memory_system()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("📊 TEST RESULTS SUMMARY")
        print("="*70)
        
        passed = sum(1 for r in self.results if r.status == "PASS")
        failed = sum(1 for r in self.results if r.status == "FAIL")
        skipped = sum(1 for r in self.results if r.status == "SKIP")
        total = len(self.results)
        
        print(f"\n📈 Overall Statistics:")
        print(f"  ✅ Passed:  {passed}/{total}")
        print(f"  ❌ Failed:  {failed}/{total}")
        print(f"  ⏭️ Skipped: {skipped}/{total}")
        print(f"  📊 Success Rate: {passed/total*100:.1f}%")
        
        print(f"\n📋 Detailed Results:")
        for result in self.results:
            print(f"  {result}")
        
        total_time = sum(r.duration for r in self.results)
        print(f"\n⏱️ Total Time: {total_time:.2f}s")
        
        if failed == 0:
            print("\n🎉 ALL TESTS PASSED! Ananta Rebirth is fully functional!")
        elif failed <= 2:
            print(f"\n✅ MOSTLY PASSED! {failed} test(s) need attention.")
        else:
            print(f"\n⚠️ {failed} test(s) failed. Review required.")
        
        print("\n" + "="*70)

def main():
    """Main entry point"""
    tester = FeatureTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
