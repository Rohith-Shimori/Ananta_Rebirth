# code_expert.py - Advanced Code Generation & Analysis
"""
Multi-language code generation with tests, documentation, and best practices.
Supports: Python, JavaScript, Rust, C++, Go, Java, TypeScript
"""

import re
from typing import Dict, List, Optional, Tuple

class CodeExpert:
    """
    Advanced code generation and analysis capabilities.
    """
    
    SUPPORTED_LANGUAGES = {
        "python": {
            "ext": ".py",
            "comment": "#",
            "doc_style": '"""..."""',
            "test_framework": "pytest",
            "package_manager": "pip"
        },
        "javascript": {
            "ext": ".js",
            "comment": "//",
            "doc_style": "/** ... */",
            "test_framework": "jest",
            "package_manager": "npm"
        },
        "typescript": {
            "ext": ".ts",
            "comment": "//",
            "doc_style": "/** ... */",
            "test_framework": "jest",
            "package_manager": "npm"
        },
        "rust": {
            "ext": ".rs",
            "comment": "//",
            "doc_style": "/// ...",
            "test_framework": "built-in",
            "package_manager": "cargo"
        },
        "cpp": {
            "ext": ".cpp",
            "comment": "//",
            "doc_style": "/** ... */",
            "test_framework": "gtest",
            "package_manager": "cmake"
        },
        "go": {
            "ext": ".go",
            "comment": "//",
            "doc_style": "// ...",
            "test_framework": "testing",
            "package_manager": "go mod"
        },
        "java": {
            "ext": ".java",
            "comment": "//",
            "doc_style": "/** ... */",
            "test_framework": "junit",
            "package_manager": "maven/gradle"
        }
    }
    
    def detect_language(self, query: str, code: str = "") -> str:
        """Detect programming language from query or code."""
        q = query.lower()
        
        # Explicit language mentions
        for lang in self.SUPPORTED_LANGUAGES:
            if lang in q:
                return lang
        
        # Language-specific keywords in code
        if code:
            if "def " in code or "import " in code:
                return "python"
            elif "function" in code or "const " in code or "let " in code:
                return "javascript"
            elif "fn " in code or "impl " in code:
                return "rust"
            elif "func " in code and "package " in code:
                return "go"
            elif "#include" in code or "std::" in code:
                return "cpp"
            elif "public class" in code or "private " in code:
                return "java"
        
        # Default to Python (most common)
        return "python"
    
    def generate_code_with_docs(self, description: str, language: str = "python",
                                include_tests: bool = True, include_examples: bool = True) -> Dict:
        """
        Generate complete code with documentation and tests.
        Returns structured result with code, docs, tests, and usage.
        """
        lang_info = self.SUPPORTED_LANGUAGES.get(language, self.SUPPORTED_LANGUAGES["python"])
        
        # Build comprehensive prompt
        prompt = self._build_generation_prompt(description, language, include_tests, include_examples)
        
        return {
            "language": language,
            "prompt": prompt,
            "includes_tests": include_tests,
            "includes_examples": include_examples,
            "file_extension": lang_info["ext"],
            "test_framework": lang_info["test_framework"]
        }
    
    def _build_generation_prompt(self, description: str, language: str, 
                                 include_tests: bool, include_examples: bool) -> str:
        """Build specialized code generation prompt."""
        lang_info = self.SUPPORTED_LANGUAGES[language]
        
        prompt = f"""Generate production-quality {language.upper()} code for:
{description}

Requirements:
1. CLEAN CODE:
   - Clear variable names
   - Proper structure and organization
   - Follow {language} best practices and idioms
   - Type hints/annotations where applicable

2. DOCUMENTATION:
   - Function/method docstrings using {lang_info['doc_style']}
   - Explain parameters, return values, exceptions
   - Add inline comments for complex logic

3. ERROR HANDLING:
   - Handle edge cases gracefully
   - Validate inputs
   - Meaningful error messages

4. PERFORMANCE:
   - Efficient algorithms (mention time/space complexity)
   - Optimize where it matters
"""
        
        if include_tests:
            prompt += f"""
5. TESTS (using {lang_info['test_framework']}):
   - Test normal cases
   - Test edge cases
   - Test error conditions
   - Clear test names describing what's being tested
"""
        
        if include_examples:
            prompt += """
6. USAGE EXAMPLES:
   - Show typical usage patterns
   - Include 2-3 concrete examples
   - Demonstrate key features
"""
        
        prompt += f"""
Output format:
```{language}
# Main implementation with docs
[code here]
```

```{language}
# Tests
[test code here]
```

```{language}
# Usage examples
[example code here]
```

Provide complete, working code that's ready to use.
"""
        
        return prompt
    
    def analyze_code(self, code: str, language: str = None) -> Dict:
        """
        Analyze code for quality, issues, and improvements.
        """
        if not language:
            language = self.detect_language("", code)
        
        analysis_prompt = f"""Analyze this {language.upper()} code:

```{language}
{code}
```

Provide detailed analysis:

1. CODE QUALITY:
   - Readability and maintainability
   - Naming conventions
   - Structure and organization
   
2. POTENTIAL ISSUES:
   - Bugs or logical errors
   - Edge cases not handled
   - Security concerns
   - Performance bottlenecks
   
3. BEST PRACTICES:
   - What's done well
   - What could be improved
   - Language-specific idioms to use
   
4. SUGGESTIONS:
   - Specific improvements with code examples
   - Alternative approaches to consider
   - Optimization opportunities
   
5. COMPLEXITY:
   - Time complexity
   - Space complexity
   - Cognitive complexity
"""
        
        return {
            "language": language,
            "code_length": len(code.split('\n')),
            "analysis_prompt": analysis_prompt
        }
    
    def debug_assistance(self, code: str, error_message: str, language: str = None) -> str:
        """
        Provide debugging guidance for code with errors.
        """
        if not language:
            language = self.detect_language("", code)
        
        debug_prompt = f"""DEBUG ASSISTANCE for {language.upper()} code:

ERROR MESSAGE:
{error_message}

CODE:
```{language}
{code}
```

Please provide:

1. ROOT CAUSE:
   - What's causing the error?
   - Line(s) where the issue occurs
   
2. EXPLANATION:
   - Why is this happening?
   - What was the code trying to do?
   
3. FIX:
   - Show corrected code
   - Explain what changed and why
   
4. PREVENTION:
   - How to avoid this in the future
   - Related best practices
   
5. TESTING:
   - How to test the fix
   - Edge cases to verify
"""
        
        return debug_prompt
    
    def optimize_code(self, code: str, optimization_goal: str = "performance", 
                     language: str = None) -> str:
        """
        Optimize code for performance, memory, or readability.
        """
        if not language:
            language = self.detect_language("", code)
        
        optimize_prompt = f"""OPTIMIZE this {language.upper()} code for {optimization_goal.upper()}:

ORIGINAL CODE:
```{language}
{code}
```

Optimization goals:
- {optimization_goal}: Primary focus
- Maintain correctness
- Keep code readable
- Document changes

Provide:

1. ANALYSIS:
   - Current bottlenecks
   - Opportunities for improvement
   - Trade-offs to consider
   
2. OPTIMIZED CODE:
   ```{language}
   [optimized version here]
   ```
   
3. IMPROVEMENTS:
   - What changed and why
   - Performance gains (with complexity analysis)
   - Any trade-offs made
   
4. BENCHMARKS:
   - How to measure improvement
   - Expected performance gains
"""
        
        return optimize_prompt
    
    def generate_tests(self, code: str, language: str = None) -> str:
        """
        Generate comprehensive tests for existing code.
        """
        if not language:
            language = self.detect_language("", code)
        
        lang_info = self.SUPPORTED_LANGUAGES.get(language, self.SUPPORTED_LANGUAGES["python"])
        
        test_prompt = f"""Generate comprehensive tests for this {language.upper()} code using {lang_info['test_framework']}:

CODE TO TEST:
```{language}
{code}
```

Generate tests that cover:

1. NORMAL CASES:
   - Typical usage scenarios
   - Expected inputs and outputs
   
2. EDGE CASES:
   - Boundary values
   - Empty/null inputs
   - Large inputs
   
3. ERROR CONDITIONS:
   - Invalid inputs
   - Exception handling
   - Error messages
   
4. INTEGRATION:
   - How components work together
   - Side effects
   
Test structure:
```{language}
# Test file with clear test names
# Use {lang_info['test_framework']} conventions
# Include setup/teardown if needed
# Add comments explaining what each test verifies
```
"""
        
        return test_prompt
    
    def explain_code(self, code: str, language: str = None, detail_level: str = "medium") -> str:
        """
        Explain what code does at different detail levels.
        detail_level: 'high' (overview), 'medium' (balanced), 'low' (line-by-line)
        """
        if not language:
            language = self.detect_language("", code)
        
        if detail_level == "high":
            prompt = f"""Explain what this {language.upper()} code does at a HIGH LEVEL:

```{language}
{code}
```

Provide:
1. OVERVIEW: What is the main purpose?
2. KEY COMPONENTS: What are the main parts?
3. FLOW: How does data move through the code?
4. RESULT: What does it produce/accomplish?
"""
        
        elif detail_level == "low":
            prompt = f"""Explain this {language.upper()} code LINE-BY-LINE:

```{language}
{code}
```

For each significant line:
- What it does
- Why it's necessary
- How it relates to the overall logic
"""
        
        else:  # medium
            prompt = f"""Explain this {language.upper()} code in DETAIL:

```{language}
{code}
```

Provide:
1. PURPOSE: What problem does this solve?
2. APPROACH: How does it solve it?
3. KEY LOGIC: Important algorithms or patterns used
4. DATA FLOW: How data is processed
5. COMPLEXITY: Time/space complexity
6. USAGE: How would you use this code?
"""
        
        return prompt
    
    def refactor_suggestions(self, code: str, language: str = None) -> str:
        """
        Suggest refactoring improvements for code.
        """
        if not language:
            language = self.detect_language("", code)
        
        refactor_prompt = f"""Suggest REFACTORING improvements for this {language.upper()} code:

```{language}
{code}
```

Analyze and suggest improvements for:

1. CODE SMELLS:
   - Duplicated code
   - Long functions/methods
   - Complex conditionals
   - Magic numbers
   
2. DESIGN PATTERNS:
   - Applicable patterns
   - Better abstractions
   - Separation of concerns
   
3. NAMING:
   - Clearer variable names
   - More descriptive function names
   - Consistent conventions
   
4. STRUCTURE:
   - Better organization
   - Reduced coupling
   - Improved cohesion
   
For each suggestion:
- Show before/after code
- Explain the benefit
- Note any trade-offs
"""
        
        return refactor_prompt
    
    def code_review(self, code: str, language: str = None) -> str:
        """
        Perform a comprehensive code review.
        """
        if not language:
            language = self.detect_language("", code)
        
        review_prompt = f"""Perform a CODE REVIEW for this {language.upper()} code:

```{language}
{code}
```

Review checklist:

1. FUNCTIONALITY:
   ✓ Does it work correctly?
   ✓ Are edge cases handled?
   ✓ Any logical errors?
   
2. READABILITY:
   ✓ Is it easy to understand?
   ✓ Good naming?
   ✓ Appropriate comments?
   
3. MAINTAINABILITY:
   ✓ Easy to modify?
   ✓ Well-structured?
   ✓ Follows conventions?
   
4. PERFORMANCE:
   ✓ Efficient algorithms?
   ✓ Any bottlenecks?
   ✓ Resource usage?
   
5. SECURITY:
   ✓ Input validation?
   ✓ Vulnerable patterns?
   ✓ Data handling?
   
6. TESTING:
   ✓ Testable design?
   ✓ Tests included?
   ✓ Coverage adequate?
   
OVERALL RATING: [Score/10]
APPROVE / REQUEST CHANGES / REJECT

Detailed feedback with specific line references and improvement suggestions.
"""
        
        return review_prompt
    
    def compare_implementations(self, code1: str, code2: str, language: str = None) -> str:
        """
        Compare two implementations of the same functionality.
        """
        if not language:
            language = self.detect_language("", code1)
        
        compare_prompt = f"""Compare these two {language.upper()} implementations:

IMPLEMENTATION A:
```{language}
{code1}
```

IMPLEMENTATION B:
```{language}
{code2}
```

Compare on:

1. CORRECTNESS:
   - Both handle all cases?
   - Any edge case differences?
   
2. PERFORMANCE:
   - Time complexity comparison
   - Space complexity comparison
   - Practical performance
   
3. READABILITY:
   - Which is clearer?
   - Easier to understand?
   
4. MAINTAINABILITY:
   - Easier to modify?
   - Better structure?
   
5. TRADE-OFFS:
   - Pros and cons of each
   - When to use which?
   
RECOMMENDATION: Which is better and why?
"""
        
        return compare_prompt
    
    def security_audit(self, code: str, language: str = None) -> str:
        """
        Audit code for security vulnerabilities.
        """
        if not language:
            language = self.detect_language("", code)
        
        security_prompt = f"""SECURITY AUDIT for this {language.upper()} code:

```{language}
{code}
```

Check for:

1. INPUT VALIDATION:
   - Untrusted input handling
   - Injection vulnerabilities
   - Type checking
   
2. AUTHENTICATION/AUTHORIZATION:
   - Proper access controls
   - Credential handling
   - Session management
   
3. DATA PROTECTION:
   - Sensitive data exposure
   - Encryption usage
   - Data sanitization
   
4. ERROR HANDLING:
   - Information leakage
   - Proper exception handling
   - Logging security
   
5. DEPENDENCIES:
   - Known vulnerable libraries
   - Outdated packages
   
6. CONFIGURATION:
   - Hardcoded secrets
   - Insecure defaults
   
RISK LEVEL: [Low/Medium/High/Critical]
VULNERABILITIES FOUND: [List with severity]
REMEDIATION: [Specific fixes]
"""
        
        return security_prompt