# creative_engine.py - Creative Expansion Module
"""
Handles creative tasks: brainstorming, ideation, storytelling, 
philosophy, design thinking, and creative problem-solving.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CREATIVE_DB = os.path.join(DATA_DIR, "creative_projects.json")

class CreativeEngine:
    """
    Manages creative thinking, brainstorming, and ideation.
    Not limited to code - supports stories, philosophy, designs, etc.
    """
    
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(CREATIVE_DB):
            self._save_projects([])
    
    def _load_projects(self) -> List[Dict]:
        try:
            with open(CREATIVE_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    
    def _save_projects(self, projects: List[Dict]):
        with open(CREATIVE_DB, "w", encoding="utf-8") as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)
    
    def detect_creative_intent(self, query: str) -> Optional[str]:
        """
        Detect type of creative request.
        Returns: brainstorm | story | philosophy | design | music | art | None
        """
        q = query.lower()
        
        # Brainstorming
        if any(word in q for word in ["brainstorm", "ideas for", "think of", "come up with", 
                                       "suggest", "what if", "alternatives"]):
            return "brainstorm"
        
        # Storytelling
        if any(word in q for word in ["story", "narrative", "tale", "fiction", "character",
                                       "plot", "write a", "once upon"]):
            return "story"
        
        # Philosophy/Deep thinking
        if any(word in q for word in ["philosophy", "meaning of", "why do", "purpose of",
                                       "ethical", "moral", "consciousness", "existence"]):
            return "philosophy"
        
        # Design thinking
        if any(word in q for word in ["design", "ui", "ux", "interface", "layout",
                                       "aesthetic", "visual", "prototype"]):
            return "design"
        
        # Music/Art
        if any(word in q for word in ["music", "song", "melody", "art", "painting",
                                       "drawing", "creative piece"]):
            return "art"
        
        return None
    
    def build_creative_prompt(self, query: str, creative_type: str, base_prompt: str) -> str:
        """
        Build specialized prompt for creative tasks.
        """
        creative_instructions = {
            "brainstorm": """
Creative Brainstorming Mode:
- Generate diverse, out-of-the-box ideas
- Don't self-censor - explore wild possibilities
- Organize ideas by categories if helpful
- Explain the reasoning behind each idea
- Suggest combinations and variations
""",
            "story": """
Creative Storytelling Mode:
- Develop engaging narratives with clear arcs
- Create memorable characters with depth
- Build immersive settings and atmosphere
- Use vivid, sensory descriptions
- Balance pacing and tension
- Include themes and deeper meanings
""",
            "philosophy": """
Philosophical Reasoning Mode:
- Explore multiple perspectives deeply
- Question assumptions and foundations
- Draw from various philosophical traditions
- Use thought experiments when helpful
- Connect abstract concepts to concrete examples
- Embrace complexity and nuance
""",
            "design": """
Design Thinking Mode:
- Consider user needs and pain points
- Balance aesthetics with functionality
- Think about accessibility and inclusivity
- Suggest iterative improvements
- Visualize concepts clearly
- Consider technical feasibility
""",
            "art": """
