# Ananta Rebirth - Engines Usage Guide

## 🎯 Quick Overview

The `engines/` folder contains 4 specialized AI engines that are **actively used** by the main controller:

| Engine | File | Status | Used By |
|--------|------|--------|---------|
| 🧠 CodeExpert | `code_expert.py` | ✅ Active | Controller |
| 🎨 CreativeEngine | `creative_engine.py` | ✅ Active | Controller |
| 👤 PersonalityEngine | `personality_engine.py` | ✅ Active | Controller |
| 🏗️ ProjectScaffolder | `project_scaffolder.py` | ✅ Active | Controller |

## 📍 Where Engines Are Used

### In `core/controller.py`

**Imports**:
```python
from engines.personality_engine import PersonalityEngine
from engines.creative_engine import CreativeEngine
from engines.code_expert import CodeExpert
from engines.project_scaffolder import ProjectScaffolder
```

**Initialization**:
```python
class AnantaController:
    def __init__(self):
        # ... other initialization ...
        self.personality = PersonalityEngine()
        self.creative = CreativeEngine()
        self.code_expert = CodeExpert()
        self.scaffolder = ProjectScaffolder()
```

### In `core/brain_manager.py`

**Imports**:
```python
from ..engines.personality_engine import PersonalityEngine
from ..engines.code_expert import CodeExpert
from ..engines.project_scaffolder import ProjectScaffolder
```

**Initialization**:
```python
self.personality = PersonalityEngine()
self.code_expert = CodeExpert()
self.scaffolder = ProjectScaffolder()
```

## 🔧 Detailed Engine Usage

### 1. CodeExpert - Code Generation & Analysis

**Location**: `engines/code_expert.py` (610 lines)

**What It Does**:
- Generates code in multiple languages
- Analyzes code quality
- Reviews code for issues
- Generates tests
- Creates documentation

**Supported Languages**:
- Python, JavaScript, TypeScript
- Rust, C++, Go, Java

**How It's Used**:
```python
# In controller
self.code_expert = CodeExpert()

# Usage example
code = self.code_expert.generate_code(
    description="Create a function to sort a list",
    language="python"
)

analysis = self.code_expert.analyze_code(code)
```

**Key Methods**:
- `analyze_code(code)` - Analyze code quality
- `generate_code(description, language)` - Generate code
- `review_code(code)` - Review for issues
- `generate_tests(code)` - Generate test cases
- `generate_documentation(code)` - Generate docs

---

### 2. CreativeEngine - Creative Content Generation

**Location**: `engines/creative_engine.py` (312 lines)

**What It Does**:
- Generates creative content
- Brainstorms ideas
- Creates stories
- Explores philosophical concepts
- Generates design thinking solutions

**Creative Types**:
- Brainstorming
- Story/Narrative
- Philosophy
- Design
- Music
- Art

**How It's Used**:
```python
# In controller
self.creative = CreativeEngine()

# Usage example
intent = self.creative.detect_creative_intent(
    "Write a story about AI"
)

content = self.creative.generate(
    prompt="Write a story about AI",
    creative_type="story"
)
```

**Key Methods**:
- `detect_creative_intent(query)` - Identify creative request type
- `generate(prompt, creative_type)` - Generate creative content
- `brainstorm(topic)` - Generate ideas
- `create_story(prompt)` - Create narrative
- `save_project(project_data)` - Save creative work

**Data Storage**:
- `data/creative_projects.json` - Project history

---

### 3. PersonalityEngine - Personality & Persona Management

**Location**: `engines/personality_engine.py` (200 lines)

**What It Does**:
- Detects query type
- Builds contextual system prompts
- Manages personality traits
- Stores and retrieves facts
- Adapts responses based on context

**Query Types Detected**:
- Teaching (explain, what is, how does)
- Problem solving (help, stuck, error)
- Casual (chat, conversation)
- Debugging (debug, fix, broken)
- Creative (create, write, design)

