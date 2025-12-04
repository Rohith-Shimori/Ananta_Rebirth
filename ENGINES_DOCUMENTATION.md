# Ananta Rebirth - Engines Documentation

## 🎯 Overview

The `engines/` folder contains specialized AI engines that handle specific domains. These are **critical components** used by the main controller.

## 📁 Engines Structure

```
engines/
├── __init__.py                    # Package initialization
├── code_expert.py                 # Code generation & analysis
├── creative_engine.py             # Creative content generation
├── personality_engine.py          # Personality & persona management
├── project_scaffolder.py          # Project structure generation
└── data/                          # Engine data files
    ├── persona_config.json        # Personality configuration
    ├── facts.json                 # Knowledge facts database
    └── creative_projects.json     # Creative projects history
```

## 🔧 Engine Details

### 1. CodeExpert (`code_expert.py`)

**Purpose**: Advanced code generation and analysis

**Capabilities**:
- Multi-language support (Python, JavaScript, TypeScript, Rust, C++, Go, Java)
- Code generation with best practices
- Code analysis and review
- Test generation
- Documentation generation
- Bug detection

**Supported Languages**:
```python
SUPPORTED_LANGUAGES = {
    "python": {"ext": ".py", "test_framework": "pytest"},
    "javascript": {"ext": ".js", "test_framework": "jest"},
    "typescript": {"ext": ".ts", "test_framework": "jest"},
    "rust": {"ext": ".rs", "test_framework": "built-in"},
    "cpp": {"ext": ".cpp", "test_framework": "gtest"},
    "go": {"ext": ".go", "test_framework": "built-in"},
    "java": {"ext": ".java", "test_framework": "junit"},
}
```

**Usage in Controller**:
```python
self.code_expert = CodeExpert()
```

**Key Methods**:
- `analyze_code()` - Analyze code quality
- `generate_code()` - Generate code from description
- `review_code()` - Review code for issues
- `generate_tests()` - Generate test cases
- `generate_documentation()` - Generate docs

---

### 2. CreativeEngine (`creative_engine.py`)

**Purpose**: Creative content generation and brainstorming

**Capabilities**:
- Brainstorming and ideation
- Story and narrative generation
- Philosophy and thought exploration
- Design thinking
- Music and art concepts
- Creative problem-solving

**Creative Types Supported**:
- `brainstorm` - Generate ideas
- `story` - Create narratives
- `philosophy` - Explore philosophical concepts
- `design` - Design thinking
- `music` - Music composition ideas
- `art` - Art and visual concepts

**Usage in Controller**:
```python
self.creative = CreativeEngine()
```

**Key Methods**:
- `detect_creative_intent()` - Identify creative request type
- `generate()` - Generate creative content
- `brainstorm()` - Generate ideas
- `create_story()` - Create narratives
- `save_project()` - Save creative work

**Data Storage**:
- `creative_projects.json` - Stores creative projects history

---

### 3. PersonalityEngine (`personality_engine.py`)

**Purpose**: Dynamic personality and persona management

**Capabilities**:
- Context-aware personality adaptation
- Query type detection
- Dynamic system prompt generation
- Personality trait management
- Fact and knowledge storage
- Contextual response adaptation

**Query Types Detected**:
- `teaching` - Educational interactions
- `problem_solving` - Help with issues
- `casual` - Casual conversation
- `debugging` - Debugging assistance
- `creative` - Creative tasks

**Usage in Controller**:
```python
self.personality = PersonalityEngine()
```

**Key Methods**:
- `detect_query_type()` - Identify interaction type
- `build_system_prompt()` - Generate contextual prompt
- `get_personality_traits()` - Get personality settings
- `update_facts()` - Update knowledge base
- `adapt_response()` - Adapt response to context

**Data Storage**:
- `persona_config.json` - Personality configuration
- `facts.json` - Knowledge facts database

---

### 4. ProjectScaffolder (`project_scaffolder.py`)

**Purpose**: Automated project structure generation

**Capabilities**:
- Generate complete project structures
- Support multiple languages and frameworks
- Create configuration files
- Generate test files
- Create documentation templates
- Generate setup scripts

**Project Templates Supported**:
- `python_cli` - Python CLI Application
- `python_api` - Python FastAPI/Flask REST API
- `python_ml` - Python Machine Learning Project
- `nodejs_api` - Node.js Express API
- `react_app` - React Web Application
- `nextjs_app` - Next.js Full-stack App
- `rust_cli` - Rust CLI Application
- `go_api` - Go REST API

**Usage in Controller**:
```python
self.scaffolder = ProjectScaffolder()
```

**Key Methods**:
- `generate_structure()` - Generate project structure
- `get_templates()` - List available templates
- `create_project()` - Create new project
- `get_template_details()` - Get template information

---

## 🔗 Integration with Controller

All engines are initialized and used in `core/controller.py`:

```python
from engines.personality_engine import PersonalityEngine
from engines.creative_engine import CreativeEngine
from engines.code_expert import CodeExpert
from engines.project_scaffolder import ProjectScaffolder

class AnantaController:
    def __init__(self):
        # Initialize engines
        self.personality = PersonalityEngine()
        self.creative = CreativeEngine()
        self.code_expert = CodeExpert()
        self.scaffolder = ProjectScaffolder()
```

## 📊 Engine Usage Map

