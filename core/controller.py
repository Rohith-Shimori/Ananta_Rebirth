"""
Ananta Ultimate Controller
Integrates ALL features: Voice, Proactive, Code Execution, Self-Improvement
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from core.ollama_client import OllamaClient
from core.retriever import Retriever
from engines.personality_engine import PersonalityEngine
from engines.creative_engine import CreativeEngine
from engines.code_expert import CodeExpert
from engines.project_scaffolder import ProjectScaffolder
from memory.adaptive_memory import AdaptiveMemory
from memory.context_manager import ContextManager
from intelligence.self_improvement import SelfImprovementEngine

# Import advanced JARVIS-like features
from core.context_engine import RealTimeContextEngine
from core.emotional_intelligence import EmotionalIntelligence
from core.advanced_emotional_intelligence import AdvancedEmotionalIntelligence
from core.proactive_intelligence import ProactiveIntelligence
from core.security_engine import AdvancedSecurityEngine
from core.system_monitor import SystemMonitoringEngine

# Import Phase 1: Smart Model Routing (Claude's Optimization)
from core.smart_model_router import SmartModelRouter

# Import Phase 2-6: Advanced Optimization Components (Claude's Optimization)
from core.batch_inference_engine import BatchInferenceEngine
from core.lightweight_agent_orchestrator import LightweightAgentOrchestrator
from memory.lightweight_vector_db import LightweightVectorDB
from core.context_window_manager import ContextWindowManager
from core.usage_pattern_tracker import UsagePatternTracker
from core.intelligent_preloader import IntelligentPreloader

# Import new features
try:
    from features.voice_interface import VoiceInterface
    VOICE_AVAILABLE = True
except:
    VOICE_AVAILABLE = False
    print("⚠️  Voice interface not available. Install: pip install pyttsx3 speechrecognition")

try:
    from features.proactive_assistant import ProactiveAssistant
    PROACTIVE_AVAILABLE = True
except:
    PROACTIVE_AVAILABLE = False

try:
    from features.code_executor import CodeExecutor
    EXECUTOR_AVAILABLE = True
except:
    EXECUTOR_AVAILABLE = False

import uuid
import time
import json
import re
from typing import List, Optional
import config

class AnantaController:
    """
    Ultimate Ananta Controller - Better than Jarvis/Friday
    """
    
    def __init__(self, model: str = None):
        # Use configured model or default
        self.model = model or config.DEFAULT_MODEL
        
        # Initialize model-specific settings
        self.coding_model = config.CODING_MODEL
        self.fast_model = config.FAST_MODEL
        self.vision_model = config.VISION_MODEL
        self.powerful_model = config.DEFAULT_MODEL  # Use default as powerful
        
        # Core systems
        self.ollama = OllamaClient(model=self.model)
        self.retriever = Retriever()
        self.personality = PersonalityEngine()
        self.creative = CreativeEngine()
        self.code_expert = CodeExpert()
        self.scaffolder = ProjectScaffolder()
        self.memory = AdaptiveMemory()
        # Share the same SentenceTransformer between retriever and context manager
        self.context_mgr = ContextManager(embedder=self.retriever.embedder)
        self.self_improve = SelfImprovementEngine()
        
        # Advanced Vision-Automation System
        from intelligence.vision_intelligence import VisionIntelligenceEngine
        from automation.smart_automation_engine import SmartAutomationEngine
        self.vision = VisionIntelligenceEngine()
        self.automation = SmartAutomationEngine()
        
        print("👁️ Vision Intelligence Engine loaded")
        print("🤖 Smart Automation Engine loaded")
        
        # New features
        if VOICE_AVAILABLE:
            self.voice = VoiceInterface()
            print("✅ Voice interface loaded")
        
        if PROACTIVE_AVAILABLE:
            self.proactive = ProactiveAssistant(data_dir=str(config.DATA_DIR))
            print("✅ Proactive assistant loaded")
        
        if EXECUTOR_AVAILABLE:
            self.executor = CodeExecutor()
            print("✅ Code executor loaded")
        
        # Load persona
        try:
            persona_file = config.DATA_DIR / "persona.json"
            with open(persona_file, 'r') as f:
                self.persona = json.load(f)
        except:
            self.persona = {}
        
        # Initialize advanced JARVIS-like features
        self.context_engine = RealTimeContextEngine()
        self.emotional_intelligence = EmotionalIntelligence()
        self.advanced_emotional_intelligence = AdvancedEmotionalIntelligence(use_ai_analysis=True)
        self.proactive_intelligence = ProactiveIntelligence()
        self.security_engine = AdvancedSecurityEngine()
        self.system_monitor = SystemMonitoringEngine()
        
        # PHASE 1: SMART MODEL ROUTING (Claude's Optimization)
        self.model_router = SmartModelRouter()
        print("🎯 Smart Model Router initialized (Phase 1)")
        
        # PHASE 2-6: ADVANCED OPTIMIZATION COMPONENTS (Claude's Optimization)
        self.batch_engine = BatchInferenceEngine()
        print("📦 Batch Inference Engine initialized (Phase 2)")
        
        self.agent_orchestrator = LightweightAgentOrchestrator()
        print("🤖 Lightweight Agent Orchestrator initialized (Phase 3)")
        
        self.vector_db = LightweightVectorDB()
        print("🗄️  Lightweight Vector DB initialized (Phase 6)")
        
        self.context_window_mgr = ContextWindowManager()
        print("📊 Context Window Manager initialized (Phase 2)")
        
        self.usage_tracker = UsagePatternTracker()
        print("📈 Usage Pattern Tracker initialized (Phase 3)")
        
        self.preloader = IntelligentPreloader(usage_tracker=self.usage_tracker)
        print("📦 Intelligent Preloader initialized (Phase 5)")
        
        # Start system monitoring
        self.system_monitor.start_monitoring(interval=10)
        
        print(f"\n🚀 Ananta Ultimate Controller initialized with {self.model}")
        print("✅ Advanced context awareness enabled")
        print("✅ Emotional intelligence enabled")
        print("✅ Proactive intelligence enabled")
        print("✅ Advanced security engine enabled")
        print("✅ System monitoring and optimization enabled")
        print("✅ Smart model routing enabled (Phase 1 - Claude's Optimization)")
        print("✅ Batch inference enabled (Phase 2)")
        print("✅ Agent orchestration enabled (Phase 3)")
        print("✅ Vector database enabled (Phase 6)")
        print("✅ Context window optimization enabled (Phase 2)")
        print("✅ Usage pattern tracking enabled (Phase 3)")
        print("✅ Intelligent preloading enabled (Phase 5)")
    
    def query(self, user_input: str, use_memory: bool = True, 
              reasoning_mode: str = "off") -> dict:
        """
        Enhanced main query method with JARVIS-like intelligence
        """
        # Get real-time context
        full_context = self.context_engine.get_full_context()
        
        # Analyze user emotion with ADVANCED emotional intelligence
        user_emotion = self.advanced_emotional_intelligence.analyze_text_emotion(user_input, full_context.get('user', {}))
        
        # Determine emotional response
        emotional_state = self.advanced_emotional_intelligence.determine_response_emotion(user_emotion, full_context.get('user', {}))
        
        # Get proactive suggestions
        recent_interactions = self.memory.get_recent_memories(limit=10)
        proactive_suggestions = self.proactive_intelligence.analyze_and_suggest(full_context, recent_interactions)
        
        # Track interaction
        self.self_improve.track_interaction(
            query_type="query",
            success=True,
            reasoning_used=(reasoning_mode != "off"),
            emotional_context=user_emotion.primary_emotion.value,
            proactive_count=len(proactive_suggestions)
        )
        
        # Classify query
        bucket = self._classify_query(user_input)
        
        # Handle identity queries with emotional intelligence
        if bucket == "identity":
            response = self._handle_identity(user_input)
            # Add emotional context
            emotional_response = self.advanced_emotional_intelligence.generate_emotional_response(
                emotional_state, user_input, full_context.get('user', {})
            )
            response['response'] = f"{emotional_response} {response['response']}"
            response['context'] = full_context
            response['proactive_suggestions'] = [s.message for s in proactive_suggestions[:2]]
            return response
        
        # Handle personal memory with emotional awareness
        if bucket.startswith("personal"):
            response = self._handle_personal(user_input, bucket)
            emotional_response = self.advanced_emotional_intelligence.generate_emotional_response(
                emotional_state, user_input, full_context.get('user', {})
            )
            response['response'] = f"{emotional_response} {response['response']}"
            response['context'] = full_context
            response['proactive_suggestions'] = [s.message for s in proactive_suggestions[:2]]
            return response
        
        # Handle creative requests
        if bucket.startswith("creative"):
            return self._handle_creative(user_input, bucket)
        
        # Handle code requests
        if "code" in bucket:
            return self._handle_code(user_input, reasoning_mode)
        
        # Default: Enhanced knowledge query with full context
        return self._handle_enhanced_knowledge(user_input, use_memory, reasoning_mode, full_context, emotional_state)
    
    def _classify_query(self, text: str) -> str:
        """Classify user query"""
        lower = text.lower()
        
        # Identity
        if any(p in lower for p in ["who are you", "what are you", "your purpose"]):
            return "identity"
        
        # Creative
        creative_type = self.creative.detect_creative_intent(text)
        if creative_type:
            return f"creative_{creative_type}"
        
        # Code
        if any(word in lower for word in ["write code", "generate code", "implement", "function"]):
            return "code_generation"
        
        if any(word in lower for word in ["analyze code", "review code", "debug"]):
            return "code_analysis"
        
        # Personal memory
        if lower.startswith(("what is my", "what's my", "do you remember")):
            return "personal_retrieve"
        
        if any(phrase in lower for phrase in ["my name is", "my favorite", "i like"]):
            return "personal_store"
        
        return "knowledge"
    
    def _handle_identity(self, user_input: str) -> dict:
        """Handle identity questions"""
        q_lower = user_input.lower()
        answers = self.persona.get("identity_answers", {})
        
        # Check interaction count
        mem = self.memory.get_recent_memories(limit=1)
        is_first = len(mem) == 0
        
        if "who are you" in q_lower:
            greeting = self.personality.get_contextual_greeting(is_first)
            # Record in semantic context
            self.context_mgr.add_turn("user", user_input)
            self.context_mgr.add_turn("assistant", greeting)
            return {"response": greeting, "bucket": "identity"}
        
        if "what do you want" in q_lower:
            response = answers.get(
                "what_do_you_want_to_become", 
                "I want to evolve into your ultimate AI partner!",
            )
            self.context_mgr.add_turn("user", user_input)
            self.context_mgr.add_turn("assistant", response)
            return {
                "response": response,
                "bucket": "identity"
            }
        
        response = self.persona.get("intro", "I'm Ananta, your AI partner.")
        self.context_mgr.add_turn("user", user_input)
        self.context_mgr.add_turn("assistant", response)
        return {
            "response": response,
            "bucket": "identity"
        }
    
    def _handle_personal(self, user_input: str, bucket: str) -> dict:
        """Handle personal memory"""
        if bucket == "personal_store":
            # Extract and store fact
            fact = self._extract_fact(user_input)
            if fact:
                category, value, importance = fact
                self.memory.store_fact(category, value, importance=importance)
                # Also track this exchange in adaptive memory and semantic context
                confirmation = f"Got it! I'll remember that your {category.replace('_', ' ')} is {value}."
                self.memory.add_memory(
                    "user", user_input, memory_type="personal", importance=importance
                )
                self.memory.add_memory(
                    "assistant", confirmation, memory_type="personal", importance=importance
                )
                self.context_mgr.add_turn("user", user_input)
                self.context_mgr.add_turn("assistant", confirmation)
                return {
                    "response": confirmation,
                    "bucket": "personal_store"
                }
        
        if bucket == "personal_retrieve":
            # Retrieve fact
            q_lower = user_input.lower()
            
            if "name" in q_lower:
                fact = self.memory.get_fact("name")
                if fact:
                    response = f"Your name is {fact['value']}."
                    self.memory.add_memory(
                        "user", user_input, memory_type="personal", importance=7
                    )
                    self.memory.add_memory(
                        "assistant", response, memory_type="personal", importance=7
                    )
                    self.context_mgr.add_turn("user", user_input)
                    self.context_mgr.add_turn("assistant", response)
                    return {"response": response, "bucket": "personal"}
            
            if "favorite" in q_lower:
                facts = self.memory.get_all_facts(min_importance=1)
                favorites = [f for f in facts if f['category'].startswith('favorite_')]
                if favorites:
                    items = ", ".join([f"{f['category'].replace('favorite_', '')}: {f['value']}" 
                                          for f in favorites])
                    response = f"Your favorites: {items}"
                    self.memory.add_memory(
                        "user", user_input, memory_type="personal", importance=6
                    )
                    self.memory.add_memory(
                        "assistant", response, memory_type="personal", importance=6
                    )
                    self.context_mgr.add_turn("user", user_input)
                    self.context_mgr.add_turn("assistant", response)
                    return {"response": response, "bucket": "personal"}
        
        fallback = "I don't have that information yet."
        self.context_mgr.add_turn("user", user_input)
        self.context_mgr.add_turn("assistant", fallback)
        return {"response": fallback, "bucket": "personal"}
    
    def _extract_fact(self, text: str) -> Optional[tuple]:
        """Extract personal fact from text"""
        text_l = text.lower()
        
        patterns = [
            (r"my name is\s+([A-Za-z\s]+)", "name", 10),
            (r"my favorite ([A-Za-z\s]+)\s+(?:is|:)\s*(.+)", "favorite_{0}", 7),
            (r"i am (\d+)\s*years?\s*old", "age", 6),
            (r"i live in\s+([A-Za-z\s,]+)", "location", 7),
        ]
        
        for pattern, key, importance in patterns:
            m = re.search(pattern, text_l, re.I)
            if m:
                if "{0}" in key:
                    category = key.format(m.group(1).strip().lower())
                    value = m.group(2).strip()
                else:
                    category = key
                    value = m.group(1).strip()
                return (category, value, importance)
        
        return None
    
    def _handle_creative(self, user_input: str, bucket: str) -> dict:
        """Handle creative requests"""
        creative_type = bucket.replace("creative_", "")
        base_prompt = self._build_system_prompt(user_input)
        creative_prompt = self.creative.build_creative_prompt(
            user_input, creative_type, base_prompt
        )
        
        response = self.ollama.generate(creative_prompt, max_tokens=768, temperature=0.7)
        
        # Store in memory
        self.memory.add_memory("user", user_input, memory_type="conversation", importance=6)
        self.memory.add_memory("assistant", response, memory_type="conversation", importance=6)
        # Track in semantic context
        self.context_mgr.add_turn("user", user_input)
        self.context_mgr.add_turn("assistant", response)
        
        return {
            "response": response,
            "bucket": bucket,
            "creative_type": creative_type
        }
    
    def _handle_code(self, user_input: str, reasoning_mode: str) -> dict:
        """Handle code-related queries with specialized coding model"""
        language = self.code_expert.detect_language(user_input)
        
        # Use specialized coding model for better performance
        coding_ollama = OllamaClient(model=self.coding_model)
        
        # Build code generation prompt
        code_prompt = self.code_expert._build_generation_prompt(
            user_input, language, include_tests=True, include_examples=True
        )
        
        # Add reasoning if requested
        if reasoning_mode == "readable":
            code_prompt += "\n\nProvide brief reasoning about your approach first."
        elif reasoning_mode == "full":
            code_prompt += "\n\nProvide detailed step-by-step reasoning."
        
        response = coding_ollama.generate(code_prompt, max_tokens=1024, temperature=0.2)
        
        # Parse reasoning if present
        reasoning = None
        if reasoning_mode != "off":
            parts = re.split(r"\bfinal answer\b|\bcode\b", response, flags=re.I, maxsplit=1)
            if len(parts) >= 2:
                reasoning = parts[0].strip()
                response = parts[1].strip()
        
        result = {
            "response": response,
            "bucket": "code",
            "language": language,
            "mode": reasoning_mode,
            "model_used": self.coding_model
        }
        
        if reasoning:
            result["reasoning"] = reasoning
        
        # Track in semantic context for future reference
        self.context_mgr.add_turn("user", user_input)
        self.context_mgr.add_turn("assistant", response)
        return result
    
    def _handle_knowledge(self, user_input: str, use_memory: bool, 
                         reasoning_mode: str) -> dict:
        """Handle knowledge queries with full context"""
        # Get context from retriever
        context_texts = []
        if use_memory:
            retrieved = self.retriever.query(user_input, top_k=3)
            for r in retrieved:
                context_texts.append(r.get("document", "")[:800])
        
        # Get relevant past context
        relevant_context = self.context_mgr.get_relevant_context(
            user_input, top_k=2, include_recent=True
        )
        
        # Build prompt
        prompt = self._build_knowledge_prompt(
            user_input, context_texts, relevant_context, reasoning_mode
        )
        
        # Generate response
        response = self.ollama.generate(prompt, max_tokens=768, temperature=0.25)
        
        # Parse reasoning
        reasoning = None
        final = response
        
        if reasoning_mode in ("readable", "full"):
            parts = re.split(r"\bfinal answer\b\s*[:\-]?", response, flags=re.I)
            if len(parts) >= 2:
                reasoning = parts[0].strip()
                final = parts[1].strip()
        
        # Store in memory
        self.memory.add_memory("user", user_input, memory_type="conversation", importance=5)
        self.memory.add_memory("assistant", final, memory_type="conversation", importance=5)
        # Track in semantic context
        self.context_mgr.add_turn("user", user_input)
        self.context_mgr.add_turn("assistant", final)
        
        result = {
            "response": final,
            "context_used": context_texts + relevant_context,
            "bucket": "knowledge",
            "mode": reasoning_mode
        }
        
        if reasoning:
            result["reasoning"] = reasoning
        
        return result
    
    def _build_system_prompt(self, user_input: str = "") -> str:
        """Build dynamic system prompt"""
        base = f"""You are Ananta, an ultimate AI partner powered by {self.model}.

