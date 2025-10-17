# 🖥️ JarvisOS on UTM (Mac)

Quick guide to run JarvisOS on UTM (Mac virtual machine).

---

## 📦 Prerequisites

### Install UTM
```bash
brew install --cask utm
```

Or download from: https://mac.getutm.app/

---

## 🚀 Quick Setup (Without ISO)

Since we don't have the ISO built yet, we'll create a VM with Arch Linux and install JarvisOS manually.

### Step 1: Download Arch Linux ISO

```bash
# Download Arch Linux ARM (for Apple Silicon) or x86_64 (for Intel)
# For Apple Silicon:
wget https://mirror.archlinuxarm.org/os/ArchLinuxARM-aarch64-latest.tar.gz

# For Intel Mac:
wget https://mirror.archlinux.org/iso/latest/archlinux-x86_64.iso
```

### Step 2: Create VM in UTM

1. Open UTM
2. Click "+" → "Virtualize"
3. Select "Linux"
4. Choose downloaded ISO
5. Configure:
   - **RAM:** 2GB (2048 MB)
   - **CPU:** 2 cores
   - **Storage:** 20GB
6. Click "Save"

### Step 3: Start VM & Install Arch

1. Start the VM
2. Boot from ISO
3. Basic Arch installation:

```bash
# Connect to internet
iwctl
station wlan0 connect "YourWiFi"

# Partition disk
cfdisk /dev/vda
# Create: 512MB EFI, rest Linux filesystem

# Format
mkfs.fat -F32 /dev/vda1
mkfs.ext4 /dev/vda2

# Mount
mount /dev/vda2 /mnt
mkdir /mnt/boot
mount /dev/vda1 /mnt/boot

# Install base
pacstrap /mnt base linux linux-firmware

# Generate fstab
genfstab -U /mnt >> /mnt/etc/fstab

# Chroot
arch-chroot /mnt

# Install essentials
pacman -S grub efibootmgr networkmanager python python-pip git base-devel

# Configure GRUB
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg

# Set root password
passwd

# Exit and reboot
exit
reboot
```

### Step 4: Install JarvisOS

After reboot, login as root:

```bash
# Connect network
systemctl start NetworkManager
systemctl enable NetworkManager
nmcli device wifi connect "YourWiFi" password "password"

# Clone JarvisOS
cd /opt
git clone https://github.com/yourusername/jarvisos.git
cd jarvisos

# Install
./install-system.sh
```

---

## 🎯 Alternative: Use Existing VM

If you already have the Ubuntu VM from Multipass, we can convert it!

### Export from Multipass
```bash
# Stop VM
multipass stop jarvisos

# Get VM location
multipass info jarvisos

# VM is at: ~/Library/Application Support/multipassd/
```

### Import to UTM
1. UTM → "+" → "Emulate"
2. Select "Other"
3. Skip ISO
4. Import existing disk
5. Point to Multipass VM disk

---

## 🧪 Testing JarvisOS in UTM

### 1. Start VM
```bash
# In UTM, start the JarvisOS VM
```

### 2. Login
```bash
# Username: ubuntu (or root)
# Password: (your password)
```

### 3. Test JarvisOS
```bash
cd /opt/jarvisos
source venv/bin/activate

# Test status
python jarvis.py status

# Test DNA
python jarvis.py dna

# Test voice (if audio passthrough enabled)
python jarvis.py speak --text "Hello from UTM"

# Test evolution
python jarvis.py evolve
```

### 4. Check Services
```bash
# Check observer
sudo systemctl status jarvisos-observer

# Check logs
sudo journalctl -u jarvisos-observer -f

# Check data
ls -la /opt/jarvisos/data/
```

---

## 🎙️ Enable Audio in UTM

For voice features to work:

1. UTM → Select VM → Edit
2. Go to "Sound"
3. Enable "Sound Card"
4. Select "Default"
5. Save and restart VM

---

## 🔧 UTM Configuration Tips

### Performance
- **CPU:** Give 2-4 cores
- **RAM:** 2-4GB
- **Graphics:** Enable hardware acceleration
- **Network:** Shared network mode

### Shared Folders
1. UTM → Edit VM → Sharing
2. Add shared directory
3. Mount in VM:
   ```bash
   sudo mount -t 9p -o trans=virtio share /mnt/share
   ```

### Copy/Paste
- Enable in UTM settings
- Use clipboard sharing

---

## 📊 Expected Performance

### Apple Silicon (M1/M2/M3)
- **Boot time:** 10-15 seconds
- **Observer:** Real-time, no lag
- **AI Analysis:** 5-10 seconds
- **Voice:** Instant

### Intel Mac
- **Boot time:** 15-20 seconds
- **Observer:** Real-time
- **AI Analysis:** 10-15 seconds
- **Voice:** Instant

---

## 🐛 Troubleshooting

### VM won't start
- Check virtualization is enabled
- Try different Linux distribution
- Reduce RAM if needed

### Network not working
- Use "Shared Network" mode
- Check host network connection
- Try bridged mode

### Audio not working
- Enable sound card in UTM
- Check macOS audio permissions
- Try different audio backend

### Slow performance
- Increase CPU cores
- Increase RAM
- Enable hardware acceleration
- Use SSD storage

---

## 🎯 Next Steps

Once VM is running:

1. ✅ Verify all services
2. ✅ Test voice features
3. ✅ Run full observation cycle
4. ✅ Test evolution
5. ✅ Take snapshot (backup)

---

## 📸 Snapshots

Create snapshots for easy rollback:

1. UTM → Select VM → Snapshots
2. Click "+" to create snapshot
3. Name it (e.g., "Fresh Install", "After Setup")
4. Restore anytime

---

## 🚀 Quick Start Commands

```bash
# After VM boot
cd /opt/jarvisos
source venv/bin/activate

# Quick test
python jarvis.py status
python jarvis.py dna
python jarvis.py speak --greet

# Start services
sudo systemctl start jarvisos-observer
sudo systemctl start jarvisos-nightly.timer

# Monitor
sudo journalctl -u jarvisos-observer -f
```

---

## 🎉 Success!

You now have JarvisOS running in UTM on your Mac!

**Next:** Let it observe for a few hours, then test evolution.

---

*UTM is perfect for testing JarvisOS safely!* 🖥️
