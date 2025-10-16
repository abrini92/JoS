# Contributing to JarvisOS

First off, thank you for considering contributing to JarvisOS! 🎉

It's people like you that make JarvisOS such a great tool.

## 🌟 Ways to Contribute

- 🐛 **Report bugs** - Help us identify and fix issues
- ✨ **Suggest features** - Share your ideas for improvements
- 📝 **Improve documentation** - Help others understand JarvisOS
- 💻 **Write code** - Implement new features or fix bugs
- 🧪 **Write tests** - Improve code quality and reliability
- 🎨 **Design** - Improve UI/UX
- 📢 **Spread the word** - Share JarvisOS with others

## 🚀 Getting Started

### 1. Fork & Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/jarvisos.git
cd jarvisos
```

### 2. Set Up Development Environment

```bash
# Run setup
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Set API key
export ANTHROPIC_API_KEY='your-key-here'

# Test installation
python test_installation.py
```

### 3. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/amazing-feature

# Or a bugfix branch
git checkout -b fix/bug-description
```

## 💻 Development Workflow

### Code Style

We follow Python best practices:

- **Formatting**: Black (line length 100)
- **Linting**: Ruff
- **Docstrings**: Google style
- **Type hints**: Encouraged

```bash
# Format code
black .

# Lint code
ruff check .

# Check syntax
make lint
```

### Writing Code

1. **Follow existing patterns** - Look at similar code
2. **Add docstrings** - Document your functions
3. **Handle errors** - Use try/except appropriately
4. **Use Rich** - For console output
5. **Test your changes** - Make sure it works

Example:

```python
def my_function(param: str) -> Dict:
    """Brief description of function
    
    Args:
        param: Description of parameter
        
    Returns:
        Dict with results
        
    Raises:
        ValueError: When param is invalid
    """
    if not param:
        raise ValueError("param cannot be empty")
    
    # Your code here
    return {"result": param}
```

### Testing

```bash
# Run installation test
python test_installation.py

# Test your changes manually
python jarvis.py status
python jarvis.py observe --duration 30
python jarvis.py analyze

# Check syntax
make lint
```

### Committing

We use conventional commits:

```bash
# Format: type(scope): description

# Types:
# feat: New feature
# fix: Bug fix
# docs: Documentation
# style: Formatting
# refactor: Code restructuring
# test: Tests
# chore: Maintenance

# Examples:
git commit -m "feat(analyzer): add time pattern detection"
git commit -m "fix(observer): handle permission errors"
git commit -m "docs(readme): update installation steps"
```

## 📝 Pull Request Process

### 1. Update Documentation

- Update README.md if needed
- Update CHANGELOG.md
- Add/update docstrings
- Update examples

### 2. Test Thoroughly

```bash
# Run all tests
make test

# Test manually
make demo
```

### 3. Push & Create PR

```bash
# Push your branch
git push origin feature/amazing-feature

# Create Pull Request on GitHub
# Fill out the PR template
# Link related issues
```

### 4. Code Review

- Address review comments
- Make requested changes
- Keep discussion respectful
- Be patient

### 5. Merge

Once approved, your PR will be merged! 🎉

## 🐛 Reporting Bugs

### Before Reporting

- Check existing issues
- Try latest version
- Read documentation
- Test with minimal setup

### Creating a Bug Report

Use the bug report template and include:

- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages
- Screenshots if applicable

## ✨ Suggesting Features

### Before Suggesting

- Check existing feature requests
- Make sure it aligns with project vision
- Consider if it benefits most users

### Creating a Feature Request

Use the feature request template and include:

- Clear description
- Use cases
- Example usage
- Why it's valuable
- Implementation ideas (optional)

## 📚 Documentation

Good documentation is crucial! Help us by:

- Fixing typos
- Clarifying confusing sections
- Adding examples
- Translating to other languages
- Creating tutorials/videos

## 🎨 Design Guidelines

### CLI Output

- Use Rich for formatting
- Color-code by importance:
  - Cyan: Info
  - Green: Success
  - Yellow: Warning
  - Red: Error
- Add emojis sparingly
- Keep it clean and readable

### Code Organization

```
jarvisos/
├── core/           # Core modules
│   ├── observer.py
│   ├── analyzer.py
│   ├── generator.py
│   └── executor.py
├── utils/          # Utilities (future)
├── plugins/        # Plugins (future)
└── web/            # Web interface (future)
```

## 🔒 Security

### Reporting Security Issues

**DO NOT** create public issues for security vulnerabilities.

Instead, email: security@jarvisos.dev (coming soon)

Or create a private security advisory on GitHub.

### Security Best Practices

- Never commit API keys
- Validate all user input
- Sanitize file paths
- Use subprocess safely
- Handle errors gracefully

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behavior:**
- Being respectful
- Accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy

**Unacceptable behavior:**
- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

### Enforcement

Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report issues to: conduct@jarvisos.dev (coming soon)

## 💬 Communication

### Where to Ask Questions

- **GitHub Discussions** - General questions
- **GitHub Issues** - Bug reports, feature requests
- **Discord** - Real-time chat (coming soon)
- **Twitter** - Updates and announcements

### Getting Help

- Read the documentation first
- Search existing issues/discussions
- Provide context and details
- Be patient and respectful

## 🎯 Priorities

### Current Focus (v0.1-0.2)

- Core stability
- Bug fixes
- Documentation
- Testing
- User feedback

### Future Focus (v0.3+)

- Web dashboard
- Plugin system
- Scheduled execution
- Multi-user support

## 🏆 Recognition

Contributors are recognized in:

- CHANGELOG.md
- README.md contributors section
- GitHub contributors page
- Release notes

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Every contribution, no matter how small, is valuable and appreciated.

Together, we're building the future of operating systems! 🚀

---

**Questions?** Open a discussion or reach out to the maintainers.

**Ready to contribute?** Pick an issue labeled `good first issue` and get started!
