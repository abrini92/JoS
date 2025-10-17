#!/bin/bash
#
# JarvisOS Desktop Environment Installer
# Installs a minimal desktop with JarvisOS integration
#

set -e

echo "🖥️  JarvisOS Desktop Installer"
echo "=============================="
echo ""

# Check if root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo"
    exit 1
fi

echo "📦 Installing desktop environment..."
echo "This will take 5-10 minutes..."
echo ""

# Update system
apt-get update -qq

# Install minimal desktop (XFCE - lightweight)
echo "Installing XFCE desktop..."
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    xfce4 \
    xfce4-terminal \
    lightdm \
    firefox \
    dbus-x11

# Install VNC server for remote access
echo "Installing VNC server..."
apt-get install -y -qq \
    tightvncserver \
    xrdp

# Configure VNC
echo "Configuring VNC..."
mkdir -p /root/.vnc
echo "jarvisos" | vncpasswd -f > /root/.vnc/passwd
chmod 600 /root/.vnc/passwd

# Create VNC startup script
cat > /root/.vnc/xstartup << 'EOF'
#!/bin/bash
xrdb $HOME/.Xresources
startxfce4 &
EOF

chmod +x /root/.vnc/xstartup

# Enable services
systemctl enable lightdm
systemctl enable xrdp

# Create JarvisOS desktop shortcut
mkdir -p /root/Desktop

cat > /root/Desktop/jarvisos.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=JarvisOS Terminal
Comment=JarvisOS Command Center
Exec=xfce4-terminal --working-directory=/opt/jarvisos --command="bash -c 'source venv/bin/activate && bash'"
Icon=utilities-terminal
Terminal=false
Categories=System;
EOF

chmod +x /root/Desktop/jarvisos.desktop

# Create JarvisOS status widget
cat > /root/Desktop/jarvisos-status.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=JarvisOS Status
Comment=View JarvisOS Status
Exec=xfce4-terminal --command="bash -c 'cd /opt/jarvisos && source venv/bin/activate && python jarvis.py status && read'"
Icon=system-monitoring
Terminal=false
Categories=System;
EOF

chmod +x /root/Desktop/jarvisos-status.desktop

# Set wallpaper (create simple JarvisOS wallpaper)
mkdir -p /usr/share/backgrounds

cat > /usr/share/backgrounds/jarvisos.svg << 'EOF'
<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#grad)"/>
  <text x="960" y="500" font-family="monospace" font-size="72" fill="white" text-anchor="middle" font-weight="bold">
    JARVISOS
  </text>
  <text x="960" y="580" font-family="monospace" font-size="24" fill="white" text-anchor="middle" opacity="0.8">
    The First Self-Building Operating System
  </text>
</svg>
EOF

echo ""
echo "✅ Desktop environment installed!"
echo ""
echo "🚀 Starting desktop..."

# Start VNC server
su - root -c "vncserver :1 -geometry 1920x1080 -depth 24" || true

# Start xrdp
systemctl start xrdp

echo ""
echo "✅ Desktop is running!"
echo ""
echo "📺 Access options:"
echo ""
echo "Option 1: VNC (Recommended)"
echo "  1. Install VNC Viewer on Mac: brew install --cask vnc-viewer"
echo "  2. Get VM IP: multipass info jarvisos | grep IPv4"
echo "  3. Connect to: <VM_IP>:5901"
echo "  4. Password: jarvisos"
echo ""
echo "Option 2: RDP"
echo "  1. Use Microsoft Remote Desktop"
echo "  2. Connect to: <VM_IP>:3389"
echo ""
echo "Option 3: Multipass GUI (if available)"
echo "  multipass shell jarvisos"
echo "  export DISPLAY=:1"
echo "  startxfce4"
echo ""
