"""
Ananta Rebirth Configuration
Local version settings without API layer
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# AI Model Configuration
OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen2.5:7b-instruct-q4_K_M"
VISION_MODEL = "qwen3-vl:8b"
CODING_MODEL = "qwen2.5-coder:7b-instruct-q4_K_M"
FAST_MODEL = "llama3.2:3b-instruct-q6_K"

# ============================================================================
# REAL MODEL LINEUP (Using Your Available Models)
# ============================================================================
OPTIMAL_MODELS = {
    "sentinel": {
        "model": "qwen2.5:7b-instruct-q4_K_M",
        "vram": 4.7,
        "speed": 42,
        "use_case": "General chat, reasoning, daily tasks",
        "priority": 1,
        "description": "Primary conversational model"
    },
    "architect": {
        "model": "qwen2.5-coder:7b-instruct-q4_K_M",
        "vram": 4.7,
        "speed": 40,
        "use_case": "Code generation, debugging, refactoring",
        "priority": 1,
        "description": "Specialized coding model"
    },
    "oracle": {
        "model": "llama3.1:8b",
        "vram": 4.9,
        "speed": 35,
        "use_case": "Deep reasoning, math, analysis, logic",
        "priority": 1,
        "description": "Advanced reasoning model"
    },
    "flash": {
        "model": "llama3.2:3b-instruct-q6_K",
        "vram": 2.6,
        "speed": 65,
        "use_case": "Quick queries, simple tasks, rapid iteration",
        "priority": 2,
        "description": "Ultra-fast lightweight model"
    },
    "vision": {
        "model": "qwen3-vl:8b",
        "vram": 6.1,
        "speed": 30,
        "use_case": "Image analysis, visual reasoning",
        "priority": 1,
        "description": "Vision-language model"
    },
    "nano": {
        "model": "llama3.2:3b-instruct-q6_K",
        "vram": 2.6,
        "speed": 70,
        "use_case": "Ultra-low latency, parallel tasks, emergency backup",
        "priority": 3,
        "description": "Tiny emergency backup model"
    }
}

# Default model for routing
ROUTING_DEFAULT_MODEL = "sentinel"

# GPU Configuration - Optimized for RTX 4050
GPU_ENABLED = True
GPU_DEVICE = "cuda"
GPU_MEMORY_FRACTION = 0.85  # Use 85% of VRAM (5.1GB of 6GB)

# ============================================================================
# RTX 4050 GPU OPTIMIZATION SETTINGS
# ============================================================================
GPU_SETTINGS = {
    "num_gpu": 1,
    "main_gpu": 0,
    "num_thread": 12,  # i5 12th gen has 12 threads
    "numa": False,  # Single-socket CPU
    
    # Memory Optimization
    "use_mmap": True,  # Memory-mapped files
    "use_mlock": True,  # Lock model in RAM
    
    # Batch Processing
    "num_batch": 512,  # Optimal for RTX 4050
    "num_ctx": 4096,  # 4K context for 6GB VRAM
    
    # Speed Optimization
    "num_predict": 512,  # Max tokens per response
    "repeat_penalty": 1.1,
    "temperature": 0.7,
    "top_k": 40,
    "top_p": 0.9,
    
    # VRAM Optimization
    "f16_kv": True,  # FP16 for KV cache (saves VRAM)
    "low_vram": False,  # We have enough VRAM
}

# Vision Configuration
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
VISION_TIMEOUT = 180  # seconds

# Automation Configuration
MAX_WORKFLOWS = 100
WORKFLOW_TIMEOUT = 300  # seconds
BATCH_SIZE = 512  # Optimized for RTX 4050

# Memory Configuration
MEMORY_DB_PATH = DATA_DIR / "ananta_memory.db"
PERSONAL_MEMORY_LIMIT = 1000
KNOWLEDGE_BASE_LIMIT = 5000

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Voice Configuration (optional)
VOICE_ENABLED = True
SPEECH_RECOGNITION_ENABLED = True
TEXT_TO_SPEECH_ENABLED = True

# Security Configuration
ENCRYPTION_ENABLED = True
SESSION_TIMEOUT = 3600  # seconds

# Monitoring Configuration
MONITORING_ENABLED = True
MONITORING_INTERVAL = 10  # seconds

# Performance Configuration - Optimized for RTX 4050
CACHE_SIZE = 2000  # Increased from 1000
MAX_CONCURRENT_TASKS = 15  # Increased from 5 (i5 12th gen can handle 15-20)
THREAD_POOL_SIZE = 12  # Match CPU cores
ENABLE_PARALLEL = True  # Enable parallel processing

# ============================================================================
# CONTEXT WINDOW OPTIMIZATION
# ============================================================================
CONTEXT_WINDOW = 4096  # 4K tokens for 6GB VRAM
MAX_CONTEXT_WINDOW = 8192  # Can expand to 8K with optimization

# ============================================================================
# STREAMING & ADVANCED FEATURES
# ============================================================================
ENABLE_STREAMING = True  # Stream responses in real-time
ENABLE_CACHING = True  # Cache models in memory
ENABLE_QUANTIZATION = True  # Already enabled (Q4_K_M)
ENABLE_MIXED_PRECISION = True  # Use FP16 where possible
ENABLE_BATCHING = True  # Batch multiple requests
ENABLE_MODEL_PRELOADING = True  # Predictive model loading

# Model switching optimization
MODEL_SWITCH_TIMEOUT = 5  # seconds to switch models
PRELOAD_NEXT_MODEL = True  # Predictively load next model

# Development Settings
DEBUG = True
VERBOSE_LOGGING = False

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Environment-specific overrides
if os.getenv("ANANTA_ENV") == "production":
    DEBUG = False
    LOG_LEVEL = "WARNING"
    VERBOSE_LOGGING = False
