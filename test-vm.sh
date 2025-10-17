#!/bin/bash
#
# JarvisOS VM Test Script
# Quick testing of JarvisOS in Multipass VM
#

set -e

echo "🧪 JarvisOS VM Test Suite"
echo "========================="
echo ""

VM_NAME="jarvisos"

# Check if VM exists
if ! multipass list | grep -q "$VM_NAME"; then
    echo "❌ VM '$VM_NAME' not found"
    echo "Create it first with: multipass launch --name $VM_NAME"
    exit 1
fi

# Check if VM is running
if ! multipass list | grep "$VM_NAME" | grep -q "Running"; then
    echo "🔄 Starting VM..."
    multipass start "$VM_NAME"
    sleep 5
fi

echo "✅ VM is running"
echo ""

# Test 1: System Status
echo "📊 Test 1: System Status"
echo "------------------------"
multipass exec "$VM_NAME" -- sudo systemctl is-active jarvisos-observer || echo "Observer not running"
multipass exec "$VM_NAME" -- sudo systemctl is-enabled jarvisos-observer || echo "Observer not enabled"
echo ""

# Test 2: Data Collection
echo "💾 Test 2: Data Collection"
echo "--------------------------"
multipass exec "$VM_NAME" -- bash -c "
if [ -f /opt/jarvisos/data/observations.json ]; then
    SIZE=\$(du -h /opt/jarvisos/data/observations.json | cut -f1)
    echo \"✅ Observations: \$SIZE\"
else
    echo \"❌ No observations yet\"
fi
"
echo ""

# Test 3: DNA Profile
echo "🧬 Test 3: DNA Profile"
echo "----------------------"
multipass exec "$VM_NAME" -- sudo bash -c "
cd /opt/jarvisos &&
source venv/bin/activate &&
python jarvis.py dna 2>&1 | tail -15
"
echo ""

# Test 4: Evolution
echo "🔬 Test 4: Evolution Engine"
echo "---------------------------"
multipass exec "$VM_NAME" -- sudo bash -c "
cd /opt/jarvisos &&
source venv/bin/activate &&
python jarvis.py evolve 2>&1 | tail -10
"
echo ""

# Test 5: Services
echo "⚙️  Test 5: Services Status"
echo "---------------------------"
multipass exec "$VM_NAME" -- sudo systemctl list-units 'jarvisos-*' --no-pager
echo ""

# Test 6: Timers
echo "⏰ Test 6: Timers"
echo "-----------------"
multipass exec "$VM_NAME" -- sudo systemctl list-timers 'jarvisos-*' --no-pager
echo ""

# Test 7: Logs
echo "📝 Test 7: Recent Logs"
echo "----------------------"
multipass exec "$VM_NAME" -- sudo journalctl -u jarvisos-observer -n 5 --no-pager
echo ""

# Summary
echo "📊 Test Summary"
echo "==============="
echo ""

# Count observations
OBS_COUNT=$(multipass exec "$VM_NAME" -- bash -c "
if [ -f /opt/jarvisos/data/observations.json ]; then
    grep -c '\"iteration\"' /opt/jarvisos/data/observations.json 2>/dev/null || echo 0
else
    echo 0
fi
")

echo "Observations collected: $OBS_COUNT"

# Check services
OBSERVER_STATUS=$(multipass exec "$VM_NAME" -- sudo systemctl is-active jarvisos-observer 2>/dev/null || echo "inactive")
echo "Observer status: $OBSERVER_STATUS"

# Check DNA
DNA_EXISTS=$(multipass exec "$VM_NAME" -- bash -c "
[ -f /opt/jarvisos/data/user_dna.json ] && echo 'yes' || echo 'no'
")
echo "DNA profile: $DNA_EXISTS"

echo ""
echo "✅ Test suite complete!"
echo ""
echo "💡 Quick commands:"
echo "  multipass shell $VM_NAME           # Enter VM"
echo "  multipass stop $VM_NAME            # Stop VM"
echo "  multipass start $VM_NAME           # Start VM"
echo "  multipass delete $VM_NAME          # Delete VM"
echo ""
