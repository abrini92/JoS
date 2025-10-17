# 💿 JarvisOS Installation Guide

Complete guide to install JarvisOS on your machine.

---

## ⚠️ WARNING

**JarvisOS is experimental software.**

- Backup your data before installing
- Test in VM first
- Not recommended as primary OS yet
- Use at your own risk

---

## 🎯 Installation Options

### Option 1: VM Installation (Recommended)
Test JarvisOS safely in a virtual machine.

### Option 2: Dual Boot
Install alongside your existing OS.

### Option 3: Dedicated Machine
Replace existing OS completely.

---

## 📋 Prerequisites

### Hardware Requirements
- **CPU:** 64-bit processor (x86_64)
- **RAM:** 2GB minimum, 4GB recommended
- **Disk:** 10GB minimum, 20GB recommended
- **Network:** Internet connection for setup

### Software Requirements
- USB drive (4GB+) for bootable media
- VM software (VirtualBox, VMware, etc.) for VM install

---

## 🚀 Option 1: VM Installation

### Step 1: Download ISO
```bash
# Download latest JarvisOS ISO
wget https://github.com/yourusername/jarvisos/releases/latest/jarvisos-x86_64.iso
```

### Step 2: Create VM

**VirtualBox:**
1. New VM → Linux → Arch Linux (64-bit)
2. RAM: 2GB
3. Disk: 20GB (dynamic)
4. Settings → Storage → Add ISO to optical drive
5. Start VM

**VMware:**
1. Create New VM → Linux → Other Linux 5.x kernel 64-bit
2. RAM: 2GB
3. Disk: 20GB
4. Use ISO image → Select JarvisOS ISO
5. Power On

**UTM (Mac):**
1. Create New VM → Virtualize → Linux
2. Boot ISO → Select JarvisOS ISO
3. RAM: 2GB, Disk: 20GB
4. Start

### Step 3: Boot & Install

1. Boot from ISO
2. Select "JarvisOS - The First Self-Building Operating System"
3. Wait for boot (1-2 minutes)
4. Follow on-screen instructions
5. Jarvis will guide you through setup

### Step 4: First Boot

After installation:
1. Remove ISO
2. Reboot
3. Jarvis introduces himself (voice)
4. Interactive onboarding begins
5. Set up API key
6. Start using!

---

## 🔧 Option 2: Dual Boot Installation

### Step 1: Prepare

1. **Backup everything**
2. Free up 20GB+ disk space
3. Create bootable USB:
   ```bash
   # Linux/Mac
   sudo dd if=jarvisos.iso of=/dev/sdX bs=4M status=progress
   
   # Windows (use Rufus or Etcher)
   ```

### Step 2: Boot from USB

1. Insert USB
2. Restart computer
3. Enter BIOS/UEFI (F2, F12, DEL, or ESC)
4. Select USB as boot device
5. Save and reboot

### Step 3: Install

1. Select "JarvisOS - Install"
2. Follow installer prompts
3. Choose "Install alongside existing OS"
4. Select partition size
5. Wait for installation (10-15 min)
6. Reboot

### Step 4: Configure Boot

GRUB will show:
- JarvisOS
- Your existing OS (Windows/Linux)

Select JarvisOS to boot.

---

## 💻 Option 3: Dedicated Installation

**⚠️ This will ERASE your entire disk!**

### Step 1: Backup

Backup ALL your data. Seriously.

### Step 2: Boot from USB

Same as dual boot option.

### Step 3: Install

1. Select "JarvisOS - Install"
2. Choose "Erase disk and install JarvisOS"
3. Confirm (last warning!)
4. Wait for installation
5. Reboot

### Step 4: First Boot

Jarvis will guide you through initial setup.

---

## 🎙️ First Boot Experience

### What Happens

1. **Boot Animation**
   - JarvisOS logo
   - Loading services

2. **Jarvis Introduction** (Voice)
   ```
   "Hello. I am Jarvis.
   
   I am not an ordinary operating system.
   
   I am here to learn who you are,
   how you work, and what you need..."
   ```

3. **Interactive Onboarding**
   - Your name
   - Primary activity
   - Tools you use
   - Work schedule
   - Permission to observe

