# project_scaffolder.py - Automated Project Setup
"""
Generate complete project structures with configs, tests, docs, and setup scripts.
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime

class ProjectScaffolder:
    """
    Generates complete project structures for different languages and frameworks.
    """
    
    PROJECT_TEMPLATES = {
        "python_cli": {
            "name": "Python CLI Application",
            "structure": [
                "src/",
                "src/__init__.py",
                "src/main.py",
                "src/cli.py",
                "src/config.py",
                "tests/",
                "tests/__init__.py",
                "tests/test_main.py",
                "docs/",
                "README.md",
                "requirements.txt",
                "setup.py",
                ".gitignore",
                ".env.example",
                "Makefile"
            ]
        },
        "python_api": {
            "name": "Python FastAPI/Flask REST API",
            "structure": [
                "app/",
                "app/__init__.py",
                "app/main.py",
                "app/models.py",
                "app/routes.py",
                "app/database.py",
                "app/config.py",
                "tests/",
                "tests/__init__.py",
                "tests/test_api.py",
                "docs/",
                "README.md",
                "requirements.txt",
                "Dockerfile",
                "docker-compose.yml",
                ".gitignore",
                ".env.example"
            ]
        },
        "javascript_react": {
            "name": "React Web Application",
            "structure": [
                "src/",
                "src/App.js",
                "src/index.js",
                "src/components/",
                "src/utils/",
                "src/styles/",
                "public/",
                "public/index.html",
                "tests/",
                "package.json",
                "README.md",
                ".gitignore",
                ".env.example",
                "webpack.config.js"
            ]
        },
        "rust_cli": {
            "name": "Rust CLI Application",
            "structure": [
                "src/",
                "src/main.rs",
                "src/lib.rs",
                "src/cli.rs",
                "tests/",
                "Cargo.toml",
                "README.md",
                ".gitignore"
            ]
        },
        "go_api": {
            "name": "Go REST API",
            "structure": [
                "cmd/",
                "cmd/api/main.go",
                "internal/",
                "internal/handlers/",
                "internal/models/",
                "internal/database/",
                "pkg/",
                "tests/",
                "go.mod",
                "go.sum",
                "README.md",
                ".gitignore",
                "Makefile",
                "Dockerfile"
            ]
        }
    }
    
    def generate_project(self, project_type: str, project_name: str, 
                        description: str = "", author: str = "") -> Dict:
        """
        Generate complete project structure and files.
        
        Returns:
            Dictionary with file paths and contents
        """
        if project_type not in self.PROJECT_TEMPLATES:
            return {"error": f"Unknown project type: {project_type}"}
        
        template = self.PROJECT_TEMPLATES[project_type]
        files = {}
        
        # Generate each file based on type
        for path in template["structure"]:
            if path.endswith("/"):
                # Directory
                files[path] = {"type": "directory"}
            else:
                # File - generate content
                content = self._generate_file_content(
                    path, project_type, project_name, description, author
                )
                files[path] = {
                    "type": "file",
                    "content": content
                }
        
        return {
            "project_name": project_name,
            "project_type": template["name"],
            "files": files,
            "setup_instructions": self._get_setup_instructions(project_type, project_name)
        }
    
    def _generate_file_content(self, filepath: str, project_type: str,
                               project_name: str, description: str, author: str) -> str:
        """Generate content for a specific file."""
        filename = os.path.basename(filepath)
        
        # README
        if filename == "README.md":
            return self._generate_readme(project_name, description, project_type, author)
        
        # Python files
        if filename == "requirements.txt":
            return self._generate_requirements(project_type)
        if filename == "setup.py":
            return self._generate_setup_py(project_name, description, author)
        if filename == "main.py":
            return self._generate_main_py(project_type)
        if filename == "__init__.py":
            return f'"""{ project_name} package."""\n__version__ = "0.1.0"\n'
        
        # Config files
        if filename == ".gitignore":
            return self._generate_gitignore(project_type)
        if filename == ".env.example":
            return self._generate_env_example(project_type)
        
        # Docker
        if filename == "Dockerfile":
            return self._generate_dockerfile(project_type)
        if filename == "docker-compose.yml":
            return self._generate_docker_compose(project_name)
        
        # Node/JS files
        if filename == "package.json":
            return self._generate_package_json(project_name, description)
        
        # Rust files
        if filename == "Cargo.toml":
            return self._generate_cargo_toml(project_name, description, author)
        
        # Go files
        if filename == "go.mod":
            return f"module github.com/{author}/{project_name}\n\ngo 1.21\n"
        
        # Makefile
        if filename == "Makefile":
            return self._generate_makefile(project_type)
        
        # Test files
        if "test_" in filename or filename.endswith("_test.go"):
            return self._generate_test_file(filepath, project_type)
        
        # Default empty or template
        return f"# {filepath}\n# TODO: Implement\n"
    
    def _generate_readme(self, name: str, desc: str, proj_type: str, author: str) -> str:
        """Generate comprehensive README."""
        return f"""# {name}

