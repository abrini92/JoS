#!/usr/bin/env python3
"""Quick test of JarvisOS components"""

print("🧪 JarvisOS Component Tests")
print("=" * 50)
print()

# Test 1: Ollama availability
print("1️⃣ Testing Ollama...")
try:
    import subprocess
    result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print(f"   ✅ Ollama installed: {result.stdout.strip()}")
    else:
        print("   ❌ Ollama not working")
except:
    print("   ❌ Ollama not found")

# Test 2: Ollama models
print("\n2️⃣ Testing Ollama models...")
try:
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
    models = [line.split()[0] for line in result.stdout.strip().split('\n')[1:] if line.strip()]
    if models:
        print(f"   ✅ Models installed: {', '.join(models)}")
    else:
        print("   ⚠️  No models installed yet")
        print("      Run: ollama pull llama3.2")
except:
    print("   ❌ Could not list models")

# Test 3: Python modules
print("\n3️⃣ Testing Python modules...")
modules = {
    "rich": "Terminal UI",
    "anthropic": "Claude API",
    "psutil": "System monitoring",
    "pyttsx3": "Text-to-speech"
}

for module, desc in modules.items():
    try:
        __import__(module)
        print(f"   ✅ {module:15} - {desc}")
    except ImportError:
        print(f"   ❌ {module:15} - {desc} (NOT INSTALLED)")

# Test 4: File structure
print("\n4️⃣ Testing file structure...")
import os
from pathlib import Path

files_to_check = [
    "jarvisos/core/ai_brain_ollama.py",
    "jarvisos/core/ai_brain_unified.py",
    "jarvisos/onboarding/interactive_welcome.py",
    "install.sh",
    "setup-boot-experience.sh",
]

for file in files_to_check:
    path = Path(file)
    if path.exists():
        size = path.stat().st_size
        print(f"   ✅ {file:45} ({size:,} bytes)")
    else:
        print(f"   ❌ {file:45} (MISSING)")

# Test 5: Ollama AI Brain
print("\n5️⃣ Testing Ollama AI Brain...")
try:
    from jarvisos.core.ai_brain_ollama import OllamaAIBrain
    brain = OllamaAIBrain()
    if brain.available:
        print(f"   ✅ Ollama AI Brain initialized")
        print(f"      Model: {brain.config.model}")
        
        # Try a simple generation
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if "llama3.2" in result.stdout:
            print(f"      Testing generation...")
            response = brain.generate("Say 'Hello from JarvisOS' in 5 words")
            if response:
                print(f"      ✅ Generation works: {response[:50]}...")
            else:
                print(f"      ⚠️  Generation returned None")
        else:
            print(f"      ⚠️  llama3.2 not downloaded yet")
    else:
        print("   ⚠️  Ollama available but not initialized")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Summary
print("\n" + "=" * 50)
print("🎯 Test Summary")
print("=" * 50)
print("\nReady for testing in VM? Check the results above!")
print("\nNext steps:")
print("1. If Ollama models missing: ollama pull llama3.2")
print("2. If Python modules missing: pip install -r requirements.txt")
print("3. Test in VM: multipass transfer files and run install.sh")
