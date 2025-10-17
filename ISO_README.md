# 🤖 JarvisOS - Bootable ISO

**The First Self-Building, Genetically Evolving Operating System**

Version: 0.3.0  
Date: October 17, 2025  
Status: Production Ready

---

## 📀 WHAT IS THIS ISO?

This is a **complete, bootable operating system** that:

- ✅ Boots on any x86_64 computer
- ✅ Installs like regular Ubuntu
- ✅ Includes JarvisOS pre-configured
- ✅ Auto-starts Jarvis on first boot
- ✅ Ready to use immediately

**Based on:** Ubuntu 22.04 LTS Desktop  
**Size:** ~4.5 GB  
**Architecture:** x86_64 (64-bit)

---

## 🚀 QUICK START

### 1. Download ISO
```
JarvisOS-v0.3.0-YYYYMMDD.iso
```

### 2. Create Bootable USB

**On macOS:**
```bash
# Find USB device
diskutil list

# Unmount (replace diskN with your USB)
diskutil unmountDisk /dev/diskN

# Write ISO
sudo dd if=JarvisOS-v0.3.0.iso of=/dev/rdiskN bs=1m

# Eject
diskutil eject /dev/diskN
```

**On Linux:**
```bash
# Find USB device
lsblk

# Write ISO (replace sdX with your USB)
sudo dd if=JarvisOS-v0.3.0.iso of=/dev/sdX bs=4M status=progress

# Sync
sudo sync
```

