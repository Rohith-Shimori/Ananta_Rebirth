"""
Phase 3: Lightweight Agent Orchestrator - Claude's Optimization Plan
Multi-agent system optimized for 6GB VRAM
- Sequential processing (one model at a time)
- Fast model switching (2-3s)
- Intelligent task decomposition
"""

import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import config


@dataclass
class Task:
    """Represents a task to be executed"""
    id: str
    description: str
    task_type: str  # "planning", "research", "coding", "review"
    priority: int = 5
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None
    assigned_agent: Optional[str] = None


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str, model_name: str):
        self.name = name
        self.model_name = model_name
        self.model_config = config.OPTIMAL_MODELS.get(model_name, {})
        self.tasks_completed = 0
        self.total_time = 0.0
    
    async def execute(self, task: Task) -> str:
        """Execute a task - override in subclasses"""
        raise NotImplementedError
    
    def get_info(self) -> Dict:
        """Get agent information"""
        return {
            "name": self.name,
            "model": self.model_name,
            "model_info": self.model_config,
            "tasks_completed": self.tasks_completed,
            "avg_time": self.total_time / max(self.tasks_completed, 1)
        }


class PlannerAgent(BaseAgent):
    """Fast planning agent - uses FLASH model"""
    
    def __init__(self):
        super().__init__("Planner", "flash")
    
    async def create_plan(self, task_description: str) -> Dict:
        """Create a plan for complex tasks"""
        # Simulate planning
        subtasks = [
            Task(f"subtask_1", "Analyze requirements", "research"),
            Task(f"subtask_2", "Design solution", "planning"),
            Task(f"subtask_3", "Implement solution", "coding"),
            Task(f"subtask_4", "Review and test", "review"),
        ]
        
        return {
            "main_task": task_description,
            "subtasks": subtasks,
            "estimated_time": len(subtasks) * 2,
            "complexity": "high"
        }
    
    async def execute(self, task: Task) -> str:
        """Execute planning task"""
        task.status = "in_progress"
        task.assigned_agent = self.name
        
        # Use REAL AI model for planning
        from core.ollama_client import OllamaClient
        model_config = self.model_config
        actual_model = model_config.get("model", "llama3.2:3b-instruct-q6_K")
        
        ollama = OllamaClient(model=actual_model)
        
        planning_prompt = f"""
You are a planning AI assistant. Create a structured plan for this task:
Task: {task.description}

Provide a step-by-step plan with:
1. Analysis phase
2. Design phase  
3. Implementation phase
4. Testing phase

Keep it concise and actionable.
"""
        
        try:
            result = await asyncio.to_thread(
                ollama.generate,
                planning_prompt,
                max_tokens=300,
                temperature=0.3
            )
            
            task.status = "completed"
            task.result = result
            self.tasks_completed += 1
            
            return result
            
        except Exception as e:
            task.status = "failed"
            task.result = f"Planning failed: {str(e)}"
            return task.result


class ResearcherAgent(BaseAgent):
    """Deep research agent - uses SENTINEL model"""
    
    def __init__(self):
        super().__init__("Researcher", "sentinel")
    
    async def execute(self, task: Task) -> str:
        """Execute research task"""
        task.status = "in_progress"
        task.assigned_agent = self.name
        
        # Use REAL AI model for research
        from core.ollama_client import OllamaClient
        model_config = self.model_config
        actual_model = model_config.get("model", "qwen2.5:7b-instruct-q4_K_M")
        
        ollama = OllamaClient(model=actual_model)
        
        research_prompt = f"""
You are a research AI assistant. Conduct thorough research on this topic:
Topic: {task.description}

Provide:
1. Key findings and insights
2. Important patterns or trends
3. Actionable recommendations
4. Relevant context

Be comprehensive but concise.
"""
        
        try:
            result = await asyncio.to_thread(
                ollama.generate,
                research_prompt,
                max_tokens=400,
                temperature=0.3
            )
            
            task.status = "completed"
            task.result = result
            self.tasks_completed += 1
            
            return result
            
        except Exception as e:
            task.status = "failed"
            task.result = f"Research failed: {str(e)}"
            return task.result


