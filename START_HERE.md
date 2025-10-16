# 👋 Welcome to JarvisOS!

**The First Self-Building Operating System**

You're looking at a complete, functional AI-powered OS that builds itself around you.

## 🎯 What Is This?

JarvisOS observes your behavior, learns your patterns, and automatically generates custom automation scripts. It's an operating system that evolves.

## ⚡ Quick Start (5 Minutes)

### 1. Setup

```bash
# Run the setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Set your Claude API key
export ANTHROPIC_API_KEY='your-key-here'
```

Get your free API key: https://console.anthropic.com/

### 2. Run Your First Automation

```bash
# Observe your system (30 seconds)
python jarvis.py observe --duration 30 --interval 5

# Analyze with AI
python jarvis.py analyze

# Generate automation script
python jarvis.py generate

# Execute it
python jarvis.py run 1 --dry-run  # Preview first
python jarvis.py run 1            # Then execute
```

**That's it!** You just created your first personalized automation.

## 📚 Documentation Guide

Choose your path:

### 🚀 **I want to use JarvisOS**
→ Read [QUICKSTART.md](QUICKSTART.md) - 5-minute guide
→ Then [README.md](README.md) - Full user guide

### 💻 **I want to contribute code**
→ Read [DEVELOPMENT.md](DEVELOPMENT.md) - Developer guide
→ Then [TESTING.md](TESTING.md) - Testing procedures

### 🎨 **I want to understand the vision**
→ Read [docs/VISION.md](docs/VISION.md) - Philosophy & roadmap

### 📊 **I want to see what was built**
→ Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Day 1 achievements

### 🎯 **I want to know what's next**
→ Read [NEXT_STEPS.md](NEXT_STEPS.md) - Roadmap & actions

## 🛠️ Project Structure

```
JoS/
├── jarvisos/core/          # Core modules
│   ├── observer.py         # Monitors behavior
│   ├── analyzer.py         # AI analysis
│   ├── generator.py        # Code generation
│   └── executor.py         # Safe execution
│
├── jarvis.py               # Main CLI
├── requirements.txt        # Dependencies
├── setup.sh               # Setup script
│
├── README.md              # Main docs
├── QUICKSTART.md          # 5-min guide
├── DEVELOPMENT.md         # Dev guide
├── VISION.md              # Philosophy
└── TESTING.md             # Tests
```

## 🎮 Available Commands

```bash
python jarvis.py observe    # Monitor behavior
python jarvis.py analyze    # AI analysis
python jarvis.py generate   # Create scripts
python jarvis.py list       # Show scripts
python jarvis.py run <id>   # Execute script
python jarvis.py status     # System status
```

## 🔥 What Makes This Special?

1. **Self-Building**: Writes code for you automatically
2. **AI-Powered**: Uses Claude to understand patterns
3. **Privacy-First**: All data stays local
4. **Open Source**: MIT licensed, fully transparent
5. **Beautiful UX**: Rich terminal interface
6. **Safe**: User approval required for execution

## 🎯 Use Cases

- **Developers**: Auto-setup environments, smart backups
- **Creators**: File organization, render management
- **Power Users**: System maintenance, custom workflows
- **Everyone**: Download cleanup, personalized automation

## 🚨 Prerequisites

- Python 3.11+
- Claude API key (free tier available)
- macOS or Linux (Ubuntu recommended)

## 💡 Example Workflow

```bash
# Morning: Start observation while you work
python jarvis.py observe --duration 3600

# Evening: Analyze and generate
python jarvis.py analyze
python jarvis.py generate

# Night: Review and execute
python jarvis.py list
python jarvis.py run 1
```

## 🤝 Get Involved

- **Star on GitHub**: Show your support
- **Report Issues**: Help us improve
- **Contribute Code**: Add features
- **Share**: Tell others about it

## 📖 Learn More

- **Full Documentation**: [README.md](README.md)
- **Vision & Philosophy**: [docs/VISION.md](docs/VISION.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Developer Guide**: [DEVELOPMENT.md](DEVELOPMENT.md)

## 🎉 Ready?

```bash
# Install
./setup.sh

# Configure
export ANTHROPIC_API_KEY='your-key'

# Run
python jarvis.py status
python jarvis.py observe
```

---

**Questions?** Check the docs or open an issue.

**Let's build an OS that builds itself.** 🤖

---

Built with ❤️ and AI | MIT License | Open Source
