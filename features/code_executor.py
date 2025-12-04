# backend/features/code_executor.py
"""
Safe Code Execution for Ananta
Run code in sandboxed environment with resource limits
"""

import subprocess
import tempfile
import os
import sys
import time
from typing import Dict, Optional, Tuple
import json

class CodeExecutor:
    """
    Execute code safely with resource limits
    """
    
    def __init__(self):
        self.supported_languages = {
            "python": {
                "extension": ".py",
                "command": [sys.executable],
                "timeout": 10
            },
            "javascript": {
                "extension": ".js",
                "command": ["node"],
                "timeout": 10
            },
            "bash": {
                "extension": ".sh",
                "command": ["bash"],
                "timeout": 5
            }
        }
        
        # Security settings
        self.max_output_size = 10000  # characters
        self.max_execution_time = 30  # seconds
    
    def execute_python(self, code: str, stdin: str = "") -> Dict:
        """
        Execute Python code safely
        
        Args:
            code: Python code to execute
            stdin: Standard input for the code
        
        Returns:
            Execution result
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            start_time = time.time()
            
            # Execute with timeout
            result = subprocess.run(
                [sys.executable, temp_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=self.supported_languages["python"]["timeout"]
            )
            
            execution_time = time.time() - start_time
            
            # Truncate output if too large
            stdout = result.stdout[:self.max_output_size]
            stderr = result.stderr[:self.max_output_size]
            
            return {
                "success": result.returncode == 0,
                "stdout": stdout,
                "stderr": stderr,
                "execution_time": round(execution_time, 3),
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Error: Execution timeout exceeded",
                "execution_time": self.supported_languages["python"]["timeout"],
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: {str(e)}",
                "execution_time": 0,
                "return_code": -1
            }
        finally:
            # Clean up
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def execute_javascript(self, code: str) -> Dict:
        """Execute JavaScript code (requires Node.js)"""
        # Check if Node.js is available
        try:
            subprocess.run(["node", "--version"], capture_output=True, check=True)
        except:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Error: Node.js not installed",
                "execution_time": 0,
                "return_code": -1
            }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            start_time = time.time()
            
            result = subprocess.run(
                ["node", temp_file],
                capture_output=True,
                text=True,
                timeout=self.supported_languages["javascript"]["timeout"]
            )
            
            execution_time = time.time() - start_time
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout[:self.max_output_size],
                "stderr": result.stderr[:self.max_output_size],
                "execution_time": round(execution_time, 3),
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Error: Execution timeout",
                "execution_time": self.supported_languages["javascript"]["timeout"],
                "return_code": -1
            }
        finally:
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def execute_code(self, code: str, language: str, stdin: str = "") -> Dict:
        """
        Execute code in specified language
        
        Args:
            code: Code to execute
            language: Programming language
            stdin: Standard input
        
        Returns:
            Execution result
        """
        if language not in self.supported_languages:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Language '{language}' not supported",
                "execution_time": 0,
                "return_code": -1
            }
        
        # Security checks
        if not self._is_safe_code(code, language):
            return {
                "success": False,
                "stdout": "",
                "stderr": "Error: Code contains potentially unsafe operations",
                "execution_time": 0,
                "return_code": -1
            }
        
        # Route to appropriate executor
        if language == "python":
            return self.execute_python(code, stdin)
        elif language == "javascript":
            return self.execute_javascript(code)
        else:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Executor for {language} not implemented",
                "execution_time": 0,
                "return_code": -1
            }
    
    def _is_safe_code(self, code: str, language: str) -> bool:
        """
        Basic security checks
        (NOT comprehensive - use proper sandboxing in production!)
        """
        code_lower = code.lower()
        
        # Common dangerous patterns
        dangerous_patterns = [
            "import os",
            "import sys",
            "import subprocess",
            "__import__",
            "exec(",
            "eval(",
            "compile(",
            "open(",  # File operations
            "rm ",
            "delete",
            "format(",  # Disk formatting
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                return False
        
        return True
    
    def test_code(self, code: str, language: str, test_cases: list) -> Dict:
        """
        Test code against test cases
        
        Args:
            code: Code to test
            language: Programming language
            test_cases: List of test cases [{"input": "", "expected": ""}]
        
        Returns:
            Test results
        """
        results = []
        passed = 0
        
        for i, test_case in enumerate(test_cases):
            test_input = test_case.get("input", "")
            expected_output = test_case.get("expected", "")
            
            # Execute with test input
            result = self.execute_code(code, language, stdin=test_input)
            
            # Check if output matches expected
            actual_output = result["stdout"].strip()
            success = actual_output == expected_output.strip()
            
            if success:
                passed += 1
            
            results.append({
                "test_case": i + 1,
                "input": test_input,
                "expected": expected_output,
                "actual": actual_output,
                "passed": success,
                "execution_time": result["execution_time"]
            })
        
        return {
            "total_tests": len(test_cases),
            "passed": passed,
            "failed": len(test_cases) - passed,
            "success_rate": (passed / len(test_cases) * 100) if test_cases else 0,
            "results": results
        }
    
    def benchmark_code(self, code: str, language: str, iterations: int = 10) -> Dict:
        """
        Benchmark code performance
        
        Args:
            code: Code to benchmark
            language: Programming language
            iterations: Number of iterations
        
        Returns:
            Benchmark results
        """
        execution_times = []
        
        for _ in range(iterations):
            result = self.execute_code(code, language)
            if result["success"]:
                execution_times.append(result["execution_time"])
        
        if not execution_times:
            return {
                "success": False,
                "error": "All iterations failed"
            }
        
        import statistics
        
        return {
            "success": True,
            "iterations": len(execution_times),
            "avg_time": round(statistics.mean(execution_times), 4),
            "min_time": round(min(execution_times), 4),
            "max_time": round(max(execution_times), 4),
            "std_dev": round(statistics.stdev(execution_times), 4) if len(execution_times) > 1 else 0
        }
    
    def get_capabilities(self) -> Dict:
        """Get executor capabilities"""
        return {
            "supported_languages": list(self.supported_languages.keys()),
            "max_execution_time": self.max_execution_time,
            "max_output_size": self.max_output_size,
            "features": ["execute", "test", "benchmark"]
        }


# Example usage
"""
executor = CodeExecutor()

# Execute Python code
result = executor.execute_code('''
print("Hello from Ananta!")
for i in range(5):
    print(f"Count: {i}")
''', language="python")

print(result)

# Test code
test_cases = [
    {"input": "5", "expected": "25"},
    {"input": "10", "expected": "100"}
]

code = '''
n = int(input())
print(n * n)
'''

test_results = executor.test_code(code, "python", test_cases)
print(test_results)
"""