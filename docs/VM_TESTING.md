# 🖥️ JarvisOS VM Testing Guide

Quick guide to test JarvisOS on a Linux VM

---

## Option 1: Multipass (Fastest - Recommended)

Multipass = Ubuntu VMs in seconds on Mac

### Install Multipass
```bash
brew install multipass
```

### Create Ubuntu VM
```bash
# Launch Ubuntu VM
multipass launch --name jarvisos --cpus 2 --memory 2G --disk 10G

# Get shell
multipass shell jarvisos
```

### Install JarvisOS
```bash
# Inside VM
# Install dependencies
sudo apt update
sudo apt install -y python3.11 python3.11-venv git

# Clone JarvisOS (or copy files)
git clone https://github.com/yourusername/jarvisos.git
cd jarvisos

# Run system installer
sudo ./install-system.sh
```

### Verify Installation
```bash
# Check service status
sudo systemctl status jarvisos-observer

# View logs
sudo journalctl -u jarvisos-observer -f

# Check data
sudo ls -la /opt/jarvisos/data/

# Check timers
sudo systemctl list-timers jarvisos-*
```

### Test Evolution
```bash
# Manually trigger nightly evolution
sudo systemctl start jarvisos-nightly

# Check generated scripts
sudo ls -la /opt/jarvisos/generated_scripts/
```

### Cleanup
```bash
# Exit VM
exit

# Stop VM
multipass stop jarvisos

# Delete VM
multipass delete jarvisos
multipass purge
```

---

## Option 2: UTM (Mac with Apple Silicon)

UTM = Free VM app for Mac

### Install UTM
```bash
brew install --cask utm
```

### Setup
1. Download Ubuntu Server 22.04 ARM64 ISO
2. Open UTM → Create New VM
3. Select "Virtualize" → Linux
4. Choose downloaded ISO
5. Allocate: 2 CPU, 2GB RAM, 10GB disk
6. Start VM and install Ubuntu

### Install JarvisOS
Same as Multipass option above

---

## Option 3: Docker (Quick Test)

Test in Docker container (not full OS, but quick)

### Create Dockerfile
```dockerfile
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    systemd \
    git

# Copy JarvisOS
COPY . /opt/jarvisos
WORKDIR /opt/jarvisos

# Install Python deps
RUN python3.11 -m venv venv && \
    venv/bin/pip install -r requirements.txt

# Create directories
RUN mkdir -p data generated_scripts logs

CMD ["/bin/bash"]
```

### Build and Run
```bash
# Build
docker build -t jarvisos .

# Run
docker run -it jarvisos

# Inside container, test manually
python jarvis.py observe --duration 30
python jarvis.py analyze
python jarvis.py generate
```

---

## Quick Test Checklist

### ✅ Installation
- [ ] `install-system.sh` runs without errors
- [ ] User `jarvis` created
- [ ] Files in `/opt/jarvisos/`
- [ ] Services installed in `/etc/systemd/system/`

### ✅ Services
- [ ] `systemctl status jarvisos-observer` shows "active (running)"
- [ ] `systemctl list-timers` shows jarvisos timers
- [ ] `journalctl -u jarvisos-observer` shows logs

### ✅ Functionality
- [ ] Observations created in `/opt/jarvisos/data/observations.json`
- [ ] File grows over time
- [ ] Analyzer runs: `sudo systemctl start jarvisos-analyzer`
- [ ] Insights created in `/opt/jarvisos/data/insights.json`
- [ ] Generator creates scripts in `/opt/jarvisos/generated_scripts/`

### ✅ Persistence
- [ ] Reboot VM: `sudo reboot`
- [ ] After reboot, services auto-start
- [ ] Data persists across reboots

---

## Expected Results

### After Installation
```bash
$ sudo systemctl status jarvisos-observer
● jarvisos-observer.service - JarvisOS Observer
   Loaded: loaded (/etc/systemd/system/jarvisos-observer.service)
   Active: active (running) since ...
   
$ sudo systemctl list-timers jarvisos-*
NEXT                         LEFT          LAST  PASSED  UNIT
Thu 2025-10-17 03:00:00 UTC  2h 27min left n/a   n/a     jarvisos-nightly.timer
Thu 2025-10-17 06:00:00 UTC  5h 27min left n/a   n/a     jarvisos-analyzer.timer
```

### After 5 Minutes
```bash
$ sudo ls -lh /opt/jarvisos/data/
-rw-r--r-- 1 jarvis jarvis 150K Oct 17 00:35 observations.json
```

### After Manual Analysis
```bash
$ sudo systemctl start jarvisos-analyzer
$ sudo ls -lh /opt/jarvisos/data/
-rw-r--r-- 1 jarvis jarvis 150K Oct 17 00:35 observations.json
-rw-r--r-- 1 jarvis jarvis   5K Oct 17 00:40 insights.json
```

### After Manual Generation
```bash
$ sudo systemctl start jarvisos-generator
$ sudo ls -lh /opt/jarvisos/generated_scripts/
-rw-r--r-- 1 jarvis jarvis 3.5K Oct 17 00:45 process_cleanup_*.py
```

---

## Troubleshooting

### Service Won't Start
```bash
# Check detailed status
sudo systemctl status jarvisos-observer -l

# Check logs
sudo journalctl -u jarvisos-observer -n 100 --no-pager

# Common fixes:
sudo systemctl daemon-reload
sudo systemctl restart jarvisos-observer
```

### Permission Errors
```bash
# Fix ownership
sudo chown -R jarvis:jarvis /opt/jarvisos

# Fix permissions
sudo chmod +x /opt/jarvisos/jarvis.py
```

### API Key Issues
```bash
# Edit service file
sudo nano /etc/systemd/system/jarvisos-observer.service

# Update API key line:
Environment="ANTHROPIC_API_KEY=your_actual_key"

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart jarvisos-observer
```

---

## Performance Monitoring

### Resource Usage
```bash
# CPU/Memory usage
top -p $(pgrep -f jarvisos)

# Systemd resource stats
systemd-cgtop
```

### Log Size
```bash
# Check log sizes
du -sh /opt/jarvisos/logs/*
journalctl --disk-usage
```

---

## Next Steps After Successful Test

1. ✅ Verify all services work
2. ✅ Test full nightly evolution
3. ✅ Confirm reboot persistence
4. 📝 Document any issues
5. 🚀 Move to Phase 3 (Custom ISO)

---

**Goal:** Confirm JarvisOS runs as true system service on Linux

**Success:** Services auto-start, data persists, evolution works