**How It's Used**:
```python
# In controller
self.personality = PersonalityEngine()

# Usage example
query_type = self.personality.detect_query_type(
    "How do I fix this error?"
)

system_prompt = self.personality.build_system_prompt(
    query_type=query_type,
    context="debugging"
)

facts = self.personality.get_personality_traits()
```

**Key Methods**:
- `detect_query_type(query)` - Identify interaction type
- `build_system_prompt(query_type, context)` - Generate prompt
- `get_personality_traits()` - Get personality settings
- `update_facts(facts)` - Update knowledge base
- `adapt_response(response, context)` - Adapt response

**Data Storage**:
- `data/persona_config.json` - Personality config
- `data/facts.json` - Knowledge facts

---

### 4. ProjectScaffolder - Project Structure Generation

**Location**: `engines/project_scaffolder.py` (696 lines)

**What It Does**:
- Generates complete project structures
- Creates configuration files
- Generates test templates
- Creates documentation templates
- Generates setup scripts

**Project Templates**:
- Python CLI, API, ML projects
- Node.js, React, Next.js projects
- Rust, Go projects
- And more...

**How It's Used**:
```python
# In controller
self.scaffolder = ProjectScaffolder()

# Usage example
structure = self.scaffolder.generate_structure({
    "name": "my_project",
    "type": "python_api",
    "description": "My API project"
})

templates = self.scaffolder.get_templates()
```

**Key Methods**:
- `generate_structure(spec)` - Generate project structure
- `get_templates()` - List available templates
- `create_project(name, template)` - Create new project
- `get_template_details(template_name)` - Get template info

---

## 📊 Engine Integration Flow

```
User Query
    ↓
Controller.query()
    ↓
PersonalityEngine.detect_query_type()
    ↓
Route to appropriate engine:
    ├─→ CodeExpert (code-related)
    ├─→ CreativeEngine (creative)
    ├─→ ProjectScaffolder (project setup)
    └─→ Other engines (other types)
    ↓
Engine processes request
    ↓
Return result
    ↓
Controller formats response
    ↓
Response to user
```

## 🧪 Testing Individual Engines

### Test CodeExpert
```bash
python -c "
from engines.code_expert import CodeExpert
expert = CodeExpert()
print('✅ CodeExpert loaded successfully')
print(f'Supported languages: {list(expert.SUPPORTED_LANGUAGES.keys())}')
"
```

### Test CreativeEngine
```bash
python -c "
from engines.creative_engine import CreativeEngine
creative = CreativeEngine()
intent = creative.detect_creative_intent('Write a story')
print(f'✅ CreativeEngine loaded')
print(f'Detected intent: {intent}')
"
```

### Test PersonalityEngine
```bash
python -c "
from engines.personality_engine import PersonalityEngine
personality = PersonalityEngine()
query_type = personality.detect_query_type('How do I fix this?')
print(f'✅ PersonalityEngine loaded')
print(f'Detected query type: {query_type}')
"
```

### Test ProjectScaffolder
```bash
python -c "
from engines.project_scaffolder import ProjectScaffolder
scaffolder = ProjectScaffolder()
templates = scaffolder.get_templates()
print(f'✅ ProjectScaffolder loaded')
print(f'Available templates: {len(templates)}')
"
```

### Run All Engine Tests
```bash
python tests/test_features_individual.py
```

Includes:
- 🏗️ Project Scaffolder test
- 🎨 Creative Engine test

## 📁 Engine Data Files

### `data/persona_config.json`
Personality configuration:
```json
{
  "name": "Ananta",
  "version": "1.0",
  "traits": {
    "helpfulness": 0.95,
    "creativity": 0.85,
    "technical_depth": 0.90,
    "friendliness": 0.88,
    "professionalism": 0.92
  },
  "communication_style": "friendly_professional",
  "expertise_areas": [
    "programming",
    "ai",
    "automation",
    "creative_thinking"
  ]
}
```

