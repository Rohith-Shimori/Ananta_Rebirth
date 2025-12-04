# context_manager.py - UPGRADED WITH SEMANTIC RETRIEVAL
import os
import json
from collections import deque
from sentence_transformers import SentenceTransformer
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONTEXT_FILE = os.path.join(DATA_DIR, "context_window.json")

class ContextManager:
    """Manages conversation context with semantic similarity retrieval."""
    
    def __init__(self, max_turns=10, max_tokens_per_message=200, embedder=None):
        self.max_turns = max_turns
        self.max_tokens_per_message = max_tokens_per_message
        self.context_file = CONTEXT_FILE
        
        # Initialize embedder for semantic search (can reuse a shared instance)
        self.embedder = embedder or SentenceTransformer("all-MiniLM-L6-v2")
        
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(self.context_file):
            self._save_context([])
    
    def _load_context(self):
        try:
            with open(self.context_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    
    def _save_context(self, context):
        with open(self.context_file, "w", encoding="utf-8") as f:
            json.dump(context, f, indent=2, ensure_ascii=False)
    
    def add_turn(self, role, message):
        """Add a conversation turn (user or assistant)."""
        context = self._load_context()
        
        # Truncate long messages
        if len(message) > self.max_tokens_per_message * 4:
            message = message[:self.max_tokens_per_message * 4] + "..."
        
        context.append({"role": role, "content": message})
        
        # Keep only last N turns
        if len(context) > self.max_turns * 2:
            context = context[-(self.max_turns * 2):]
        
        self._save_context(context)
    
    def get_context_for_prompt(self, include_last_n=5):
        """Get formatted context for including in prompts (chronological)."""
        context = self._load_context()
        recent = context[-(include_last_n * 2):]
        
        formatted = []
        for turn in recent:
            role = turn["role"].upper()
            content = turn["content"][:500]
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted) if formatted else "No previous context."
    
    def get_relevant_context(self, current_query: str, top_k=3, include_recent=True):
        """
        Get semantically relevant past exchanges using embedding similarity.
        
        Args:
            current_query: User's current question
            top_k: Number of relevant past exchanges to retrieve
            include_recent: If True, always include the last exchange for continuity
        
        Returns:
            List of formatted relevant exchanges
        """
        context = self._load_context()
        
        if not context:
            return []
        
        # Get user messages only (we'll include their assistant responses)
        user_turns = [
            (i, turn["content"]) 
            for i, turn in enumerate(context) 
            if turn["role"] == "user"
        ]
        
        if not user_turns:
            return []
        
        # Embed current query
        query_embedding = self.embedder.encode([current_query])[0]
        
        # Embed all past user messages
        past_messages = [msg for _, msg in user_turns]
        if not past_messages:
            return []
        
        past_embeddings = self.embedder.encode(past_messages)
        
        # Calculate cosine similarity
        similarities = []
        for i, (turn_idx, msg) in enumerate(user_turns):
            similarity = self._cosine_similarity(query_embedding, past_embeddings[i])
            similarities.append((turn_idx, similarity, msg))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get top_k most relevant (excluding exact matches if same query)
        relevant_indices = []
        for turn_idx, sim, msg in similarities:
            # Skip if it's the current query being repeated
            if msg.strip().lower() == current_query.strip().lower():
                continue
            relevant_indices.append(turn_idx)
            if len(relevant_indices) >= top_k:
                break
        
        # Format relevant exchanges (user + assistant response)
        formatted = []
        for idx in relevant_indices:
            user_msg = context[idx]["content"][:300]
            
            # Get corresponding assistant response (next turn)
            if idx + 1 < len(context) and context[idx + 1]["role"] == "assistant":
                assistant_msg = context[idx + 1]["content"][:300]
                formatted.append(f"USER: {user_msg}\nASSISTANT: {assistant_msg}")
        
        # Optionally include most recent exchange for continuity
        if include_recent and len(context) >= 2:
            last_user = None
            last_assistant = None
            
            # Find last user-assistant pair
            for i in range(len(context) - 1, -1, -1):
                if context[i]["role"] == "assistant" and last_assistant is None:
                    last_assistant = context[i]["content"][:300]
                if context[i]["role"] == "user" and last_user is None:
                    last_user = context[i]["content"][:300]
                if last_user and last_assistant:
                    break
            
            if last_user and last_assistant:
                recent_exchange = f"USER: {last_user}\nASSISTANT: {last_assistant}"
                # Add only if not already in relevant list
                if recent_exchange not in formatted:
                    formatted.insert(0, f"[RECENT] {recent_exchange}")
        
        return formatted
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def clear_context(self):
        """Clear all conversation context."""
        self._save_context([])
        return {"status": "context cleared"}
    
    def get_summary(self):
        """Get a summary of conversation statistics."""
        context = self._load_context()
        user_msgs = sum(1 for t in context if t["role"] == "user")
        assistant_msgs = sum(1 for t in context if t["role"] == "assistant")
        
        return {
            "total_turns": len(context),
            "user_messages": user_msgs,
            "assistant_messages": assistant_msgs
        }