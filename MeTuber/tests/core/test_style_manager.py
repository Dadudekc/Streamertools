import pytest
from unittest.mock import MagicMock, patch
from src.core.style_manager import StyleManager
from styles.base import Style

class MockStyle(Style):
    """Mock style class for testing."""
    def __init__(self):
        super().__init__()
        self.name = "mock_style"
        self.category = "test_category"
        self.description = "Test style"
    
    def define_parameters(self):
        return [
            {"name": "param1", "type": "int", "min": 0, "max": 100, "default": 50},
            {"name": "param2", "type": "float", "min": 0.0, "max": 1.0, "default": 0.5}
        ]
    
    def apply(self, frame, params):
        return frame

@pytest.fixture
def style_manager():
    """Create a StyleManager instance."""
    return StyleManager()

@patch('importlib.import_module')
def test_style_manager_initialization(mock_import_module, style_manager):
    """Test StyleManager initialization."""
    assert style_manager is not None
    assert isinstance(style_manager.style_instances, dict)
    assert isinstance(style_manager.style_categories, dict)

def test_style_manager_get_style(style_manager):
    """Test getting a style instance."""
    # Test with nonexistent style
    assert style_manager.get_style("nonexistent") is None
    
    # Test with existing style
    mock_style = MockStyle()
    style_manager.style_instances["mock_style"] = mock_style
    assert style_manager.get_style("mock_style") == mock_style

def test_style_manager_get_categories(style_manager):
    """Test getting style categories."""
    # Add some test categories
    style_manager.style_categories = {
        "category1": ["style1", "style2"],
        "category2": ["style3"]
    }
    
    categories = style_manager.get_categories()
    assert isinstance(categories, dict)
    assert "category1" in categories
    assert "category2" in categories
    assert categories["category1"] == ["style1", "style2"]

def test_style_manager_get_styles_in_category(style_manager):
    """Test getting styles in a category."""
    # Add test category
    style_manager.style_categories["test_category"] = ["style1", "style2"]
    
    styles = style_manager.get_styles_in_category("test_category")
    assert isinstance(styles, list)
    assert "style1" in styles
    assert "style2" in styles
    
    # Test nonexistent category
    assert style_manager.get_styles_in_category("nonexistent") == []

def test_style_manager_validate_style_parameters(style_manager):
    """Test style parameter validation."""
    mock_style = MockStyle()
    style_manager.style_instances["mock_style"] = mock_style
    
    # Test valid parameters
    params = {"param1": 50, "param2": 0.5}
    validated = style_manager.validate_style_parameters("mock_style", params)
    assert validated == params
    
    # Test invalid parameters
    invalid_params = {"param1": 150, "param2": 2.0}  # Out of range
    validated = style_manager.validate_style_parameters("mock_style", invalid_params)
    assert validated["param1"] == 100  # Clamped to max
    assert validated["param2"] == 1.0  # Clamped to max
    
    # Test missing parameters
    partial_params = {"param1": 75}
    validated = style_manager.validate_style_parameters("mock_style", partial_params)
    assert validated["param1"] == 75
    assert validated["param2"] == 0.5  # Default value
    
    # Test empty parameters
    validated = style_manager.validate_style_parameters("mock_style", {})
    assert validated["param1"] == 50  # Default value
    assert validated["param2"] == 0.5  # Default value
    
    # Test nonexistent style
    assert style_manager.validate_style_parameters("nonexistent", params) == {}

def test_style_manager_get_default_parameters(style_manager):
    """Test getting default parameters."""
    mock_style = MockStyle()
    style_manager.style_instances["mock_style"] = mock_style
    
    params = style_manager.get_default_parameters("mock_style")
    assert params["param1"] == 50
    assert params["param2"] == 0.5
    
    # Test nonexistent style
    assert style_manager.get_default_parameters("nonexistent") == {}

def test_style_manager_get_style_info(style_manager):
    """Test getting style information."""
    mock_style = MockStyle()
    style_manager.style_instances["mock_style"] = mock_style
    
    info = style_manager.get_style_info("mock_style")
    assert info is not None
    assert info["name"] == "mock_style"
    assert info["category"] == "test_category"
    assert info["description"] == "Test style"
    assert len(info["parameters"]) == 2
    
    # Test nonexistent style
    assert style_manager.get_style_info("nonexistent") is None 