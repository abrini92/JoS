#!/bin/bash
# JarvisOS - Complete Test Suite
# Run this before shipping to catch ALL bugs

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0
TESTS_WARNING=0

# Test result
test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((TESTS_FAILED++))
        [ -n "$3" ] && echo -e "   ${RED}Error: $3${NC}"
    fi
}

test_warning() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
    ((TESTS_WARNING++))
}

test_info() {
    echo -e "${BLUE}ℹ️  INFO${NC}: $1"
}

echo "🧪 JarvisOS Complete Test Suite"
echo "================================="
echo ""

# Test 1: File structure
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣ Testing File Structure"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

CRITICAL_FILES=(
    "jarvis.py"
    "install.sh"
    "requirements.txt"
    "README.md"
    "jarvisos/core/ai_brain_ollama.py"
    "jarvisos/core/ai_brain_unified.py"
    "jarvisos/onboarding/interactive_welcome.py"
    "jarvisos/onboarding/__init__.py"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        test_result 0 "File exists: $file"
    else
        test_result 1 "File missing: $file"
    fi
done

# Test 2: Python syntax
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣ Testing Python Syntax"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

find jarvisos -name "*.py" -type f | while read pyfile; do
    if python3 -m py_compile "$pyfile" 2>/dev/null; then
        test_result 0 "Syntax OK: $pyfile"
    else
        test_result 1 "Syntax error: $pyfile" "$(python3 -m py_compile "$pyfile" 2>&1)"
    fi
done

if python3 -m py_compile jarvis.py 2>/dev/null; then
    test_result 0 "Syntax OK: jarvis.py"
else
    test_result 1 "Syntax error: jarvis.py"
fi

# Test 3: Script permissions
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣ Testing Script Permissions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SCRIPTS=(
    "install.sh"
    "setup-boot-experience.sh"
    "validate_before_ship.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            test_result 0 "Executable: $script"
        else
            test_warning "Not executable: $script (fixing...)"
            chmod +x "$script"
        fi
    fi
done

# Test 4: Python imports
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣ Testing Python Imports"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 -c "
try:
    import sys
    sys.path.insert(0, 'jarvisos')
    from core.ai_brain_ollama import OllamaAIBrain
    from core.ai_brain_unified import UnifiedAIBrain
    from onboarding import JarvisOnboarding
    print('OK')
except Exception as e:
    print(f'FAIL: {e}')
    sys.exit(1)
" 2>/dev/null

if [ $? -eq 0 ]; then
    test_result 0 "All imports work"
else
    test_result 1 "Import errors detected"
fi

# Test 5: Dependencies in requirements.txt
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣ Testing requirements.txt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REQUIRED_DEPS=("rich" "anthropic" "psutil" "pyttsx3")

for dep in "${REQUIRED_DEPS[@]}"; do
    if grep -q "$dep" requirements.txt; then
        test_result 0 "Dependency listed: $dep"
    else
        test_result 1 "Missing dependency: $dep"
    fi
done

# Test 6: Git status
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6️⃣ Testing Git Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d ".git" ]; then
    test_result 0 "Git repository exists"
    
    UNCOMMITTED=$(git status --porcelain | wc -l | tr -d ' ')
    if [ "$UNCOMMITTED" -gt 0 ]; then
        test_warning "$UNCOMMITTED uncommitted changes"
        test_info "Run: git add -A && git commit -m 'Pre-launch commit'"
    else
        test_result 0 "No uncommitted changes"
    fi
    
    # Check remote
    if git remote -v | grep -q "origin"; then
        test_result 0 "Git remote configured"
    else
        test_warning "No git remote configured"
    fi
else
    test_result 1 "Not a git repository"
fi

# Test 7: Documentation
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7️⃣ Testing Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DOCS=(
    "README.md"
    "QUICKSTART_UTM.md"
    "OLLAMA_INTEGRATION.md"
    "DEPENDENCIES.md"
    "FOUNDER_MODE.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        test_result 0 "Doc exists: $doc"
        
        # Check if not empty
        if [ -s "$doc" ]; then
            test_result 0 "Doc has content: $doc"
        else
            test_result 1 "Doc is empty: $doc"
        fi
    else
        test_warning "Doc missing: $doc"
    fi
done

# Test 8: Ollama integration
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "8️⃣ Testing Ollama Integration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v ollama &> /dev/null; then
    test_result 0 "Ollama installed"
    
    # Check version
    VERSION=$(ollama --version 2>/dev/null)
    test_info "Ollama version: $VERSION"
    
    # Check if running
    if pgrep -x "ollama" > /dev/null; then
        test_result 0 "Ollama is running"
    else
        test_warning "Ollama not running"
    fi
    
    # Check models
    if ollama list 2>/dev/null | grep -q "llama3.2"; then
        test_result 0 "llama3.2 model installed"
    else
        test_warning "llama3.2 model not installed"
        test_info "Run: ollama pull llama3.2"
    fi
else
    test_warning "Ollama not installed (will be installed by install.sh)"
fi

# Test 9: Code quality
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "9️⃣ Testing Code Quality"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for common issues
if grep -r "print(" jarvisos/*.py | grep -v "#" | grep -v "console.print" | head -1 > /dev/null; then
    test_warning "Found print() statements (use console.print instead)"
fi

if grep -r "TODO" jarvisos/*.py | head -1 > /dev/null; then
    test_warning "Found TODO comments"
fi

if grep -r "FIXME" jarvisos/*.py | head -1 > /dev/null; then
    test_warning "Found FIXME comments"
fi

# Check line lengths
LONG_LINES=$(find jarvisos -name "*.py" -exec awk 'length>120' {} + | wc -l | tr -d ' ')
if [ "$LONG_LINES" -gt 10 ]; then
    test_warning "$LONG_LINES lines exceed 120 characters"
fi

# Test 10: Installation script
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔟 Testing Installation Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for error handling
if grep -q "error_exit" install.sh; then
    test_result 0 "Error handling present"
else
    test_result 1 "No error handling in install.sh"
fi

# Check for set -e
if head -10 install.sh | grep -q "set -e"; then
    test_result 0 "Exit on error enabled (set -e)"
else
    test_result 1 "Exit on error not enabled"
fi

# Check for validation
if grep -q "apt-get update" install.sh; then
    test_result 0 "System packages installation present"
else
    test_result 1 "No system packages installation"
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 TEST SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "Passed:   ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Failed:   ${RED}${TESTS_FAILED}${NC}"
echo -e "Warnings: ${YELLOW}${TESTS_WARNING}${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ ALL CRITICAL TESTS PASSED!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "🚀 Ready to ship!"
    echo ""
    echo "Next steps:"
    echo "1. Test in clean VM (UTM)"
    echo "2. Fix any issues found"
    echo "3. Commit and push"
    echo "4. Create release"
    echo "5. Launch!"
    exit 0
elif [ $TESTS_FAILED -le 3 ]; then
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}⚠️  MINOR ISSUES DETECTED${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Fix these issues before shipping:"
    echo "- Review failed tests above"
    echo "- Run this script again"
    exit 1
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}❌ CRITICAL ISSUES DETECTED${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "DO NOT SHIP until these are fixed!"
    echo "Review all failed tests above."
    exit 1
fi
