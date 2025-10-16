# 🛠️ JarvisOS Development Guide

Guide for developers working on JarvisOS.

## Project Structure

```
JoS/
├── jarvisos/                  # Main package
│   ├── __init__.py
│   └── core/                  # Core modules
│       ├── __init__.py
│       ├── observer.py        # System observation
│       ├── analyzer.py        # AI analysis
│       ├── generator.py       # Code generation
│       └── executor.py        # Script execution
│
├── data/                      # Generated data (gitignored)
│   ├── observations.json
│   ├── insights.json
│   └── generated_tasks.json
│
├── generated_scripts/         # Auto-generated scripts (gitignored)
│   └── *.py
│
├── docs/                      # Documentation
│   └── VISION.md
│
├── jarvis.py                  # Main CLI entry point
├── requirements.txt           # Python dependencies
├── setup.sh                   # Setup script
├── README.md                  # Main documentation
├── QUICKSTART.md             # Quick start guide
├── LICENSE                    # MIT License
├── .env.example              # Environment template
└── .gitignore                # Git ignore rules
```

## Core Modules

### observer.py
**Purpose**: Monitor user behavior and system activity

**Key Classes**:
- `Observer`: Main observation class

**Key Methods**:
- `observe(duration, interval)`: Run observation loop
- `get_running_apps()`: Get current applications
- `get_system_stats()`: Get CPU, memory, disk stats
- `save_observations()`: Save to JSON

**Output**: `data/observations.json`

### analyzer.py
**Purpose**: Analyze observations using Claude AI

**Key Classes**:
- `Analyzer`: AI-powered analysis

**Key Methods**:
- `analyze()`: Main analysis workflow
- `load_observations()`: Load observation data
- `preprocess_observations()`: Prepare data for AI
- `analyze_with_claude()`: Call Claude API
- `display_insights()`: Beautiful console output

**Input**: `data/observations.json`
**Output**: `data/insights.json`

### generator.py
**Purpose**: Generate automation scripts

**Key Classes**:
- `Generator`: Code generation engine

**Key Methods**:
- `generate(task_index)`: Main generation workflow
- `suggest_tasks()`: Ask Claude for task ideas
- `generate_script()`: Generate Python code
- `validate_syntax()`: AST validation
- `save_script()`: Save to file

**Input**: `data/insights.json`
**Output**: `generated_scripts/*.py`

### executor.py
**Purpose**: Safely execute generated scripts

**Key Classes**:
- `Executor`: Safe script execution

**Key Methods**:
- `run(script_id, dry_run, timeout)`: Execute script
- `list_scripts()`: Get available scripts
- `preview_script()`: Show code preview
- `execute_script()`: Run with subprocess

**Input**: `generated_scripts/*.py`
**Output**: Script execution results

## Development Workflow

### Setup Development Environment

```bash
# Clone repo
git clone https://github.com/yourusername/jarvisos.git
cd jarvisos

# Run setup
./setup.sh

# Activate venv
source venv/bin/activate

# Set API key
export ANTHROPIC_API_KEY='your-key'
```

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov black ruff

# Run tests (when available)
pytest

# Check coverage
pytest --cov=jarvisos

# Format code
black .

# Lint
ruff check .
```

### Adding a New Feature

1. **Create feature branch**
```bash
git checkout -b feature/my-feature
```

2. **Write code**
```python
# Example: Add new analyzer method
class Analyzer:
    def analyze_time_patterns(self):
        """Analyze time-based patterns"""
        # Your code here
        pass
```

3. **Test locally**
```bash
python jarvis.py status
python jarvis.py observe --duration 30
python jarvis.py analyze
```

4. **Commit and push**
```bash
git add .
git commit -m "feat: add time pattern analysis"
git push origin feature/my-feature
```

5. **Open Pull Request**

### Code Style

- **Formatting**: Black (line length 100)
- **Linting**: Ruff
- **Docstrings**: Google style
- **Type hints**: Encouraged but not required
- **Imports**: Organized (stdlib, third-party, local)

### Example Code Style

```python
"""
Module docstring explaining purpose
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from anthropic import Anthropic
from rich.console import Console


class MyClass:
    """Class docstring
    
    Args:
        param1: Description
        param2: Description
    """
    
    def __init__(self, param1: str, param2: int = 10):
        self.param1 = param1
        self.param2 = param2
    
    def my_method(self, arg: str) -> Dict:
        """Method docstring
        
        Args:
            arg: Description
            
        Returns:
            Dict with results
            
        Raises:
            ValueError: When arg is invalid
        """
        if not arg:
            raise ValueError("arg cannot be empty")
        
        return {"result": arg}
```

## API Integration

### Claude API Usage

```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    messages=[
        {"role": "user", "content": "Your prompt here"}
    ]
)

response = message.content[0].text
```

### Best Practices

1. **Always use environment variables for API keys**
2. **Handle API errors gracefully**
3. **Add retry logic for transient failures**
4. **Cache responses when appropriate**
5. **Monitor token usage**

## Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
```

### Common Issues

**Issue**: "ANTHROPIC_API_KEY not found"
```bash
export ANTHROPIC_API_KEY='your-key'
```

**Issue**: "No module named 'jarvisos'"
```bash
# Make sure you're in the right directory
cd /path/to/JoS
python jarvis.py status
```

**Issue**: Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Performance Optimization

### Observer Performance
- Use `psutil` efficiently
- Don't observe too frequently (5-10s interval minimum)
- Filter out system processes early

### Analyzer Performance
- Batch API calls when possible
- Cache preprocessed data
- Use async for I/O operations

### Generator Performance
- Validate syntax before saving
- Cache generated code templates
- Reuse common patterns

## Security Considerations

### Script Execution Safety
1. **Always preview scripts** before execution
2. **Use subprocess with timeout**
3. **Sandbox execution** (future: Docker)
4. **Validate generated code** with AST
5. **User approval required**

### API Key Security
1. **Never commit .env files**
2. **Use environment variables**
3. **Rotate keys regularly**
4. **Monitor API usage**

### Data Privacy
1. **All data stored locally**
2. **No telemetry**
3. **User controls data deletion**
4. **Transparent data usage**

## Contributing Guidelines

### Before Submitting PR

- [ ] Code follows style guide
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented)
- [ ] Commits are clear and descriptive

### Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Examples**:
```
feat(analyzer): add time pattern detection
fix(observer): handle permission errors gracefully
docs(readme): update installation instructions
```

## Release Process

1. Update version in `jarvisos/__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v0.2.0`
4. Push tag: `git push origin v0.2.0`
5. Create GitHub release
6. Build and publish (future: PyPI)

## Future Roadmap

### Short Term (v0.2)
- [ ] Add tests
- [ ] Improve error handling
- [ ] Add logging system
- [ ] Performance optimizations

### Medium Term (v0.3)
- [ ] Web dashboard (FastAPI)
- [ ] Plugin system
- [ ] Scheduled execution
- [ ] Multi-user support

### Long Term (v1.0)
- [ ] Custom Ubuntu distribution
- [ ] Docker deployment
- [ ] Enterprise features
- [ ] Hardware optimization

## Resources

- [Anthropic API Docs](https://docs.anthropic.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Python Best Practices](https://docs.python-guide.org/)

## Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Questions and ideas
- **Discord**: Community chat (coming soon)
- **Email**: maintainer@jarvisos.dev (coming soon)

---

**Happy coding! 🚀**
