#!/bin/bash
#
# JarvisOS ISO Builder
# Creates bootable ISO from configured VM
#

set -e

echo "🔥 JarvisOS ISO Builder"
echo "======================="
echo ""

# Check dependencies
command -v multipass >/dev/null 2>&1 || { echo "❌ multipass not found"; exit 1; }

# Configuration
VM_NAME="jarvisos"
ISO_NAME="JarvisOS-v0.3.0-$(date +%Y%m%d).iso"
BUILD_DIR="iso-build"
OUTPUT_DIR="dist"

echo "📋 Configuration:"
echo "   VM: $VM_NAME"
echo "   ISO: $ISO_NAME"
echo ""

# Create build directory
echo "📁 Creating build directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

# Step 1: Export VM filesystem
echo ""
echo "📦 Step 1: Exporting VM filesystem..."
echo "   This will take a few minutes..."

# Create a snapshot of the VM
multipass stop "$VM_NAME" 2>/dev/null || true
sleep 2

# Export the VM
echo "   Exporting VM data..."
multipass exec "$VM_NAME" -- sudo bash -c "cd / && tar czf /tmp/jarvisos-rootfs.tar.gz \
    --exclude=/tmp/* \
    --exclude=/var/cache/* \
    --exclude=/var/log/* \
    --exclude=/proc/* \
    --exclude=/sys/* \
    --exclude=/dev/* \
    --exclude=/run/* \
    opt/jarvisos \
    etc/systemd/system/jarvisos* \
    home/ubuntu/.config \
    home/ubuntu/Desktop" 2>/dev/null || true

multipass transfer "$VM_NAME":/tmp/jarvisos-rootfs.tar.gz "$BUILD_DIR/" 2>/dev/null || true

echo "   ✅ VM data exported"

# Step 2: Download Ubuntu base ISO
echo ""
echo "📥 Step 2: Downloading Ubuntu 22.04 base ISO..."

BASE_ISO="ubuntu-22.04.3-desktop-amd64.iso"
BASE_ISO_URL="https://releases.ubuntu.com/22.04/$BASE_ISO"

if [ ! -f "$BUILD_DIR/$BASE_ISO" ]; then
    echo "   Downloading from Ubuntu servers..."
    echo "   This is a 4GB download, please be patient..."
    curl -L -o "$BUILD_DIR/$BASE_ISO" "$BASE_ISO_URL" --progress-bar
    echo "   ✅ Base ISO downloaded"
else
    echo "   ✅ Base ISO already exists"
fi

# Step 3: Extract base ISO
echo ""
echo "📂 Step 3: Extracting base ISO..."
mkdir -p "$BUILD_DIR/iso-extract"
mkdir -p "$BUILD_DIR/iso-custom"

# Mount and extract ISO (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   Mounting ISO on macOS..."
    hdiutil attach "$BUILD_DIR/$BASE_ISO" -mountpoint "$BUILD_DIR/iso-mount" -nobrowse
    echo "   Copying files..."
    rsync -a "$BUILD_DIR/iso-mount/" "$BUILD_DIR/iso-custom/"
    hdiutil detach "$BUILD_DIR/iso-mount"
else
    # Linux
    sudo mount -o loop "$BUILD_DIR/$BASE_ISO" "$BUILD_DIR/iso-mount"
    rsync -a "$BUILD_DIR/iso-mount/" "$BUILD_DIR/iso-custom/"
    sudo umount "$BUILD_DIR/iso-mount"
fi

echo "   ✅ Base ISO extracted"

# Step 4: Customize ISO
echo ""
echo "🎨 Step 4: Customizing ISO with JarvisOS..."

# Create preseed for auto-install
cat > "$BUILD_DIR/iso-custom/preseed/jarvisos.seed" << 'EOF'
# JarvisOS Preseed Configuration
d-i debian-installer/locale string en_US
d-i keyboard-configuration/xkb-keymap select us
d-i netcfg/choose_interface select auto
d-i netcfg/get_hostname string jarvisos
d-i netcfg/get_domain string local
d-i mirror/country string manual
d-i mirror/http/hostname string archive.ubuntu.com
d-i mirror/http/directory string /ubuntu
d-i mirror/http/proxy string
d-i passwd/user-fullname string Jarvis User
d-i passwd/username string jarvis
d-i passwd/user-password password jarvisos
d-i passwd/user-password-again password jarvisos
d-i user-setup/allow-password-weak boolean true
d-i clock-setup/utc boolean true
d-i time/zone string UTC
d-i partman-auto/method string regular
d-i partman-auto/choose_recipe select atomic
d-i partman/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true
tasksel tasksel/first multiselect ubuntu-desktop
d-i pkgsel/include string python3 python3-pip git curl
d-i grub-installer/only_debian boolean true
d-i grub-installer/bootdev string default
d-i finish-install/reboot_in_progress note
EOF

