#!/bin/bash
# JarvisOS - Setup Boot Experience
# Configures Plymouth boot screen and first-boot onboarding

set -e

echo "🎨 Setting up JarvisOS Boot Experience"
echo "========================================"
echo ""

# Install Plymouth
echo "📦 Installing Plymouth..."
sudo apt-get update -qq
sudo apt-get install -y plymouth plymouth-themes

# Create JarvisOS Plymouth theme
echo "🎨 Creating JarvisOS boot theme..."

THEME_DIR="/usr/share/plymouth/themes/jarvisos"
sudo mkdir -p "$THEME_DIR"

# Create theme files
sudo tee "$THEME_DIR/jarvisos.plymouth" > /dev/null << 'EOF'
[Plymouth Theme]
Name=JarvisOS
Description=JarvisOS Arc Reactor Boot Theme
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/jarvisos
ScriptFile=/usr/share/plymouth/themes/jarvisos/jarvisos.script
EOF

# Create boot animation script
sudo tee "$THEME_DIR/jarvisos.script" > /dev/null << 'EOF'
# JarvisOS Plymouth Boot Animation
# Arc Reactor Blue Theme

Window.SetBackgroundTopColor(0.04, 0.05, 0.10);     # #0A0E1A
Window.SetBackgroundBottomColor(0.04, 0.05, 0.10);

# Logo (you can replace with actual image later)
message_sprite = Sprite();
message_sprite.SetPosition(Window.GetX() + Window.GetWidth() / 2 - 100,
                          Window.GetY() + Window.GetHeight() / 2 - 50,
                          10000);

# Loading text
text = "Initializing JarvisOS...";
text_sprite = Sprite();
text_sprite.SetPosition(Window.GetX() + Window.GetWidth() / 2 - 80,
                       Window.GetY() + Window.GetHeight() / 2 + 50,
                       10000);

# Progress bar
progress_box.image = Image.Text(text, 0, 0.8, 1);  # Cyan color
progress_box.sprite = Sprite(progress_box.image);
progress_box.sprite.SetPosition(Window.GetX() + Window.GetWidth() / 2 - 100,
                               Window.GetY() + Window.GetHeight() / 2 + 80,
                               10000);

# Animation loop
fun refresh_callback() {
    # Pulse effect for Arc Reactor feel
    progress_box.sprite.SetOpacity(Math.Sin(Plymouth.GetTime()) * 0.5 + 0.5);
}

Plymouth.SetRefreshFunction(refresh_callback);

# Boot progress
fun boot_progress_callback(duration, progress) {
    if (progress >= 0.9)
        text = "JarvisOS Online...";
    else if (progress >= 0.7)
        text = "Loading AI Brain...";
    else if (progress >= 0.5)
        text = "Initializing Predictive Engine...";
    else if (progress >= 0.3)
        text = "Starting System...";
    else
        text = "Booting JarvisOS...";
    
    progress_box.image = Image.Text(text, 0, 0.8, 1);
    progress_box.sprite.SetImage(progress_box.image);
}

Plymouth.SetBootProgressFunction(boot_progress_callback);
EOF

# Install theme
echo "⚙️  Installing theme..."
sudo update-alternatives --install \
    /usr/share/plymouth/themes/default.plymouth \
    default.plymouth \
    "$THEME_DIR/jarvisos.plymouth" \
    100

sudo update-alternatives --set default.plymouth "$THEME_DIR/jarvisos.plymouth"
sudo update-initramfs -u

# Create first-boot service
echo "🤖 Creating first-boot onboarding service..."

sudo tee /etc/systemd/system/jarvisos-onboarding.service > /dev/null << EOF
[Unit]
Description=JarvisOS Interactive Onboarding
After=graphical.target
ConditionPathExists=!/home/$USER/.jarvisos/profile.json

[Service]
Type=oneshot
User=$USER
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/$USER/.Xauthority
ExecStart=/usr/bin/python3 $(pwd)/jarvisos/onboarding/interactive_welcome.py
StandardInput=tty
StandardOutput=journal+console
StandardError=journal+console
TTYPath=/dev/tty1
TTYReset=yes
TTYVHangup=yes

[Install]
WantedBy=graphical.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable jarvisos-onboarding.service

# Create desktop entry for manual launch
echo "🖥️  Creating desktop launcher..."
mkdir -p ~/.local/share/applications

cat > ~/.local/share/applications/jarvisos-onboard.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=JarvisOS Setup
Comment=Interactive JarvisOS onboarding
Exec=python3 $(pwd)/jarvisos/onboarding/interactive_welcome.py
Icon=applications-system
Terminal=true
Categories=System;Settings;
EOF

echo ""
echo "✅ Boot Experience Setup Complete!"
echo "======================================"
echo ""
echo "🎨 Plymouth Theme: JarvisOS Arc Reactor Blue"
echo "🤖 First-Boot: Interactive onboarding enabled"
echo ""
echo "📝 Next steps:"
echo "1. Reboot to see boot animation"
echo "2. First boot will run interactive onboarding"
echo "3. Jarvis will introduce himself and learn about you"
echo ""
echo "🧪 Test onboarding now:"
echo "   python3 jarvisos/onboarding/interactive_welcome.py --force"
echo ""
echo "🔥 READY!"
