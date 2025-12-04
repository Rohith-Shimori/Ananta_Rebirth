#!/usr/bin/env python3
"""Debug import issues"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Testing individual imports...")

try:
    from core.ollama_client import OllamaClient
    print("✅ OllamaClient imported successfully")
except Exception as e:
    print(f"❌ OllamaClient import failed: {e}")

try:
    from core.batch_inference_engine import BatchInferenceEngine
    print("✅ BatchInferenceEngine imported successfully")
except Exception as e:
    print(f"❌ BatchInferenceEngine import failed: {e}")

try:
    from core.lightweight_agent_orchestrator import LightweightAgentOrchestrator
    print("✅ LightweightAgentOrchestrator imported successfully")
except Exception as e:
    print(f"❌ LightweightAgentOrchestrator import failed: {e}")

try:
    from core.controller import AnantaController
    print("✅ AnantaController imported successfully")
except Exception as e:
    print(f"❌ AnantaController import failed: {e}")
    import traceback
    traceback.print_exc()
