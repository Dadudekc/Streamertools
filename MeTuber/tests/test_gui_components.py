import sys
import unittest
from unittest.mock import MagicMock
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from gui_components import DeviceSelector, StyleTabManager, ParameterControls, ActionButtons

# Ensure a single global QApplication instance
app = QApplication([])

class TestDeviceSelector(unittest.TestCase):
    def setUp(self):
        self.devices = ["Camera 1", "Camera 2"]
        self.default_device = "Camera 1"
        self.selector = DeviceSelector(None, self.devices, self.default_device)

    def test_device_list_populated(self):
        layout = self.selector.create()
        self.assertEqual(self.selector.device_combo.count(), len(self.devices))

    def test_default_device_selected(self):
        layout = self.selector.create()
        self.assertEqual(self.selector.device_combo.currentText(), self.default_device)

    def test_combo_editable(self):
        layout = self.selector.create()
        self.assertTrue(self.selector.device_combo.isEditable())


class TestStyleTabManager(unittest.TestCase):
    def setUp(self):
        self.style_categories = {"Category 1": ["Style A", "Style B"]}
        self.style_instances = {"Style A": MagicMock(), "Style B": MagicMock()}
        self.settings = {"style": "Style A"}
        self.manager = StyleTabManager(None, self.style_categories, self.style_instances, self.settings)

    def test_tabs_created(self):
        self.manager.init_tabs()
        self.assertEqual(self.manager.count(), len(self.style_categories))

    def test_style_selection_signal(self):
        mock_slot = MagicMock()
        self.manager.style_changed.connect(mock_slot)
        self.manager.init_tabs()
        # Simulate button click
        category_tab = self.manager.widget(0)
        button = category_tab.layout().itemAt(0).widget()
        QTest.mouseClick(button, Qt.LeftButton)
        mock_slot.assert_called_once_with("Style A")

class TestParameterControls(unittest.TestCase):
    def setUp(self):
        self.params = [
            {"name": "param1", "type": "int", "min": 0, "max": 100, "default": 50, "step": 10, "label": "Parameter 1"},
            {"name": "param2", "type": "float", "min": 0.0, "max": 1.0, "default": 0.5, "step": 0.1, "label": "Parameter 2"},
            {"name": "param3", "type": "str", "options": ["Option 1", "Option 2"], "default": "Option 1", "label": "Parameter 3"},
        ]
        self.current_params = {"param1": 70, "param2": 0.3}
        self.controls = ParameterControls(None)

    def test_update_parameters(self):
        mock_callback = MagicMock()
        self.controls.update_parameters(self.params, self.current_params, mock_callback)
        # Calculate the expected number of widgets
        expected_widgets = 0
        for param in self.params:
            if param["type"] in ["int", "float"]:
                expected_widgets += 2  # Label + Slider with value display
            elif param["type"] == "str":
                expected_widgets += 2  # Label + ComboBox

        self.assertEqual(self.controls.form_layout.count(), expected_widgets)

    def test_clear_layout(self):
        mock_callback = MagicMock()
        self.controls.update_parameters(self.params, {}, mock_callback)
        self.controls.clear_layout()
        self.assertEqual(self.controls.form_layout.count(), 0)

class TestActionButtons(unittest.TestCase):
    def setUp(self):
        self.buttons = ActionButtons(None)

    def test_button_callbacks(self):
        mock_start = MagicMock()
        mock_stop = MagicMock()
        mock_snapshot = MagicMock()

        # Create buttons
        layout = self.buttons.create(mock_start, mock_stop, mock_snapshot)

        # Assert buttons are initialized
        self.assertIsNotNone(self.buttons.start_button, "Start button not initialized.")
        self.assertIsNotNone(self.buttons.stop_button, "Stop button not initialized.")
        self.assertIsNotNone(self.buttons.snapshot_button, "Snapshot button not initialized.")

        # Simulate button clicks
        QTest.mouseClick(self.buttons.start_button, Qt.LeftButton)
        QTest.mouseClick(self.buttons.stop_button, Qt.LeftButton)
        QTest.mouseClick(self.buttons.snapshot_button, Qt.LeftButton)

        # Assert callbacks are triggered
        mock_start.assert_called_once()
        mock_stop.assert_called_once()
        mock_snapshot.assert_called_once()

if __name__ == "__main__":
    unittest.main()
