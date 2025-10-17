#!/bin/bash
# JarvisOS - Create Bootable System (No ISO rebuild needed)
# Approach: Install on any Ubuntu, then create backup image

set -e

echo "🚀 JarvisOS Bootable System Creator"
echo "====================================="
echo ""
echo "This will:"
echo "1. Install JarvisOS on current system"
echo "2. Create a system image"
echo "3. Make it bootable on any machine"
echo ""

# Install JarvisOS
echo "🤖 Installing JarvisOS..."
cd /home/ubuntu
if [ ! -d "JoS" ]; then
    git clone https://github.com/abrini92/JoS.git
fi

cd JoS
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt

# Create system service
echo "⚙️  Creating system service..."
sudo tee /etc/systemd/system/jarvisos.service > /dev/null << EOF
[Unit]
Description=JarvisOS Background Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/JoS
ExecStart=/home/$USER/JoS/venv/bin/python jarvis.py status
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable jarvisos

# Configure desktop
echo "🎨 Configuring desktop..."
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/jarvisos.desktop << EOF
[Desktop Entry]
Type=Application
Name=JarvisOS
Exec=/home/$USER/JoS/jarvis.py status
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF

# Create backup script
echo "💾 Creating backup image..."
cat > ~/create-jarvisos-image.sh << 'BACKUP'
#!/bin/bash
# Creates a deployable JarvisOS image

echo "Creating JarvisOS deployment image..."
cd ~
tar czf jarvisos-system-$(date +%Y%m%d).tar.gz \
    JoS/ \
    .config/autostart/jarvisos.desktop \
    --exclude='JoS/venv' \
    --exclude='JoS/__pycache__' \
    --exclude='JoS/.git'

echo "✅ Image created: ~/jarvisos-system-$(date +%Y%m%d).tar.gz"
echo ""
echo "To deploy on another machine:"
echo "1. Install Ubuntu 22.04"
echo "2. Copy this tarball"
echo "3. Extract: tar xzf jarvisos-system-*.tar.gz -C ~"
echo "4. Run: cd ~/JoS && ./setup.sh"
BACKUP

chmod +x ~/create-jarvisos-image.sh

echo ""
echo "✅ JarvisOS INSTALLED!"
echo "======================================"
echo "🎯 System is now JarvisOS-ready!"
echo ""
echo "📦 To create deployable image:"
echo "   ~/create-jarvisos-image.sh"
echo ""
echo "🔥 READY TO USE!"