4. **System Configuration**
   - API key setup
   - Network configuration
   - User preferences

5. **Ready to Use!**
   - Observer starts
   - Desktop environment loads
   - Jarvis is listening

---

## ⚙️ Post-Installation Setup

### 1. Set API Key

```bash
# Edit .env file
nano /opt/jarvisos/.env

# Add your Anthropic API key
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx...

# Restart services
sudo systemctl restart jarvisos-*
```

### 2. Verify Services

```bash
# Check observer
sudo systemctl status jarvisos-observer

# Check timers
systemctl list-timers jarvisos-*

# View logs
sudo journalctl -u jarvisos-observer -f
```

### 3. Test Voice

```bash
cd /opt/jarvisos
source venv/bin/activate

# Test speech
python jarvis.py speak --introduce

# Test listening (if microphone available)
python jarvis.py listen
```

### 4. Run Onboarding

```bash
# Interactive voice onboarding
python jarvis.py onboard
```

---

## 🔧 Troubleshooting

### Boot Issues

**Problem:** Won't boot from USB
- **Solution:** Check BIOS boot order, disable Secure Boot

**Problem:** Black screen after boot
- **Solution:** Boot in Safe Mode, check graphics drivers

### Installation Issues

**Problem:** Installation fails
- **Solution:** Check disk space, try different partition

**Problem:** Network not working
- **Solution:** Check WiFi drivers, use ethernet

### Service Issues

**Problem:** Observer not starting
- **Solution:** 
  ```bash
  sudo systemctl status jarvisos-observer
  sudo journalctl -u jarvisos-observer -n 50
  ```

**Problem:** Voice not working
- **Solution:** Check audio drivers, test with `speaker-test`

### API Issues

**Problem:** "Invalid API key"
- **Solution:** Check .env file, verify key is correct

---

## 📊 System Requirements

### Minimum
- CPU: 1.5 GHz dual-core
- RAM: 2GB
- Disk: 10GB
- Network: Required for AI features

### Recommended
- CPU: 2.0 GHz quad-core
- RAM: 4GB
- Disk: 20GB SSD
- Network: Broadband
- Microphone: For voice interaction

### Optimal
- CPU: 3.0 GHz+ multi-core
- RAM: 8GB+
- Disk: 50GB+ NVMe SSD
- Network: High-speed
- Microphone: Quality USB mic
- Speakers: Good audio output

---

## 🎯 What to Expect

### Day 1
- Fresh install
- Jarvis introduces himself
- Onboarding complete
- Observer starts collecting data

### Day 3
- First AI analysis
- Pattern recognition begins
- Initial suggestions

### Week 1
- 5-10 automation scripts generated
- Workflow optimizations
- Personalization starts

### Month 1
- 50+ scripts in gene pool
- Natural selection active
- OS evolving for you
- Noticeable productivity gains

### Month 6
- 200+ genes
- Highly personalized OS
- Unique to you
- Completely different from any other JarvisOS

---

## 🆘 Getting Help

### Documentation
- [README.md](../README.md)
- [OS Deployment Guide](OS_DEPLOYMENT.md)
- [API Key Setup](API_KEY_SETUP.md)

### Community
- GitHub Issues
- Discord Server
- Twitter: @JarvisOS

### Logs
```bash
# System logs
sudo journalctl -xe

# JarvisOS logs
sudo journalctl -u 'jarvisos-*'
tail -f /opt/jarvisos/logs/*.log
```

---

## ✅ Installation Checklist

- [ ] Hardware requirements met
- [ ] Data backed up
- [ ] ISO downloaded
- [ ] Bootable media created
- [ ] BIOS configured
- [ ] Installation completed
- [ ] First boot successful
- [ ] API key configured
- [ ] Services running
- [ ] Voice tested
- [ ] Onboarding done
- [ ] Observer collecting data

---

## 🎉 Welcome to JarvisOS!

You now have a self-building, genetically evolving, voice-enabled operating system.

**It will learn from you.**
**It will adapt to you.**
**It will evolve for you.**

**Enjoy the future of computing!** 🚀

---

*For advanced configuration, see [OS_DEPLOYMENT.md](OS_DEPLOYMENT.md)*
