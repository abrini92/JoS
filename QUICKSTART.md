# 🚀 JarvisOS Quick Start Guide

Get JarvisOS running in **5 minutes**.

## Prerequisites

- Python 3.11+
- Claude API key ([get free key](https://console.anthropic.com/))

## Installation

```bash
# 1. Clone or navigate to JarvisOS directory
cd JoS

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Set your API key
export ANTHROPIC_API_KEY='your-key-here'
```

## Your First Automation (2 minutes)

### Step 1: Observe (30 seconds)

```bash
python jarvis.py observe --duration 30 --interval 5
```

This monitors your system for 30 seconds.

### Step 2: Analyze (20 seconds)

```bash
python jarvis.py analyze
```

Claude AI analyzes your behavior and suggests automations.

### Step 3: Generate (30 seconds)

```bash
python jarvis.py generate
```

JarvisOS creates a custom Python script for you.

### Step 4: Execute (40 seconds)

```bash
# List scripts
python jarvis.py list

# Preview (dry run)
python jarvis.py run 1 --dry-run

# Execute
python jarvis.py run 1
```

## 🎉 Done!

You just:
1. ✅ Observed your system
2. ✅ Got AI insights
3. ✅ Generated custom automation
4. ✅ Executed it safely

## What's Next?

### Run a Real Observation

```bash
# Observe for 5 minutes
python jarvis.py observe --duration 300 --interval 10

# Analyze
python jarvis.py analyze

# Generate automation
python jarvis.py generate
```

### Check System Status

```bash
python jarvis.py status
```

### Generate More Automations

```bash
# Generate second task
python jarvis.py generate --task-index 1

# Generate third task
python jarvis.py generate --task-index 2
```

## Common Commands

```bash
# Observe for 10 minutes
python jarvis.py observe --duration 600

# Analyze observations
python jarvis.py analyze

# Generate automation (first task)
python jarvis.py generate

# List all scripts
python jarvis.py list

# Preview script
python jarvis.py run 1 --dry-run

# Execute script
python jarvis.py run 1

# Check status
python jarvis.py status
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found"

```bash
export ANTHROPIC_API_KEY='your-key-here'

# Or add to .env file
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

### "No observations file found"

Run observation first:
```bash
python jarvis.py observe
```

### "No insights file found"

Run analysis first:
```bash
python jarvis.py analyze
```

## Tips

1. **Longer observations = Better insights**
   - Run for at least 5-10 minutes for meaningful data

2. **Review generated code**
   - Always preview with `--dry-run` first
   - Read the code before executing

3. **Multiple automations**
   - Generate different tasks with `--task-index`
   - Build a library of personal tools

4. **Daily workflow**
   - Morning: `jarvis observe` while working
   - Evening: `jarvis analyze && jarvis generate`
   - Night: Review and execute scripts

## Need Help?

- Read the full [README.md](README.md)
- Check [VISION.md](docs/VISION.md) for philosophy
- Open an issue on GitHub
- Join the community

---

**Happy automating! 🤖**
