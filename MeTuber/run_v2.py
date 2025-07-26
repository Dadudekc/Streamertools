#!/usr/bin/env python3
"""
Launcher script for Webcam Filter App V2.
This script provides a simple way to run the V2 application with proper error handling.
"""

import sys
import os
import logging
from pathlib import Path

def setup_environment():
    """Setup the Python environment for the V2 application."""
    # Add the project root to Python path
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Set up basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def check_dependencies():
    """Check if required dependencies are available."""
    required_modules = [
        'PyQt5',
        'cv2',
        'numpy',
        'av',
        'pyvirtualcam'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ Missing required dependencies:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\nPlease install missing dependencies with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main launcher function."""
    print("=" * 60)
    print("Webcam Filter App V2 Launcher")
    print("=" * 60)
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        return 1
    
    print("✅ All dependencies available")
    
    # Try to import and run the V2 application
    try:
        print("Starting V2 application...")
        from src.v2_main import main as v2_main
        return v2_main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this script from the project root directory.")
        return 1
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 