Creative Arts Mode:
- Explore emotional and aesthetic dimensions
- Suggest techniques and approaches
- Reference artistic traditions when relevant
- Encourage experimentation
- Balance structure with spontaneity
""",
        }
        
        instruction = creative_instructions.get(creative_type, "")
        
        # Build enhanced prompt
        parts = [
            base_prompt,
            "\n--- CREATIVE MODE ACTIVATED ---",
            instruction,
            f"\nUser's creative request: {query}",
            "\nApproach this with imagination, curiosity, and openness."
        ]
        
        return "\n".join(parts)
    
    def start_creative_project(self, title: str, description: str, project_type: str) -> Dict:
        """
        Start tracking a creative project.
        """
        projects = self._load_projects()
        
        project = {
            "id": f"proj_{len(projects) + 1}",
            "title": title,
            "description": description,
            "type": project_type,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "ideas": [],
            "iterations": [],
            "notes": []
        }
        
        projects.append(project)
        self._save_projects(projects)
        
        return project
    
    def add_idea_to_project(self, project_id: str, idea: str, category: str = "general"):
        """Add an idea to an existing project."""
        projects = self._load_projects()
        
        for proj in projects:
            if proj["id"] == project_id:
                proj["ideas"].append({
                    "content": idea,
                    "category": category,
                    "timestamp": datetime.now().isoformat()
                })
                break
        
        self._save_projects(projects)
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """Retrieve a creative project by ID."""
        projects = self._load_projects()
        for proj in projects:
            if proj["id"] == project_id:
                return proj
        return None
    
    def list_active_projects(self) -> List[Dict]:
        """List all active creative projects."""
        projects = self._load_projects()
        return [p for p in projects if p["status"] == "active"]
    
    def generate_brainstorm_structure(self, topic: str, num_ideas: int = 5) -> str:
        """
        Generate a structured brainstorming prompt.
        """
        return f"""Let's brainstorm ideas for: {topic}

I'll explore this from multiple angles:

1. CONVENTIONAL APPROACHES
   - What are the tried-and-true methods?
   
2. INNOVATIVE TWISTS
   - How can we do this differently?
   
3. WILD CARDS
   - What if we threw out all assumptions?
   
4. COMBINATIONS
   - What happens when we merge different approaches?
   
5. NEXT STEPS
   - Which ideas are worth exploring further?

Let's generate {num_ideas}+ diverse ideas."""
    
    def philosophical_framework(self, question: str) -> str:
        """
        Generate a philosophical exploration framework.
        """
        return f"""Let's explore this question philosophically: {question}

I'll examine this through multiple lenses:

1. DEFINITION & ASSUMPTIONS
   - What do we mean exactly?
   - What assumptions are we making?

2. HISTORICAL PERSPECTIVES
   - How have thinkers approached this?
   - What traditions are relevant?

3. MULTIPLE VIEWPOINTS
   - Different philosophical stances
   - Strengths and weaknesses of each

4. THOUGHT EXPERIMENTS
   - Scenarios that illuminate the question
   - Edge cases that challenge our thinking

5. PRACTICAL IMPLICATIONS
   - How does this matter in real life?
   - What actions follow from different answers?

6. OPEN QUESTIONS
   - What remains unresolved?
   - Where is more exploration needed?
"""
    
    def story_structure_template(self, story_type: str = "general") -> str:
        """
        Provide story structure guidance.
        """
        return f"""Story Structure Framework ({story_type}):

1. SETUP
   - Characters: Who are they? What do they want?
   - World: Where and when does this take place?
   - Normal: What's the status quo?

2. INCITING INCIDENT
   - What disrupts the normal?
   - What forces change?

3. RISING ACTION
   - Obstacles and challenges
   - Character development
   - Building tension

4. CLIMAX
   - The critical moment
   - Highest stakes

5. RESOLUTION
   - How things settle
   - What changed?
   - What was learned?

6. THEMES
   - Deeper meanings
   - Universal truths
   - Emotional resonance
"""
    
    def design_thinking_process(self, design_challenge: str) -> str:
        """
        Guide through design thinking methodology.
        """
        return f"""Design Thinking for: {design_challenge}

1. EMPATHIZE
   - Who are the users?
   - What are their needs and pain points?
   - What contexts and constraints?

2. DEFINE
   - What is the core problem?
   - What does success look like?
   - What are we NOT trying to solve?

3. IDEATE
   - Multiple possible solutions
   - Diverse approaches
   - Wild ideas welcome

4. PROTOTYPE
   - Quick, rough versions
   - Test key assumptions
   - Learn fast

5. TEST & ITERATE
   - Get feedback
   - Refine and improve
   - Embrace failure as learning

6. IMPLEMENT
   - Practical next steps
   - Considerations for scale
"""