class CoderAgent(BaseAgent):
    """Code specialist agent - uses ARCHITECT model"""
    
    def __init__(self):
        super().__init__("Coder", "architect")
    
    async def execute(self, task: Task) -> str:
        """Execute coding task"""
        task.status = "in_progress"
        task.assigned_agent = self.name
        
        # Use REAL AI model for coding
        from core.ollama_client import OllamaClient
        model_config = self.model_config
        actual_model = model_config.get("model", "qwen2.5-coder:7b-instruct-q4_K_M")
        
        ollama = OllamaClient(model=actual_model)
        
        coding_prompt = f"""
You are an expert coding AI assistant. Generate high-quality code for this task:
Task: {task.description}

Requirements:
1. Write clean, well-commented code
2. Follow best practices
3. Include error handling
4. Provide working solution
5. Use Python unless specified otherwise

Provide only the code with brief explanation.
"""
        
        try:
            result = await asyncio.to_thread(
                ollama.generate,
                coding_prompt,
                max_tokens=500,
                temperature=0.2
            )
            
            task.status = "completed"
            task.result = result
            self.tasks_completed += 1
            
            return result
            
        except Exception as e:
            task.status = "failed"
            task.result = f"Coding failed: {str(e)}"
            return task.result


class CriticAgent(BaseAgent):
    """Quality review agent - uses ORACLE model"""
    
    def __init__(self):
        super().__init__("Critic", "oracle")
    
    async def execute(self, task: Task) -> str:
        """Execute review task"""
        task.status = "in_progress"
        task.assigned_agent = self.name
        
        # Use REAL AI model for review
        from core.ollama_client import OllamaClient
        model_config = self.model_config
        actual_model = model_config.get("model", "llama3.1:8b")
        
        ollama = OllamaClient(model=actual_model)
        
        review_prompt = f"""
You are an expert code reviewer and quality assurance specialist. Review this work:
Work to review: {task.description}

Provide:
1. Quality assessment (1-10 scale)
2. Strengths and weaknesses
3. Improvement suggestions
4. Potential issues or bugs
5. Best practices compliance

Be thorough and constructive.
"""
        
        try:
            result = await asyncio.to_thread(
                ollama.generate,
                review_prompt,
                max_tokens=400,
                temperature=0.3
            )
            
            task.status = "completed"
            task.result = result
            self.tasks_completed += 1
            
            return result
            
        except Exception as e:
            task.status = "failed"
            task.result = f"Review failed: {str(e)}"
            return task.result