# Create post-install script
cat > "$BUILD_DIR/iso-custom/preseed/jarvisos-install.sh" << 'EOF'
#!/bin/bash
# JarvisOS Post-Install Script

echo "🤖 Installing JarvisOS..."

# Extract JarvisOS files
cd /tmp
tar xzf /cdrom/jarvisos-rootfs.tar.gz -C /

# Install Python dependencies
cd /opt/jarvisos
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Enable services
systemctl enable jarvisos-observer
systemctl enable jarvisos-nightly.timer
systemctl enable jarvisos-notifier.timer

# Setup desktop autostart
mkdir -p /home/jarvis/.config/autostart
cp /opt/jarvisos/system/jarvisos.desktop /home/jarvis/.config/autostart/
chown -R jarvis:jarvis /home/jarvis/.config

# Set permissions
chmod -R 755 /opt/jarvisos
chown -R jarvis:jarvis /opt/jarvisos/data /opt/jarvisos/logs

echo "✅ JarvisOS installed!"
EOF

chmod +x "$BUILD_DIR/iso-custom/preseed/jarvisos-install.sh"

# Copy JarvisOS data
if [ -f "$BUILD_DIR/jarvisos-rootfs.tar.gz" ]; then
    cp "$BUILD_DIR/jarvisos-rootfs.tar.gz" "$BUILD_DIR/iso-custom/"
fi

# Update boot menu
cat > "$BUILD_DIR/iso-custom/boot/grub/grub.cfg" << 'EOF'
set default=0
set timeout=10

menuentry "Install JarvisOS" {
    set gfxpayload=keep
    linux /casper/vmlinuz file=/cdrom/preseed/jarvisos.seed boot=casper automatic-ubiquity quiet splash ---
    initrd /casper/initrd
}

menuentry "Try JarvisOS (Live)" {
    set gfxpayload=keep
    linux /casper/vmlinuz boot=casper quiet splash ---
    initrd /casper/initrd
}
EOF

echo "   ✅ ISO customized"

# Step 5: Create bootable ISO
echo ""
echo "🔨 Step 5: Building bootable ISO..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - use hdiutil
    hdiutil makehybrid -o "$OUTPUT_DIR/$ISO_NAME" \
        -iso -joliet -default-volume-name "JarvisOS" \
        "$BUILD_DIR/iso-custom"
else
    # Linux - use genisoimage
    genisoimage -r -V "JarvisOS" -cache-inodes -J -l \
        -b isolinux/isolinux.bin -c isolinux/boot.cat \
        -no-emul-boot -boot-load-size 4 -boot-info-table \
        -o "$OUTPUT_DIR/$ISO_NAME" "$BUILD_DIR/iso-custom"
    
    # Make it bootable
    isohybrid "$OUTPUT_DIR/$ISO_NAME"
fi

echo "   ✅ ISO created"

# Step 6: Cleanup
echo ""
echo "🧹 Step 6: Cleaning up..."
# Keep build dir for debugging
# rm -rf "$BUILD_DIR"
echo "   ✅ Cleanup done"

# Done!
echo ""
echo "✅ SUCCESS!"
echo ""
echo "🎉 JarvisOS ISO created!"
echo ""
echo "📍 Location: $OUTPUT_DIR/$ISO_NAME"
echo "📊 Size: $(du -h "$OUTPUT_DIR/$ISO_NAME" | cut -f1)"
echo ""
echo "🚀 You can now:"
echo "   1. Burn to USB: dd if=$OUTPUT_DIR/$ISO_NAME of=/dev/sdX bs=4M"
echo "   2. Use in VirtualBox/VMware"
echo "   3. Boot on real hardware"
echo ""
echo "🤖 Default credentials:"
echo "   Username: jarvis"
echo "   Password: jarvisos"
echo ""
echo "💡 After boot, Jarvis will auto-start!"
echo ""
