#!/usr/bin/env python3
"""
Test complet des notifications natives
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from jarvisos.ui.native_notifications import (
    notify_jarvis,
    notify_success,
    notify_info,
    notify_warning,
    notify_error,
    get_notifier
)
import time

def test_all_notifications():
    """Test all notification types"""
    
    print("🧪 TESTING ALL NOTIFICATION TYPES\n")
    
    notifier = get_notifier()
    print(f"System: {notifier.system}")
    print(f"Available: {notifier.notifier_available}\n")
    
    tests = [
        ("Jarvis Welcome", lambda: notify_jarvis(
            "Good afternoon! I'm ready to help you accomplish great things today.",
            subtitle="System Ready"
        )),
        
        ("Success", lambda: notify_success(
            "Task Complete",
            "Your automation script finished successfully in 2.3 seconds"
        )),
        
        ("Info", lambda: notify_info(
            "Insights Ready",
            "I've analyzed 1,247 data points and found 3 optimization opportunities"
        )),
        
        ("Warning", lambda: notify_warning(
            "Low Energy Detected",
            "You've been working for 2 hours. Consider taking a 10-minute break."
        )),
        
        ("Error", lambda: notify_error(
            "Script Failed",
            "automation_script_42.py encountered an error. Check logs for details."
        )),
        
        ("Jarvis Prediction", lambda: notify_jarvis(
            "I predict you'll need your test environment in 5 minutes. Shall I prepare it?",
            subtitle="Predictive Engine",
            actions=["Yes", "No", "Later"]
        )),
        
        ("Jarvis Celebration", lambda: notify_jarvis(
            "Excellent work! You've completed 5 tasks today with 95% efficiency.",
            subtitle="Daily Summary"
        )),
    ]
    
    for i, (name, test_func) in enumerate(tests, 1):
        print(f"Test {i}/{len(tests)}: {name}")
        test_func()
        print("✅ Sent")
        
        if i < len(tests):
            print("Waiting 3 seconds...\n")
            time.sleep(3)
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS COMPLETE!")
    print("="*60)
    print("\nCheck your Notification Center!")
    print("You should see 7 beautiful notifications from Jarvis\n")

if __name__ == "__main__":
    test_all_notifications()
