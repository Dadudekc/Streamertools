import logging
import importlib
import pkgutil
import inspect
from typing import Dict, Any, List, Optional, Type
from styles.base import Style

class StyleManager:
    """Manages style loading and instantiation with proper error handling and logging."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.style_instances: Dict[str, Style] = {}
        self.style_categories: Dict[str, List[str]] = {}
        self._load_styles()
    
    def _load_styles(self) -> None:
        """Load all available styles from the styles package."""
        try:
            # List of all style-related packages to scan
            packages_to_scan = ['styles']
            seen_classes = set()
            
            for pkg_name in packages_to_scan:
                self.logger.debug(f"Scanning package: {pkg_name}")
                try:
                    package = importlib.import_module(pkg_name)
                except ImportError as e:
                    self.logger.error(f"Error loading package {pkg_name}: {e}")
                    continue
                
                for _, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if ispkg:
                        continue
                    
                    self.logger.debug(f"Found module: {modname}")
                    try:
                        module = importlib.import_module(modname)
                        
                        for cls_name in dir(module):
                            cls = getattr(module, cls_name)
                            if (
                                inspect.isclass(cls) and
                                issubclass(cls, Style) and
                                cls is not Style and
                                not inspect.isabstract(cls) and
                                cls not in seen_classes
                            ):
                                try:
                                    instance = cls()  # Instantiate
                                    seen_classes.add(cls)
                                    
                                    category = getattr(instance, "category", "Uncategorized")
                                    if category not in self.style_categories:
                                        self.style_categories[category] = []
                                    
                                    # Avoid duplicate style names in the same category
                                    if instance.name not in self.style_categories[category]:
                                        self.style_categories[category].append(instance.name)
                                    
                                    self.style_instances[instance.name] = instance
                                    self.logger.info(f"Loaded style: {instance.name} (Category: {category})")
                                    
                                except Exception as instantiation_error:
                                    self.logger.error(f"Failed to instantiate style '{cls.__name__}': {instantiation_error}")
                    
                    except Exception as module_error:
                        self.logger.error(f"Failed to load module '{modname}': {module_error}")
            
        except Exception as e:
            self.logger.error(f"Error loading styles: {e}")
    
    def get_style(self, name: str) -> Optional[Style]:
        """Get a style instance by name."""
        try:
            return self.style_instances.get(name)
        except Exception as e:
            self.logger.error(f"Error getting style {name}: {e}")
            return None
    
    def get_categories(self) -> Dict[str, List[str]]:
        """Get all style categories and their styles."""
        return self.style_categories.copy()
    
    def get_styles_in_category(self, category: str) -> List[str]:
        """Get all styles in a specific category."""
        try:
            return self.style_categories.get(category, []).copy()
        except Exception as e:
            self.logger.error(f"Error getting styles for category {category}: {e}")
            return []
    
    def validate_style_parameters(self, style_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameters for a specific style."""
        try:
            style = self.get_style(style_name)
            if not style:
                self.logger.warning(f"Style {style_name} not found")
                return {}
            
            # Get default parameters
            defaults = self.get_default_parameters(style_name)
            
            # Start with defaults and update with provided parameters
            validated = defaults.copy()
            validated.update(parameters)
            
            # Validate each parameter
            param_defs = {p["name"]: p for p in style.define_parameters()}
            for name, value in validated.items():
                if name in param_defs:
                    param_def = param_defs[name]
                    
                    # Type validation
                    if param_def["type"] == "int":
                        value = int(value)
                    elif param_def["type"] == "float":
                        value = float(value)
                    
                    # Range validation
                    if "min" in param_def:
                        value = max(param_def["min"], value)
                    if "max" in param_def:
                        value = min(param_def["max"], value)
                    
                    validated[name] = value
            
            return validated
            
        except Exception as e:
            self.logger.error(f"Error validating parameters for style {style_name}: {e}")
            return {}
    
    def get_default_parameters(self, style_name: str) -> Dict[str, Any]:
        """Get default parameters for a specific style."""
        try:
            style = self.get_style(style_name)
            if not style:
                self.logger.warning(f"Style {style_name} not found")
                return {}
            
            return {
                param['name']: param.get("default", 0)
                for param in style.define_parameters()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting default parameters for style {style_name}: {e}")
            return {}
    
    def refresh_styles(self) -> None:
        """Reload all styles."""
        self.style_instances.clear()
        self.style_categories.clear()
        self._load_styles()
    
    def get_style_info(self, style_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific style."""
        try:
            style = self.get_style(style_name)
            if not style:
                return None
            
            return {
                "name": style.name,
                "category": getattr(style, "category", "Uncategorized"),
                "description": getattr(style, "description", ""),
                "parameters": style.define_parameters()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting info for style {style_name}: {e}")
            return None 