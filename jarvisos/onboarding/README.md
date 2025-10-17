# 🤖 JarvisOS Interactive Onboarding

**The first experience when booting JarvisOS**

---

## 🎬 The Experience

When you boot JarvisOS for the first time:

1. **🎨 Boot Screen** - Arc Reactor Blue Plymouth theme
2. **⚡ Boot Sequence** - Animated initialization (AI Brain, Predictive Engine, etc.)
3. **👋 Welcome** - Jarvis introduces himself (with voice!)
4. **🗣️ Introduction** - Jarvis asks your name (type or speak)
5. **💼 Role** - What do you do? (Developer, Designer, etc.)
6. **🎯 Features Tour** - Quick overview of capabilities
7. **🎬 Demo** - Optional quick demo
8. **✅ Ready!** - Profile saved, system ready

---

## 🛠️ Setup

### Option 1: Automatic (Recommended)

```bash
cd /path/to/JoS
chmod +x setup-boot-experience.sh
./setup-boot-experience.sh
```

This will:
- Install Plymouth boot screen theme
- Configure first-boot onboarding service
- Create desktop launcher

### Option 2: Manual

```bash
# Just run the onboarding
python3 jarvisos/onboarding/interactive_welcome.py
```

---

## 🎨 Features

### Voice Interaction
- **Jarvis speaks** using pyttsx3
- **Jarvis listens** using speech_recognition (optional)
- **Fallback to typing** if voice not available

### Personalization
- Saves user profile to `~/.jarvisos/profile.json`
- Remembers name and role
- Customizes experience based on user type

### Beautiful UI
- Rich terminal UI with colors and animations
- Arc Reactor Blue theme
- Smooth transitions

---

## 🔧 Configuration

### Voice Settings

Edit `interactive_welcome.py`:

```python
# Disable voice
onboarding = JarvisOnboarding()
onboarding.voice_enabled = False
onboarding.run()

# Change voice speed
onboarding.engine.setProperty('rate', 150)  # Slower
```

### Skip Onboarding

Already completed? The system checks automatically.

Force re-run:
```bash
python3 jarvisos/onboarding/interactive_welcome.py --force
```

Or delete profile:
```bash
rm ~/.jarvisos/profile.json
```

---

## 📋 Technical Details

### Dependencies

Required:
- `rich` - Terminal UI
- `python3` - Core

Optional (for voice):
- `pyttsx3` - Text-to-speech
- `speech_recognition` - Speech-to-text
- `pyaudio` - Microphone input

### Files

- `interactive_welcome.py` - Main onboarding script
- `setup-boot-experience.sh` - Installation script
- `/etc/systemd/system/jarvisos-onboarding.service` - First-boot service

### Boot Screen

Plymouth theme location:
```
/usr/share/plymouth/themes/jarvisos/
├── jarvisos.plymouth
└── jarvisos.script
```

---

## 🎯 Flow Diagram

```
Boot
  ↓
Plymouth Animation (Arc Reactor)
  ↓
Login
  ↓
First Boot Check
  ↓
[If first boot]
  ↓
Interactive Onboarding
  ├─ Welcome
  ├─ Ask Name
  ├─ Ask Role
  ├─ Show Features
  ├─ Quick Demo
  └─ Save Profile
  ↓
Desktop (JarvisOS Ready)
```

---

## 🚀 Testing

### Test Onboarding Now

```bash
python3 jarvisos/onboarding/interactive_welcome.py
```

### Test Boot Screen

```bash
sudo plymouthd --debug
sudo plymouth --show-splash
# Wait 5 seconds
sudo plymouth quit
```

### Test First-Boot Service

```bash
# Simulate first boot
rm ~/.jarvisos/profile.json
sudo systemctl start jarvisos-onboarding.service
journalctl -u jarvisos-onboarding.service -f
```

---

## 🎨 Customization

### Change Theme Colors

Edit `jarvisos.script`:

```javascript
Window.SetBackgroundTopColor(0.04, 0.05, 0.10);  // Change RGB values
```

### Change Welcome Message

Edit `interactive_welcome.py`:

```python
welcome = Panel(
    "[cyan]Your custom message here![/cyan]",
    ...
)
```

### Add More Questions

```python
def ask_custom_question(self):
    answer = Prompt.ask("[cyan]Your question?[/cyan]")
    # Save to profile
```

---

## 📊 User Profile

Saved to: `~/.jarvisos/profile.json`

```json
{
  "name": "John Doe",
  "role": "Developer",
  "onboarding_completed": true,
  "first_boot": 1729197000.0
}
```

---

## 🔥 FOUNDER MODE Integration

This onboarding is part of the **FOUNDER MODE** focus:

✅ **Ship something people can use**  
✅ **Beautiful first impression**  
✅ **Interactive and memorable**  
✅ **Works out of the box**

---

## 🐛 Troubleshooting

### Voice doesn't work

```bash
# Install dependencies
pip install pyttsx3 SpeechRecognition pyaudio

# Test
python3 -c "import pyttsx3; e = pyttsx3.init(); e.say('Test'); e.runAndWait()"
```

### Onboarding doesn't start on boot

```bash
# Check service status
systemctl status jarvisos-onboarding.service

# Check logs
journalctl -u jarvisos-onboarding.service
```

### Boot screen doesn't show

```bash
# Verify Plymouth is installed
plymouth --version

# Rebuild initramfs
sudo update-initramfs -u

# Reboot
sudo reboot
```

---

## 📝 TODO

- [ ] Add logo image to Plymouth theme
- [ ] Support more languages
- [ ] Video recording capability (auto-demo)
- [ ] Integration with system settings
- [ ] Custom themes per role (dev vs designer)

---

**Created with ❤️ in FOUNDER MODE**  
**Real artists ship. 🚀**
