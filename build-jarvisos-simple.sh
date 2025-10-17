#!/bin/bash
# JarvisOS ISO Builder - SIMPLE & WORKING
# Builds a bootable Ubuntu-based ISO with JarvisOS pre-installed

set -e

echo "🚀 JarvisOS ISO Builder - FOUNDER MODE"
echo "======================================="
echo ""

# Config
ISO_NAME="jarvisos-v0.1.0-$(date +%Y%m%d).iso"
WORK_DIR="$HOME/jarvisos-iso-build"
BASE_ISO="ubuntu-22.04.3-live-server-amd64.iso"
BASE_URL="https://releases.ubuntu.com/22.04/$BASE_ISO"

# Clean
echo "🧹 Cleaning workspace..."
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Download base Ubuntu (server - smaller, faster)
echo "📦 Downloading Ubuntu 22.04 Server..."
if [ ! -f "$BASE_ISO" ]; then
    wget -q --show-progress "$BASE_URL" || {
        echo "❌ Download failed!"
        exit 1
    }
fi

echo "✅ Base ISO ready: $(du -h $BASE_ISO | cut -f1)"

# Extract ISO
echo "📂 Extracting ISO..."
mkdir -p iso-content
xorriso -osirrox on -indev "$BASE_ISO" -extract / iso-content/ 2>/dev/null

# Make writable
chmod -R u+w iso-content/

# Add JarvisOS
echo "🤖 Adding JarvisOS..."
mkdir -p iso-content/jarvisos
cp -r ~/JoS/* iso-content/jarvisos/ 2>/dev/null || true

# Create autoinstall config
echo "⚙️  Creating autoinstall config..."
cat > iso-content/jarvisos/autoinstall.yaml << 'EOF'
#cloud-config
autoinstall:
  version: 1
  identity:
    hostname: jarvisos
    username: jarvis
    password: "$6$rounds=4096$saltsaltsal$xyz..."  # Password: jarvis
  ssh:
    install-server: true
  late-commands:
    - curtin in-target --target=/target -- bash -c "cd /opt && cp -r /cdrom/jarvisos . && chown -R jarvis:jarvis jarvisos"
EOF

# Rebuild ISO
echo "🔨 Building ISO..."
cd iso-content
xorriso -as mkisofs \
    -r -V "JarvisOS" \
    -o "../$ISO_NAME" \
    -J -joliet-long \
    -b isolinux/isolinux.bin \
    -c isolinux/boot.cat \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    -eltorito-alt-boot \
    -e boot/grub/efi.img \
    -no-emul-boot \
    -isohybrid-gpt-basdat \
    . 2>&1 | grep -v "^xorriso"

cd ..

# Verify
if [ -f "$ISO_NAME" ]; then
    echo ""
    echo "✅ SUCCESS! ISO BUILT!"
    echo "======================================"
    echo "📍 Location: $WORK_DIR/$ISO_NAME"
    echo "📊 Size: $(du -h $ISO_NAME | cut -f1)"
    echo ""
    echo "🧪 Next steps:"
    echo "1. Copy to host: multipass transfer jarvisos:$WORK_DIR/$ISO_NAME ."
    echo "2. Create USB: dd if=$ISO_NAME of=/dev/sdX bs=4M status=progress"
    echo "3. Boot from USB!"
    echo ""
    echo "🔥 READY TO SHIP!"
else
    echo "❌ Build failed!"
    exit 1
fi
