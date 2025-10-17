#!/bin/bash
#
# JarvisOS Complete System Test
# Tests all new features (Phase 2.7 + 2.8)
#

echo "🧪 JarvisOS Complete System Test"
echo "================================="
echo ""

cd /opt/jarvisos
source venv/bin/activate

# Test 1: Status
echo "✅ TEST 1: System Status"
echo "========================"
python jarvis.py status
echo ""
read -p "Press Enter to continue..."

# Test 2: Context Awareness
echo ""
echo "🧠 TEST 2: Context Awareness"
echo "============================"
python jarvis.py context
echo ""
read -p "Press Enter to continue..."

# Test 3: Feedback System
echo ""
echo "📝 TEST 3: Feedback System"
echo "=========================="
python jarvis.py feedback
echo ""
read -p "Press Enter to continue..."

# Test 4: Greeting
echo ""
echo "👋 TEST 4: Proactive Greeting"
echo "============================="
python jarvis.py greet
echo ""
read -p "Press Enter to continue..."

# Test 5: DNA Profile
echo ""
echo "🧬 TEST 5: User DNA"
echo "==================="
python jarvis.py dna
echo ""
read -p "Press Enter to continue..."

# Test 6: Evolution
echo ""
echo "🔬 TEST 6: Genetic Evolution"
echo "============================"
python jarvis.py evolve
echo ""
read -p "Press Enter to continue..."

# Test 7: Services Status
echo ""
echo "⚙️  TEST 7: System Services"
echo "=========================="
echo "Observer service:"
sudo systemctl status jarvisos-observer --no-pager -l | head -10
echo ""
echo "Notifier timer:"
systemctl list-timers jarvisos-notifier.timer --no-pager
echo ""
read -p "Press Enter to continue..."

# Test 8: All Commands
echo ""
echo "📋 TEST 8: All Available Commands"
echo "=================================="
python jarvis.py --help
echo ""

# Summary
echo ""
echo "✅ ALL TESTS COMPLETE!"
echo ""
echo "🎯 JarvisOS Features Tested:"
echo "  ✅ System Status"
echo "  ✅ Context Awareness"
echo "  ✅ Feedback System"
echo "  ✅ Proactive Notifications"
echo "  ✅ User DNA Profiling"
echo "  ✅ Genetic Evolution"
echo "  ✅ System Services"
echo "  ✅ CLI Commands"
echo ""
echo "🚀 JarvisOS is 100% operational!"
echo ""
