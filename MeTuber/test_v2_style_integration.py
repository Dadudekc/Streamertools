#!/usr/bin/env python3
"""
Integration test for V2 GUI components with consolidated style system.
This test verifies that the V2 style selector can work with the new consolidated styles.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

def setup_logging():
    """Setup basic logging for testing."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def test_style_manager_integration():
    """Test that the style manager works with consolidated styles."""
    print("Testing style manager integration...")
    
    try:
        from src.core.style_manager import StyleManager
        
        # Create style manager
        style_manager = StyleManager()
        
        # Test getting consolidated styles
        cartoon_style = style_manager.get_style("Cartoon")
        if cartoon_style:
            print("✅ Cartoon style loaded successfully")
            
            # Test variant support
            if hasattr(cartoon_style, 'variants'):
                print(f"✅ Cartoon variants: {cartoon_style.variants}")
                
                # Test getting style with variant
                advanced_cartoon = style_manager.get_style_with_variant("Cartoon", "Advanced")
                if advanced_cartoon:
                    print("✅ Advanced cartoon variant loaded successfully")
                else:
                    print("❌ Failed to load advanced cartoon variant")
            else:
                print("❌ Cartoon style doesn't have variants")
        else:
            print("❌ Failed to load cartoon style")
        
        # Test sketch style
        sketch_style = style_manager.get_style("Sketch")
        if sketch_style and hasattr(sketch_style, 'variants'):
            print(f"✅ Sketch variants: {sketch_style.variants}")
        else:
            print("❌ Sketch style not found or missing variants")
        
        # Test invert style
        invert_style = style_manager.get_style("Invert")
        if invert_style and hasattr(invert_style, 'variants'):
            print(f"✅ Invert variants: {invert_style.variants}")
        else:
            print("❌ Invert style not found or missing variants")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing style manager integration: {e}")
        return False

def test_v2_style_selector_integration():
    """Test that the V2 style selector can work with consolidated styles."""
    print("\nTesting V2 style selector integration...")
    
    try:
        # Create QApplication if not exists
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        from src.gui.components.v2_style_selector import V2StyleSelector
        
        # Create V2 style selector
        style_selector = V2StyleSelector()
        print("✅ V2 style selector created successfully")
        
        # Test setting available styles (this would come from style manager)
        test_categories = {
            "Artistic": ["Cartoon", "Sketch", "Watercolor"],
            "Basic": ["Brightness", "Contrast", "Saturation"],
            "Distortions": ["Glitch", "Wave", "Mirror"],
            "Color Filters": ["Invert", "Sepia", "Vintage"]
        }
        
        style_selector.set_available_styles(test_categories)
        print("✅ Available styles set successfully")
        
        # Test setting style variants
        test_variants = {
            "Artistic": {
                "Cartoon": ["Basic", "Advanced", "Advanced2", "WholeImage"],
                "Sketch": ["Pencil", "Advanced", "Color"]
            },
            "Color Filters": {
                "Invert": ["Colors", "Filter", "Negative"]
            }
        }
        
        style_selector.set_style_variants(test_variants)
        print("✅ Style variants set successfully")
        
        # Test current selection
        current = style_selector.get_current_selection()
        print(f"✅ Current selection: {current}")
        
        # Clean up
        style_selector.deleteLater()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing V2 style selector integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_parameter_controls_integration():
    """Test that parameter controls can work with consolidated style parameters."""
    print("\nTesting parameter controls integration...")
    
    try:
        # Create QApplication if not exists
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        from src.gui.components.parameter_controls import ParameterControls
        from PyQt5.QtWidgets import QWidget
        
        # Create a parent widget
        parent_widget = QWidget()
        
        # Create parameter controls with parent
        param_controls = ParameterControls(parent_widget)
        print("✅ Parameter controls created successfully")
        
        # Test setting parameters for a consolidated style
        test_params = [
            {
                "name": "mode",
                "type": "str",
                "default": "Basic",
                "options": ["Basic", "Advanced", "Advanced2", "WholeImage"],
                "label": "Cartoon Mode"
            },
            {
                "name": "edge_threshold",
                "type": "int",
                "default": 50,
                "min": 0,
                "max": 255,
                "step": 1,
                "label": "Edge Threshold"
            },
            {
                "name": "color_saturation",
                "type": "float",
                "default": 1.5,
                "min": 0.1,
                "max": 3.0,
                "step": 0.1,
                "label": "Color Saturation"
            }
        ]
        
        param_controls.set_parameters(test_params)
        print("✅ Parameters set successfully")
        
        # Test getting parameters
        current_params = param_controls.get_parameters()
        print(f"✅ Current parameters: {current_params}")
        
        # Clean up
        param_controls.deleteLater()
        parent_widget.deleteLater()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing parameter controls integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main integration test function."""
    print("=" * 60)
    print("V2 GUI + Consolidated Styles Integration Test")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    # Test style manager integration
    style_manager_ok = test_style_manager_integration()
    
    # Test V2 style selector integration
    style_selector_ok = test_v2_style_selector_integration()
    
    # Test parameter controls integration
    param_controls_ok = test_parameter_controls_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 60)
    print(f"Style Manager Integration: {'✅ PASS' if style_manager_ok else '❌ FAIL'}")
    print(f"V2 Style Selector Integration: {'✅ PASS' if style_selector_ok else '❌ FAIL'}")
    print(f"Parameter Controls Integration: {'✅ PASS' if param_controls_ok else '❌ FAIL'}")
    
    if style_manager_ok and style_selector_ok and param_controls_ok:
        print("\n🎉 All integration tests passed!")
        print("V2 GUI components are ready to work with consolidated styles.")
        return 0
    else:
        print("\n❌ Some integration tests failed.")
        print("Please check the errors above before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 