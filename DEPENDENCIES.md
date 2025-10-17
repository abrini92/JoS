# 📦 JarvisOS Dependencies

**Complete list of all dependencies**

---

## 🐍 Python Dependencies (pip)

**From requirements.txt:**
```
anthropic>=0.18.0          # Claude API (optional)
psutil>=5.9.0              # System monitoring
rich>=13.7.0               # Terminal UI
fastapi>=0.109.0           # API services
uvicorn>=0.27.0            # ASGI server
pydantic>=2.5.0            # Data validation
sqlalchemy>=2.0.25         # Database ORM
aiosqlite>=0.19.0          # Async SQLite
python-dotenv>=1.0.0       # Environment variables
watchdog>=3.0.0            # File system monitoring
schedule>=1.2.0            # Task scheduling
pyttsx3>=2.90              # Text-to-Speech
SpeechRecognition>=3.10.0  # Speech-to-Text
PyAudio>=0.2.13            # Audio I/O
pytest>=7.4.0              # Testing
black>=24.1.0              # Code formatting
ruff>=0.1.0                # Linting
```

**Install:**
```bash
pip install -r requirements.txt
```

---

## 💻 System Dependencies (apt)

**Required packages:**
```bash
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    portaudio19-dev \
    python3-pyaudio \
    espeak \
    espeak-ng \
    alsa-utils \
    plymouth \
    plymouth-themes
```

**Breakdown:**

### Core
- `python3` - Python runtime (3.10+)
- `python3-pip` - Package manager
- `python3-venv` - Virtual environments
- `git` - Version control
- `curl` - Download tool

### Audio (Voice features)
- `portaudio19-dev` - Audio I/O library
- `python3-pyaudio` - Python audio bindings
- `espeak` - Text-to-speech engine
- `espeak-ng` - Next-gen TTS engine
- `alsa-utils` - Audio system utilities

### Boot Experience
- `plymouth` - Boot splash screen
- `plymouth-themes` - Boot themes

---

## 🤖 External Tools

### Ollama (Local AI)

**Install:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Models needed:**
```bash
ollama pull llama3.2  # 2GB - Recommended
```

**Optional models:**
```bash
ollama pull phi3       # 2.3GB - Faster
ollama pull mistral    # 4GB - Better quality
ollama pull codellama  # 4GB - Code focus
```

**Service:**
```bash
# Enable at boot
sudo systemctl enable ollama

# Start now
sudo systemctl start ollama

# Check status
systemctl status ollama
```

---

## 🖥️ UTM/VM Requirements

**For testing in VM:**

### VM Specs (Minimum)
- RAM: 4GB
- Storage: 20GB
- CPU: 2 cores

### VM Specs (Recommended)
- RAM: 6GB
- Storage: 30GB
- CPU: 4 cores

### Host Requirements
- Mac: Apple Silicon or Intel
- UTM installed
- 10GB free space for ISO + VM

---

## 🔧 Optional Dependencies

### For Development
```bash
# Code quality
pip install black ruff mypy

# Testing
pip install pytest pytest-asyncio pytest-cov

# Documentation
pip install mkdocs mkdocs-material
```

### For Advanced Features
```bash
# Better speech recognition
pip install openai-whisper

# GPU acceleration (if available)
pip install torch torchvision
```

---

## 📊 Dependency Check

**Run this to check all dependencies:**

```bash
cd /path/to/JoS
chmod +x validate_before_ship.sh
./validate_before_ship.sh
```

**Or test specific components:**

```bash
# Test Python modules
python3 test_now.py

# Test Ollama
ollama --version
ollama list

# Test audio
espeak "Hello from Jarvis"

# Test plymouth
sudo plymouthd --debug
```

---

## 🐛 Troubleshooting

### Python module not found
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

### Ollama not working
```bash
# Check installation
which ollama

# Reinstall
curl -fsSL https://ollama.com/install.sh | sh

# Start service
ollama serve &
```

### Audio/TTS not working
```bash
# Install espeak
sudo apt-get install espeak espeak-ng

# Test
espeak "Test"

# Check audio devices
aplay -l
```

### Plymouth not showing
```bash
# Install
sudo apt-get install plymouth plymouth-themes

# Update initramfs
sudo update-initramfs -u

# Reboot
sudo reboot
```

---

## 📝 Installation Order

**Correct order matters!**

1. **System packages** (apt-get)
2. **Python venv** (python3 -m venv)
3. **Python packages** (pip install)
4. **Ollama** (curl install)
5. **Ollama models** (ollama pull)
6. **Boot setup** (setup-boot-experience.sh)

**The install.sh does this automatically!**

---

## 💾 Disk Space Requirements

| Component | Size |
|-----------|------|
| Ubuntu base | ~5GB |
| JarvisOS code | ~50MB |
| Python deps | ~500MB |
| Ollama binary | ~100MB |
| llama3.2 model | ~2GB |
| System packages | ~200MB |
| **Total** | **~8GB** |

**Recommended:** 20GB disk space

---

## 🚀 Quick Install

**Everything at once (recommended):**

```bash
curl -sSL https://raw.githubusercontent.com/abrini92/JoS/main/install.sh | bash
```

**This installs ALL dependencies automatically!**

---

## ✅ Verification

**After installation, verify:**

```bash
# JarvisOS command
jarvis --help

# Ollama
ollama list

# Python
python3 --version

# TTS
espeak "Test"

# Full test
cd ~/JoS
python3 test_now.py
```

---

**All dependencies handled by install.sh!** 🎉
