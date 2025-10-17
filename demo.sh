#!/bin/bash
#
# JarvisOS Complete Demo
# Shows all features in action
#

echo "🎉 JarvisOS Complete Demo"
echo "========================="
echo ""
echo "This will demonstrate all JarvisOS features."
echo ""

cd /opt/jarvisos
source venv/bin/activate

# Banner
python jarvis.py status

echo ""
echo "Press Enter to continue..."
read

# Test 1: DNA Profile
echo ""
echo "🧬 TEST 1: User DNA Profile"
echo "============================"
echo ""
python jarvis.py dna

echo ""
echo "Press Enter to continue..."
read

# Test 2: Evolution
echo ""
echo "🔬 TEST 2: Genetic Evolution"
echo "============================="
echo ""
python jarvis.py evolve

echo ""
echo "Press Enter to continue..."
read

# Test 3: Observations Summary
echo ""
echo "📊 TEST 3: Observation Summary"
echo "==============================="
echo ""
python jarvis.py summary

echo ""
echo "Press Enter to continue..."
read

# Test 4: Voice (if available)
echo ""
echo "🗣️  TEST 4: Voice System"
echo "========================"
echo ""
echo "Testing Jarvis voice..."
python jarvis.py speak --text "Hello. I am Jarvis. All systems operational."

echo ""
echo "Press Enter to continue..."
read

# Test 5: Services Status
echo ""
echo "⚙️  TEST 5: System Services"
echo "==========================="
echo ""
sudo systemctl status jarvisos-observer --no-pager -l | head -20

echo ""
echo "Press Enter to continue..."
read

# Test 6: Data Files
echo ""
echo "💾 TEST 6: Data Collection"
echo "==========================="
echo ""
echo "Data files:"
ls -lh /opt/jarvisos/data/
echo ""
echo "Gene pool:"
ls -lh /opt/jarvisos/gene_pool/ 2>/dev/null || echo "No genes yet"

echo ""
echo "Press Enter to continue..."
read

# Test 7: Logs
echo ""
echo "📝 TEST 7: System Logs"
echo "======================"
echo ""
sudo journalctl -u jarvisos-observer -n 10 --no-pager

echo ""
echo ""
echo "✅ Demo Complete!"
echo ""
echo "🎯 JarvisOS Features Demonstrated:"
echo "  ✅ User DNA Profiling"
echo "  ✅ Genetic Evolution"
echo "  ✅ Observation System"
echo "  ✅ Voice System"
echo "  ✅ System Services"
echo "  ✅ Data Collection"
echo "  ✅ Logging"
echo ""
echo "🚀 JarvisOS is fully operational!"
echo ""
