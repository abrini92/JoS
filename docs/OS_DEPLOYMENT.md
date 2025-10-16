# 🐧 JarvisOS - Operating System Deployment Guide

## Overview

This guide explains how to deploy JarvisOS as a **system-level service** that runs automatically at boot, making it a true operating system component rather than just scripts.

---

## 🎯 What This Achieves

### Before (Scripts)
```
User manually runs:
$ python jarvis.py observe
$ python jarvis.py analyze
$ python jarvis.py generate
```

### After (OS Integration)
```
✅ Observer runs continuously in background
✅ Analyzer runs every 6 hours automatically
✅ Generator runs nightly at 3 AM
✅ Full evolution happens while you sleep
✅ Survives reboots
✅ Managed by systemd (like any OS service)
```

---

## 📋 Prerequisites

### Supported Systems
- **Ubuntu 20.04+** (recommended)
- **Debian 11+**
- **Arch Linux**
- **Fedora 35+**
- Any Linux with systemd

### Requirements
- Root access (sudo)
- Python 3.11+
- systemd
- Internet connection (for AI API)

---

## 🚀 Installation

### Option 1: Automated Install (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/jarvisos.git
cd jarvisos

# Run system installer
sudo ./install-system.sh
```

The installer will:
1. Create `jarvis` system user
2. Install to `/opt/jarvisos`
3. Setup Python environment
4. Install systemd services
5. Configure API key
6. Enable and start services

### Option 2: Manual Install

```bash
# 1. Create user
sudo useradd -r -s /bin/bash -d /opt/jarvisos -m jarvis

# 2. Copy files
sudo cp -r . /opt/jarvisos/
sudo chown -R jarvis:jarvis /opt/jarvisos

# 3. Setup Python
cd /opt/jarvisos
sudo -u jarvis python3 -m venv venv
sudo -u jarvis venv/bin/pip install -r requirements.txt

# 4. Configure API key
sudo nano /etc/systemd/system/jarvisos-observer.service
# Edit: Environment="ANTHROPIC_API_KEY=your_key_here"

