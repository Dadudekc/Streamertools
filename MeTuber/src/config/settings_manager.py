import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

class SettingsManager:
    """Manages application settings with proper error handling and logging."""
    
    def __init__(self, config_file: str = "config.json"):
        self.logger = logging.getLogger(__name__)
        self.config_file = config_file
        self.default_settings = {
            "input_device": "",
            "style": "Original",
            "parameters": {},
            "log_level": "INFO",
            "virtual_camera": {
                "width": 640,
                "height": 480,
                "fps": 30
            }
        }
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from config file or use defaults."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    settings = {**self.default_settings, **loaded}
                    self.logger.info(f"Settings loaded from {self.config_file}")
                    return settings
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
        except IOError as e:
            self.logger.error(f"Error reading config file: {e}")
        
        self.logger.info("Using default settings")
        return self.default_settings.copy()
    
    def save_settings(self) -> bool:
        """Save current settings to config file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.settings, f, indent=4)
            self.logger.info(f"Settings saved to {self.config_file}")
            return True
        except IOError as e:
            self.logger.error(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value with optional default."""
        try:
            return self.settings.get(key, default)
        except Exception as e:
            self.logger.error(f"Error getting setting {key}: {e}")
            return default
    
    def set_setting(self, key: str, value: Any) -> bool:
        """Set a setting value."""
        try:
            if not key or key not in self.default_settings:
                self.logger.error(f"Invalid setting key: {key}")
                return False
            self.settings[key] = value
            return True
        except Exception as e:
            self.logger.error(f"Error setting {key}: {e}")
            return False
    
    def get_style_parameters(self, style_name: str) -> Dict[str, Any]:
        """Get parameters for a specific style."""
        try:
            return self.settings["parameters"].get(style_name, {})
        except Exception as e:
            self.logger.error(f"Error getting parameters for style {style_name}: {e}")
            return {}
    
    def set_style_parameters(self, style_name: str, parameters: Dict[str, Any]) -> bool:
        """Set parameters for a specific style."""
        try:
            if "parameters" not in self.settings:
                self.settings["parameters"] = {}
            self.settings["parameters"][style_name] = parameters
            return True
        except Exception as e:
            self.logger.error(f"Error setting parameters for style {style_name}: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset all settings to defaults."""
        try:
            self.settings = self.default_settings.copy()
            return self.save_settings()
        except Exception as e:
            self.logger.error(f"Error resetting settings: {e}")
            return False
    
    def validate_settings(self) -> bool:
        """Validate current settings against defaults."""
        try:
            # Ensure all default keys exist
            for key in self.default_settings:
                if key not in self.settings:
                    self.settings[key] = self.default_settings[key]
            return True
        except Exception as e:
            self.logger.error(f"Error validating settings: {e}")
            return False 