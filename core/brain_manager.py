import time
import requests
import json
from typing import Optional, Dict, Any

# --- Import Your Original Engines ---
from .ollama_client import OllamaClient
from .retriever import Retriever
from ..engines.personality_engine import PersonalityEngine
from ..engines.code_expert import CodeExpert
from ..engines.project_scaffolder import ProjectScaffolder
from ..memory.adaptive_memory import AdaptiveMemory
from ..memory.context_manager import ContextManager

class BrainManager:
    def __init__(self):
        # 1. Initialize The Neural Modes
        self.MODES = {
            "sentinel": {
                "model": "qwen3-vl:8b", 
                "color": "#00F0FF", 
                "type": "GPU (Fast)",
                "desc": "Daily Driver, Vision, Chat"
            },
            "architect": {
                "model": "gpt-oss:20b", 
                "color": "#FFD700", 
                "type": "CPU/RAM (Builder)",
                "desc": "Code Generation, Project Structure"
            },
            "oracle": {
                "model": "phi4-reasoning", 
                "color": "#BD00FF", 
                "type": "CPU/RAM (Logic)",
                "desc": "Deep Reasoning, Math, Analysis"
            }
        }
        
        # 2. Initialize The Tools (The "Body")
        print("⚙️ Loading Ananta Engines...")
        self.retriever = Retriever()
        self.personality = PersonalityEngine()
        self.code_expert = CodeExpert()
        self.scaffolder = ProjectScaffolder()
        self.memory = AdaptiveMemory()
        self.context_mgr = ContextManager(embedder=self.retriever.embedder)
        
        # 3. Start System
        self.current_mode = "sentinel"
        self.client = OllamaClient(model=self.MODES["sentinel"]["model"])
        print(f"🛡️ Ananta Ultimate Online: {self.current_mode.upper()}")

    def set_mode(self, mode_name: str):
        """Switches brains and unloads previous model to save RAM"""
        if mode_name not in self.MODES:
            return "System Error: Invalid Neural Mode"
            
        if self.current_mode == mode_name:
            return f"Already in {mode_name.upper()} mode."

        print(f"🔄 SHIFTING GEARS: {self.current_mode.upper()} -> {mode_name.upper()}")
        
        # Kill old model
        self.client.unload_model()
        
        # Set new model
        target_model = self.MODES[mode_name]["model"]
        self.current_mode = mode_name
        self.client.model = target_model
        
        return f"System: Switched to {mode_name.upper()} ({self.MODES[mode_name]['type']})"

    def process_query(self, text: str):
        """
        The Master Logic Pipeline:
        1. Check Commands
        2. Retrieve Context (Memory)
        3. Enhance Prompt (Personality/Expertise)
        4. Generate
        5. Save Memory
        """
        # --- 1. Mode Switching Commands ---
        if text.lower() in ["/architect", "mode: architect"]: return self.set_mode("architect")
        if text.lower() in ["/oracle", "mode: oracle"]:    return self.set_mode("oracle")
        if text.lower() in ["/sentinel", "mode: sentinel"]: return self.set_mode("sentinel")

        # --- 2. Context Retrieval (RAG) ---
        # We get relevant docs regardless of mode, but usage varies
        context_str = ""
        try:
            recent_memories = self.context_mgr.get_relevant_context(text, top_k=3)
            retrieved_docs = self.retriever.query(text, top_k=2)
            
            doc_text = "\n".join([d['document'] for d in retrieved_docs])
            mem_text = "\n".join(recent_memories)
            
            context_str = f"MEMORY CONTEXT:\n{mem_text}\n\nKNOWLEDGE BASE:\n{doc_text}\n"
        except Exception as e:
            print(f"⚠️ Memory Retrieval Warning: {e}")

        # --- 3. Prompt Engineering by Mode ---
        final_prompt = ""
        
        if self.current_mode == "sentinel":
            # SENTINEL: Focus on Personality & Conversation
            system_prompt = self.personality.build_dynamic_prompt(text, base_prompt="You are Ananta, a helpful AI Assistant.")
            final_prompt = f"{system_prompt}\n\n{context_str}\nUser: {text}"

        elif self.current_mode == "architect":
            # ARCHITECT: Focus on Code Structure
            # We use your CodeExpert engine to build the prompt
            lang = self.code_expert.detect_language(text)
            tech_prompt = self.code_expert._build_generation_prompt(text, lang, include_tests=True)
            final_prompt = f"You are in ARCHITECT MODE. Focus on high-quality code.\n{context_str}\n{tech_prompt}"

        elif self.current_mode == "oracle":
            # ORACLE: Focus on Pure Logic (Chain of Thought)
            final_prompt = f"You are in ORACLE MODE. Think step-by-step. Verify every assumption.\n{context_str}\nProblem: {text}\n\nDetailed Solution:"

        # --- 4. Execution ---
        response = self.client.generate(final_prompt)

        # --- 5. Memory Storage ---
        # We save the interaction to short-term and long-term memory
        self.memory.add_memory("user", text, importance=5)
        self.memory.add_memory("assistant", response, importance=5)
        self.context_mgr.add_turn("user", text)
        self.context_mgr.add_turn("assistant", response)

        return response

    def get_status(self):
        return {
            "mode": self.current_mode,
            "color": self.MODES[self.current_mode]["color"],
            "model": self.MODES[self.current_mode]["model"]
        }