# 5. Install services
sudo cp system/*.service /etc/systemd/system/
sudo cp system/*.timer /etc/systemd/system/
sudo systemctl daemon-reload

# 6. Enable services
sudo systemctl enable jarvisos-observer.service
sudo systemctl enable jarvisos-nightly.timer

# 7. Start services
sudo systemctl start jarvisos-observer.service
sudo systemctl start jarvisos-nightly.timer
```

---

## 🔧 System Services

### Observer Service
**File:** `jarvisos-observer.service`

- **Purpose:** Continuous system monitoring
- **Runs:** Always (background daemon)
- **Interval:** Observes every 10 seconds
- **Duration:** 5-minute observation windows
- **Restart:** Automatic on failure

```bash
# Status
sudo systemctl status jarvisos-observer

# Logs
sudo journalctl -u jarvisos-observer -f

# Restart
sudo systemctl restart jarvisos-observer
```

### Analyzer Service
**File:** `jarvisos-analyzer.service` + `jarvisos-analyzer.timer`

- **Purpose:** AI pattern analysis
- **Runs:** Every 6 hours
- **Trigger:** Timer-based
- **Depends:** Observer data

```bash
# Status
sudo systemctl status jarvisos-analyzer

# Run manually
sudo systemctl start jarvisos-analyzer

# Check timer
sudo systemctl list-timers jarvisos-analyzer
```

### Nightly Evolution Service
**File:** `jarvisos-nightly.service` + `jarvisos-nightly.timer`

- **Purpose:** Full evolution pipeline
- **Runs:** Every night at 3 AM
- **Steps:**
  1. Observe (1 hour)
  2. Analyze patterns
  3. Generate new code
- **Result:** New automation scripts created

```bash
# Status
sudo systemctl status jarvisos-nightly

# Run manually (test)
sudo systemctl start jarvisos-nightly

# Check timer
sudo systemctl list-timers jarvisos-nightly
```

---

## 📊 Monitoring

### Check Service Status
```bash
# All JarvisOS services
sudo systemctl status 'jarvisos-*'

# Specific service
sudo systemctl status jarvisos-observer
```

### View Logs
```bash
# Real-time logs
sudo journalctl -u jarvisos-observer -f

# Last 100 lines
sudo journalctl -u jarvisos-observer -n 100

# Today's logs
sudo journalctl -u jarvisos-observer --since today

# All JarvisOS logs
sudo journalctl -u 'jarvisos-*' -f
```

### Check Data
```bash
# Observations
sudo cat /opt/jarvisos/data/observations.json | jq

# Insights
sudo cat /opt/jarvisos/data/insights.json | jq

# Generated scripts
sudo ls -la /opt/jarvisos/generated_scripts/

# Logs
sudo tail -f /opt/jarvisos/logs/observer.log
```

---

## 🔄 Management

### Start/Stop Services
```bash
# Start
sudo systemctl start jarvisos-observer

# Stop
sudo systemctl stop jarvisos-observer

# Restart
sudo systemctl restart jarvisos-observer
```

### Enable/Disable Auto-Start
```bash
# Enable (start on boot)
sudo systemctl enable jarvisos-observer

# Disable
sudo systemctl disable jarvisos-observer
```

### Update JarvisOS
```bash
# Stop services
sudo systemctl stop 'jarvisos-*'

# Update code
cd /opt/jarvisos
sudo -u jarvis git pull

# Update dependencies
sudo -u jarvis venv/bin/pip install -r requirements.txt --upgrade

# Restart services
sudo systemctl start jarvisos-observer
sudo systemctl start jarvisos-nightly.timer
```

---

## 🐛 Troubleshooting

### Service Won't Start
```bash
# Check status
sudo systemctl status jarvisos-observer

# Check logs
sudo journalctl -u jarvisos-observer -n 50

# Common issues:
# 1. API key not set
# 2. Python dependencies missing
# 3. Permission issues
```

### No Observations
```bash
# Check if observer is running
sudo systemctl status jarvisos-observer

# Check data directory
sudo ls -la /opt/jarvisos/data/

# Check permissions
sudo chown -R jarvis:jarvis /opt/jarvisos
```

### API Errors
```bash
# Update API key
sudo nano /etc/systemd/system/jarvisos-observer.service
# Edit: Environment="ANTHROPIC_API_KEY=new_key"

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart jarvisos-observer
```

---

## 🔐 Security

### User Isolation
- JarvisOS runs as dedicated `jarvis` user
- Limited permissions
- No root access required for operation

### API Key Protection
- Stored in systemd service files
- Only readable by root
- Not in code or logs

### Data Privacy
- All data in `/opt/jarvisos/data/`
- Owned by `jarvis` user
- Not accessible to other users

---

## 🎯 Next Steps

### Phase 2: Custom Init System
Replace systemd with JarvisOS-native init:
- Boot directly into JarvisOS
- Custom service management
- Faster boot times

### Phase 3: Desktop Environment
- Minimal window manager
- JarvisOS-aware UI
- Real-time evolution display

### Phase 4: Custom Kernel
- Kernel modules for observation
- System-level integration
- Hardware optimization

---

## 📝 Files Reference

### Service Files
```
system/
├── jarvisos-observer.service    # Continuous monitoring
├── jarvisos-analyzer.service    # Pattern analysis
├── jarvisos-analyzer.timer      # Analysis schedule
├── jarvisos-generator.service   # Code generation
├── jarvisos-nightly.service     # Full pipeline
└── jarvisos-nightly.timer       # Nightly schedule
```

### Installation Locations
```
/opt/jarvisos/                   # Main installation
├── jarvis.py                    # CLI
├── jarvisos/                    # Core modules
├── data/                        # Observations & insights
├── generated_scripts/           # Auto-generated code
├── logs/                        # Application logs
└── venv/                        # Python environment

/etc/systemd/system/             # Service files
├── jarvisos-observer.service
├── jarvisos-nightly.timer
└── ...
```

---

## 🎉 Success Criteria

Your JarvisOS is properly installed when:

✅ `systemctl status jarvisos-observer` shows "active (running)"
✅ `/opt/jarvisos/data/observations.json` exists and grows
✅ `journalctl -u jarvisos-observer` shows regular observations
✅ Nightly timer is scheduled: `systemctl list-timers`
✅ Generated scripts appear in `/opt/jarvisos/generated_scripts/`

---

**You now have a self-building operating system running at the system level!** 🚀

The OS observes, learns, and evolves automatically in the background.