Core traits:
- Intelligent and adaptive
- Clear and concise
- Supportive but honest
- Expert in coding, reasoning, and creativity

Current capabilities:
- Voice interface with emotion
- Proactive assistance
- Real-time code execution
- Self-improvement
- Multi-language expertise

Respond naturally to: {user_input}
"""
        
        if user_input and self.personality:
            base = self.personality.build_dynamic_prompt(user_input, base)
        
        return base
    
    def _build_knowledge_prompt(self, user_input: str, context_texts: List[str],
                                relevant_context: List[str], reasoning_mode: str) -> str:
        """Build complete knowledge prompt"""
        system = self._build_system_prompt(user_input)
        
        ctx = "\n".join(context_texts) if context_texts else ""
        recent = "\n".join(relevant_context) if relevant_context else ""
        
        prompt = f"""{system}

Context from knowledge base:
{ctx}

Recent relevant conversations:
{recent}

User: {user_input}

Assistant guidelines:
- Be concise and precise; avoid repetition.
- Use clear, ordered structure (steps or bullet points) when helpful.
- If you are unsure or missing information, say so explicitly and ask a short clarifying question instead of guessing.

"""
        
        if reasoning_mode == "readable":
            prompt += "\nProvide brief reasoning, then your final answer."
        elif reasoning_mode == "full":
            prompt += "\nProvide detailed step-by-step reasoning, then your final answer."
        
        return prompt
    
    def stream_query(self, text: str, use_memory: bool = True, 
                    reasoning_mode: str = "off"):
        """Enhanced streaming version of query with context and adaptive response"""
        bucket = self._classify_query(text)
        
        # For simple responses, stream in chunks for consistent UI
        if bucket in ("identity", "personal_store", "personal_retrieve"):
            result = self.query(text, use_memory, reasoning_mode)
            response = result.get("response", "")
            for chunk in self._chunk_response(response):
                yield json.dumps({"response": chunk}) + "\n"
            return
            
        # For knowledge and code queries, use enhanced streaming
        context_texts = []
        if use_memory:
            # Get relevant context
            retrieved = self.retriever.query(text, top_k=3)
            for r in retrieved:
                context_texts.append(r.get("document", "")[:800])
                
        # Get conversation context
        relevant_context = self.context_mgr.get_relevant_context(
            text, top_k=2, include_recent=True
        )
        
        # Build enhanced prompt
        prompt = self._build_knowledge_prompt(
            text, context_texts, relevant_context, reasoning_mode
        )

        # Share context metadata up-front
        context_payload = {}
        if context_texts:
            context_payload["retrieved"] = context_texts
        if relevant_context:
            context_payload["recent"] = relevant_context
        if context_payload:
            yield json.dumps({"context": context_payload}) + "\n"
        
        # Stream with fine-grained chunks so the UI feels like true typing
        reasoning_buffer = ""
        is_reasoning = reasoning_mode != "off"
        reasoning_complete = False
        reasoning_token_count = 0
        full_response = ""
        
        for chunk in self.ollama.stream(prompt, temperature=0.25):
            # Detect error sentinel from OllamaClient.stream and surface as structured error
            if isinstance(chunk, str) and chunk.startswith("ERROR:"):
                error_message = chunk.split("ERROR:", 1)[1].strip() or "Upstream model error"
                yield json.dumps({"error": error_message}) + "\n"
                return

            if is_reasoning and not reasoning_complete:
                # Check for transition from reasoning to final answer
                if "final answer" in chunk.lower():
                    reasoning_complete = True
                    if reasoning_buffer:
                        yield json.dumps({
                            "reasoning": reasoning_buffer.strip(),
                            "response": ""
                        }) + "\n"
                        reasoning_buffer = ""
                    continue
                chunk_tokens = len(chunk.strip().split()) if chunk.strip() else 0
                reasoning_token_count += chunk_tokens
                reasoning_buffer += chunk
                continue
                
            # For the visible response, stream each chunk directly so the client
            # can render smooth typing inside the assistant bubble.
            if not chunk:
                continue

            response_chunk = {
                "response": chunk,
            }
            if reasoning_complete and reasoning_buffer:
                response_chunk["reasoning"] = reasoning_buffer.strip()
                reasoning_buffer = ""

            # Accumulate full response text for memory/context logging
            full_response += chunk
            yield json.dumps(response_chunk) + "\n"

        # After streaming finishes, surface any remaining reasoning/metadata
        if reasoning_buffer.strip() or reasoning_token_count:
            final_chunk = {}
            if reasoning_buffer.strip():
                final_chunk["reasoning"] = reasoning_buffer.strip()
            if reasoning_token_count:
                final_chunk["meta"] = {"reasoning_tokens": reasoning_token_count}
            if final_chunk:
                yield json.dumps(final_chunk) + "\n"

        # After streaming finishes, store conversation in adaptive memory and context
        if full_response.strip():
            self.memory.add_memory("user", text, memory_type="conversation", importance=5)
            self.memory.add_memory("assistant", full_response.strip(), memory_type="conversation", importance=5)
            self.context_mgr.add_turn("user", text)
            self.context_mgr.add_turn("assistant", full_response.strip())
    
    def _chunk_response(self, text: str, max_chars: int = 160):
        """Yield natural language chunks for streaming simple responses."""
        if not text:
            return
        buffer: list[str] = []
        length = 0
        for word in text.split():
            buffer.append(word)
            length += len(word) + 1
            if length >= max_chars or any(word.endswith(p) for p in (".", "?", "!")):
                yield " ".join(buffer).strip()
                buffer = []
                length = 0
        if buffer:
            yield " ".join(buffer).strip()
    
    # Helper methods for app endpoints
    def get_user_name(self) -> str:
        """Get user's name from memory"""
        fact = self.memory.get_fact("name")
        return fact["value"] if fact else ""
    
    def get_pending_tasks(self) -> List[dict]:
        """Get pending tasks"""
        # Placeholder - implement with task manager if needed
        return []
    
    def get_recent_topic(self) -> str:
        """Get recent conversation topic"""
        recent = self.memory.get_recent_memories(limit=2, memory_type="conversation")
        if recent:
            return recent[0].get("content", "")[:50]
        return ""
    
    def generate_code(self, description: str, language: str, include_tests: bool) -> dict:
        """Generate code with tests"""
        result = self.code_expert.generate_code_with_docs(
            description, language, include_tests, include_examples=True
        )
        
        # Actually generate the code
        prompt = result["prompt"]
        code = self.ollama.generate(prompt, max_tokens=1024, temperature=0.2)
        
        result["generated_code"] = code
        return result
    
    def analyze_code(self, code: str, language: str = None) -> dict:
        """Analyze code quality"""
        analysis = self.code_expert.analyze_code(code, language)
        prompt = analysis["analysis_prompt"]
        
        result = self.ollama.generate(prompt, max_tokens=768, temperature=0.3)
        
        return {
            "language": analysis["language"],
            "analysis": result
        }
    
    def explain_code(self, code: str, detail_level: str = "medium") -> dict:
        """Explain code"""
        language = self.code_expert.detect_language("", code)
        prompt = self.code_expert.explain_code(code, language, detail_level)
        
        explanation = self.ollama.generate(prompt, max_tokens=768, temperature=0.3)
        
        return {
            "language": language,
            "explanation": explanation
        }
    
    def brainstorm(self, topic: str, num_ideas: int = 5) -> dict:
        """Generate brainstorming ideas"""
        structure = self.creative.generate_brainstorm_structure(topic, num_ideas)
        ideas = self.ollama.generate(structure, max_tokens=768, temperature=0.8)
        
        return {
            "topic": topic,
            "ideas": ideas
        }
    
    def get_self_reflection(self) -> str:
        """Get self-reflection report"""
        return self.self_improve.reflection_report()
    
    def get_improvement_suggestions(self) -> List[dict]:
        """Get improvement suggestions"""
        return self.self_improve.get_improvement_suggestions()
    
    def respond_to_improvement(self, proposal_id: str, decision: str, feedback: str) -> dict:
        """Respond to improvement proposal"""
        return self.self_improve.user_feedback_on_proposal(proposal_id, decision, feedback)
    
    def get_performance_metrics(self) -> dict:
        """Get performance metrics"""
        return self.self_improve.get_status()
    
    def get_memory_stats(self) -> dict:
        """Get memory statistics"""
        return self.memory.get_statistics()
    
    def show_personal(self) -> dict:
        """Show personal memory"""
        recent = self.memory.get_recent_memories(limit=20, memory_type="personal")
        facts = self.memory.get_all_facts(min_importance=1)
        
        return {
            "recent_memories": recent,
            "facts": facts
        }
    
    def show_knowledge(self) -> dict:
        """Show knowledge memory"""
        recent = self.memory.get_recent_memories(limit=20, memory_type="conversation")
        
        return {
            "recent_memories": recent
        }
    
    def forget_personal(self) -> dict:
        """Clear personal memory"""
        stats = self.memory.clear_personal()
        return {
            "status": "personal memory cleared",
            "details": stats,
        }
    
    def forget_knowledge(self) -> dict:
        """Clear knowledge memory"""
        deleted = self.memory.clear_conversation()
        # Also clear semantic conversation context window
        self.context_mgr.clear_context()
        return {
            "status": "knowledge memory cleared",
            "cleared_conversation_memories": deleted,
        }
    
    def list_project_templates(self) -> dict:
        """List project templates"""
        return self.scaffolder.list_available_templates()
    
    def create_project(self, project_type: str, name: str, description: str) -> dict:
        """Create project from template"""
        return self.scaffolder.create_project(project_type, name, description)
    
    def _handle_enhanced_knowledge(self, user_input: str, use_memory: bool, 
                                 reasoning_mode: str, context: dict, emotional_state) -> dict:
        """Enhanced knowledge query with context and emotional intelligence"""
        
        # Build contextual prompt
        context_info = f"""
Current Context:
- Time: {context.get('user', {}).get('current_time', 'Unknown')}
- Activity: {context.get('user', {}).get('estimated_activity', 'Unknown')}
- Focus Level: {context.get('user', {}).get('focus_level', 'Unknown')}
- Environment: {context.get('environment', {}).get('development_mode', False) and 'Development' or 'General'}
- System Load: {context.get('environment', {}).get('system_load', 'Unknown')}
"""
        
        # Get relevant context from memory
        relevant_context = []
        if use_memory:
            relevant_context = self.context_mgr.get_relevant_context(user_input, top_k=3)
        
        # Build enhanced system prompt
        system_prompt = self._build_enhanced_system_prompt(user_input, context_info, emotional_state)
        
        # Add relevant context
        if relevant_context:
            context_text = "\n".join([f"- {ctx}" for ctx in relevant_context])
            system_prompt += f"\n\nRelevant Context:\n{context_text}"
        
        # Generate response with emotional intelligence
        response = self.ollama.generate(system_prompt, max_tokens=512, temperature=0.3)
        
        # Add emotional touch
        emotional_response = self.emotional_intelligence.generate_emotional_response(
            emotional_state, user_input, context.get('user', {})
        )
        
        enhanced_response = f"{emotional_response}\n\n{response}"
        
        # Store interaction
        self.memory.add_memory("user", user_input, memory_type="conversation", importance=6)
        self.memory.add_memory("assistant", enhanced_response, memory_type="conversation", importance=6)
        self.context_mgr.add_turn("user", user_input)
        self.context_mgr.add_turn("assistant", enhanced_response)
        
        return {
            "response": enhanced_response,
            "bucket": "knowledge",
            "context": context,
            "emotional_state": emotional_state.primary_emotion.value,
            "reasoning_mode": reasoning_mode
        }
    
    def _build_enhanced_system_prompt(self, user_input: str, context_info: str, emotional_state) -> str:
        """Build enhanced system prompt with context and emotion"""
        
        base_prompt = f"""You are Ananta, an advanced AI partner with emotional intelligence and contextual awareness.

{context_info}

User's emotional state suggests a {emotional_state.primary_emotion.value} response approach.

Respond to: "{user_input}"

Be:
- Contextually aware of the user's current situation
- Emotionally appropriate and supportive
- Intelligent and helpful
- Concise but thorough"""
        
        return base_prompt
    
    def get_proactive_suggestions(self) -> dict:
        """Get current proactive suggestions"""
        context = self.context_engine.get_full_context()
        recent_interactions = self.memory.get_recent_memories(limit=10)
        suggestions = self.proactive_intelligence.analyze_and_suggest(context, recent_interactions)
        
        return {
            "suggestions": [{"message": s.message, "priority": s.priority, "action": s.action.value} 
                          for s in suggestions],
            "context": context,
            "summary": self.proactive_intelligence.get_proactive_summary()
        }
    
    def get_emotional_state(self) -> dict:
        """Get current emotional intelligence summary"""
        return self.emotional_intelligence.get_emotional_summary()
    
    def get_full_context(self) -> dict:
        """Get comprehensive real-time context"""
        return self.context_engine.get_full_context()
    
    def get_system_status(self) -> dict:
        """Get comprehensive system status"""
        return {
            "ai_status": {
                "model": self.model,
                "coding_model": self.coding_model,
                "fast_model": self.fast_model,
                "vision_model": self.vision_model,
                "powerful_model": self.powerful_model,
                "memory_stats": self.get_memory_stats(),
                "performance_metrics": self.get_performance_metrics(),
                "emotional_state": self.get_emotional_state(),
                "proactive_suggestions": self.get_proactive_suggestions()
            },
            "system_monitoring": self.system_monitor.get_system_status(),
            "security_status": self.security_engine.get_security_status(),
            "features": {
                "voice_available": VOICE_AVAILABLE,
                "proactive_available": PROACTIVE_AVAILABLE,
                "executor_available": EXECUTOR_AVAILABLE,
                "context_awareness": True,
                "emotional_intelligence": True,
                "security_engine": True,
                "system_monitoring": True
            }
        }
    
    def switch_model(self, model_type: str = "default") -> dict:
        """Switch between different models based on use case"""
        model_map = {
            "default": self.model,
            "coding": self.coding_model,
            "fast": self.fast_model,
            "vision": self.vision_model,
            "powerful": self.powerful_model
        }
        
        if model_type not in model_map:
            return {"error": f"Unknown model type: {model_type}"}
        
        new_model = model_map[model_type]
        old_model = self.model
        
        # Update the main ollama client
        self.ollama = OllamaClient(model=new_model)
        self.model = new_model
        
        return {
            "status": "success",
            "old_model": old_model,
            "new_model": new_model,
            "model_type": model_type
        }
    
    def optimize_system(self, category: str = 'all') -> dict:
        """Run system optimization"""
        return self.system_monitor.run_optimization(category)
    
    def get_security_analysis(self, request_data: dict) -> dict:
        """Analyze request for security threats"""
        return self.security_engine.analyze_request(request_data)
    
    def create_secure_session(self, user_id: str, context: dict = None) -> str:
        """Create secure session"""
        return self.security_engine.create_session(user_id, context)
    
    def validate_session(self, session_id: str, ip_address: str = None) -> dict:
        """Validate secure session"""
        return self.security_engine.validate_session(session_id, ip_address)
    
    # ============================================================================
    # VISION-AUTOMATION API
    # ============================================================================
    
    def analyze_code_image(self, image_path: str, language_hint: str = None) -> dict:
        """Analyze code from screenshot/image and generate automation"""
        try:
            # Vision analysis
            vision_result = self.vision.analyze_code_image(image_path, language_hint)
            
            if not vision_result.get("success"):
                return vision_result
            
            # Generate automation
            automation_result = self.automation.process_vision_insight(vision_result)
            
            return {
                "vision_analysis": vision_result,
                "automation_suggestions": automation_result,
                "success": True
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def analyze_screenshot(self, image_path: str, context: str = None) -> dict:
        """Analyze screenshot for contextual understanding and automation"""
        try:
            # Vision analysis
            vision_result = self.vision.analyze_screenshot(image_path, context)
            
            if not vision_result.get("success"):
                return vision_result
            
            # Generate automation
            automation_result = self.automation.process_vision_insight(vision_result)
            
            return {
                "vision_analysis": vision_result,
                "automation_suggestions": automation_result,
                "success": True
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def convert_design_to_code(self, image_path: str, target_framework: str = "html") -> dict:
        """Convert UI design/mockup to working code with automation"""
        try:
            # Vision analysis
            vision_result = self.vision.convert_design_to_code(image_path, target_framework)
            
            if not vision_result.get("success"):
                return vision_result
            
            # Generate automation
            automation_result = self.automation.process_vision_insight(vision_result)
            
            return {
                "vision_analysis": vision_result,
                "automation_suggestions": automation_result,
                "success": True
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def analyze_document(self, image_path: str) -> dict:
        """Extract and analyze content from document images with automation"""
        try:
            # Vision analysis
            vision_result = self.vision.analyze_document(image_path)
            
            if not vision_result.get("success"):
                return vision_result
            
            # Generate automation
            automation_result = self.automation.process_vision_insight(vision_result)
            
            return {
                "vision_analysis": vision_result,
                "automation_suggestions": automation_result,
                "success": True
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def detect_errors_in_image(self, image_path: str) -> dict:
        """Detect errors in code screenshots or error messages with fixes"""
        try:
            # Vision analysis
            vision_result = self.vision.detect_errors_in_image(image_path)
            
            if not vision_result.get("success"):
                return vision_result
            
            # Generate automation
            automation_result = self.automation.process_vision_insight(vision_result)
            
            return {
                "vision_analysis": vision_result,
                "automation_suggestions": automation_result,
                "success": True
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_vision_capabilities(self) -> dict:
        """Get vision engine capabilities"""
        return self.vision.get_capabilities()
    
    def get_automation_capabilities(self) -> dict:
        """Get automation engine capabilities"""
        return self.automation.get_capabilities()
    
    def process_vision_automation(self, image_path: str, analysis_type: str = "auto", **kwargs) -> dict:
        """Unified vision-automation processing endpoint"""
        try:
            # Auto-detect analysis type if not specified
            if analysis_type == "auto":
                analysis_type = self._detect_image_type(image_path)
            
            # Route to appropriate method
            if analysis_type == "code":
                return self.analyze_code_image(image_path, kwargs.get("language_hint"))
            elif analysis_type == "screenshot":
                return self.analyze_screenshot(image_path, kwargs.get("context"))
            elif analysis_type == "design":
                return self.convert_design_to_code(image_path, kwargs.get("target_framework", "html"))
            elif analysis_type == "document":
                return self.analyze_document(image_path)
            elif analysis_type == "error":
                return self.detect_errors_in_image(image_path)
            else:
                return {"error": f"Unknown analysis type: {analysis_type}", "success": False}
                
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _detect_image_type(self, image_path: str) -> str:
        """Auto-detect image type based on filename and content"""
        filename = os.path.basename(image_path).lower()
        
        if any(keyword in filename for keyword in ["code", "screenshot", "ide", "terminal"]):
            return "code"
        elif any(keyword in filename for keyword in ["design", "mockup", "ui", "prototype"]):
            return "design"
        elif any(keyword in filename for keyword in ["error", "bug", "exception"]):
            return "error"
        elif any(keyword in filename for keyword in ["doc", "document", "pdf", "text"]):
            return "document"
        else:
            return "screenshot"
    
    # ============================================================================
    # ADVANCED AUTOMATION API
    # ============================================================================
    
    async def execute_automation_workflow(self, workflow_id: str, execution_mode: str = "full") -> dict:
        """Execute automation workflow with advanced options"""
        try:
            result = await self.automation.execute_automation(workflow_id, execution_mode)
            
            return {
                "success": True,
                "execution_result": result,
                "workflow_id": workflow_id,
                "execution_mode": execution_mode
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_automation_workflow_status(self, workflow_id: str) -> dict:
        """Get detailed workflow status"""
        try:
            status = self.automation.get_workflow_status(workflow_id)
            return {"success": True, "status": status}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_active_automation_workflows(self) -> dict:
        """Get all active automation workflows"""
        try:
            workflows = self.automation.get_active_workflows()
            return {
                "success": True,
                "active_workflows": workflows,
                "count": len(workflows)
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_automation_execution_history(self, limit: int = 10) -> dict:
        """Get automation execution history"""
        try:
            history = self.automation.get_automation_history(limit)
            return {
                "success": True,
                "history": history,
                "count": len(history)
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_automation_statistics(self) -> dict:
        """Get comprehensive automation statistics"""
        try:
            stats = self.automation.get_automation_stats()
            return {"success": True, "statistics": stats}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    async def batch_process_vision_automation(self, vision_results: list) -> dict:
        """Batch process multiple vision results for automation"""
        try:
            results = await self.automation.batch_process_vision_insights(vision_results)
            
            return {
                "success": True,
                "batch_results": results,
                "processed_count": len(results),
                "success_rate": sum(1 for r in results if r.get("success")) / len(results)
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def create_custom_automation_rule(self, rule_name: str, rule_config: dict) -> dict:
        """Create custom automation rule"""
        try:
            result = self.automation.create_custom_automation_rule(rule_name, rule_config)
            return result
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_automation_capabilities(self) -> dict:
        """Get comprehensive automation capabilities"""
        try:
            capabilities = self.automation.get_automation_capabilities()
            return {"success": True, "capabilities": capabilities}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_automation_suggestions(self, vision_result: dict, limit: int = 5) -> dict:
        """Get quick automation suggestions"""
        try:
            suggestions = self.automation.get_automation_suggestions(vision_result, limit)
            return {
                "success": True,
                "suggestions": suggestions,
                "count": len(suggestions)
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    async def preview_automation_workflow(self, workflow_id: str) -> dict:
        """Preview automation workflow without execution"""
        try:
            result = await self.automation.execute_automation(workflow_id, "preview")
            return {
                "success": True,
                "preview": result,
                "workflow_id": workflow_id
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def cancel_automation_workflow(self, workflow_id: str) -> dict:
        """Cancel running automation workflow"""
        try:
            if workflow_id in self.automation.active_workflows:
                workflow = self.automation.active_workflows[workflow_id]
                workflow.status = "cancelled"
                
                return {
                    "success": True,
                    "message": f"Workflow {workflow_id} cancelled",
                    "workflow_id": workflow_id
                }
            else:
                return {
                    "success": False,
                    "error": "Workflow not found or not active"
                }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def restart_automation_workflow(self, workflow_id: str) -> dict:
        """Restart cancelled or failed automation workflow"""
        try:
            if workflow_id in self.automation.active_workflows:
                workflow = self.automation.active_workflows[workflow_id]
                workflow.status = "created"
                workflow.progress = 0.0
                
                return {
                    "success": True,
                    "message": f"Workflow {workflow_id} restarted",
                    "workflow_id": workflow_id
                }
            else:
                return {
                    "success": False,
                    "error": "Workflow not found"
                }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_workflow_execution_logs(self, workflow_id: str) -> dict:
        """Get detailed execution logs for workflow"""
        try:
            if workflow_id in self.automation.active_workflows:
                workflow = self.automation.active_workflows[workflow_id]
                
                logs = {
                    "workflow_id": workflow_id,
                    "created_at": workflow.created_at,
                    "status": workflow.status,
                    "progress": workflow.progress,
                    "steps_executed": [],
                    "total_steps": len(workflow.steps)
                }
                
                # Add step logs
                for i, step in enumerate(workflow.steps):
                    step_log = {
                        "step_number": i + 1,
                        "step_name": step.name,
                        "step_id": step.step_id,
                        "actions_count": len(step.actions),
                        "parallel_execution": step.parallel_execution,
                        "status": "completed" if workflow.progress > ((i + 1) / len(workflow.steps) * 100) else "pending"
                    }
                    logs["steps_executed"].append(step_log)
                
                return {
                    "success": True,
                    "logs": logs
                }
            else:
                return {
                    "success": False,
                    "error": "Workflow not found"
                }
        except Exception as e:
            return {"error": str(e), "success": False}