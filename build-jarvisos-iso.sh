#!/bin/bash
#
# JarvisOS ISO Builder - Expert Edition
# Creates a bootable ISO from Multipass VM
#

set -e

echo "🔥 JarvisOS ISO Builder - Expert Mode"
echo "======================================"
echo ""

# Configuration
VM_NAME="jarvisos"
ISO_NAME="JarvisOS-v0.3.0-$(date +%Y%m%d).iso"
BUILD_DIR="iso-build"
OUTPUT_DIR="dist"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check dependencies
log_info "Checking dependencies..."

if ! command -v multipass &> /dev/null; then
    log_error "Multipass not found"
    exit 1
fi

if ! command -v curl &> /dev/null; then
    log_error "curl not found"
    exit 1
fi

log_success "All dependencies found"

# Create directories
log_info "Creating build directories..."
rm -rf "$BUILD_DIR" "$OUTPUT_DIR"
mkdir -p "$BUILD_DIR" "$OUTPUT_DIR"
log_success "Directories created"

# Step 1: Get correct Ubuntu ISO URL
log_info "Finding latest Ubuntu 22.04 ISO..."

# Use Ubuntu's release server
UBUNTU_VERSION="22.04.3"
BASE_URL="https://releases.ubuntu.com/22.04"

# Try to get the actual ISO filename
log_info "Checking Ubuntu releases..."
ISO_FILENAME=$(curl -s "$BASE_URL/" | grep -o 'ubuntu-22.04.[0-9]*-desktop-amd64.iso' | head -1)

if [ -z "$ISO_FILENAME" ]; then
    # Fallback to known version
    ISO_FILENAME="ubuntu-22.04.3-desktop-amd64.iso"
    log_warning "Using fallback: $ISO_FILENAME"
else
    log_success "Found: $ISO_FILENAME"
fi

BASE_ISO_URL="$BASE_URL/$ISO_FILENAME"
BASE_ISO_PATH="$BUILD_DIR/$ISO_FILENAME"

# Step 2: Download Ubuntu ISO
log_info "Downloading Ubuntu ISO (this will take 15-30 minutes)..."
log_info "URL: $BASE_ISO_URL"
log_info "Size: ~4.5 GB"
echo ""

if [ -f "$BASE_ISO_PATH" ]; then
    log_warning "ISO already exists, skipping download"
else
    # Download with progress
    curl -L -o "$BASE_ISO_PATH" "$BASE_ISO_URL" \
        --progress-bar \
        --retry 3 \
        --retry-delay 5 \
        --max-time 3600
    
    if [ $? -ne 0 ]; then
        log_error "Download failed"
        log_info "Trying alternative mirror..."
        
        # Try alternative mirror
        ALT_URL="http://old-releases.ubuntu.com/releases/22.04/$ISO_FILENAME"
        curl -L -o "$BASE_ISO_PATH" "$ALT_URL" \
            --progress-bar \
            --retry 3 \
            --retry-delay 5 \
            --max-time 3600
        
        if [ $? -ne 0 ]; then
            log_error "All downloads failed"
            exit 1
        fi
    fi
fi

# Verify download
ISO_SIZE=$(stat -f%z "$BASE_ISO_PATH" 2>/dev/null || stat -c%s "$BASE_ISO_PATH" 2>/dev/null)
if [ "$ISO_SIZE" -lt 1000000000 ]; then
    log_error "Downloaded ISO is too small ($ISO_SIZE bytes)"
    log_error "Expected ~4.5 GB"
    exit 1
fi

log_success "Ubuntu ISO downloaded ($(numfmt --to=iec-i --suffix=B $ISO_SIZE 2>/dev/null || echo "$ISO_SIZE bytes"))"

# Step 3: Export JarvisOS from VM
log_info "Exporting JarvisOS from VM..."

# Stop VM if running
multipass stop "$VM_NAME" 2>/dev/null || true
sleep 2

# Start VM
multipass start "$VM_NAME"
sleep 5