**On Windows:**
- Use [Rufus](https://rufus.ie/)
- Select ISO
- Write to USB

### 3. Boot from USB

1. Insert USB
2. Restart computer
3. Enter BIOS/UEFI (usually F2, F12, or DEL)
4. Select USB as boot device
5. Boot!

---

## 💻 INSTALLATION

### Automatic Installation

The ISO includes an **automated installer**:

1. **Boot from USB**
2. **Select "Install JarvisOS"**
3. **Wait 10-15 minutes**
4. **Reboot**
5. **Done!**

### Default Credentials

```
Username: jarvis
Password: jarvisos
```

**⚠️ Change password after first login!**

### Manual Installation

If you prefer manual installation:

1. Select "Try JarvisOS (Live)"
2. Click "Install Ubuntu"
3. Follow installer
4. After install, JarvisOS auto-configures

---

## 🎯 FIRST BOOT EXPERIENCE

### What Happens

1. **System boots** to desktop
2. **Terminal opens automatically**
3. **Jarvis greets you:**
   ```
   Good morning! Let's make today exceptional.
   
   Hello! I am Jarvis, your personal operating system.
   I'm quite excited to get to know you. Shall we begin?
   ```
4. **Interactive onboarding starts**
5. **You answer a few questions**
6. **Jarvis begins learning!**

### Onboarding Questions

- What's your name?
- What do you do for work?
- When do you usually start working?
- What's your main goal?

**Takes:** ~5 minutes  
**Result:** Personalized AI companion

---

## 🧬 WHAT JARVIS DOES

### Day 0: First Boot
- Interactive onboarding
- Learns about you
- Sets up profile

### Day 1-3: Silent Learning
- Observes your workflow
- Collects patterns
- Analyzes behavior

### Day 3: First Insights
- AI analysis complete
- Insights ready
- Automation suggestions

### Day 4+: Active Automation
- Generates custom scripts
- Executes automations
- Saves you time

### Ongoing: Evolution
- Scripts compete (natural selection)
- Best scripts survive
- System improves daily

---

## 📋 SYSTEM REQUIREMENTS

### Minimum
- **CPU:** 2 cores, 2 GHz
- **RAM:** 4 GB
- **Disk:** 25 GB
- **Graphics:** 1024x768

### Recommended
- **CPU:** 4 cores, 2.5 GHz
- **RAM:** 8 GB
- **Disk:** 50 GB
- **Graphics:** 1920x1080

### Supported Hardware
- ✅ Intel/AMD x86_64 processors
- ✅ Most laptops (2015+)
- ✅ Desktop PCs
- ✅ VirtualBox/VMware
- ⚠️ ARM not supported (yet)

---

## 🎨 WHAT'S INCLUDED

### Pre-installed Software
- Ubuntu 22.04 LTS Desktop
- Python 3.10+
- JarvisOS Core System
- All dependencies
- Desktop environment (XFCE)
- VNC server (optional)

### JarvisOS Components
- Observer (monitors workflow)
- Analyzer (AI insights with Claude)
- Generator (creates automations)
- Executor (runs scripts safely)
- Evolution Engine (genetic algorithms)
- Voice System (TTS/STT ready)
- Context Awareness
- Feedback System
- Proactive Notifications

### Services (Auto-start)
- `jarvisos-observer` - Continuous monitoring
- `jarvisos-nightly` - Daily analysis & evolution
- `jarvisos-notifier` - Proactive notifications
- `jarvisos-firstboot` - First boot onboarding

---

## 🔧 POST-INSTALL SETUP

### 1. Configure Claude API (Required)

```bash
cd /opt/jarvisos
source venv/bin/activate

# Add your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

**Get API key:** https://console.anthropic.com/

### 2. Test Installation

```bash
jarvis status
# Should show all components ready
```

### 3. Start Observing

```bash
jarvis observe --duration 60
# Observes for 1 hour
```

### 4. Check Progress

```bash
jarvis status
jarvis summary
jarvis dna
```

---

## 📚 COMMANDS REFERENCE

### Core Commands
```bash
jarvis status        # System status
jarvis observe       # Start observing
jarvis analyze       # Analyze data
jarvis generate      # Generate scripts
jarvis summary       # Show insights
jarvis dna           # Show user DNA
jarvis evolve        # Run evolution
```

### Interaction Commands
```bash
jarvis greet         # Morning greeting
jarvis context       # Show current context
jarvis feedback      # Feedback summary
jarvis rate [id]     # Rate a script
```

### Voice Commands
```bash
jarvis speak --text "Hello"
jarvis speak --greet
jarvis listen
```

### System Commands
```bash
jarvis onboard       # Re-run onboarding
jarvis notify        # Check notifications
jarvis genes         # List gene pool
```

---

## 🛠️ TROUBLESHOOTING

### Jarvis doesn't start

```bash
# Check services
sudo systemctl status jarvisos-observer

# Restart services
sudo systemctl restart jarvisos-observer

# Check logs
tail -f /opt/jarvisos/logs/jarvisos_*.log
```

### No AI insights

```bash
# Check API key
cat /opt/jarvisos/.env

# Test API
cd /opt/jarvisos
source venv/bin/activate
python -c "import anthropic; print('OK')"
```

### Permission errors

```bash
# Fix permissions
sudo chown -R jarvis:jarvis /opt/jarvisos/data
sudo chown -R jarvis:jarvis /opt/jarvisos/logs
sudo chmod -R 755 /opt/jarvisos
```

---

## 🔒 SECURITY & PRIVACY

### Data Privacy
- ✅ **100% local** - All data stays on your machine
- ✅ **No telemetry** - We don't collect anything
- ✅ **No cloud** - Everything runs locally
- ✅ **Open source** - Audit the code yourself

### API Usage
- Claude API used for analysis only
- You control your API key
- No data stored by Anthropic
- You can use local LLMs instead

### Script Execution
- Scripts run in your user context
- Review before execution
- Sandboxed execution (optional)
- Full audit trail

---

## 📖 DOCUMENTATION

### Online Docs
- GitHub: https://github.com/yourusername/JarvisOS
- Docs: https://jarvisos.dev/docs
- Community: https://discord.gg/jarvisos

### Included Docs
```bash
/opt/jarvisos/README.md
/opt/jarvisos/docs/
/opt/jarvisos/notes/
```

---

## 🆘 SUPPORT

### Get Help
- GitHub Issues: Report bugs
- Discord: Community support
- Email: support@jarvisos.dev

### Contributing
- Pull requests welcome!
- See CONTRIBUTING.md
- Join our community

---

## 📜 LICENSE

**JarvisOS** is open source software.

- License: MIT
- Free to use, modify, distribute
- Commercial use allowed
- Attribution appreciated

---

## 🎉 WELCOME TO JARVISOS!

**You're about to experience:**
- An OS that learns from you
- Automation that evolves
- An AI companion that helps
- A system that gets better every day

**Enjoy the journey!** 🚀

---

**Built with ❤️ by the JarvisOS Team**  
**Version 0.3.0 - October 2025**
