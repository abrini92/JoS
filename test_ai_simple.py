#!/usr/bin/env python3
"""
Simple AI Brain Test - See what Claude actually responds
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from jarvisos.core.ai_brain import AIBrain
import os
import json

def test_simple():
    """Simple test to see Claude's actual response"""
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set")
        return
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print("🧠 Simple AI Brain Test\n")
    
    brain = AIBrain(data_dir)
    
    print("Test: Predicting next actions after opening VSCode\n")
    
    # Call think directly to see what happens
    situation = {"current_activity": "User opened VSCode"}
    question = "What will the user need next?"
    
    print("Calling brain.think()...")
    think_result = brain.think(situation, question)
    
    print("\n=== THINK RESULT ===")
    print(json.dumps(think_result, indent=2))
    print()
    
    # Call predict
    print("Calling brain.predict_next_actions()...")
    result = brain.predict_next_actions("User opened VSCode")
    
    print("=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(json.dumps(result, indent=2))
    print()
    
    # Check conversation history
    if brain.conversation_history:
        last_conv = brain.conversation_history[-1]
        print("=" * 60)
        print("LAST CONVERSATION:")
        print("=" * 60)
        print(json.dumps(last_conv, indent=2))
        print()
        
        if 'response' in last_conv and 'raw_response' in last_conv['response']:
            print("=" * 60)
            print("RAW CLAUDE RESPONSE:")
            print("=" * 60)
            print(last_conv['response']['raw_response'])
            print()

if __name__ == "__main__":
    test_simple()
