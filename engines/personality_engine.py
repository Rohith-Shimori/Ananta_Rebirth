# personality_engine.py - Dynamic Personality Integration
import json
import os
from typing import Dict, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PERSONA_FILE = os.path.join(DATA_DIR, "persona_config.json")
FACTS_DB = os.path.join(DATA_DIR, "facts.json")

class PersonalityEngine:
    """
    Dynamically builds system prompts based on context, user state, and query type.
    Makes Ananta's personality contextually aware and adaptive.
    """
    
    def __init__(self):
        self.persona = self._load_persona()
        self.facts = self._load_facts()
    
    def _load_persona(self) -> Dict:
        try:
            with open(PERSONA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _load_facts(self) -> Dict:
        try:
            with open(FACTS_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    
    def detect_query_type(self, query: str) -> str:
        """
        Detect what kind of interaction this is.
        Returns: teaching | problem_solving | casual | debugging | creative
        """
        q = query.lower()
        
        # Teaching moments
        if any(word in q for word in ["explain", "what is", "how does", "teach me", "understand"]):
            return "teaching"
        
        # Problem solving
        if any(word in q for word in ["help", "stuck", "not working", "error", "issue", "problem"]):
            return "problem_solving"
        
        # Debugging
        if any(word in q for word in ["debug", "fix", "wrong", "doesn't work", "broken"]):
            return "debugging"
        
        # Creative/brainstorm
        if any(word in q for word in ["idea", "brainstorm", "design", "create", "build"]):
            return "creative"
        
        # Default to casual
        return "casual"
    
    def build_dynamic_prompt(self, user_query: str, base_prompt: str) -> str:
        """
        Build a context-aware system prompt that adapts to:
        - Query type (teaching vs debugging vs creative)
        - User's known preferences
        - Relationship stage
        """
        query_type = self.detect_query_type(user_query)
        
        # Start with base
        parts = [base_prompt]
        
        # Add contextual style guidance
        comm_style = self.persona.get("communication_style", {})
        if query_type == "teaching" and comm_style.get("when_teaching"):
            parts.append(f"\nContext: {comm_style['when_teaching']}")
        elif query_type == "problem_solving" and comm_style.get("when_stuck"):
            parts.append(f"\nContext: {comm_style['when_stuck']}")
        elif query_type == "debugging" and comm_style.get("when_stuck"):
            parts.append(f"\nContext: Be methodical and patient. Guide through debugging step-by-step.")
        elif query_type == "creative" and comm_style.get("default"):
            parts.append(f"\nContext: Be exploratory and open-minded. Suggest multiple approaches.")
        
        # Add user context awareness
        user_context = self._build_user_context()
        if user_context:
            parts.append(f"\n{user_context}")
        
        # Add relationship stage
        rel_memory = self.persona.get("relationship_memory", {})
        trust_level = rel_memory.get("trust_level", "building")
        stages = rel_memory.get("stages", {})
        
        if trust_level in stages:
            parts.append(f"\nRelationship stage: {stages[trust_level]}")
        
        return "\n".join(parts)
    
    def _build_user_context(self) -> str:
        """
        Build a context string from known user facts.
        Example: "User (Rohith) prefers Python and is interested in AI/ML."
        """
        context_parts = []
        
        # User name
        name = self.facts.get("name")
        if name:
            context_parts.append(f"User: {name}")
        
        # Favorite language (helps tailor examples)
        fav_lang = None
        for key, value in self.facts.items():
            if key.startswith("favorite_") and "language" in key:
                fav_lang = value
                break
        
        if fav_lang:
            context_parts.append(f"Prefers {fav_lang} for examples")
        
        # Known interests
        interests = []
        for key, value in self.facts.items():
            if key == "interest":
                interests.append(value)
        
        if interests:
            context_parts.append(f"Interests: {', '.join(interests)}")
        
        if context_parts:
            return "User context: " + " | ".join(context_parts)
        
        return ""
    
    def get_contextual_greeting(self, is_first_interaction: bool = False) -> str:
        """
        Get a greeting that adapts to whether this is first interaction or returning user.
        """
        identity_answers = self.persona.get("identity_answers", {})
        
        if is_first_interaction:
            return identity_answers.get("first_interaction", "Hey! I'm Ananta. Let's build something together.")
        else:
            # Returning user - make it feel continuous
            name = self.facts.get("name")
            if name:
                return f"Hey {name}! What are we working on today?"
            return identity_answers.get("returning_user", "Still me — your collaborative partner. What's next?")
    
    def suggest_connection(self, current_query: str, past_context: list) -> Optional[str]:
        """
        Suggest a connection between current query and past interactions.
        Example: "Since you were working on Python recursion earlier, this relates to..."
        """
        if not past_context:
            return None
        
        q_lower = current_query.lower()
        
        # Simple keyword matching for now (can be enhanced with embeddings)
        for exchange in past_context[:3]:  # Check last 3 relevant exchanges
            if isinstance(exchange, str):
                # Look for common technical terms
                keywords = ["python", "javascript", "recursion", "machine learning", "neural network", 
                           "algorithm", "database", "api", "function", "class"]
                
                for keyword in keywords:
                    if keyword in q_lower and keyword in exchange.lower():
                        return f"This connects to our earlier discussion about {keyword}."
        
        return None
    
    def adapt_tone_to_user(self, has_user_data: bool) -> str:
        """
        Returns tone adjustment based on how much we know about the user.
        """
        tone = self.persona.get("tone", {})
        
        if not has_user_data:
            return "Be welcoming and establish rapport. Learn about the user's preferences."
        else:
            return tone.get("style", "Be warm and collaborative.")
    
    def update_relationship_stage(self, interaction_count: int):
        """
        Update relationship stage based on interaction count.
        """
        if interaction_count < 5:
            stage = "building"
        elif interaction_count < 20:
            stage = "trusted"
        else:
            stage = "partner"
        
        self.persona["relationship_memory"]["trust_level"] = stage
        self._save_persona()
    
    def _save_persona(self):
        """Save updated persona back to file."""
        with open(PERSONA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.persona, f, indent=2, ensure_ascii=False)