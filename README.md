# 🤖 JarvisOS

**The First Self-Building Operating System**

JarvisOS is an AI-powered operating system that observes your behavior, learns your patterns, and automatically generates custom automation scripts tailored specifically for you. Every night, it evolves to better serve your needs.

## 🎯 Vision

Traditional operating systems are static. **JarvisOS is alive.**

- 👀 **Observes** your daily computer usage
- 🧠 **Analyzes** patterns with Claude AI
- ⚙️ **Generates** custom automation scripts
- 🚀 **Executes** safely with your approval
- 🌙 **Evolves** every night while you sleep

## ✨ Features

- **Behavior Observation**: Monitors running applications, system stats, and usage patterns
- **AI Analysis**: Uses Claude AI to identify automation opportunities
- **Code Generation**: Automatically writes Python scripts for your specific needs
- **Safe Execution**: Preview and approve all scripts before running
- **Privacy First**: All data stays local, no cloud storage
- **Open Source**: MIT licensed, fully transparent

## 🛠️ Tech Stack

- **Base**: Linux (Ubuntu)
- **Language**: Python 3.11+
- **AI**: Claude API (Anthropic)
- **API Framework**: FastAPI
- **Database**: SQLite
- **CLI**: Rich (beautiful terminal output)

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- Ubuntu/Linux (macOS for development)
- Claude API key ([get one here](https://console.anthropic.com/))

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/jarvisos.git
cd jarvisos

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Make CLI executable
chmod +x jarvis.py
```

## 🚀 Quick Start

### 1. Observe Your Behavior

```bash
python jarvis.py observe --duration 60 --interval 5
```

This will monitor your system for 60 seconds, collecting data every 5 seconds.

### 2. Analyze with AI

```bash
python jarvis.py analyze
```

Claude AI will analyze your behavior and suggest automation opportunities.

### 3. Generate Automation Scripts

```bash
python jarvis.py generate
```

JarvisOS will generate a custom Python script for your first automation task.

### 4. Review and Execute

```bash
# List available scripts
python jarvis.py list

# Preview script (dry run)
python jarvis.py run 1 --dry-run

# Execute script
python jarvis.py run 1
```

### 5. Check Status

```bash
python jarvis.py status
```

## 📖 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `observe` | Monitor user behavior | `jarvis.py observe --duration 120` |
| `analyze` | Analyze with Claude AI | `jarvis.py analyze` |
| `generate` | Generate automation scripts | `jarvis.py generate` |
| `list` | List available scripts | `jarvis.py list` |
| `run` | Execute a script | `jarvis.py run 1` |
| `status` | Show system status | `jarvis.py status` |

## 🏗️ Architecture

```
jarvisos/
├── core/
│   ├── observer.py    # Observes user behavior
│   ├── analyzer.py    # AI analysis with Claude
│   ├── generator.py   # Generates automation code
│   └── executor.py    # Executes scripts safely
├── data/              # Local data storage
│   ├── observations.json
│   └── insights.json
├── generated_scripts/ # Auto-generated scripts
├── docs/
│   └── VISION.md
├── jarvis.py          # Main CLI
└── requirements.txt
```

## 🔒 Privacy & Security

- **Local First**: All data stored locally on your machine
- **No Cloud Storage**: Observations never leave your computer
- **Transparent**: All generated code is visible and reviewable
- **User Approval**: Scripts require explicit approval before execution
- **Open Source**: Full code transparency (MIT License)

## 🎨 Example Workflow

```bash
# Day 1: Collect data
$ python jarvis.py observe --duration 300

# Analyze patterns
$ python jarvis.py analyze
🧠 JarvisOS AI Insights
📊 Usage Patterns:
  • Heavy browser usage (Chrome, Firefox)
  • Frequent terminal sessions
  • Code editor active 80% of time

🤖 Automation Opportunities:
  1. Auto-organize downloads folder
  2. Backup code projects daily
  3. Clean up temp files

# Generate automation
$ python jarvis.py generate
✨ Generated: auto_organize_downloads.py

# Execute
$ python jarvis.py run 1
✅ Script executed successfully!
```

## 🌟 Principles

1. **Freedom First**: No backdoors, no telemetry, no tracking
2. **Privacy by Default**: Your data is yours
3. **Open Source**: MIT licensed, fork-friendly
4. **User Control**: You approve everything
5. **Continuous Evolution**: Gets better every day

## 🛣️ Roadmap

- [x] Core observer implementation
- [x] Claude AI integration
- [x] Script generation
- [x] Safe execution engine
- [ ] Web dashboard (FastAPI)
- [ ] Scheduled nightly evolution
- [ ] Plugin system
- [ ] Multi-user support
- [ ] Docker deployment
- [ ] Custom OS distribution

## 🤝 Contributing

Contributions welcome! This is an open-source project.

```bash
# Fork the repo
# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes
# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Open a Pull Request
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com) for Claude AI
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- The open-source community

## 📧 Contact

- Twitter: [@yourusername](https://twitter.com/yourusername)
- GitHub: [@yourusername](https://github.com/yourusername)

---

**Built with ❤️ and AI**

*JarvisOS - Your computer, evolved.*
