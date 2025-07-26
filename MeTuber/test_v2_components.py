#!/usr/bin/env python3
"""
Test script for V2 GUI components.
This script tests that all V2 components can be imported and instantiated without errors.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication

def setup_logging():
    """Setup basic logging for testing."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def test_imports():
    """Test that all V2 components can be imported."""
    print("Testing V2 component imports...")
    
    try:
        # Test accessibility manager
        from src.gui.components.accessibility_manager import AccessibilityManager
        print("✅ AccessibilityManager imported successfully")
        
        # Test V2 style selector
        from src.gui.components.v2_style_selector import V2StyleSelector
        print("✅ V2StyleSelector imported successfully")
        
        # Test preview area
        from src.gui.components.preview_area import PreviewArea
        print("✅ PreviewArea imported successfully")
        
        # Test help/about components
        from src.gui.components.help_about import HelpAboutDialog, HelpButton, TooltipManager
        print("✅ Help/About components imported successfully")
        
        # Test V2 main window
        from src.gui.v2_main_window import V2MainWindow
        print("✅ V2MainWindow imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        return False

def test_component_instantiation():
    """Test that all V2 components can be instantiated."""
    print("\nTesting V2 component instantiation...")
    
    try:
        # Create QApplication if not exists
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test accessibility manager
        from src.gui.components.accessibility_manager import AccessibilityManager
        accessibility_manager = AccessibilityManager()
        print("✅ AccessibilityManager instantiated successfully")
        
        # Test V2 style selector
        from src.gui.components.v2_style_selector import V2StyleSelector
        style_selector = V2StyleSelector()
        print("✅ V2StyleSelector instantiated successfully")
        
        # Test preview area
        from src.gui.components.preview_area import PreviewArea
        preview_area = PreviewArea()
        print("✅ PreviewArea instantiated successfully")
        
        # Test help button
        from src.gui.components.help_about import HelpButton
        help_button = HelpButton()
        print("✅ HelpButton instantiated successfully")
        
        # Test tooltip manager
        from src.gui.components.help_about import TooltipManager
        tooltip_manager = TooltipManager()
        print("✅ TooltipManager instantiated successfully")
        
        # Test V2 main window (this might take longer)
        print("Testing V2MainWindow instantiation (this may take a moment)...")
        from src.gui.v2_main_window import V2MainWindow
        main_window = V2MainWindow()
        print("✅ V2MainWindow instantiated successfully")
        
        # Clean up
        main_window.close()
        main_window.deleteLater()
        
        return True
        
    except Exception as e:
        print(f"❌ Error during component instantiation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_theme_loading():
    """Test that the V2 theme can be loaded."""
    print("\nTesting V2 theme loading...")
    
    try:
        # Create QApplication if not exists
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test theme loading
        with open("src/gui/styles/v2_theme.qss", "r") as f:
            theme_content = f.read()
        
        if theme_content:
            print("✅ V2 theme file loaded successfully")
            print(f"   Theme file size: {len(theme_content)} characters")
            return True
        else:
            print("❌ V2 theme file is empty")
            return False
            
    except FileNotFoundError:
        print("❌ V2 theme file not found")
        return False
    except Exception as e:
        print(f"❌ Error loading V2 theme: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("V2 GUI Components Test")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    # Test imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n❌ Import tests failed. Cannot continue with instantiation tests.")
        return 1
    
    # Test component instantiation
    instantiation_ok = test_component_instantiation()
    
    # Test theme loading
    theme_ok = test_theme_loading()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Instantiation: {'✅ PASS' if instantiation_ok else '❌ FAIL'}")
    print(f"Theme Loading: {'✅ PASS' if theme_ok else '❌ FAIL'}")
    
    if imports_ok and instantiation_ok and theme_ok:
        print("\n🎉 All V2 component tests passed!")
        print("The V2 GUI components are ready for use.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 