{desc or "A new project built with modern best practices."}

## Features

- Modern architecture
- Comprehensive testing
- Docker support
- CI/CD ready

## Installation

```bash
# Clone the repository
git clone https://github.com/{author}/{name}.git
cd {name}

# Install dependencies
{"pip install -r requirements.txt" if "python" in proj_type else "npm install" if "javascript" in proj_type else "cargo build" if "rust" in proj_type else "go mod download"}
```

## Usage

```bash
# Run the application
{"python src/main.py" if "python" in proj_type else "npm start" if "javascript" in proj_type else "cargo run" if "rust" in proj_type else "go run cmd/api/main.go"}
```

## Testing

```bash
# Run tests
{"pytest" if "python" in proj_type else "npm test" if "javascript" in proj_type else "cargo test" if "rust" in proj_type else "go test ./..."}
```

## Development

```bash
# Setup development environment
{"python -m venv venv && source venv/bin/activate" if "python" in proj_type else "npm install --dev"}

# Run in development mode
{"python src/main.py --dev" if "python" in proj_type else "npm run dev"}
```

## Project Structure

```
{name}/
├── src/          # Source code
├── tests/        # Test files
├── docs/         # Documentation
└── README.md     # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Author

{author or "Your Name"}

## Acknowledgments

Built with ❤️ using modern development practices.
"""
    
    def _generate_requirements(self, proj_type: str) -> str:
        """Generate Python requirements.txt."""
        if "api" in proj_type:
            return """fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
pytest==7.4.3
httpx==0.25.2
"""
        else:
            return """click==8.1.7
python-dotenv==1.0.0
pytest==7.4.3
"""
    
    def _generate_setup_py(self, name: str, desc: str, author: str) -> str:
        """Generate setup.py for Python projects."""
        return f"""from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{name}",
    version="0.1.0",
    author="{author or 'Your Name'}",
    description="{desc or 'A Python project'}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # Read from requirements.txt
    ],
    entry_points={{
        "console_scripts": [
            "{name}=src.main:main",
        ],
    }},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
"""
    
    def _generate_main_py(self, proj_type: str) -> str:
        """Generate main.py for Python projects."""
        if "api" in proj_type:
            return '''"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        else:
            return '''"""Main CLI application."""
import click

@click.command()
@click.option("--name", default="World", help="Name to greet")
def main(name):
    """Simple CLI application."""
    click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    main()
'''
    
    def _generate_gitignore(self, proj_type: str) -> str:
        """Generate .gitignore file."""
        common = """# Environment
.env
.venv
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
        if "python" in proj_type:
            return common + """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
"""
        elif "javascript" in proj_type or "react" in proj_type:
            return common + """
# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Build
build/
dist/
"""
        elif "rust" in proj_type:
            return common + """
# Rust
/target/
Cargo.lock
"""
        else:
            return common
    
    def _generate_env_example(self, proj_type: str) -> str:
        """Generate .env.example file."""
        if "api" in proj_type:
            return """# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256

# External Services
EXTERNAL_API_KEY=your-api-key
"""
        else:
            return """# Application Configuration
APP_ENV=development
DEBUG=false
LOG_LEVEL=INFO
"""
    
    def _generate_dockerfile(self, proj_type: str) -> str:
        """Generate Dockerfile."""
        if "python" in proj_type:
            return """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "src/main.py"]
"""
        elif "javascript" in proj_type:
            return """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
"""
        else:
            return "# TODO: Add Dockerfile for this project type\n"
    
    def _generate_docker_compose(self, name: str) -> str:
        """Generate docker-compose.yml."""
        return f"""version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/{name}
    depends_on:
      - db
    volumes:
      - .:/app
    
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB={name}
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""
    
    def _generate_package_json(self, name: str, desc: str) -> str:
        """Generate package.json for Node projects."""
        return json.dumps({
            "name": name,
            "version": "0.1.0",
            "description": desc or "A JavaScript project",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "dev": "nodemon src/index.js",
                "test": "jest",
                "lint": "eslint src/"
            },
            "keywords": [],
            "author": "",
            "license": "MIT",
            "dependencies": {},
            "devDependencies": {
                "jest": "^29.0.0",
                "nodemon": "^3.0.0",
                "eslint": "^8.0.0"
            }
        }, indent=2)
    
    def _generate_cargo_toml(self, name: str, desc: str, author: str) -> str:
        """Generate Cargo.toml for Rust projects."""
        return f"""[package]
name = "{name}"
version = "0.1.0"
edition = "2021"
authors = ["{author or 'Your Name <email@example.com>'}"]
description = "{desc or 'A Rust project'}"

[dependencies]
clap = {{ version = "4.4", features = ["derive"] }}
serde = {{ version = "1.0", features = ["derive"] }}
tokio = {{ version = "1.0", features = ["full"] }}

[dev-dependencies]
"""
    
    def _generate_makefile(self, proj_type: str) -> str:
        """Generate Makefile."""
        if "python" in proj_type:
            return """.PHONY: install test lint run clean

install:
\tpip install -r requirements.txt

test:
\tpytest tests/

lint:
\tpylint src/

run:
\tpython src/main.py

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {} +
\tfind . -type f -name '*.pyc' -delete
"""
        else:
            return "# TODO: Add Makefile targets\n"
    
    def _generate_test_file(self, filepath: str, proj_type: str) -> str:
        """Generate test file template."""
        if "python" in proj_type:
            return '''"""Test module."""
import pytest

def test_example():
    """Example test case."""
    assert True

# Add more tests here
'''
        elif "javascript" in proj_type:
            return '''describe('Example Test Suite', () => {
  test('should pass', () => {
    expect(true).toBe(true);
  });
});
'''
        else:
            return "// TODO: Add tests\n"
    
    def _get_setup_instructions(self, proj_type: str, proj_name: str) -> str:
        """Get setup instructions for project type."""
        if "python" in proj_type:
            return f"""Setup Instructions:

1. Create virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Configure environment:
   cp .env.example .env
   # Edit .env with your settings

4. Run the application:
   python src/main.py

5. Run tests:
   pytest
"""
        elif "javascript" in proj_type:
            return f"""Setup Instructions:

1. Install dependencies:
   npm install

2. Configure environment:
   cp .env.example .env
   # Edit .env with your settings

3. Run development server:
   npm run dev

4. Build for production:
   npm run build

5. Run tests:
   npm test
"""
        elif "rust" in proj_type:
            return f"""Setup Instructions:

1. Build the project:
   cargo build

2. Run the application:
   cargo run

3. Run tests:
   cargo test

4. Build release version:
   cargo build --release
"""
        elif "go" in proj_type:
            return f"""Setup Instructions:

1. Download dependencies:
   go mod download

2. Run the application:
   go run cmd/api/main.go

3. Run tests:
   go test ./...

4. Build binary:
   go build -o bin/{proj_name} cmd/api/main.go
"""
        else:
            return "Setup instructions will be provided based on project type."
    
    def list_available_templates(self) -> Dict:
        """List all available project templates."""
        return {
            "templates": [
                {"id": key, "name": val["name"]} 
                for key, val in self.PROJECT_TEMPLATES.items()
            ]
        }