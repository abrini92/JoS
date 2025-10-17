#!/bin/bash
# JarvisOS - One-Line Installer
# curl -sSL https://raw.githubusercontent.com/abrini92/JoS/main/install.sh | bash

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Error handler
error_exit() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
    echo ""
    echo "Installation failed. Check errors above."
    echo "For help, visit: https://github.com/abrini92/JoS/issues"
    exit 1
}

# Success handler
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Warning handler
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "🤖 JarvisOS Installer - FOUNDER MODE"
echo "====================================="
echo ""

# Check if running on Ubuntu/Debian
if [ ! -f /etc/debian_version ]; then
    error_exit "This installer only works on Ubuntu/Debian. Your OS: $(uname -s)"
fi

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    error_exit "Don't run as root! Run as regular user. Sudo will be used when needed."
fi

# Check internet connection
if ! ping -c 1 google.com &> /dev/null; then
    error_exit "No internet connection. Please connect and try again."
fi

# Check available disk space (need at least 5GB)
AVAILABLE=$(df -BG ~ | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$AVAILABLE" -lt 5 ]; then
    error_exit "Not enough disk space. Need 5GB, have ${AVAILABLE}GB"
fi

echo "📦 Installing dependencies..."
if ! sudo apt-get update -qq; then
    error_exit "apt-get update failed. Check your internet connection."
fi

if ! sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    portaudio19-dev \
    python3-pyaudio \
    plymouth \
    plymouth-themes \
    espeak \
    espeak-ng \
    alsa-utils 2>&1 | tee /tmp/jarvisos-apt-install.log; then
    error_exit "Failed to install dependencies. See /tmp/jarvisos-apt-install.log"
fi

success "Dependencies installed"

echo "📥 Cloning JarvisOS..."
cd ~ || error_exit "Cannot access home directory"

if [ -d "JoS" ]; then
    warning "JoS directory already exists"
    cd JoS || error_exit "Cannot access JoS directory"
    
    if ! git pull; then
        warning "Git pull failed, continuing with existing code"
    fi
else
    if ! git clone https://github.com/abrini92/JoS.git; then
        error_exit "Failed to clone repository. Check internet connection."
    fi
    cd JoS || error_exit "Cannot access JoS directory"
fi

success "Repository ready"

echo "🔧 Setting up Python environment..."
if ! python3 -m venv venv; then
    error_exit "Failed to create virtual environment"
fi

if ! source venv/bin/activate; then
    error_exit "Failed to activate virtual environment"
fi

if ! pip install -q --upgrade pip; then
    error_exit "Failed to upgrade pip"
fi

echo "   Installing Python packages (this may take a minute)..."
if ! pip install -q -r requirements.txt 2>&1 | tee /tmp/jarvisos-pip-install.log; then
    error_exit "Failed to install Python packages. See /tmp/jarvisos-pip-install.log"
fi

success "Python environment ready"

echo "🎙️  Installing Piper TTS (Better voice quality)..."
PIPER_DIR="$HOME/.local/bin"
mkdir -p "$PIPER_DIR"

if ! command -v piper &> /dev/null; then
    echo "   Downloading Piper TTS..."
    
    # Detect architecture
    ARCH=$(uname -m)
    if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
        PIPER_URL="https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_aarch64.tar.gz"
    else
        PIPER_URL="https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz"
    fi
    
    if curl -L "$PIPER_URL" | tar -xzf - -C "$PIPER_DIR" --strip-components=1; then
        # Add to PATH if not already there
        if ! grep -q "$PIPER_DIR" ~/.bashrc; then
            echo "export PATH=\"\$PATH:$PIPER_DIR\"" >> ~/.bashrc
        fi
        export PATH="$PATH:$PIPER_DIR"
        success "Piper TTS installed"
    else
        warning "Piper TTS install failed (will use pyttsx3 fallback)"
    fi
else
    success "Piper TTS already installed"
fi

echo "🤖 Installing Ollama (Local AI)..."
if ! command -v ollama &> /dev/null; then
    echo "   Installing Ollama..."
    if ! curl -fsSL https://ollama.com/install.sh | sh; then
        error_exit "Failed to install Ollama"
    fi
    
    # Start Ollama service
    sudo systemctl enable ollama 2>/dev/null || true
    sudo systemctl start ollama 2>/dev/null || true
    
    success "Ollama installed"
else
    success "Ollama already installed"
fi

# Ensure Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "   Starting Ollama service..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
fi

# Verify Ollama is responsive
if ! ollama list > /dev/null 2>&1; then
    warning "Ollama not responding, trying to start..."
    killall ollama 2>/dev/null || true
    sleep 1
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
fi

echo "📥 Downloading AI model (llama3.2 - 2GB)..."
echo "   This may take 5-10 minutes depending on your connection..."
if timeout 600 ollama pull llama3.2; then
    success "AI model ready (llama3.2)"
else
    warning "AI model download failed or timed out"
    warning "JarvisOS will work but AI features limited"
    warning "Run manually later: ollama pull llama3.2"
fi

echo "🎨 Setting up boot experience..."
if [ -f setup-boot-experience.sh ]; then
    chmod +x setup-boot-experience.sh
    if ! ./setup-boot-experience.sh 2>&1 | tee /tmp/jarvisos-boot-setup.log; then
        warning "Boot experience setup had issues. See /tmp/jarvisos-boot-setup.log"
        warning "Core JarvisOS still works, just no fancy boot screen"
    else
        success "Boot experience configured"
    fi
else
    warning "setup-boot-experience.sh not found, skipping boot setup"
fi

echo "⚙️  Creating jarvis command..."
if ! sudo tee /usr/local/bin/jarvis > /dev/null << 'EOF'
#!/bin/bash
# JarvisOS wrapper command
if [ ! -d ~/JoS ]; then
    echo "❌ JarvisOS not found in ~/JoS"
    exit 1
fi

cd ~/JoS || exit 1

if [ ! -d venv ]; then
    echo "❌ Virtual environment not found"
    echo "   Run: cd ~/JoS && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

source venv/bin/activate || exit 1
python jarvis.py "$@"
EOF
then
    error_exit "Failed to create jarvis command"
fi

if ! sudo chmod +x /usr/local/bin/jarvis; then
    error_exit "Failed to make jarvis command executable"
fi

success "jarvis command created"

# Final verification
echo ""
echo "🧪 Running final checks..."

# Check Python
if ! ~/JoS/venv/bin/python3 --version > /dev/null 2>&1; then
    error_exit "Python environment broken"
fi

# Check jarvis command
if ! which jarvis > /dev/null 2>&1; then
    error_exit "jarvis command not in PATH"
fi

# Check Ollama
if ! command -v ollama > /dev/null 2>&1; then
    warning "Ollama not found in PATH"
fi

success "All checks passed"

echo ""
echo "======================================"
echo "✅ JARVISOS SUCCESSFULLY INSTALLED!"
echo "======================================"
echo ""
echo "🎬 What to do next:"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Option 1: Quick test (RECOMMENDED)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   jarvis onboard"
echo "   → Interactive setup with Jarvis"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Option 2: Full experience"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   sudo reboot"
echo "   → See Arc Reactor boot screen"
echo "   → Jarvis welcomes you at boot"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Quick commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   jarvis status    - Check system"
echo "   jarvis predict   - AI predictions"
echo "   jarvis plan      - Plan your work"
echo "   jarvis --help    - All commands"
echo ""
echo "📚 Docs: ~/JoS/README.md"
echo "🐛 Issues: github.com/abrini92/JoS/issues"
echo ""
echo "🔥 Enjoy JarvisOS!"
echo ""

# Save installation info
cat > ~/.jarvisos-install-info << INFEOF
Installation completed: $(date)
Version: 0.1.0
Ollama: $(command -v ollama && echo "installed" || echo "not found")
Piper TTS: $(command -v piper && echo "installed" || echo "not found")
Models: $(ollama list 2>/dev/null | grep -c llama3.2 || echo 0) installed
Logs:
- APT: /tmp/jarvisos-apt-install.log
- PIP: /tmp/jarvisos-pip-install.log
- Boot: /tmp/jarvisos-boot-setup.log
- Ollama: /tmp/ollama.log

Voice Quality:
$(command -v piper &> /dev/null && echo "✅ Using Piper TTS (neural, high quality)" || echo "⚠️  Using pyttsx3 (basic quality)")
INFEOF

success "Installation info saved to ~/.jarvisos-install-info"