# Export JarvisOS files
log_info "Creating JarvisOS archive..."
multipass exec "$VM_NAME" -- sudo bash -c "
    cd / && \
    tar czf /tmp/jarvisos-system.tar.gz \
        --exclude=/tmp/* \
        --exclude=/var/cache/* \
        --exclude=/var/log/* \
        --exclude=/proc/* \
        --exclude=/sys/* \
        --exclude=/dev/* \
        --exclude=/run/* \
        opt/jarvisos \
        etc/systemd/system/jarvisos* \
        home/ubuntu/.config/autostart \
        home/ubuntu/Desktop
"

# Transfer to host
multipass transfer "$VM_NAME":/tmp/jarvisos-system.tar.gz "$BUILD_DIR/"

JARVIS_SIZE=$(stat -f%z "$BUILD_DIR/jarvisos-system.tar.gz" 2>/dev/null || stat -c%s "$BUILD_DIR/jarvisos-system.tar.gz" 2>/dev/null)
log_success "JarvisOS exported ($(numfmt --to=iec-i --suffix=B $JARVIS_SIZE 2>/dev/null || echo "$JARVIS_SIZE bytes"))"

# Step 4: Extract base ISO
log_info "Extracting base ISO..."
mkdir -p "$BUILD_DIR/iso-mount" "$BUILD_DIR/iso-custom"

# Mount ISO (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    hdiutil attach "$BASE_ISO_PATH" -mountpoint "$BUILD_DIR/iso-mount" -nobrowse -quiet
    
    # Copy files
    log_info "Copying ISO contents..."
    rsync -a --info=progress2 "$BUILD_DIR/iso-mount/" "$BUILD_DIR/iso-custom/"
    
    # Unmount
    hdiutil detach "$BUILD_DIR/iso-mount" -quiet
else
    # Linux
    sudo mount -o loop "$BASE_ISO_PATH" "$BUILD_DIR/iso-mount"
    rsync -a "$BUILD_DIR/iso-mount/" "$BUILD_DIR/iso-custom/"
    sudo umount "$BUILD_DIR/iso-mount"
fi

log_success "Base ISO extracted"

# Step 5: Customize ISO
log_info "Customizing ISO with JarvisOS..."

# Copy JarvisOS archive
cp "$BUILD_DIR/jarvisos-system.tar.gz" "$BUILD_DIR/iso-custom/"

# Create autoinstall configuration
mkdir -p "$BUILD_DIR/iso-custom/autoinstall"

cat > "$BUILD_DIR/iso-custom/autoinstall/user-data" << 'EOF'
#cloud-config
autoinstall:
  version: 1
  locale: en_US
  keyboard:
    layout: us
  identity:
    hostname: jarvisos
    username: jarvis
    password: "$6$rounds=4096$saltsalt$hash"
  ssh:
    install-server: true
  packages:
    - python3
    - python3-pip
    - python3-venv
    - git
    - curl
  late-commands:
    - curtin in-target --target=/target -- bash -c "cd / && tar xzf /cdrom/jarvisos-system.tar.gz"
    - curtin in-target --target=/target -- systemctl enable jarvisos-observer
    - curtin in-target --target=/target -- systemctl enable jarvisos-nightly.timer
    - curtin in-target --target=/target -- systemctl enable jarvisos-notifier.timer
EOF

# Create boot configuration
cat > "$BUILD_DIR/iso-custom/boot/grub/grub.cfg" << 'EOF'
set timeout=10
set default=0

menuentry "Install JarvisOS" {
    set gfxpayload=keep
    linux /casper/vmlinuz autoinstall ds=nocloud\;s=/cdrom/autoinstall/ quiet splash ---
    initrd /casper/initrd
}

menuentry "Try JarvisOS (Live)" {
    set gfxpayload=keep
    linux /casper/vmlinuz boot=casper quiet splash ---
    initrd /casper/initrd
}

menuentry "Boot from first hard disk" {
    set root=(hd0)
    chainloader +1
}
EOF

# Update isolinux for BIOS boot
if [ -f "$BUILD_DIR/iso-custom/isolinux/txt.cfg" ]; then
    cat > "$BUILD_DIR/iso-custom/isolinux/txt.cfg" << 'EOF'
default install
label install
  menu label ^Install JarvisOS
  kernel /casper/vmlinuz
  append autoinstall ds=nocloud;s=/cdrom/autoinstall/ initrd=/casper/initrd quiet splash ---
label live
  menu label ^Try JarvisOS
  kernel /casper/vmlinuz
  append boot=casper initrd=/casper/initrd quiet splash ---
EOF
fi

log_success "ISO customized"

# Step 6: Create bootable ISO
log_info "Building bootable ISO..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - use hdiutil
    hdiutil makehybrid \
        -o "$OUTPUT_DIR/$ISO_NAME" \
        -iso \
        -joliet \
        -eltorito-boot "$BUILD_DIR/iso-custom/isolinux/isolinux.bin" \
        -no-emul-boot \
        -boot-load-size 4 \
        -boot-info-table \
        -eltorito-catalog "$BUILD_DIR/iso-custom/isolinux/boot.cat" \
        -default-volume-name "JarvisOS" \
        "$BUILD_DIR/iso-custom"
else
    # Linux - use xorriso
    xorriso -as mkisofs \
        -iso-level 3 \
        -full-iso9660-filenames \
        -volid "JarvisOS" \
        -eltorito-boot isolinux/isolinux.bin \
        -eltorito-catalog isolinux/boot.cat \
        -no-emul-boot \
        -boot-load-size 4 \
        -boot-info-table \
        -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
        -eltorito-alt-boot \
        -e EFI/BOOT/BOOTX64.EFI \
        -no-emul-boot \
        -isohybrid-gpt-basdat \
        -output "$OUTPUT_DIR/$ISO_NAME" \
        "$BUILD_DIR/iso-custom"
fi

log_success "ISO created"

# Step 7: Generate checksums
log_info "Generating checksums..."

cd "$OUTPUT_DIR"
shasum -a 256 "$ISO_NAME" > "$ISO_NAME.sha256"
md5 "$ISO_NAME" > "$ISO_NAME.md5" 2>/dev/null || md5sum "$ISO_NAME" > "$ISO_NAME.md5" 2>/dev/null
cd - > /dev/null

log_success "Checksums generated"

# Final report
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
log_success "JarvisOS ISO BUILD COMPLETE!"
echo ""
echo "📍 Location: $OUTPUT_DIR/$ISO_NAME"
echo "📊 Size: $(ls -lh "$OUTPUT_DIR/$ISO_NAME" | awk '{print $5}')"
echo ""
echo "🔐 Checksums:"
echo "   SHA256: $(cat "$OUTPUT_DIR/$ISO_NAME.sha256" | awk '{print $1}')"
echo ""
echo "🚀 You can now:"
echo "   1. Burn to USB:"
echo "      sudo dd if=$OUTPUT_DIR/$ISO_NAME of=/dev/sdX bs=4M status=progress"
echo ""
echo "   2. Use in VirtualBox:"
echo "      - Create new VM"
echo "      - Mount this ISO"
echo "      - Install"
echo ""
echo "   3. Boot on real hardware"
echo ""
echo "🤖 Default credentials:"
echo "   Username: jarvis"
echo "   Password: jarvisos"
echo ""
echo "💡 After boot, Jarvis will auto-start!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Cleanup option
read -p "🧹 Clean build directory? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$BUILD_DIR"
    log_success "Build directory cleaned"
fi

log_success "DONE!"
