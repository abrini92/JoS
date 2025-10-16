#!/bin/bash
#
# JarvisOS System Installation Script
# Installs JarvisOS as a system-level service
#
# Usage: sudo ./install-system.sh
#

set -e

echo "🚀 JarvisOS System Installation"
echo "================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (sudo ./install-system.sh)"
    exit 1
fi

# Variables
INSTALL_DIR="/opt/jarvisos"
SERVICE_DIR="/etc/systemd/system"
USER="jarvis"
GROUP="jarvis"

echo "📋 Installation Configuration:"
echo "  Install Directory: $INSTALL_DIR"
echo "  Service Directory: $SERVICE_DIR"
echo "  User: $USER"
echo "  Group: $GROUP"
echo ""

# Create jarvis user if doesn't exist
if ! id "$USER" &>/dev/null; then
    echo "👤 Creating jarvis user..."
    useradd -r -s /bin/bash -d $INSTALL_DIR -m $USER
    echo "✅ User created"
else
    echo "✅ User already exists"
fi

# Create installation directory
echo "📁 Creating installation directory..."
mkdir -p $INSTALL_DIR
cp -r . $INSTALL_DIR/
chown -R $USER:$GROUP $INSTALL_DIR
echo "✅ Files copied to $INSTALL_DIR"

# Setup Python virtual environment
echo "🐍 Setting up Python environment..."
cd $INSTALL_DIR
sudo -u $USER python3 -m venv venv
sudo -u $USER venv/bin/pip install --upgrade pip
sudo -u $USER venv/bin/pip install -r requirements.txt
echo "✅ Python environment ready"

# Create directories
echo "📂 Creating data directories..."
sudo -u $USER mkdir -p $INSTALL_DIR/data
sudo -u $USER mkdir -p $INSTALL_DIR/generated_scripts
sudo -u $USER mkdir -p $INSTALL_DIR/logs
echo "✅ Directories created"

# Install systemd services
echo "⚙️  Installing systemd services..."
cp system/*.service $SERVICE_DIR/
cp system/*.timer $SERVICE_DIR/
systemctl daemon-reload
echo "✅ Services installed"

# Configure API key
echo ""
echo "🔑 API Key Configuration"
echo "========================"
echo ""
echo "Please enter your Anthropic API key:"
read -p "API Key: " API_KEY

# Update service files with API key
for service in $SERVICE_DIR/jarvisos-*.service; do
    sed -i "s/your_key_here/$API_KEY/g" "$service"
done
echo "✅ API key configured"

# Enable services
echo ""
echo "🔄 Enabling services..."
systemctl enable jarvisos-observer.service
systemctl enable jarvisos-nightly.timer
echo "✅ Services enabled"

# Start services
echo ""
echo "▶️  Starting services..."
systemctl start jarvisos-observer.service
systemctl start jarvisos-nightly.timer
echo "✅ Services started"

# Show status
echo ""
echo "📊 Service Status:"
echo "=================="
systemctl status jarvisos-observer.service --no-pager -l
echo ""
systemctl list-timers jarvisos-* --no-pager

echo ""
echo "✅ JarvisOS Installation Complete!"
echo ""
echo "📝 Next Steps:"
echo "  1. Check logs: journalctl -u jarvisos-observer -f"
echo "  2. View status: systemctl status jarvisos-observer"
echo "  3. Check data: ls -la $INSTALL_DIR/data/"
echo ""
echo "🌙 JarvisOS will now:"
echo "  • Observe continuously in background"
echo "  • Analyze patterns every 6 hours"
echo "  • Generate new code every night at 3 AM"
echo "  • Evolve automatically"
echo ""
echo "🎉 Your OS is now self-building!"