| Engine | Used By | Purpose |
|--------|---------|---------|
| CodeExpert | Controller | Code analysis & generation |
| CreativeEngine | Controller | Creative content |
| PersonalityEngine | Controller | Personality adaptation |
| ProjectScaffolder | Controller | Project generation |

## 💾 Data Files

### `data/persona_config.json`
Stores personality configuration:
```json
{
  "name": "Ananta",
  "traits": {
    "helpfulness": 0.95,
    "creativity": 0.85,
    "technical_depth": 0.90
  },
  "communication_style": "friendly_professional"
}
```

### `data/facts.json`
Stores knowledge facts:
```json
{
  "creator": "User",
  "purpose": "Local AI Assistant",
  "capabilities": ["reasoning", "coding", "creativity"]
}
```

### `data/creative_projects.json`
Stores creative project history:
```json
[
  {
    "id": "project_1",
    "type": "story",
    "title": "Example Story",
    "content": "..."
  }
]
```

## 🧪 Testing Engines

### Individual Engine Tests

**Test CodeExpert**:
```bash
python -c "
from engines.code_expert import CodeExpert
expert = CodeExpert()
print('✅ CodeExpert loaded')
"
```

**Test CreativeEngine**:
```bash
python -c "
from engines.creative_engine import CreativeEngine
creative = CreativeEngine()
print('✅ CreativeEngine loaded')
"
```

**Test PersonalityEngine**:
```bash
python -c "
from engines.personality_engine import PersonalityEngine
personality = PersonalityEngine()
print('✅ PersonalityEngine loaded')
"
```

**Test ProjectScaffolder**:
```bash
python -c "
from engines.project_scaffolder import ProjectScaffolder
scaffolder = ProjectScaffolder()
print('✅ ProjectScaffolder loaded')
"
```

### Run All Engine Tests
```bash
python tests/test_features_individual.py
```

This includes:
- 🏗️ Project Scaffolder test
- 🎨 Creative Engine test

## 🎯 Use Cases

### CodeExpert Use Cases
1. **Code Review** - Analyze code quality
2. **Code Generation** - Generate code from description
3. **Bug Detection** - Find potential issues
4. **Test Generation** - Create test cases
5. **Documentation** - Generate API docs

### CreativeEngine Use Cases
1. **Brainstorming** - Generate ideas
2. **Story Writing** - Create narratives
3. **Design Thinking** - Solve problems creatively
4. **Philosophy** - Explore concepts
5. **Music/Art** - Generate creative concepts

### PersonalityEngine Use Cases
1. **Context Awareness** - Adapt to user needs
2. **Query Classification** - Identify request type
3. **Personality Adaptation** - Adjust tone/style
4. **Knowledge Management** - Store facts
5. **Response Customization** - Tailor responses

### ProjectScaffolder Use Cases
1. **Project Setup** - Generate project structure
2. **Framework Setup** - Initialize frameworks
3. **Configuration** - Generate config files
4. **Testing** - Create test structure
5. **Documentation** - Generate docs template

## 🔄 Engine Workflow

```
User Query
    ↓
Controller receives query
    ↓
PersonalityEngine detects query type
    ↓
Route to appropriate engine:
    ├─→ CodeExpert (if code-related)
    ├─→ CreativeEngine (if creative)
    ├─→ ProjectScaffolder (if project setup)
    └─→ Other engines (if other)
    ↓
Engine processes request
    ↓
Return result to Controller
    ↓
Controller formats response
    ↓
Response to user
```

## 📈 Performance Optimization

### CodeExpert
- Caches language configurations
- Reuses templates
- Batch processes multiple files

### CreativeEngine
- Stores project history in JSON
- Caches creative templates
- Efficient idea generation

### PersonalityEngine
- Loads persona config once
- Caches query type patterns
- Fast fact lookup

### ProjectScaffolder
- Pre-defined templates
- Efficient structure generation
- Template caching

## 🔒 Security Considerations

### CodeExpert
- Validates code syntax
- Checks for security issues
- Sandboxes code execution

### CreativeEngine
- Validates input
- Prevents injection attacks
- Sanitizes output

### PersonalityEngine
- Protects fact database
- Validates persona config
- Secure fact storage

### ProjectScaffolder
- Validates project names
- Prevents path traversal
- Safe file generation

## 🚀 Future Enhancements

### CodeExpert
- [ ] Support more languages
- [ ] Advanced code analysis
- [ ] Performance profiling
- [ ] Security scanning

### CreativeEngine
- [ ] Multi-modal generation
- [ ] Collaborative features
- [ ] Version control
- [ ] Advanced brainstorming

### PersonalityEngine
- [ ] Machine learning adaptation
- [ ] User preference learning
- [ ] Dynamic trait adjustment
- [ ] Advanced context awareness

### ProjectScaffolder
- [ ] Custom templates
- [ ] Framework integration
- [ ] Dependency management
- [ ] CI/CD setup

## 📚 Related Documentation

- **PROJECT_STRUCTURE.md** - Overall architecture
- **TESTING_GUIDE.md** - Testing instructions
- **core/controller.py** - Main controller integration

## ✅ Verification Checklist

- [x] All engines documented
- [x] Usage patterns explained
- [x] Data files described
- [x] Integration shown
- [x] Testing instructions provided
- [x] Use cases listed
- [x] Performance notes included
- [x] Security considerations covered

---

**Status**: ✅ Engines fully documented and organized
**Last Updated**: 2024
**Version**: 1.0
