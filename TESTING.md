# 🧪 JarvisOS Testing Guide

Quick guide to test JarvisOS before first use.

## Pre-Flight Checklist

### 1. Install Dependencies

```bash
# Make sure you're in the JoS directory
cd /Users/abderrahim/JoS

# Run setup script
chmod +x setup.sh
./setup.sh

# OR manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set API Key

```bash
# Get your key from: https://console.anthropic.com/
export ANTHROPIC_API_KEY='your-api-key-here'

# Verify it's set
echo $ANTHROPIC_API_KEY
```

### 3. Test CLI

```bash
# Activate venv if not already
source venv/bin/activate

# Test help
python jarvis.py --help

# Test status
python jarvis.py status
```

## Quick Test (5 minutes)

### Test 1: Observer (30 seconds)

```bash
python jarvis.py observe --duration 30 --interval 5
```

**Expected Output**:
- Beautiful progress bar
- "Observation complete!" message
- File created: `data/observations.json`

**Verify**:
```bash
ls -lh data/observations.json
cat data/observations.json | head -20
```

### Test 2: Analyzer (30 seconds)

```bash
python jarvis.py analyze
```

**Expected Output**:
- "Analyzing with Claude AI..." message
- Beautiful insights display
- Usage patterns
- Automation opportunities
- File created: `data/insights.json`

**Verify**:
```bash
ls -lh data/insights.json
cat data/insights.json | head -30
```

### Test 3: Generator (1 minute)

```bash
python jarvis.py generate
```

**Expected Output**:
- Task suggestions from Claude
- "Generating script..." message
- Syntax-highlighted code preview
- "✅ Script generation complete!"
- File created in `generated_scripts/`

**Verify**:
```bash
ls -lh generated_scripts/
```

### Test 4: List Scripts (5 seconds)

```bash
python jarvis.py list
```

**Expected Output**:
- Table of available scripts
- Script names, sizes, dates

### Test 5: Dry Run (10 seconds)

```bash
python jarvis.py run 1 --dry-run
```

**Expected Output**:
- Script preview
- "DRY RUN MODE - Script not executed"

### Test 6: Execute (variable)

```bash
python jarvis.py run 1
```

**Expected Output**:
- Script preview
- Approval prompt
- Execution output (if approved)
- Success or error message

## Full Workflow Test (10 minutes)

```bash
# 1. Clean start
rm -rf data/ generated_scripts/

# 2. Long observation (5 minutes)
python jarvis.py observe --duration 300 --interval 10

# 3. Analyze
python jarvis.py analyze

# 4. Generate multiple tasks
python jarvis.py generate --task-index 0
python jarvis.py generate --task-index 1
python jarvis.py generate --task-index 2

# 5. List all
python jarvis.py list

# 6. Execute first script
python jarvis.py run 1 --dry-run
python jarvis.py run 1
```

## Troubleshooting Tests

### Test: Missing API Key

```bash
# Unset key
unset ANTHROPIC_API_KEY

# Try to analyze
python jarvis.py analyze
```

**Expected**: Clear error message about missing API key

### Test: No Observations

```bash
# Remove observations
rm -f data/observations.json

# Try to analyze
python jarvis.py analyze
```

**Expected**: Error message telling you to run `observe` first

### Test: No Insights

```bash
# Remove insights
rm -f data/insights.json

# Try to generate
python jarvis.py generate
```

**Expected**: Error message telling you to run `analyze` first

### Test: Invalid Script ID

```bash
python jarvis.py run 999
```

**Expected**: Error message about invalid script ID

## Performance Tests

### Test: Observer Performance

```bash
# Monitor system resources while observing
python jarvis.py observe --duration 60 --interval 1 &
top -pid $!
```

**Expected**: Low CPU and memory usage

### Test: Large Observation

```bash
# Long observation
python jarvis.py observe --duration 600 --interval 5
```

**Expected**: 
- Smooth progress
- No memory leaks
- File size reasonable (<1MB)

## Integration Tests

### Test: Full Pipeline

```bash
#!/bin/bash
set -e

echo "Testing full JarvisOS pipeline..."

# Clean
rm -rf data/ generated_scripts/

# Observe
echo "1. Observing..."
python jarvis.py observe --duration 30 --interval 5

# Analyze
echo "2. Analyzing..."
python jarvis.py analyze

# Generate
echo "3. Generating..."
python jarvis.py generate

# List
echo "4. Listing..."
python jarvis.py list

# Status
echo "5. Status..."
python jarvis.py status

echo "✅ All tests passed!"
```

Save as `test_pipeline.sh` and run:
```bash
chmod +x test_pipeline.sh
./test_pipeline.sh
```

## Manual Verification

### Check File Structure

```bash
# Should exist
ls jarvis.py
ls requirements.txt
ls setup.sh
ls README.md
ls jarvisos/core/observer.py
ls jarvisos/core/analyzer.py
ls jarvisos/core/generator.py
ls jarvisos/core/executor.py

# Should be created after running
ls data/observations.json
ls data/insights.json
ls generated_scripts/
```

### Check Permissions

```bash
# Should be executable
ls -l jarvis.py | grep "x"
ls -l setup.sh | grep "x"
```

### Check Python Syntax

```bash
# Validate all Python files
python -m py_compile jarvis.py
python -m py_compile jarvisos/core/observer.py
python -m py_compile jarvisos/core/analyzer.py
python -m py_compile jarvisos/core/generator.py
python -m py_compile jarvisos/core/executor.py
```

## Expected File Sizes

After running full workflow:

```
jarvis.py              ~8-10 KB
requirements.txt       ~750 bytes
observer.py            ~4-5 KB
analyzer.py            ~7-8 KB
generator.py           ~9-10 KB
executor.py            ~7-8 KB
observations.json      ~50-500 KB (depends on duration)
insights.json          ~2-5 KB
generated_script.py    ~1-3 KB
```

## Success Criteria

✅ **All tests pass if**:
1. No Python syntax errors
2. CLI help displays correctly
3. Observer collects data
4. Analyzer produces insights
5. Generator creates valid Python
6. Executor runs safely
7. All error messages are clear
8. No crashes or hangs

## Common Issues

### Issue: Import errors
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Permission denied
**Solution**: Make scripts executable
```bash
chmod +x jarvis.py setup.sh
```

### Issue: API errors
**Solution**: Check API key
```bash
echo $ANTHROPIC_API_KEY
```

### Issue: No data directory
**Solution**: Create it
```bash
mkdir -p data generated_scripts
```

## Ready to Ship?

Run this final checklist:

```bash
# ✅ Dependencies installed
pip list | grep anthropic
pip list | grep rich
pip list | grep psutil

# ✅ API key set
echo $ANTHROPIC_API_KEY

# ✅ CLI works
python jarvis.py --help

# ✅ Status shows ready
python jarvis.py status

# ✅ Full workflow works
python jarvis.py observe --duration 30
python jarvis.py analyze
python jarvis.py generate
python jarvis.py list
```

If all pass: **🎉 Ready to ship!**

---

**Happy testing! 🧪**
