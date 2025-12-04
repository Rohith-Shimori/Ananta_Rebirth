#!/usr/bin/env python3
"""
Smart Automation Engine
Integrates vision insights with intelligent automation workflows
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from pathlib import Path
import os

from .vision_automation_pipeline import (
    VisionAutomationPipeline, 
    AutomationWorkflow, 
    AutomationType, 
    AutomationPriority
)

class SmartAutomationEngine:
    """Main automation engine that orchestrates vision-to-automation workflows"""
    
    def __init__(self):
        self.pipeline = VisionAutomationPipeline()
        self.active_workflows = {}
        self.workflow_queue = []
        self.execution_history = []
        self.automation_stats = {
            "total_processed": 0,
            "successful_automations": 0,
            "failed_automations": 0,
            "average_execution_time": 0,
            "automation_types_used": {}
        }
        
    async def process_vision_insight(self, vision_result: Dict) -> Dict:
        """Main entry point - process vision insight and return automation suggestions"""
        try:
            self.automation_stats["total_processed"] += 1
            
            # Create automation workflow
            workflow = await self.pipeline.process_vision_insight(vision_result)
            
            if not workflow:
                return {
                    "success": False,
                    "error": "Failed to create automation workflow",
                    "automation_type": "none"
                }
            
            # Store workflow
            self.active_workflows[workflow.workflow_id] = workflow
            
            # Generate quick suggestions (without full execution)
            suggestions = await self._generate_quick_suggestions(workflow)
            
            # Determine automation type
            automation_type = self._determine_automation_type(vision_result, workflow)
            
            return {
                "success": True,
                "workflow_id": workflow.workflow_id,
                "automation_type": automation_type,
                "suggestions": suggestions,
                "estimated_time": self._estimate_workflow_time(workflow),
                "complexity": self._assess_complexity(workflow),
                "actions_count": sum(len(step.actions) for step in workflow.steps),
                "priority": self._get_workflow_priority(workflow)
            }
            
        except Exception as e:
            self.automation_stats["failed_automations"] += 1
            return {
                "success": False,
                "error": str(e),
                "automation_type": "error"
            }
    
    async def execute_automation(self, workflow_id: str, execution_mode: str = "full") -> Dict:
        """Execute automation workflow"""
        try:
            if workflow_id not in self.active_workflows:
                return {
                    "success": False,
                    "error": "Workflow not found"
                }
            
            workflow = self.active_workflows[workflow_id]
            
            if execution_mode == "full":
                # Execute complete workflow
                result = await self.pipeline.execute_workflow(workflow_id)
                self.automation_stats["successful_automations"] += 1
                
                # Update execution history
                self.execution_history.append({
                    "workflow_id": workflow_id,
                    "execution_mode": execution_mode,
                    "completed_at": datetime.now().isoformat(),
                    "success": result.get("success", False),
                    "execution_time": result.get("execution_time", 0)
                })
                
                return result
                
            elif execution_mode == "preview":
                # Preview what would be executed
                return {
                    "success": True,
                    "mode": "preview",
                    "workflow_preview": self._generate_workflow_preview(workflow),
                    "estimated_time": self._estimate_workflow_time(workflow)
                }
                
            else:
                return {
                    "success": False,
                    "error": f"Unknown execution mode: {execution_mode}"
                }
                
        except Exception as e:
            self.automation_stats["failed_automations"] += 1
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _generate_quick_suggestions(self, workflow: AutomationWorkflow) -> List[Dict]:
        """Generate quick automation suggestions"""
        suggestions = []
        
        for step in workflow.steps:
            for action in step.actions:
                suggestion = {
                    "action_id": action.action_id,
                    "type": action.type.value,
                    "priority": action.priority.value,
                    "description": action.description,
                    "estimated_time": action.estimated_time,
                    "step": step.name
                }
                
                # Add code preview if available
                if action.code_snippet:
                    suggestion["code_preview"] = action.code_snippet[:200] + "..." if len(action.code_snippet) > 200 else action.code_snippet
                
                suggestions.append(suggestion)
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        suggestions.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        return suggestions
    
    def _determine_automation_type(self, vision_result: Dict, workflow: AutomationWorkflow) -> str:
        """Determine primary automation type"""
        vision_type = vision_result.get("type", "unknown")
        
        # Map vision types to automation types
        type_mapping = {
            "code_analysis": "code_improvement",
            "design_to_code": "code_generation",
            "error_detection": "error_resolution",
            "document_analysis": "workflow_automation",
            "screenshot_analysis": "contextual_actions"
        }
        
        base_type = type_mapping.get(vision_type, "smart_suggestions")
        
        # Refine based on workflow actions
        action_types = [action.type.value for step in workflow.steps for action in step.actions]
        
        if "error_resolution" in action_types:
            return "error_resolution"
        elif "code_generation" in action_types:
            return "code_generation"
        elif "workflow_automation" in action_types:
            return "workflow_automation"
        
        return base_type
    
    def _estimate_workflow_time(self, workflow: AutomationWorkflow) -> int:
        """Estimate total workflow execution time in seconds"""
        total_time = 0
        for step in workflow.steps:
            step_time = max(action.estimated_time or 0 for action in step.actions)
            if step.parallel_execution:
                total_time += step_time
            else:
                total_time += sum(action.estimated_time or 0 for action in step.actions)
        
        return total_time
    
    def _assess_complexity(self, workflow: AutomationWorkflow) -> str:
        """Assess workflow complexity"""
        total_actions = sum(len(step.actions) for step in workflow.steps)
        has_parallel = any(step.parallel_execution for step in workflow.steps)
        
        if total_actions <= 3:
            return "simple"
        elif total_actions <= 8:
            return "moderate"
        elif has_parallel:
            return "complex"
        else:
            return "advanced"
    
    def _get_workflow_priority(self, workflow: AutomationWorkflow) -> str:
        """Get overall workflow priority"""
        priorities = []
        for step in workflow.steps:
            for action in step.actions:
                priorities.append(action.priority.value)
        
        if "critical" in priorities:
            return "critical"
        elif "high" in priorities:
            return "high"
        elif priorities.count("medium") > priorities.count("low"):
            return "medium"
        else:
            return "low"
    
    def _generate_workflow_preview(self, workflow: AutomationWorkflow) -> Dict:
        """Generate preview of workflow execution"""
        preview = {
            "workflow_id": workflow.workflow_id,
            "name": workflow.name,
            "description": workflow.description,
            "vision_type": workflow.vision_insight.get("type", "unknown"),
            "steps": []
        }
        
        for step in workflow.steps:
            step_preview = {
                "step_id": step.step_id,
                "name": step.name,
                "description": step.description,
                "parallel_execution": step.parallel_execution,
                "actions": []
            }
            
            for action in step.actions:
                action_preview = {
                    "action_id": action.action_id,
                    "type": action.type.value,
                    "priority": action.priority.value,
                    "description": action.description,
                    "estimated_time": action.estimated_time
                }
                
                if action.code_snippet:
                    action_preview["has_code"] = True
                    action_preview["code_lines"] = len(action.code_snippet.split('\n'))
                
                step_preview["actions"].append(action_preview)
            
            preview["steps"].append(step_preview)
        
        return preview
    
    def get_automation_suggestions(self, vision_result: Dict, limit: int = 5) -> List[Dict]:
        """Get top automation suggestions without full workflow creation"""
        # Quick analysis for immediate suggestions
        suggestions = []
        
        vision_type = vision_result.get("type", "unknown")
        analysis = vision_result.get("analysis", "").lower()
        
        # Generate context-based suggestions
        if "error" in analysis or "bug" in analysis:
            suggestions.extend([
                {
                    "type": "error_resolution",
                    "action": "fix_detected_error",
                    "description": "Fix the detected error automatically",
                    "priority": "critical",
                    "estimated_time": 30
                },
                {
                    "type": "code_generation",
                    "action": "add_error_handling",
                    "description": "Add comprehensive error handling",
                    "priority": "high",
                    "estimated_time": 15
                }
            ])
        
        if "code" in analysis and vision_type == "code_analysis":
            suggestions.extend([
                {
                    "type": "code_generation",
                    "action": "improve_code_quality",
                    "description": "Improve code quality and performance",
                    "priority": "medium",
                    "estimated_time": 45
                },
                {
                    "type": "code_generation",
                    "action": "create_unit_tests",
                    "description": "Generate comprehensive unit tests",
                    "priority": "medium",
                    "estimated_time": 60
                }
            ])
        
        if "design" in analysis or "ui" in analysis:
            suggestions.extend([
                {
                    "type": "code_generation",
                    "action": "convert_to_html_css",
                    "description": "Convert design to responsive HTML/CSS",
                    "priority": "high",
                    "estimated_time": 90
                },
                {
                    "type": "code_generation",
                    "action": "add_javascript_interactions",
                    "description": "Add interactive JavaScript functionality",
                    "priority": "medium",
                    "estimated_time": 45
                }
            ])
        
        # Sort by priority and limit
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        suggestions.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        return suggestions[:limit]
    
    def get_workflow_status(self, workflow_id: str) -> Dict:
        """Get detailed workflow status"""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}
        
        status = self.pipeline.get_workflow_status(workflow_id)
        
        # Add additional engine-specific information
        if "error" not in status:
            workflow = self.active_workflows[workflow_id]
            status.update({
                "vision_analysis": workflow.vision_insight.get("analysis", ""),
                "automation_type": self._determine_automation_type(workflow.vision_insight, workflow),
                "complexity": self._assess_complexity(workflow),
                "estimated_remaining_time": self._estimate_remaining_time(workflow)
            })
        
        return status
    
    def _estimate_remaining_time(self, workflow: AutomationWorkflow) -> int:
        """Estimate remaining execution time"""
        if workflow.status == "completed":
            return 0
        elif workflow.status == "running":
            # Calculate based on progress
            total_time = self._estimate_workflow_time(workflow)
            remaining_percentage = 100 - workflow.progress
            return int(total_time * (remaining_percentage / 100))
        else:
            return self._estimate_workflow_time(workflow)
    
    def get_active_workflows(self) -> List[Dict]:
        """Get all active workflows"""
        active = []
        for workflow_id in self.pipeline.get_active_workflows():
            workflow_id = workflow_id["workflow_id"]
            status = self.get_workflow_status(workflow_id)
            active.append(status)
        
        return active
    
    def get_automation_history(self, limit: int = 10) -> List[Dict]:
        """Get automation execution history"""
        history = self.pipeline.get_execution_history(limit)
        
        # Add engine statistics
        for entry in history:
            entry.update({
                "engine_stats": {
                    "total_processed": self.automation_stats["total_processed"],
                    "success_rate": (self.automation_stats["successful_automations"] / 
                                  max(1, self.automation_stats["total_processed"])) * 100
                }
            })
        
        return history
    
    def get_automation_stats(self) -> Dict:
        """Get comprehensive automation statistics"""
        return {
            "automation_stats": self.automation_stats,
            "pipeline_capabilities": self.pipeline.get_capabilities(),
            "active_workflows": len(self.get_active_workflows()),
            "total_workflows_created": len(self.active_workflows),
            "execution_history_size": len(self.execution_history),
            "average_workflow_time": self._calculate_average_workflow_time(),
            "most_used_automation_types": self._get_most_used_types()
        }
    
    def _calculate_average_workflow_time(self) -> float:
        """Calculate average workflow execution time"""
        if not self.execution_history:
            return 0.0
        
        total_time = sum(entry.get("execution_time", 0) for entry in self.execution_history)
        return total_time / len(self.execution_history)
    
    def _get_most_used_types(self) -> Dict[str, int]:
        """Get most used automation types"""
        type_counts = self.automation_stats["automation_types_used"]
        return dict(sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5])
    
    async def batch_process_vision_insights(self, vision_results: List[Dict]) -> List[Dict]:
        """Process multiple vision insights in batch"""
        results = []
        
        for vision_result in vision_results:
            result = await self.process_vision_insight(vision_result)
            results.append(result)
            
            # Brief pause to avoid overwhelming
            await asyncio.sleep(0.1)
        
        return results
    
    def create_custom_automation_rule(self, rule_name: str, rule_config: Dict) -> Dict:
        """Create custom automation rule"""
        try:
            # Validate rule configuration
            required_fields = ["triggers", "actions", "priority_mapping"]
            for field in required_fields:
                if field not in rule_config:
                    return {
                        "success": False,
                        "error": f"Missing required field: {field}"
                    }
            
            # Add to pipeline rules
            self.pipeline.automation_rules[rule_name] = rule_config
            
            return {
                "success": True,
                "rule_name": rule_name,
                "message": "Custom automation rule created successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_automation_capabilities(self) -> Dict:
        """Get comprehensive automation capabilities"""
        return {
            "automation_types": [t.value for t in AutomationType],
            "priority_levels": [p.value for p in AutomationPriority],
            "workflow_patterns": list(self.pipeline.workflow_patterns.keys()),
            "code_templates": list(self.pipeline.code_templates.keys()),
            "automation_rules": list(self.pipeline.automation_rules.keys()),
            "total_workflows": len(self.active_workflows),
            "active_workflows": len(self.get_active_workflows()),
            "completed_executions": len(self.execution_history),
            "batch_processing": True,
            "custom_rules": True,
            "execution_modes": ["full", "preview"],
            "vision_types_supported": [
                "code_analysis",
                "design_to_code", 
                "error_detection",
                "document_analysis",
                "screenshot_analysis"
            ]
        }
