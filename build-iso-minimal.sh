#!/bin/bash
# JarvisOS - MINIMAL ISO Builder (FOUNDER MODE)
# Goal: Boot. That's it.

set -e

echo "🔥 FOUNDER MODE - MINIMAL ISO BUILD"
echo "===================================="
echo ""

# Config
ISO_NAME="jarvisos-minimal-v0.1.0.iso"
BUILD_DIR="/tmp/jarvisos-build"
MOUNT_DIR="/tmp/iso-mount"

# Clean
echo "🧹 Cleaning previous builds..."
sudo rm -rf "$BUILD_DIR"
sudo rm -rf "$MOUNT_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$MOUNT_DIR"

# Download base Ubuntu
echo "📦 Downloading Ubuntu 22.04 LTS..."
cd "$BUILD_DIR"
if [ ! -f ubuntu-22.04.3-desktop-amd64.iso ]; then
    wget -q --show-progress https://releases.ubuntu.com/22.04/ubuntu-22.04.3-desktop-amd64.iso
fi

# Mount
echo "💿 Mounting ISO..."
sudo mount -o loop ubuntu-22.04.3-desktop-amd64.iso "$MOUNT_DIR"

# Copy
echo "📋 Copying files..."
sudo rsync -av "$MOUNT_DIR/" "$BUILD_DIR/iso/"
sudo umount "$MOUNT_DIR"

# Customize
echo "🎨 Minimal customization..."

# Add JarvisOS
sudo mkdir -p "$BUILD_DIR/iso/jarvisos"
sudo cp -r ../JoS/* "$BUILD_DIR/iso/jarvisos/" 2>/dev/null || true

# Create auto-install script
cat > "$BUILD_DIR/iso/jarvisos-install.sh" << 'EOF'
#!/bin/bash
echo "🤖 Installing JarvisOS..."
cd /opt/jarvisos
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
echo "✅ JarvisOS installed!"
EOF
chmod +x "$BUILD_DIR/iso/jarvisos-install.sh"

# Build ISO
echo "🔨 Building ISO..."
cd "$BUILD_DIR"
sudo genisoimage \
    -rational-rock \
    -volid "JarvisOS" \
    -cache-inodes \
    -joliet \
    -full-iso9660-filenames \
    -b isolinux/isolinux.bin \
    -c isolinux/boot.cat \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    -eltorito-alt-boot \
    -e boot/grub/efi.img \
    -no-emul-boot \
    -o "../$ISO_NAME" \
    iso/

# Make bootable
echo "🥾 Making bootable..."
cd ..
sudo isohybrid --uefi "$ISO_NAME" 2>/dev/null || true

# Done
echo ""
echo "✅ ISO BUILT!"
echo "📍 Location: $(pwd)/$ISO_NAME"
echo "📊 Size: $(du -h $ISO_NAME | cut -f1)"
echo ""
echo "🧪 Test with:"
echo "   multipass launch file://$(pwd)/$ISO_NAME --name jarvisos-test"
echo ""
echo "🔥 SHIP IT!"
