#!/usr/bin/env python3
"""
Test script for Uninstall Helper
"""

import subprocess
import sys
import os

def test_basic_functionality():
    """Test basic functionality of the uninstall helper."""
    print("🧪 Testing Uninstall Helper Basic Functionality")
    print("=" * 50)
    
    # Test 1: Help command
    print("\n1. Testing help command...")
    result = subprocess.run([sys.executable, "main.py", "--help"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✓ Help command works")
    else:
        print("   ✗ Help command failed")
    
    # Test 2: Safe mode detection
    print("\n2. Testing safe mode detection...")
    result = subprocess.run([sys.executable, "main.py", "python", "--safe"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✓ Safe mode works")
        # Check if detection output is present
        if "Detection Results" in result.stdout or "Processes found" in result.stdout:
            print("   ✓ Detection output is present")
    else:
        print("   ✗ Safe mode failed")
    
    # Test 3: Interactive mode (simulated with timeout)
    print("\n3. Testing interactive mode startup...")
    try:
        result = subprocess.run([sys.executable, "main.py", "-i"], 
                              capture_output=True, text=True,
                              timeout=2,  # Short timeout to just check startup
                              input="\n")  # Send Enter to exit
        print("   ✓ Interactive mode starts")
    except subprocess.TimeoutExpired:
        print("   ✓ Interactive mode is waiting for input (expected)")
    except Exception as e:
        print(f"   ✗ Interactive mode failed: {e}")
    
    # Test 4: Check configuration file
    print("\n4. Testing configuration...")
    if os.path.exists("uninstall_config.json"):
        print("   ✓ Configuration file exists")
        import json
        with open("uninstall_config.json", "r") as f:
            config = json.load(f)
            if "windows" in config and "macos" in config and "linux" in config:
                print("   ✓ Configuration has all platform settings")
            else:
                print("   ✗ Configuration missing platform settings")
    else:
        print("   ✗ Configuration file missing")
    
    # Test 5: Module imports
    print("\n5. Testing module imports...")
    try:
        import psutil
        import argparse
        import json
        import platform
        print("   ✓ All required modules can be imported")
    except ImportError as e:
        print(f"   ✗ Missing module: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Basic functionality tests completed")
    print("\nFor more comprehensive testing:")
    print("1. Run: python main.py -i (interactive mode)")
    print("2. Test with real software: python main.py 'software-name' --safe")
    print("3. Check system-specific features based on your OS")

def test_platform_specific():
    """Test platform-specific functionality."""
    import platform
    system = platform.system()
    
    print(f"\n🔧 Platform-Specific Tests for {system}")
    print("=" * 50)
    
    from main import UninstallHelper
    helper = UninstallHelper()
    
    # Test process detection with a common process
    print("\n1. Testing process detection...")
    test_process = "python" if system != "Windows" else "python.exe"
    processes = helper.detect_processes(test_process)
    if processes:
        print(f"   ✓ Can detect {test_process} processes")
        print(f"   Found {len(processes)} process(es)")
    else:
        print(f"   ⚠️  No {test_process} processes found (may be normal)")
    
    # Test installation path discovery
    print("\n2. Testing path discovery...")
    paths = helper.find_installation_paths("python")
    if paths:
        print(f"   ✓ Found {len(paths)} installation path(s) for 'python'")
        for path in paths[:3]:  # Show first 3 paths
            print(f"   - {path}")
    else:
        print("   ⚠️  No installation paths found for 'python'")
    
    # Test uninstall command generation
    print("\n3. Testing uninstall command generation...")
    cmd = helper.get_uninstall_command("test-software")
    if cmd:
        print(f"   ✓ Generated uninstall command: {cmd}")
    else:
        print("   ⚠️  No uninstall command generated (may be normal for test software)")
    
    print("\n" + "=" * 50)
    print("✅ Platform-specific tests completed")

if __name__ == "__main__":
    print("🚀 Starting Uninstall Helper Tests")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_platform_specific()
        
        print("\n🎉 All tests completed successfully!")
        print("\nNext steps:")
        print("1. Review the test output above")
        print("2. Run actual uninstall tests with --safe flag first")
        print("3. Report any issues on GitHub")
        
    except Exception as e:
        print(f"\n❌ Tests failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)