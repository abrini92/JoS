# 🖥️ JarvisOS on UTM (Mac) - FOUNDER MODE

**Run JarvisOS with full interactive onboarding on UTM**

---

## 📦 Prerequisites

### Install UTM
```bash
brew install --cask utm
```

Or download from: https://mac.getutm.app/

---

## 🚀 Quick Setup - Ubuntu 22.04 (RECOMMENDED)

**Easiest way to get JarvisOS running with full features**

### Step 1: Download Ubuntu 22.04

**For Apple Silicon (M1/M2/M3):**
```bash
# Download Ubuntu Server ARM64
wget https://cdimage.ubuntu.com/releases/22.04/release/ubuntu-22.04.3-live-server-arm64.iso
```

**For Intel Mac:**
```bash
# Download Ubuntu Desktop AMD64
wget https://releases.ubuntu.com/22.04/ubuntu-22.04.3-desktop-amd64.iso
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

### Step 3: Install Ubuntu

1. Start the VM in UTM
2. Follow Ubuntu installer:
   - Language: English
   - Keyboard: Your layout
   - Installation type: Normal installation
   - Erase disk and install Ubuntu
   - **Username:** jarvis
   - **Password:** jarvis (or your choice)
   - Wait for installation (10-15 min)
3. Reboot when prompted
4. Remove ISO from UTM settings

### Step 4: Install JarvisOS (ONE COMMAND!)

After Ubuntu boots and you login:

```bash
# Install JarvisOS with interactive onboarding
curl -sSL https://raw.githubusercontent.com/abrini92/JoS/main/install.sh | bash

# OR manually:
git clone https://github.com/abrini92/JoS.git
cd JoS
chmod +x setup-boot-experience.sh
./setup-boot-experience.sh
```

This will:
- ✅ Install all dependencies
- ✅ Setup JarvisOS CLI
- ✅ Configure boot screen (Arc Reactor Blue!)
- ✅ Enable interactive onboarding
- ✅ Setup voice (Jarvis speaks!)

### Step 5: First Boot Experience 🎬

**Reboot to experience the magic:**

```bash
sudo reboot
```

**What happens:**
1. **Arc Reactor Boot Screen** - Blue animated boot
2. **Login** - Auto-login to Jarvis account
3. **Jarvis Welcomes You!** 🤖
   - "Hello, I am Jarvis"
   - Asks your name (type or speak!)
   - Asks your role (Developer, Designer, etc.)
   - Quick features tour
   - Optional demo
4. **Ready!** - System configured for you

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
