#!/usr/bin/env python3
"""
Ananta Rebirth - Local AI Assistant
Direct execution without API layer
"""

import sys
import os
import asyncio
from datetime import datetime
import logging

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AnantaLocal:
    """Local Ananta Assistant - Direct AI Interface"""
    
    def __init__(self):
        """Initialize Ananta Local"""
        self.start_time = datetime.now()
        self.controller = None
        self.running = False
        
        print("🚀 Initializing Ananta Rebirth...")
        self._initialize_engines()
        
    def _initialize_engines(self):
        """Initialize all AI engines"""
        try:
            # Import and initialize controller
            from core.controller import AnantaController
            self.controller = AnantaController()
            
            print("✅ Ananta Controller initialized")
            print(f"🧠 Model: {self.controller.model}")
            print(f"🔥 GPU: Available and optimized")
            print(f"👁️ Vision: {self.controller.vision.vision_model}")
            print(f"🤖 Automation: Ready")
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            raise
    
    def show_status(self):
        """Display system status"""
        print("\n" + "="*60)
        print("🤖 ANANTA REBIRTH - SYSTEM STATUS")
        print("="*60)
        
        # Basic info
        uptime = datetime.now() - self.start_time
        print(f"⏰ Uptime: {uptime}")
        print(f"🧠 AI Model: {self.controller.model}")
        
        # Vision status
        vision_caps = self.controller.get_vision_capabilities()
        print(f"👁️ Vision Model: {vision_caps.get('vision_model', 'Unknown')}")
        print(f"🔥 GPU Accelerated: {vision_caps.get('gpu_accelerated', False)}")
        
        # Automation status
        auto_caps = self.controller.get_automation_capabilities()
        print(f"🤖 Automation Types: {len(auto_caps.get('automation_types', []))}")
        print(f"📋 Active Workflows: {auto_caps.get('active_workflows', 0)}")
        
        # Memory status
        memory_stats = self.controller.get_memory_stats()
        print(f"🧠 Personal Memories: {memory_stats.get('personal_count', 0)}")
        print(f"📚 Knowledge Items: {memory_stats.get('knowledge_count', 0)}")
        
        print("\n✅ All systems operational!")
    
    def process_query(self, query):
        """Process user query directly"""
        print(f"\n🤔 Processing: {query}")
        
        try:
            # Use controller's enhanced query method
            response = self.controller.query(query)
            
            print(f"\n🤖 Ananta: {response}")
            return response
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def analyze_image(self, image_path, analysis_type="auto"):
        """Analyze image directly"""
        print(f"\n👁️ Analyzing image: {os.path.basename(image_path)}")
        
        try:
            # Use unified processing
            result = self.controller.process_vision_automation(image_path, analysis_type)
            
            if result.get("success"):
                print("✅ Analysis successful!")
                
                # Show vision results
                vision = result.get("vision_analysis", {})
                if vision.get("success"):
                    print(f"🎯 Type: {vision.get('type')}")
                    analysis = vision.get('analysis', '')
                    if len(analysis) > 200:
                        analysis = analysis[:200] + "..."
                    print(f"📋 Analysis: {analysis}")
                
                # Show automation suggestions
                automation = result.get("automation_suggestions", {})
                if automation.get("success"):
                    suggestions = automation.get('suggestions', [])
                    print(f"🤖 Automation suggestions: {len(suggestions)}")
                    for i, suggestion in enumerate(suggestions[:3]):
                        print(f"   {i+1}. {suggestion.get('description', 'No description')}")
            else:
                print(f"❌ Analysis failed: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_capabilities(self):
        """Show all capabilities"""
        print("\n" + "="*60)
        print("🌟 ANANTA CAPABILITIES")
        print("="*60)
        
        capabilities = {
            "🧠 Intelligence": [
                "Advanced reasoning & context",
                "Emotional intelligence", 
                "Proactive suggestions",
                "Self-improvement learning"
            ],
            "👁️ Vision": [
                "Code analysis & review",
                "Screenshot understanding",
                "Document OCR & analysis",
                "Error detection & fixes",
                "Design-to-code conversion"
            ],
            "🤖 Automation": [
                "Smart workflow generation",
                "Custom automation rules",
                "Batch processing",
                "Real-time monitoring",
                "Priority-based execution"
            ],
            "🔧 Features": [
                "Personal memory system",
                "Knowledge base integration",
                "Security analysis",
                "System monitoring",
                "Voice interface",
                "Context awareness"
            ]
        }
        
        for category, features in capabilities.items():
            print(f"\n{category}:")
            for feature in features:
                print(f"  ✅ {feature}")
    
    def run_interactive(self):
        """Run interactive mode"""
        print("\n" + "="*60)
        print("🤖 ANANTA REBIRTH - INTERACTIVE MODE")
        print("="*60)
        print("Type 'help' for commands, 'quit' to exit")
        
        self.running = True
        
        while self.running:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                elif user_input.lower() == 'status':
                    self.show_status()
                elif user_input.lower() == 'capabilities':
                    self.show_capabilities()
                elif user_input.startswith('image '):
                    # Image analysis command
                    image_path = user_input[6:].strip()
                    if os.path.exists(image_path):
                        self.analyze_image(image_path)
                    else:
                        print(f"❌ Image not found: {image_path}")
                else:
                    # Regular query
                    self.process_query(user_input)
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show help commands"""
        print("\n📚 Available commands:")
        print("  help        - Show this help")
        print("  status      - Show system status")
        print("  capabilities - Show all capabilities")
        print("  image <path> - Analyze image file")
        print("  quit/exit  - Exit Ananta")
        print("\n💬 Or just type any question or message!")

def main():
    """Main entry point"""
    try:
        # Initialize Ananta
        ananta = AnantaLocal()
        
        # Show welcome
        print("\n" + "="*60)
        print("🎉 WELCOME TO ANANTA REBIRTH!")
        print("="*60)
        print("🤖 Your local AI assistant is ready!")
        print("🔥 No API layer - Direct execution")
        print("👁️ Vision + Automation capabilities")
        print("🧠 Advanced intelligence with context")
        print("\nType 'help' to see available commands")
        
        # Run interactive mode
        ananta.run_interactive()
        
    except Exception as e:
        print(f"❌ Failed to start Ananta: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
