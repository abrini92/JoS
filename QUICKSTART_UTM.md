# ⚡ JarvisOS UTM QuickStart - 15 Minutes

**Get JarvisOS running on UTM with full interactive experience**

---

## 🎯 What You'll Get

- ✅ Bootable JarvisOS on UTM
- ✅ Arc Reactor Blue boot screen
- ✅ Jarvis speaks and welcomes you
- ✅ Interactive onboarding
- ✅ **Local AI with Ollama (FREE!)** 🔥
- ✅ Full Predictive Engine
- ✅ Ready to use in 15 min

---

## 📋 Prerequisites

1. **Mac** (Apple Silicon or Intel)
2. **UTM** installed:
   ```bash
   brew install --cask utm
   ```
3. **10GB free space**

---

## 🚀 5 Steps to JarvisOS

### 1. Download Ubuntu (2 min)

**Apple Silicon (M1/M2/M3):**
```bash
wget https://cdimage.ubuntu.com/releases/22.04/release/ubuntu-22.04.3-live-server-arm64.iso
```

**Intel Mac:**
```bash
wget https://releases.ubuntu.com/22.04/ubuntu-22.04.3-desktop-amd64.iso
```

### 2. Create VM in UTM (1 min)

1. Open UTM → Click **"+"**
2. Select **"Virtualize"**
3. Choose **"Linux"**
4. Select the downloaded ISO
5. Settings:
   - **RAM:** 4GB (4096 MB)
   - **CPU:** 2 cores
   - **Storage:** 20GB
6. Click **"Save"**

### 3. Install Ubuntu (10 min)

1. Start VM → Boot Ubuntu installer
2. Quick setup:
   - Language: **English**
   - Type: **Normal installation**
   - Erase disk: **Yes**
   - Username: **jarvis**
   - Password: **jarvis**
3. Wait for install (coffee time ☕)
4. Reboot when done
5. Remove ISO in UTM settings

### 4. Install JarvisOS (2 min)

Login to Ubuntu, open terminal:

```bash
curl -sSL https://raw.githubusercontent.com/abrini92/JoS/main/install.sh | bash
```

**This installs everything:**
- Python dependencies
- JarvisOS CLI
- Arc Reactor boot theme
- Interactive onboarding
- Voice support

### 5. Reboot & Enjoy! 🎬

```bash
sudo reboot
```

**What happens:**
1. **Blue Arc Reactor boot animation**
2. **Jarvis speaks:** "Hello, I am Jarvis..."
3. **Interactive chat:**
   - What's your name?
   - What do you do?
   - Features tour
4. **Ready!** JarvisOS configured for you

---

## 🎮 Using JarvisOS

After onboarding, use these commands:

```bash
# System status
jarvis status

# AI predictions
jarvis predict

# Plan work session
jarvis plan "Build a web app"

# Get suggestions
jarvis suggest "Setup dev environment"

# See all commands
jarvis --help
```

---

## 🎨 What Makes It Special

### Arc Reactor Boot Screen
- Custom Plymouth theme
- Cyan/blue animations
- "Initializing JarvisOS..." messages

### Jarvis Speaks!
- Text-to-speech welcome
- Optional voice input
- Natural conversation

### AI-Powered
- Claude Haiku brain
- Predictive intelligence
- Learns from your work

---

## 🐛 Troubleshooting

### VM won't boot
- Increase RAM to 4GB
- Try different Ubuntu ISO
- Check virtualization enabled

### No sound/voice
- UTM → Edit VM → Sound → Enable
- Test: `jarvis speak --text "Test"`

### Slow performance
- Give more CPU cores (4)
- Increase RAM (6GB)
- Enable hardware acceleration

### Network issues
- Use "Shared Network" mode in UTM
- Check host internet connection

---

## 📸 Take Snapshot!

**Before doing anything else:**

1. UTM → Select VM → **Snapshots**
2. Click **"+"**
3. Name: **"Fresh JarvisOS Install"**

Now you can always restore to this point!

---

## 🎯 Next Steps

1. **Use it!** Let Jarvis observe your work
2. **Test features:**
   - `jarvis observe` - Start observation
   - `jarvis analyze` - AI analysis
   - `jarvis generate` - Generate scripts
3. **Customize:**
   - Edit `~/.jarvisos/profile.json`
   - Check `jarvis --help`

---

## 📊 Expected Timeline

| Step | Time | What Happens |
|------|------|--------------|
| Download ISO | 2 min | Ubuntu download |
| Create VM | 1 min | UTM setup |
| Install Ubuntu | 10 min | OS installation |
| Install JarvisOS | 2 min | One-line install |
| **Total** | **15 min** | **Ready to use!** |

---

## 🔥 That's It!

**You now have a fully functional JarvisOS!**

- Boot screen? ✅ Arc Reactor Blue
- Voice? ✅ Jarvis speaks
- AI? ✅ Predictive Engine
- Onboarding? ✅ Interactive
- Ready? ✅ Let's build!

---

## 📚 More Info

- Full docs: `/Users/you/JoS/docs/`
- Onboarding guide: `/Users/you/JoS/jarvisos/onboarding/README.md`
- Troubleshooting: `/Users/you/JoS/docs/UTM_SETUP.md`

---

**Created with 🔥 in FOUNDER MODE**

**Real artists ship. You just did. 🚀**
