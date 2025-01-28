# File: MeTuber/tests/test_gui_components.py

import sys
import unittest
from unittest.mock import MagicMock
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QListWidget
from gui_components import DeviceSelector, StyleTabManager, ParameterControls, ActionButtons

# Ensure a single global QApplication instance
app = QApplication(sys.argv)

class TestStyleTabManager(unittest.TestCase):
    def setUp(self):
        self.style_categories = {"Category 1": ["Style A", "Style B"]}
        self.style_instances = {"Style A": MagicMock(), "Style B": MagicMock()}
        self.settings = {"style": "Style A"}
        self.manager = StyleTabManager(None, self.style_categories, self.style_instances, self.settings)

    def test_tabs_created(self):
        # Remove redundant init_tabs() call if already called in __init__
        expected_tabs = len(self.style_categories)
        actual_tabs = self.manager.count()
        self.assertEqual(actual_tabs, expected_tabs, f"Expected {expected_tabs} tabs, got {actual_tabs}.")

    def test_style_selection_signal(self):
        mock_slot = MagicMock()
        self.manager.style_changed.connect(mock_slot)
        # Simulate clicking on the first style in the first category
        category_tab = self.manager.widget(0)
        list_widget = category_tab.findChild(QListWidget)
        item = list_widget.item(0)  # "Style A"
        # Simulate mouse click on the item
        QTest.mouseClick(list_widget.viewport(), Qt.LeftButton, pos=list_widget.visualItemRect(item).center())
        # Assert the signal was emitted with "Style A"
        mock_slot.assert_called_once_with("Style A")
