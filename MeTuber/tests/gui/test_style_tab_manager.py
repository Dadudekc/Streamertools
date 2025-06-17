import pytest
from PyQt5.QtWidgets import QApplication
from src.gui.components.style_tab_manager import StyleTabManager

class MockStyle:
    """Mock style class for testing."""
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.parameters = [
            {"name": "param1", "type": "int", "min": 0, "max": 100, "default": 50}
        ]
    
    def apply(self, frame, params):
        return frame

@pytest.fixture
def style_tab_manager(qtbot):
    """Create a StyleTabManager instance."""
    categories = {
        "Basic": ["Original", "Grayscale"],
        "Advanced": ["Blur"]
    }
    styles = {
        "Original": MockStyle("Original", "Basic"),
        "Grayscale": MockStyle("Grayscale", "Basic"),
        "Blur": MockStyle("Blur", "Advanced")
    }
    settings = {"style": "Original"}
    manager = StyleTabManager(None, categories, styles, settings)
    qtbot.addWidget(manager)
    return manager

def test_style_tab_manager_initialization(style_tab_manager):
    """Test style tab manager initialization."""
    assert style_tab_manager is not None
    assert style_tab_manager.tab_widget.count() == 2
    assert style_tab_manager.tab_widget.tabText(0) == "Basic"
    assert style_tab_manager.tab_widget.tabText(1) == "Advanced"
    assert style_tab_manager.get_current_style() == "Original"

def test_style_tab_manager_get_current_style(style_tab_manager):
    """Test getting the current style."""
    assert style_tab_manager.get_current_style() == "Original"

def test_style_tab_manager_set_current_style(style_tab_manager):
    """Test setting the current style."""
    assert style_tab_manager.set_current_style("Grayscale")
    assert style_tab_manager.get_current_style() == "Grayscale"

def test_style_tab_manager_update_styles(style_tab_manager):
    """Test updating styles."""
    new_categories = {
        "Basic": ["Original", "Sepia"],
        "Advanced": ["Edge"]
    }
    new_styles = {
        "Original": MockStyle("Original", "Basic"),
        "Sepia": MockStyle("Sepia", "Basic"),
        "Edge": MockStyle("Edge", "Advanced")
    }
    style_tab_manager.update_styles(new_categories, new_styles)
    assert style_tab_manager.get_current_style() == "Original"

def test_style_tab_manager_error_handling(style_tab_manager):
    """Test error handling."""
    # Test with invalid style
    assert not style_tab_manager.set_current_style("Invalid")
    assert style_tab_manager.get_current_style() == "Original"

def test_style_tab_manager_style_changed_signal(style_tab_manager, qtbot):
    """Test style changed signal."""
    style_changed = []
    style_tab_manager.style_changed.connect(lambda s: style_changed.append(s))
    style_tab_manager.set_current_style("Grayscale")
    assert style_changed == ["Grayscale"] 