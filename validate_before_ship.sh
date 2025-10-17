#!/bin/bash
# Pre-ship validation - Check everything before shipping

set -e

echo "🔍 JarvisOS Pre-Ship Validation"
echo "================================"
echo ""

ERRORS=0
WARNINGS=0

# Check 1: Critical files exist
echo "1️⃣ Checking critical files..."
FILES=(
    "jarvis.py"
    "install.sh"
    "setup-boot-experience.sh"
    "requirements.txt"
    "jarvisos/core/ai_brain_ollama.py"
    "jarvisos/core/ai_brain_unified.py"
    "jarvisos/onboarding/__init__.py"
    "jarvisos/onboarding/interactive_welcome.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (MISSING)"
        ((ERRORS++))
    fi
done

# Check 2: Scripts are executable
echo ""
echo "2️⃣ Checking script permissions..."
SCRIPTS=(
    "install.sh"
    "setup-boot-experience.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -x "$script" ]; then
        echo "   ✅ $script (executable)"
    else
        echo "   ⚠️  $script (not executable)"
        chmod +x "$script"
        echo "      → Fixed!"
    fi
done

# Check 3: Python syntax
echo ""
echo "3️⃣ Checking Python syntax..."
PYTHON_FILES=(
    "jarvis.py"
    "jarvisos/core/ai_brain_ollama.py"
    "jarvisos/core/ai_brain_unified.py"
    "jarvisos/onboarding/interactive_welcome.py"
)

for file in "${PYTHON_FILES[@]}"; do
    if python3 -m py_compile "$file" 2>/dev/null; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (SYNTAX ERROR)"
        ((ERRORS++))
    fi
done

# Check 4: Requirements file valid
echo ""
echo "4️⃣ Checking requirements.txt..."
if [ -f "requirements.txt" ]; then
    if grep -q "rich" requirements.txt && \
       grep -q "anthropic" requirements.txt && \
       grep -q "psutil" requirements.txt; then
        echo "   ✅ requirements.txt looks good"
    else
        echo "   ⚠️  requirements.txt might be incomplete"
        ((WARNINGS++))
    fi
else
    echo "   ❌ requirements.txt missing"
    ((ERRORS++))
fi

# Check 5: Documentation exists
echo ""
echo "5️⃣ Checking documentation..."
DOCS=(
    "README.md"
    "QUICKSTART_UTM.md"
    "OLLAMA_INTEGRATION.md"
    "FOUNDER_MODE.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo "   ✅ $doc"
    else
        echo "   ⚠️  $doc (missing, nice to have)"
        ((WARNINGS++))
    fi
done

# Check 6: Git status
echo ""
echo "6️⃣ Checking git status..."
if [ -d ".git" ]; then
    UNCOMMITTED=$(git status --porcelain | wc -l)
    if [ "$UNCOMMITTED" -gt 0 ]; then
        echo "   ⚠️  $UNCOMMITTED uncommitted changes"
        echo "      Files:"
        git status --short | head -5
        if [ "$UNCOMMITTED" -gt 5 ]; then
            echo "      ... and $((UNCOMMITTED - 5)) more"
        fi
        ((WARNINGS++))
    else
        echo "   ✅ No uncommitted changes"
    fi
else
    echo "   ⚠️  Not a git repository"
    ((WARNINGS++))
fi

# Summary
echo ""
echo "================================"
echo "🎯 Validation Summary"
echo "================================"
echo ""
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ Ready to ship!"
    echo ""
    echo "Next steps:"
    echo "1. Test in clean VM: multipass launch ubuntu"
    echo "2. Run: curl -sSL https://raw.githubusercontent.com/abrini92/JoS/main/install.sh | bash"
    echo "3. Verify boot and onboarding work"
    echo "4. Record demo video"
    echo "5. Ship!"
    exit 0
else
    echo "❌ NOT ready to ship - fix errors first!"
    exit 1
fi
