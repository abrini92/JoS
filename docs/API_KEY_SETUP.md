# 🔑 API Key Setup Guide

Quick guide to configure your Anthropic API key for JarvisOS.

---

## 📋 Prerequisites

1. Get your API key from: https://console.anthropic.com/
2. Access to your JarvisOS installation

---

## 🚀 Setup Methods

### Method 1: .env File (Recommended)

**Pros:** Secure, easy to update, standard practice
**Cons:** None

```bash
# 1. Edit .env file
cd /home/ubuntu  # or /opt/jarvisos
nano .env

# 2. Add your key
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx

# 3. Save (Ctrl+X, Y, Enter)

# 4. Secure the file
chmod 600 .env

# 5. Reload services
sudo systemctl daemon-reload
sudo systemctl restart jarvisos-observer
sudo systemctl restart jarvisos-analyzer

# 6. Verify
sudo systemctl status jarvisos-analyzer
```

### Method 2: Direct in Service File (Quick)

**Pros:** Fast
**Cons:** Less secure, harder to update

```bash
# 1. Edit service file
sudo nano /etc/systemd/system/jarvisos-analyzer.service

# 2. Find line:
Environment="ANTHROPIC_API_KEY=test_placeholder"

# 3. Replace with your key:
Environment="ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx"

# 4. Save and reload
sudo systemctl daemon-reload
sudo systemctl restart jarvisos-analyzer
```

---

## ✅ Verification

### Test Analyzer
```bash
# Start analyzer
sudo systemctl start jarvisos-analyzer

# Check logs (should see AI analysis, no errors)
sudo journalctl -u jarvisos-analyzer -n 50 --no-pager

# Check insights file created
ls -lh /opt/jarvisos/data/insights.json
cat /opt/jarvisos/data/insights.json
```

### Test Generator
```bash
# Start generator
sudo systemctl start jarvisos-generator

# Check logs
sudo journalctl -u jarvisos-generator -n 50 --no-pager

# Check generated scripts
ls -la /opt/jarvisos/generated_scripts/
```

### Expected Success Output
```
✅ Analyzer logs should show:
   - "🧠 Analyzing observations..."
   - "🔍 INSIGHTS FROM CLAUDE:"
   - No "401 authentication_error"

✅ Files should exist:
   - /opt/jarvisos/data/insights.json
   - /opt/jarvisos/generated_scripts/*.py
```

---

## 🐛 Troubleshooting

### Error: "invalid x-api-key"
**Cause:** API key incorrect or not loaded

**Fix:**
```bash
# Check .env file
cat /home/ubuntu/.env

# Verify service reads it
sudo systemctl show jarvisos-analyzer | grep EnvironmentFile

# Reload
sudo systemctl daemon-reload
sudo systemctl restart jarvisos-analyzer
```

### Error: "rate_limit_error"
**Cause:** Too many API calls

**Fix:**
```bash
# Wait a few minutes
# Or increase interval in observer service
sudo nano /etc/systemd/system/jarvisos-observer.service
# Change: --interval 10 → --interval 30
```

### Error: Service won't start
**Cause:** Various

**Fix:**
```bash
# Check detailed logs
sudo journalctl -xeu jarvisos-analyzer

# Check service file syntax
sudo systemd-analyze verify jarvisos-analyzer.service

# Check permissions
ls -la /home/ubuntu/.env
# Should be: -rw------- (600)
```

---

## 🔒 Security Best Practices

### 1. File Permissions
```bash
# .env should be readable only by owner
chmod 600 /home/ubuntu/.env

# Verify
ls -la /home/ubuntu/.env
# Should show: -rw------- 1 ubuntu ubuntu
```

### 2. Don't Commit API Keys
```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore
```

### 3. Rotate Keys Regularly
```bash
# Update key in .env
nano /home/ubuntu/.env

# Restart services
sudo systemctl restart jarvisos-*
```

### 4. Use Environment-Specific Keys
```bash
# Development
ANTHROPIC_API_KEY=sk-ant-api03-dev-xxxxx

# Production
ANTHROPIC_API_KEY=sk-ant-api03-prod-xxxxx
```

---

## 📊 Monitoring API Usage

### Check Logs
```bash
# All API calls
sudo journalctl -u 'jarvisos-*' | grep -i "claude\|anthropic\|api"

# Count API calls today
sudo journalctl -u 'jarvisos-*' --since today | grep -c "Analyzing with Claude"
```

### Monitor Costs
- Visit: https://console.anthropic.com/settings/usage
- Set budget alerts
- Track token usage

---

## 🎯 Quick Reference

### Update API Key
```bash
# 1. Edit
nano /home/ubuntu/.env

# 2. Restart
sudo systemctl restart jarvisos-*

# 3. Verify
sudo systemctl status jarvisos-analyzer
```

### Test Full Pipeline
```bash
# 1. Observe (manual)
cd /opt/jarvisos
source venv/bin/activate
python jarvis.py observe --duration 30

# 2. Analyze
sudo systemctl start jarvisos-analyzer

# 3. Generate
sudo systemctl start jarvisos-generator

# 4. Check results
ls -la data/
ls -la generated_scripts/
```

### View All Service Status
```bash
sudo systemctl status 'jarvisos-*' --no-pager
```

---

## 📝 Configuration Files

### Current Setup
```
/home/ubuntu/.env                          ← API key here
/etc/systemd/system/jarvisos-*.service     ← Services read from .env
/opt/jarvisos/                             ← Working directory
```

### Service Configuration
```ini
[Service]
Type=oneshot
User=root
Group=root
WorkingDirectory=/opt/jarvisos
EnvironmentFile=/home/ubuntu/.env          ← Reads API key
Environment="PATH=/opt/jarvisos/venv/bin:/usr/local/bin:/usr/bin"
ExecStart=/opt/jarvisos/venv/bin/python /opt/jarvisos/jarvis.py analyze
```

---

## 🎉 Success Checklist

After setup, verify:

- [ ] .env file exists with real API key
- [ ] File permissions: 600 (read/write owner only)
- [ ] Services restarted: `sudo systemctl restart jarvisos-*`
- [ ] Analyzer runs without errors
- [ ] insights.json created
- [ ] Generator creates scripts
- [ ] No "401 authentication_error" in logs

---

**Once configured, JarvisOS will use AI automatically!** 🚀

The nightly timer will run analysis and generation every night at 3 AM.
