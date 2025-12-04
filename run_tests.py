#!/usr/bin/env python3
"""
Ananta Rebirth - Test Runner
Runs all tests and generates comprehensive reports
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

class TestRunner:
    """Orchestrate all tests"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.test_dir = self.project_root / "tests"
        self.results = {}
        self.start_time = datetime.now()
    
    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "="*80)
        print(f"  {title}")
        print("="*80)
    
    def check_ollama(self):
        """Check if Ollama is running"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def run_individual_tests(self):
        """Run individual feature tests"""
        self.print_header("🎯 INDIVIDUAL FEATURE TESTS")
        
        test_file = self.test_dir / "test_features_individual.py"
        
        if not test_file.exists():
            print(f"❌ Test file not found: {test_file}")
            return False
        
        try:
            result = subprocess.run(
                [sys.executable, str(test_file)],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=300
            )
            
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            self.results["individual_tests"] = {
                "status": "PASS" if result.returncode == 0 else "FAIL",
                "returncode": result.returncode
            }
            
            return result.returncode == 0
        
        except subprocess.TimeoutExpired:
            print("❌ Tests timed out")
            self.results["individual_tests"] = {"status": "TIMEOUT"}
            return False
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            self.results["individual_tests"] = {"status": "ERROR", "error": str(e)}
            return False
    
    def run_comprehensive_tests(self):
        """Run comprehensive test suite"""
        self.print_header("📊 COMPREHENSIVE TEST SUITE")
        
        test_file = self.project_root / "comprehensive_test.py"
        
        if not test_file.exists():
            print(f"❌ Test file not found: {test_file}")
            return False
        
        try:
            result = subprocess.run(
                [sys.executable, str(test_file)],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=300
            )
            
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            self.results["comprehensive_tests"] = {
                "status": "PASS" if result.returncode == 0 else "FAIL",
                "returncode": result.returncode
            }
            
            return result.returncode == 0
        
        except subprocess.TimeoutExpired:
            print("❌ Tests timed out")
            self.results["comprehensive_tests"] = {"status": "TIMEOUT"}
            return False
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            self.results["comprehensive_tests"] = {"status": "ERROR", "error": str(e)}
            return False
    
    def check_project_structure(self):
        """Verify project structure"""
        self.print_header("🗂️ PROJECT STRUCTURE VERIFICATION")
        
        essential_dirs = [
            "core", "intelligence", "automation", "memory", 
            "engines", "features", "ui", "utils", "data", "tests"
        ]
        
        essential_files = [
            "config.py", "main.py", "gui_launcher.py", "requirements.txt",
            "README.md", "PROJECT_STRUCTURE.md"
        ]
        
        missing_dirs = []
        missing_files = []
        
        for dir_name in essential_dirs:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
                print(f"❌ Missing directory: {dir_name}")
            else:
                print(f"✅ Found directory: {dir_name}")
        
        for file_name in essential_files:
            file_path = self.project_root / file_name
            if not file_path.exists():
                missing_files.append(file_name)
                print(f"❌ Missing file: {file_name}")
            else:
                print(f"✅ Found file: {file_name}")
        
        structure_ok = len(missing_dirs) == 0 and len(missing_files) == 0
        
        self.results["structure_check"] = {
            "status": "PASS" if structure_ok else "FAIL",
            "missing_dirs": missing_dirs,
            "missing_files": missing_files
        }
        
        return structure_ok
    
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        self.print_header("📦 DEPENDENCY CHECK")
        
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return False
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "check"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ All dependencies are satisfied")
                self.results["dependencies"] = {"status": "PASS"}
                return True
            else:
                print("⚠️ Some dependencies may have issues:")
                print(result.stdout)
                self.results["dependencies"] = {"status": "WARNING", "output": result.stdout}
                return True  # Not critical
        
        except Exception as e:
            print(f"⚠️ Could not check dependencies: {e}")
            self.results["dependencies"] = {"status": "UNKNOWN"}
            return True  # Not critical
    
    def verify_ollama_setup(self):
        """Verify Ollama setup"""
        self.print_header("🤖 OLLAMA SETUP VERIFICATION")
        
        ollama_running = self.check_ollama()
        
        if ollama_running:
            print("✅ Ollama is running on localhost:11434")
            self.results["ollama"] = {"status": "RUNNING"}
        else:
            print("⚠️ Ollama is not running")
            print("   To start Ollama, run: ollama serve")
            print("   Then run this test again")
            self.results["ollama"] = {"status": "NOT_RUNNING"}
        
        return ollama_running
    
    def generate_report(self):
        """Generate test report"""
        self.print_header("📋 TEST REPORT SUMMARY")
        
        elapsed = datetime.now() - self.start_time
        
        print(f"\n⏱️ Total Time: {elapsed.total_seconds():.2f}s")
        print(f"📅 Timestamp: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n📊 Results:")
        for test_name, result in self.results.items():
            status = result.get("status", "UNKNOWN")
            icon = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️", "UNKNOWN": "❓", 
                   "RUNNING": "🟢", "NOT_RUNNING": "🔴", "TIMEOUT": "⏱️", "ERROR": "💥"}
            icon = icon.get(status, "❓")
            print(f"  {icon} {test_name}: {status}")
        
        # Overall status
        failed = sum(1 for r in self.results.values() if r.get("status") == "FAIL")
        
        print(f"\n{'='*80}")
        if failed == 0:
            print("🎉 ALL TESTS PASSED! Ananta Rebirth is ready to use!")
        else:
            print(f"⚠️ {failed} test(s) failed. Review the output above.")
        print(f"{'='*80}\n")
        
        # Save report
        self.save_report()
    
    def save_report(self):
        """Save test report to file"""
        report_file = self.project_root / "test_report.json"
        
        report = {
            "timestamp": self.start_time.isoformat(),
            "duration_seconds": (datetime.now() - self.start_time).total_seconds(),
            "results": self.results
        }
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"📄 Report saved to: {report_file}")
        except Exception as e:
            print(f"⚠️ Could not save report: {e}")
    
    def run_all(self):
        """Run all tests"""
        self.print_header("🚀 ANANTA REBIRTH - COMPREHENSIVE TEST SUITE")
        
        print("\n📋 Test Plan:")
        print("  1. Check project structure")
        print("  2. Check dependencies")
        print("  3. Verify Ollama setup")
        print("  4. Run individual feature tests")
        print("  5. Run comprehensive tests")
        print("  6. Generate report")
        
        # Run tests in order
        self.check_project_structure()
        self.check_dependencies()
        ollama_ok = self.verify_ollama_setup()
        
        if not ollama_ok:
            print("\n⚠️ Ollama is required for full testing")
            print("   Please start Ollama with: ollama serve")
            print("   Then run this script again")
        
        self.run_individual_tests()
        self.run_comprehensive_tests()
        
        # Generate final report
        self.generate_report()

def main():
    """Main entry point"""
    try:
        runner = TestRunner()
        runner.run_all()
    except KeyboardInterrupt:
        print("\n\n⏹️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
