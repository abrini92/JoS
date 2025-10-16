#!/usr/bin/env python3
"""
JarvisOS Installation Test
Quick script to verify everything is set up correctly
"""

import sys
from pathlib import Path

def test_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("  ⚠️  Warning: Python 3.11+ recommended")
        return False
    return True

def test_imports():
    """Test required imports"""
    required = {
        'anthropic': 'Claude API client',
        'psutil': 'System monitoring',
        'rich': 'Beautiful terminal output',
        'fastapi': 'Web framework (future)',
        'pydantic': 'Data validation'
    }
    
    print("\nTesting imports:")
    all_ok = True
    
    for module, description in required.items():
        try:
            __import__(module)
            print(f"  ✓ {module:15} - {description}")
        except ImportError:
            print(f"  ✗ {module:15} - {description} (MISSING)")
            all_ok = False
    
    return all_ok

def test_api_key():
    """Check for API key"""
    import os
    
    print("\nTesting API key:")
    key = os.getenv('ANTHROPIC_API_KEY')
    
    if key:
        masked = key[:8] + '...' + key[-4:] if len(key) > 12 else '***'
        print(f"  ✓ ANTHROPIC_API_KEY found: {masked}")
        return True
    else:
        print("  ✗ ANTHROPIC_API_KEY not set")
        print("    Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        return False

def test_file_structure():
    """Check file structure"""
    print("\nTesting file structure:")
    
    required_files = [
        'jarvis.py',
        'requirements.txt',
        'setup.sh',
        'jarvisos/core/observer.py',
        'jarvisos/core/analyzer.py',
        'jarvisos/core/generator.py',
        'jarvisos/core/executor.py',
    ]
    
    all_ok = True
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            all_ok = False
    
    return all_ok

def test_directories():
    """Check/create required directories"""
    print("\nTesting directories:")
    
    dirs = ['data', 'generated_scripts', 'logs']
    
    for dir_name in dirs:
        path = Path(dir_name)
        if path.exists():
            print(f"  ✓ {dir_name}/ exists")
        else:
            path.mkdir(exist_ok=True)
            print(f"  ✓ {dir_name}/ created")
    
    return True

def test_cli():
    """Test CLI import"""
    print("\nTesting CLI:")
    
    try:
        # Add to path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from jarvisos.core import Observer, Analyzer, Generator, Executor
        print("  ✓ Core modules import successfully")
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("JarvisOS Installation Test")
    print("="*60)
    
    results = {
        'Python Version': test_python_version(),
        'Required Imports': test_imports(),
        'API Key': test_api_key(),
        'File Structure': test_file_structure(),
        'Directories': test_directories(),
        'CLI Modules': test_cli(),
    }
    
    print("\n" + "="*60)
    print("Summary:")
    print("="*60)
    
    for test, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status:8} - {test}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed! JarvisOS is ready to use.")
        print("\nNext steps:")
        print("  1. python jarvis.py status")
        print("  2. python jarvis.py observe --duration 30")
        print("  3. python jarvis.py analyze")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Set API key: export ANTHROPIC_API_KEY='your-key'")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