### `data/facts.json`
Knowledge facts database:
```json
{
  "creator": "User",
  "purpose": "Local AI Assistant",
  "capabilities": [
    "advanced_reasoning",
    "code_generation",
    "creative_thinking",
    "project_scaffolding"
  ],
  "knowledge_base": {}
}
```

### `data/creative_projects.json`
Creative project history:
```json
[
  {
    "id": "project_1",
    "type": "story",
    "title": "Example Story",
    "content": "...",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

## 🎯 Common Use Cases

### Use Case 1: Code Review Request
```
User: "Review this Python code for issues"
    ↓
PersonalityEngine: Detects "problem_solving"
    ↓
CodeExpert: Analyzes code
    ↓
Returns: Code review with suggestions
```

### Use Case 2: Creative Brainstorming
```
User: "Brainstorm ideas for a mobile app"
    ↓
PersonalityEngine: Detects "creative"
    ↓
CreativeEngine: Generates ideas
    ↓
Returns: List of creative ideas
```

### Use Case 3: Project Setup
```
User: "Generate a Python API project structure"
    ↓
PersonalityEngine: Detects "problem_solving"
    ↓
ProjectScaffolder: Generates structure
    ↓
Returns: Complete project structure
```

### Use Case 4: Teaching Moment
```
User: "Explain how decorators work in Python"
    ↓
PersonalityEngine: Detects "teaching"
    ↓
CodeExpert: Generates examples
    ↓
Returns: Explanation with code examples
```

## 🔍 How to Verify Engines Are Working

### Quick Verification
```bash
python quick_test.py
```

Expected output includes:
```
✅ Creative Engine: OK (loaded)
✅ Project Scaffolder: OK (generated X files)
```

### Detailed Verification
```bash
python tests/test_features_individual.py
```

Expected output includes:
```
🎨 Testing Creative Engine...
  ✅ Creative content generated

🏗️ Testing Project Scaffolder...
  ✅ Generated project structure
```

### Full Verification
```bash
python run_tests.py
```

Generates `test_report.json` with engine test results.

## 📊 Engine Statistics

| Engine | Lines | Classes | Methods | Status |
|--------|-------|---------|---------|--------|
| CodeExpert | 610 | 1 | 10+ | ✅ Active |
| CreativeEngine | 312 | 1 | 8+ | ✅ Active |
| PersonalityEngine | 200 | 1 | 6+ | ✅ Active |
| ProjectScaffolder | 696 | 1 | 8+ | ✅ Active |
| **Total** | **1,818** | **4** | **32+** | **✅ Active** |

## 🚀 Performance Notes

### CodeExpert
- Fast: <1s for most operations
- Caches language configs
- Efficient template reuse

### CreativeEngine
- Medium: 1-2s for generation
- JSON-based storage
- Efficient idea generation

### PersonalityEngine
- Very fast: <100ms
- Loads config once
- Pattern matching for query types

### ProjectScaffolder
- Fast: <1s for structure generation
- Pre-defined templates
- Efficient file generation

## 🔒 Security Features

### CodeExpert
- Validates code syntax
- Checks for security issues
- Sandboxes execution

### CreativeEngine
- Input validation
- Injection prevention
- Output sanitization

### PersonalityEngine
- Fact database protection
- Config validation
- Secure storage

### ProjectScaffolder
- Project name validation
- Path traversal prevention
- Safe file generation

## 📚 Related Files

- **ENGINES_DOCUMENTATION.md** - Detailed engine documentation
- **PROJECT_STRUCTURE.md** - Overall architecture
- **core/controller.py** - Main controller (uses engines)
- **core/brain_manager.py** - Brain manager (uses engines)

## ✅ Verification Checklist

- [x] All engines documented
- [x] Usage patterns explained
- [x] Integration shown
- [x] Testing instructions provided
- [x] Data files described
- [x] Use cases listed
- [x] Performance notes included
- [x] Security features documented

---

**Status**: ✅ Engines fully organized and documented
**Last Updated**: 2024
**Version**: 1.0
