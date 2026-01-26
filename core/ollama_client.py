import os
import requests
import json
from typing import Generator, Optional, Dict, List
import config

class OllamaClient:
    """Enhanced Ollama client with GPU optimization for RTX 4050"""
    
    def __init__(self, model: str = None, base_url: Optional[str] = None):
        # Use config model or provided model
        self.model = model or config.DEFAULT_MODEL
        self.base_url = base_url or config.OLLAMA_URL
        self.generate_url = f"{self.base_url}/api/generate"
        self.chat_url = f"{self.base_url}/api/chat"
        
        # Initialize persistent session for connection reuse
        self.session = requests.Session()

        # Configure GPU settings
        import torch
        self.gpu_available = torch.cuda.is_available()
        self.gpu_layers = -1 if self.gpu_available else 0  # Use all GPU layers if available
        
        # ====================================================================
        # RTX 4050 OPTIMIZATION SETTINGS (Claude's Plan)
        # ====================================================================
        self.gpu_settings = config.GPU_SETTINGS.copy()
        
        if self.gpu_available:
            print(f"🚀 GPU Acceleration enabled: {torch.cuda.get_device_name(0)}")
            print(f"📊 GPU Settings (RTX 4050 Optimized):")
            print(f"   - Batch Size: {self.gpu_settings['num_batch']}")
            print(f"   - Context Window: {self.gpu_settings['num_ctx']} tokens")
            print(f"   - Threads: {self.gpu_settings['num_thread']}")
            print(f"   - FP16 KV Cache: {self.gpu_settings['f16_kv']}")
            print(f"   - Memory Mapping: {self.gpu_settings['use_mmap']}")
            print(f"   - Memory Lock: {self.gpu_settings['use_mlock']}")

    def generate_with_system(
        self, 
        system_prompt: str, 
        user_message: str, 
        max_tokens: int = 512, 
        temperature: float = 0.3
    ) -> str:
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Build options with RTX 4050 optimization
            options = {
                "temperature": temperature,
                "num_predict": min(max_tokens, self.gpu_settings["num_predict"]),
                "top_p": self.gpu_settings["top_p"],
                "top_k": self.gpu_settings["top_k"],
                "num_gpu": self.gpu_layers,
                "num_thread": self.gpu_settings["num_thread"],
                "num_batch": self.gpu_settings["num_batch"],
                "num_ctx": self.gpu_settings["num_ctx"],
                "repeat_penalty": self.gpu_settings["repeat_penalty"],
            }
            
            resp = self.session.post(
                self.chat_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "options": options,
                    "stream": False
                },
                timeout=120
            )
            
            data = resp.json()
            if "message" in data and "content" in data["message"]:
                return data["message"]["content"].strip()
            
            return self.generate(f"{system_prompt}\n\n{user_message}", max_tokens, temperature)
            
        except Exception as e:
            print(f"Chat endpoint failed: {e}, falling back to generate")
            return self.generate(f"{system_prompt}\n\n{user_message}", max_tokens, temperature)

    def _estimate_tokens(self, text: str) -> int:
        """Estimate tokens needed based on text length and complexity"""
        # Base estimation: ~1.5 tokens per word
        words = len(text.split())
        base_tokens = words * 1.5
        
        # Add extra tokens for code blocks
        code_blocks = text.count("```")
        if code_blocks > 0:
            base_tokens += code_blocks * 50  # Extra tokens for code formatting
            
        # Add tokens for special characters and technical content
        special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
        base_tokens += special_chars * 0.5
        
        return int(base_tokens * 1.5)  # Add 50% buffer for safety

    def generate(self, prompt: str, max_tokens: int = None, temperature: float = 0.2) -> str:
        try:
            # Dynamically estimate tokens if not specified
            if max_tokens is None:
                estimated_tokens = self._estimate_tokens(prompt)
                max_tokens = min(max(estimated_tokens, 256), 4096)  # Cap between 256 and 4096
            
            # Implement retrying with exponential backoff
            retries = 3
            for attempt in range(retries):
                try:
                    resp = self.session.post(
                        self.generate_url,
                        json={
                            "model": self.model,
                            "prompt": prompt,
                            "options": {
                                "temperature": temperature,
                                "num_predict": max_tokens,
                                "stop": ["User:", "USER:", "\nUser:", "\nUSER:"],
                                "num_ctx": 4096,  # Maximum context window
                                "top_k": 40,
                                "top_p": 0.9,
                                "repeat_penalty": 1.1
                            },
                            "stream": True
                        },
                        stream=True,
                        timeout=180  # Increased timeout for larger responses
                    )
                    full_text = ""
                    for line in resp.iter_lines():
                        if not line:
                            continue
                        try:
                            data = json.loads(line.decode("utf-8"))
                        except Exception:
                            continue
                        if "response" in data:
                            full_text += data["response"]
                        if data.get("done", False):
                            break
                    
                    if full_text.strip():  # Valid response received
                        return full_text.strip()
                    
                except requests.exceptions.Timeout:
                    if attempt < retries - 1:  # Don't sleep on last attempt
                        import time
                        time.sleep((attempt + 1) * 2)  # Exponential backoff
                    continue
                    
            return "ERROR: Failed to generate response after retries"
        except Exception as e:
            return f"ERROR: {e}"

    def stream_with_system(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 512,
        temperature: float = 0.3
    ) -> Generator[str, None, None]:
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            resp = self.session.post(
                self.chat_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                        "num_gpu": self.gpu_layers,  # Use GPU layers if available
                        "num_thread": 8 if not self.gpu_available else 4
                    },
                    "stream": True
                },
                stream=True,
                timeout=120
            )
            
            for line in resp.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                except Exception:
                    continue
                if "message" in data and "content" in data["message"]:
                    yield data["message"]["content"]
                if data.get("done", False):
                    break
        except Exception as e:
            yield f"ERROR: {e}"

    def stream(self, prompt: str, max_tokens: int = None, temperature: float = 0.2) -> Generator[str, None, None]:
        try:
            # Use dynamic token estimation
            if max_tokens is None:
                max_tokens = self._estimate_tokens(prompt)
                # Clamp for responsiveness so generations don't become excessively long
                max_tokens = min(max(max_tokens, 256), 1024)
                
            # Configure keepalive and chunk size for smoother streaming
            headers = {
                'Connection': 'keep-alive',
                'Accept': 'text/event-stream',
                'Cache-Control': 'no-cache'
            }
            
            resp = self.session.post(
                self.generate_url,
                headers=headers,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                        "stop": ["User:", "USER:", "\nUser:", "\nUSER:"],
                        "num_ctx": 4096,
                        "top_k": 40,
                        "top_p": 0.9,
                        "repeat_penalty": 1.1,
                        "num_gpu": self.gpu_layers,  # Use GPU layers if available
                        "num_thread": 8 if not self.gpu_available else 4
                    },
                    "stream": True
                },
                stream=True,
                timeout=180
            )

            for line in resp.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        chunk = data["response"]
                        # Stream raw chunks directly so the UI can update as fast
                        # as the model sends tokens/segments.
                        if chunk:
                            yield chunk

                    if data.get("done", False):
                        break

                except Exception as e:
                    print(f"Streaming error: {e}")
                    continue

        except Exception as e:
            yield f"ERROR: {e}"
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 512,
        temperature: float = 0.3
    ) -> str:
        try:
            resp = self.session.post(
                self.chat_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                        "num_gpu": self.gpu_layers,  # Use GPU layers if available
                        "num_thread": 8 if not self.gpu_available else 4
                    },
                    "stream": False
                },
                timeout=120
            )
            
            data = resp.json()
            if "message" in data and "content" in data["message"]:
                return data["message"]["content"].strip()
            return "ERROR: No response from model"
        except Exception as e:
            return f"ERROR: {e}"

