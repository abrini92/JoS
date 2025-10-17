#!/bin/bash
#
# JarvisOS Installation Verification Script
# Checks that everything is working correctly
#

set -e

echo "🔍 JarvisOS Installation Verification"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

check_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
}

echo "📋 System Checks"
echo "================"
echo ""

# Check 1: Python version
echo -n "Checking Python version... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    check_pass "Python $PYTHON_VERSION installed"
else
    check_fail "Python 3 not found"
fi

# Check 2: Virtual environment
echo -n "Checking virtual environment... "
if [ -d "/opt/jarvisos/venv" ]; then
    check_pass "Virtual environment exists"
else
    check_fail "Virtual environment not found at /opt/jarvisos/venv"
fi

# Check 3: Dependencies
echo -n "Checking Python dependencies... "
if /opt/jarvisos/venv/bin/pip list | grep -q "anthropic"; then
    check_pass "Dependencies installed"
else
    check_fail "Dependencies missing"
fi

echo ""
echo "📁 Directory Checks"
echo "==================="
echo ""

# Check 4: Installation directory
echo -n "Checking installation directory... "
if [ -d "/opt/jarvisos" ]; then
    check_pass "Installation directory exists"
else
    check_fail "Installation directory not found"
fi

# Check 5: Data directory
echo -n "Checking data directory... "
if [ -d "/opt/jarvisos/data" ]; then
    check_pass "Data directory exists"
else
    check_fail "Data directory not found"
fi

# Check 6: Logs directory
echo -n "Checking logs directory... "
if [ -d "/opt/jarvisos/logs" ]; then
    check_pass "Logs directory exists"
else
    check_fail "Logs directory not found"
fi

# Check 7: Generated scripts directory
echo -n "Checking generated_scripts directory... "
if [ -d "/opt/jarvisos/generated_scripts" ]; then
    check_pass "Generated scripts directory exists"
else
    check_fail "Generated scripts directory not found"
fi

echo ""
echo "⚙️  Service Checks"
echo "=================="
echo ""

# Check 8: Observer service installed
echo -n "Checking observer service... "
if systemctl list-unit-files | grep -q "jarvisos-observer.service"; then
    check_pass "Observer service installed"
else
    check_fail "Observer service not installed"
fi

# Check 9: Observer service running
echo -n "Checking observer service status... "
if systemctl is-active --quiet jarvisos-observer; then
    check_pass "Observer service is running"
else
    check_warn "Observer service is not running"
fi

# Check 10: Observer service enabled
echo -n "Checking observer service auto-start... "
if systemctl is-enabled --quiet jarvisos-observer; then
    check_pass "Observer service enabled for boot"
else
    check_warn "Observer service not enabled for boot"
fi

# Check 11: Nightly timer installed
echo -n "Checking nightly timer... "
if systemctl list-unit-files | grep -q "jarvisos-nightly.timer"; then
    check_pass "Nightly timer installed"
else
    check_fail "Nightly timer not installed"
fi

# Check 12: Nightly timer active
echo -n "Checking nightly timer status... "
if systemctl is-active --quiet jarvisos-nightly.timer; then
    check_pass "Nightly timer is active"
else
    check_warn "Nightly timer is not active"
fi

echo ""
echo "🔑 Configuration Checks"
echo "======================="
echo ""

# Check 13: API key configured
echo -n "Checking API key... "
if [ -f "/home/ubuntu/.env" ]; then
    if grep -q "ANTHROPIC_API_KEY" /home/ubuntu/.env; then
        API_KEY=$(grep "ANTHROPIC_API_KEY" /home/ubuntu/.env | cut -d'=' -f2)
        if [ "$API_KEY" != "test_placeholder" ] && [ "$API_KEY" != "test_placeholder_key" ] && [ "$API_KEY" != "your_key_here" ]; then
            check_pass "API key configured"
        else
            check_warn "API key is placeholder (update with real key)"
        fi
    else
        check_fail "API key not found in .env"
    fi
else
    check_fail ".env file not found"
fi

# Check 14: .env permissions
echo -n "Checking .env permissions... "
if [ -f "/home/ubuntu/.env" ]; then
    PERMS=$(stat -c %a /home/ubuntu/.env 2>/dev/null || stat -f %A /home/ubuntu/.env)
    if [ "$PERMS" = "600" ]; then
        check_pass ".env has secure permissions (600)"
    else
        check_warn ".env permissions are $PERMS (should be 600)"
    fi
fi

echo ""
echo "💾 Data Checks"
echo "=============="
echo ""

# Check 15: Observations file
echo -n "Checking observations data... "
if [ -f "/opt/jarvisos/data/observations.json" ]; then
    SIZE=$(du -h /opt/jarvisos/data/observations.json | cut -f1)
    check_pass "Observations file exists ($SIZE)"
else
    check_warn "No observations file yet (run observer first)"
fi

# Check 16: Insights file
echo -n "Checking insights data... "
if [ -f "/opt/jarvisos/data/insights.json" ]; then
    SIZE=$(du -h /opt/jarvisos/data/insights.json | cut -f1)
    check_pass "Insights file exists ($SIZE)"
else
    check_warn "No insights file yet (run analyzer first)"
fi

# Check 17: Generated scripts
echo -n "Checking generated scripts... "
SCRIPT_COUNT=$(find /opt/jarvisos/generated_scripts -name "*.py" 2>/dev/null | wc -l)
if [ "$SCRIPT_COUNT" -gt 0 ]; then
    check_pass "$SCRIPT_COUNT generated scripts found"
else
    check_warn "No generated scripts yet (run generator first)"
fi

echo ""
echo "📊 Summary"
echo "=========="
echo ""
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 All critical checks passed!${NC}"
    echo ""
    echo "✅ JarvisOS is properly installed and running"
    echo ""
    echo "Next steps:"
    echo "  1. Update API key: nano /home/ubuntu/.env"
    echo "  2. Test analyzer: sudo systemctl start jarvisos-analyzer"
    echo "  3. View logs: sudo journalctl -u jarvisos-observer -f"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Some checks failed${NC}"
    echo ""
    echo "Please fix the failed checks and run again."
    echo ""
    exit 1
fi