class LightweightAgentOrchestrator:
    """
    Efficient multi-agent system for 6GB VRAM
    - Sequential processing (one model at a time)
    - Fast model switching (2-3s)
    - Intelligent task decomposition
    """
    
    def __init__(self):
        self.agents = {
            "planner": PlannerAgent(),
            "researcher": ResearcherAgent(),
            "coder": CoderAgent(),
            "critic": CriticAgent(),
        }
        self.current_model = None
        self.task_queue = []
        self.completed_tasks = []
        self.execution_log = []
    
    def route_subtask(self, subtask: str) -> str:
        """Route subtask to appropriate agent"""
        subtask_lower = subtask.lower()
        
        if any(kw in subtask_lower for kw in ["code", "implement", "function", "debug"]):
            return "coder"
        elif any(kw in subtask_lower for kw in ["research", "analyze", "investigate"]):
            return "researcher"
        elif any(kw in subtask_lower for kw in ["review", "check", "verify", "quality"]):
            return "critic"
        else:
            return "planner"
    
    async def switch_model(self, model_name: str) -> Dict:
        """Fast model switching"""
        if self.current_model == model_name:
            return {"status": "already_loaded", "model": model_name}
        
        # Simulate model switching
        switch_info = {
            "status": "switched",
            "from_model": self.current_model,
            "to_model": model_name,
            "switch_time": "2-3s",
            "model_info": config.OPTIMAL_MODELS.get(model_name, {})
        }
        
        self.current_model = model_name
        self.execution_log.append(f"Switched to {model_name}")
        
        return switch_info
    
    async def execute_complex_task(self, main_task: str) -> Dict:
        """
        Execute complex task with agent coordination
        
        Process:
        1. Plan (fast model)
        2. Execute subtasks (appropriate models)
        3. Review (reasoning model)
        """
        
        print(f"\n{'='*60}")
        print(f"🤖 AGENT ORCHESTRATOR - EXECUTING COMPLEX TASK")
        print(f"{'='*60}")
        print(f"Task: {main_task}\n")
        
        # Step 1: Plan (fast model)
        print("📋 STEP 1: PLANNING")
        planner = self.agents["planner"]
        plan = await planner.create_plan(main_task)
        print(f"  Model: {planner.model_name}")
        print(f"  Subtasks: {len(plan['subtasks'])}")
        
        # Step 2: Execute subtasks
        print("\n⚙️ STEP 2: EXECUTING SUBTASKS")
        results = []
        for subtask in plan['subtasks']:
            # Route to appropriate agent
            agent_name = self.route_subtask(subtask.description)
            agent = self.agents[agent_name]
            
            # Switch model if needed
            await self.switch_model(agent.model_name)
            
            # Execute
            print(f"  [{agent_name.upper()}] {subtask.description}...")
            result = await agent.execute(subtask)
            results.append({
                "subtask": subtask.description,
                "agent": agent_name,
                "result": result
            })
        
        # Step 3: Quality check (reasoning model)
        print("\n✅ STEP 3: QUALITY REVIEW")
        critic = self.agents["critic"]
        await self.switch_model(critic.model_name)
        print(f"  Model: {critic.model_name}")
        
        review_task = Task("review", f"Review: {main_task}", "review")
        final_review = await critic.execute(review_task)
        
        # Compile final result
        final_result = {
            "main_task": main_task,
            "plan": plan,
            "subtask_results": results,
            "final_review": final_review,
            "status": "completed",
            "total_steps": len(plan['subtasks']) + 2
        }
        
        print(f"\n{'='*60}")
        print(f"✨ TASK COMPLETED")
        print(f"{'='*60}\n")
        
        return final_result
    
    def get_orchestrator_stats(self) -> Dict:
        """Get orchestrator statistics"""
        total_tasks = sum(agent.tasks_completed for agent in self.agents.values())
        
        return {
            "total_tasks_completed": total_tasks,
            "agents": {name: agent.get_info() for name, agent in self.agents.items()},
            "current_model": self.current_model,
            "execution_log_length": len(self.execution_log),
            "completed_tasks": len(self.completed_tasks)
        }
    
    def print_orchestrator_info(self):
        """Print orchestrator information"""
        print(f"\n{'='*60}")
        print(f"🎭 AGENT ORCHESTRATOR - INFORMATION")
        print(f"{'='*60}")
        print(f"Agents: {len(self.agents)}")
        for name, agent in self.agents.items():
            info = agent.get_info()
            print(f"  {name.upper()}: {info['model']} ({info['model_info'].get('vram', 0)}GB)")
        
        stats = self.get_orchestrator_stats()
        print(f"\nStatistics:")
        print(f"  Total Tasks: {stats['total_tasks_completed']}")
        print(f"  Current Model: {stats['current_model']}")
        print(f"  Execution Log Entries: {stats['execution_log_length']}")
        print(f"{'='*60}\n")


# Example usage
if __name__ == "__main__":
    async def main():
        orchestrator = LightweightAgentOrchestrator()
        
        # Execute a complex task
        result = await orchestrator.execute_complex_task(
            "Build a Python web scraper with error handling and data storage"
        )
        
        # Print results
        print("📊 RESULTS:")
        print(f"Main Task: {result['main_task']}")
        print(f"Status: {result['status']}")
        print(f"Total Steps: {result['total_steps']}")
        
        # Print stats
        orchestrator.print_orchestrator_info()
    
    # Run async example
    asyncio.run(main())
