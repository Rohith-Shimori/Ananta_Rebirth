# vision_intelligence.py - Advanced Vision AI Engine
"""
Computer Vision and Image Analysis for Ananta
- Screenshot analysis
- Code image understanding  
- Document OCR
- Visual code review
- UI/UX analysis
"""

import os
import base64
import json
from typing import Dict, List, Optional, Union, Tuple
from PIL import Image
import io
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VisionIntelligenceEngine:
    """
    Advanced Vision AI for Ananta
    Combines computer vision with intelligent automation
    """
    
    def __init__(self):
        self.vision_model = "qwen3-vl:8b"
        self.ollama_url = "http://127.0.0.1:11434"
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        self.max_image_size = 10 * 1024 * 1024  # 10MB
        
        # Vision capabilities
        self.capabilities = {
            "code_analysis": True,
            "screenshot_analysis": True,
            "document_ocr": True,
            "ui_ux_analysis": True,
            "diagram_understanding": True,
            "error_detection": True,
            "design_to_code": True
        }
        
        logger.info("👁️ Vision Intelligence Engine initialized")
        logger.info(f"🎯 Vision model: {self.vision_model}")
        logger.info(f"📊 Capabilities: {list(self.capabilities.keys())}")
    
    def encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """Convert image to base64 for API processing"""
        try:
            # Validate file
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            file_size = os.path.getsize(image_path)
            if file_size > self.max_image_size:
                raise ValueError(f"Image too large: {file_size/1024/1024:.1f}MB > 10MB limit")
            
            # Check format
            ext = os.path.splitext(image_path)[1].lower()
            if ext not in self.supported_formats:
                raise ValueError(f"Unsupported format: {ext}")
            
            # Optimize image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large (max 1024x1024 for vision models)
                max_size = 1024
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=85, optimize=True)
                img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                logger.info(f"✅ Image encoded: {len(img_base64)} chars")
                return img_base64
                
        except Exception as e:
            logger.error(f"❌ Image encoding failed: {e}")
            return None
    
    def analyze_code_image(self, image_path: str, language_hint: str = None) -> Dict:
        """Analyze code from screenshot/image"""
        try:
            img_base64 = self.encode_image_to_base64(image_path)
            if not img_base64:
                return {"error": "Failed to process image"}
            
            # Build specialized prompt for code analysis
            prompt = self._build_code_analysis_prompt(language_hint)
            
            # Call vision model
            response = self._call_vision_model(img_base64, prompt)
            
            if response and not response.startswith("ERROR"):
                return {
                    "type": "code_analysis",
                    "success": True,
                    "analysis": response,
                    "language_detected": self._extract_language(response),
                    "code_quality": self._assess_code_quality(response),
                    "suggestions": self._extract_suggestions(response),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"error": "Vision model failed", "details": response}
                
        except Exception as e:
            logger.error(f"❌ Code analysis failed: {e}")
            return {"error": str(e)}
    
    def analyze_screenshot(self, image_path: str, context: str = None) -> Dict:
        """Analyze screenshot for contextual understanding"""
        try:
            img_base64 = self.encode_image_to_base64(image_path)
            if not img_base64:
                return {"error": "Failed to process image"}
            
            prompt = self._build_screenshot_analysis_prompt(context)
            
            response = self._call_vision_model(img_base64, prompt)
            
            if response and not response.startswith("ERROR"):
                return {
                    "type": "screenshot_analysis",
                    "success": True,
                    "analysis": response,
                    "context_detected": self._extract_context(response),
                    "elements_found": self._extract_ui_elements(response),
                    "actions_suggested": self._extract_actions(response),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"error": "Vision model failed", "details": response}
                
        except Exception as e:
            logger.error(f"❌ Screenshot analysis failed: {e}")
            return {"error": str(e)}
    
    def convert_design_to_code(self, image_path: str, target_framework: str = "html") -> Dict:
        """Convert UI design/mockup to code"""
        try:
            img_base64 = self.encode_image_to_base64(image_path)
            if not img_base64:
                return {"error": "Failed to process image"}
            
            prompt = self._build_design_to_code_prompt(target_framework)
            
            response = self._call_vision_model(img_base64, prompt)
            
            if response and not response.startswith("ERROR"):
                return {
                    "type": "design_to_code",
                    "success": True,
                    "framework": target_framework,
                    "code": response,
                    "components": self._extract_components(response),
                    "styling": self._extract_styling(response),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"error": "Vision model failed", "details": response}
                
        except Exception as e:
            logger.error(f"❌ Design-to-code failed: {e}")
            return {"error": str(e)}
    
    def analyze_document(self, image_path: str) -> Dict:
        """Extract and analyze content from document images"""
        try:
            img_base64 = self.encode_image_to_base64(image_path)
            if not img_base64:
                return {"error": "Failed to process image"}
            
            prompt = self._build_document_analysis_prompt()
            
            response = self._call_vision_model(img_base64, prompt)
            
            if response and not response.startswith("ERROR"):
                return {
                    "type": "document_analysis",
                    "success": True,
                    "content": response,
                    "text_extracted": self._extract_text(response),
                    "key_points": self._extract_key_points(response),
                    "summary": self._generate_summary(response),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"error": "Vision model failed", "details": response}
                
        except Exception as e:
            logger.error(f"❌ Document analysis failed: {e}")
            return {"error": str(e)}
    
    def detect_errors_in_image(self, image_path: str) -> Dict:
        """Detect errors in code screenshots or error messages"""
        try:
            img_base64 = self.encode_image_to_base64(image_path)
            if not img_base64:
                return {"error": "Failed to process image"}
            
            prompt = self._build_error_detection_prompt()
            
            response = self._call_vision_model(img_base64, prompt)
            
            if response and not response.startswith("ERROR"):
                return {
                    "type": "error_detection",
                    "success": True,
                    "analysis": response,
                    "errors_found": self._extract_errors(response),
                    "solutions": self._extract_solutions(response),
                    "severity": self._assess_error_severity(response),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"error": "Vision model failed", "details": response}
                
        except Exception as e:
            logger.error(f"❌ Error detection failed: {e}")
            return {"error": str(e)}
    
    def _call_vision_model(self, image_base64: str, prompt: str) -> str:
        """Call the vision model via Ollama API"""
        try:
            import requests
            
            payload = {
                "model": self.vision_model,
                "prompt": prompt,
                "images": [image_base64],
                "options": {
                    "temperature": 0.1,
                    "num_predict": 2048,
                    "top_p": 0.9,
                    "top_k": 40
                },
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=180  # Extended timeout for large images
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                return f"ERROR: API returned {response.status_code}"
                
        except Exception as e:
            logger.error(f"❌ Vision model call failed: {e}")
            return f"ERROR: {str(e)}"
    
    def _build_code_analysis_prompt(self, language_hint: str = None) -> str:
        """Build specialized prompt for code analysis"""
        hint_text = f"The code appears to be in {language_hint}." if language_hint else ""
        
        return f"""Analyze this code image in detail. {hint_text}

Provide:
1. Language and framework identification
2. Code structure and architecture
3. Quality assessment (best practices, potential issues)
4. Functionality explanation
5. Improvement suggestions
6. Security considerations
7. Performance optimization opportunities

Be thorough and actionable. Focus on practical insights a developer can use."""
    
    def _build_screenshot_analysis_prompt(self, context: str = None) -> str:
        """Build prompt for screenshot analysis"""
        context_text = f"Context: {context}" if context else ""
        
        return f"""Analyze this screenshot in detail. {context_text}

Identify:
1. Application type and purpose
2. UI/UX elements and components
3. User interface patterns
4. Technologies/frameworks likely used
5. Design principles and accessibility
6. Potential improvements
7. Actions that could be automated

Provide actionable insights for developers and designers."""
    
    def _build_design_to_code_prompt(self, target_framework: str) -> str:
        """Build prompt for design-to-code conversion"""
        return f"""Convert this UI design/mockup to clean, modern {target_framework.upper()} code.

Requirements:
1. Semantic HTML structure
2. Modern CSS with responsive design
3. Accessible markup (ARIA labels, etc.)
4. Clean, maintainable code
5. Component-based structure
6. Proper styling and layout

Provide complete, working code that matches the design exactly."""
    
    def _build_document_analysis_prompt(self) -> str:
        """Build prompt for document analysis"""
        return """Extract and analyze all content from this document image.

Provide:
1. Complete text extraction (preserving structure)
2. Key information and main points
3. Summary of the document
4. Important details and data
5. Action items or next steps
6. Context and purpose of the document

Be thorough and accurate in extraction."""
    
    def _build_error_detection_prompt(self) -> str:
        """Build prompt for error detection"""
        return """Analyze this image for errors, bugs, or issues.

Identify:
1. Error messages and their meanings
2. Code bugs or syntax issues
3. Logic problems
4. Performance bottlenecks
5. Security vulnerabilities
6. UI/UX issues
7. Configuration problems

For each error found, provide:
- Clear explanation
- Root cause analysis
- Specific solution steps
- Prevention recommendations"""
    
    # Helper methods for extracting structured data
    def _extract_language(self, response: str) -> str:
        """Extract programming language from analysis"""
        languages = ['python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'typescript', 'html', 'css']
        response_lower = response.lower()
        for lang in languages:
            if lang in response_lower:
                return lang
        return "unknown"
    
    def _assess_code_quality(self, response: str) -> str:
        """Assess code quality from analysis"""
        if "excellent" in response.lower() or "well-structured" in response.lower():
            return "high"
        elif "needs improvement" in response.lower() or "issues" in response.lower():
            return "medium"
        elif "poor" in response.lower() or "major issues" in response.lower():
            return "low"
        return "medium"
    
    def _extract_suggestions(self, response: str) -> List[str]:
        """Extract improvement suggestions from response"""
        suggestions = []
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['suggest', 'recommend', 'improve', 'fix', 'add']):
                suggestions.append(line.strip())
        return suggestions[:5]  # Return top 5 suggestions
    
    def _extract_context(self, response: str) -> str:
        """Extract context information"""
        contexts = ['development', 'design', 'documentation', 'error', 'tutorial', 'dashboard']
        response_lower = response.lower()
        for context in contexts:
            if context in response_lower:
                return context
        return "general"
    
    def _extract_ui_elements(self, response: str) -> List[str]:
        """Extract UI elements from analysis"""
        elements = ['button', 'input', 'menu', 'navigation', 'form', 'modal', 'card', 'table', 'chart']
        found = []
        response_lower = response.lower()
        for element in elements:
            if element in response_lower:
                found.append(element)
        return found
    
    def _extract_actions(self, response: str) -> List[str]:
        """Extract actionable items from analysis"""
        actions = []
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['automate', 'implement', 'create', 'optimize', 'improve']):
                actions.append(line.strip())
        return actions[:3]
    
    def _extract_components(self, response: str) -> List[str]:
        """Extract components from generated code"""
        components = []
        lines = response.split('\n')
        for line in lines:
            if 'component' in line.lower() or 'class' in line.lower() or 'function' in line.lower():
                components.append(line.strip())
        return components[:10]
    
    def _extract_styling(self, response: str) -> List[str]:
        """Extract styling information"""
        styles = []
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['color', 'size', 'margin', 'padding', 'font']):
                styles.append(line.strip())
        return styles[:10]
    
    def _extract_text(self, response: str) -> str:
        """Extract clean text from document analysis"""
        # Simple extraction - in production, use more sophisticated NLP
        return response.replace('\n', ' ').strip()
    
    def _extract_key_points(self, response: str) -> List[str]:
        """Extract key points from document"""
        points = []
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['important', 'key', 'main', 'critical']):
                points.append(line.strip())
        return points[:5]
    
    def _generate_summary(self, response: str) -> str:
        """Generate summary from analysis"""
        # Simple summary - first few sentences
        sentences = response.split('. ')
        return '. '.join(sentences[:3]) + '.'
    
    def _extract_errors(self, response: str) -> List[Dict]:
        """Extract errors from analysis"""
        errors = []
        lines = response.split('\n')
        for i, line in enumerate(lines):
            if 'error' in line.lower() or 'issue' in line.lower():
                errors.append({
                    "line": i,
                    "description": line.strip()
                })
        return errors[:5]
    
    def _extract_solutions(self, response: str) -> List[str]:
        """Extract solutions from error analysis"""
        solutions = []
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['solution', 'fix', 'resolve', 'correct']):
                solutions.append(line.strip())
        return solutions[:5]
    
    def _assess_error_severity(self, response: str) -> str:
        """Assess error severity"""
        if "critical" in response.lower() or "severe" in response.lower():
            return "high"
        elif "minor" in response.lower() or "low" in response.lower():
            return "low"
        return "medium"
    
    def get_capabilities(self) -> Dict:
        """Get vision engine capabilities"""
        return {
            "vision_model": self.vision_model,
            "supported_formats": self.supported_formats,
            "max_image_size": f"{self.max_image_size/1024/1024:.0f}MB",
            "capabilities": self.capabilities,
            "gpu_accelerated": True
        }
