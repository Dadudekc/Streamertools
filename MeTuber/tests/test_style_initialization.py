# tests/test_style_initialization.py

import unittest
from MeTuber.styles.base import Style
from MeTuber.styles.effects.original import Original

class TestStyleInitialization(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.original_style = Original()

    def test_style_name(self):
        """Test if the style name is correctly set."""
        self.assertEqual(self.original_style.name, "Original")

    def test_style_category(self):
        """Test if the style category is correctly set."""
        self.assertEqual(self.original_style.category, "Effects")

    def test_define_parameters(self):
        """Test if the style defines parameters correctly."""
        params = self.original_style.define_parameters()
        self.assertIsInstance(params, list)
        self.assertEqual(len(params), 0)  # Original has no parameters

    def test_apply_original_style(self):
        """Test if applying the Original style returns the frame unmodified."""
        import numpy as np
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        styled_frame = self.original_style.apply(frame, {})
        self.assertTrue((styled_frame == frame).all())

    def test_validate_params_with_defaults(self):
        """Test parameter validation with defaults."""
        params = {}
        validated = self.original_style.validate_params(params)
        self.assertEqual(validated, {})  # No parameters to validate

    def test_validate_params_with_extra(self):
        """Test parameter validation ignores extra parameters."""
        params = {"extra_param": 10}
        validated = self.original_style.validate_params(params)
        self.assertEqual(validated, {})  # Extra params are ignored
