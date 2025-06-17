import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

class SettingsManager:
    """Manages application settings with validation and error handling."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        self.default_settings = {
            "input_device": "",
            "style": "Original",
            "parameters": {},
            "virtual_camera": {
                "width": 640,
                "height": 480,
                "fps": 30
            }
        }
        self._settings = self.default_settings.copy()

    def load(self) -> Dict[str, Any]:
        """Load settings from config file with validation."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    loaded = json.load(f)
                    self._settings = self._validate_settings(loaded)
                    self.logger.info("Settings loaded successfully")
            else:
                self.logger.info("No config file found, using default settings")
                self._settings = self.default_settings.copy()
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error loading settings: {e}")
            self._settings = self.default_settings.copy()
        
        return self._settings

    def save(self, settings: Dict[str, Any]) -> bool:
        """Save settings to config file with validation."""
        try:
            validated = self._validate_settings(settings)
            with open(self.config_file, "w") as f:
                json.dump(validated, f, indent=4)
            self._settings = validated
            self.logger.info("Settings saved successfully")
            return True
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error saving settings: {e}")
            return False

    def _validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate settings structure and values."""
        validated = self.default_settings.copy()
        
        # Validate input device
        if "input_device" in settings:
            validated["input_device"] = str(settings["input_device"])
        
        # Validate style
        if "style" in settings:
            validated["style"] = str(settings["style"])
        
        # Validate parameters
        if "parameters" in settings and isinstance(settings["parameters"], dict):
            validated["parameters"] = settings["parameters"]
        
        # Validate virtual camera settings
        if "virtual_camera" in settings and isinstance(settings["virtual_camera"], dict):
            vcam = settings["virtual_camera"]
            validated["virtual_camera"] = {
                "width": max(320, min(4096, int(vcam.get("width", 640)))),
                "height": max(240, min(2160, int(vcam.get("height", 480)))),
                "fps": max(1, min(60, int(vcam.get("fps", 30))))
            }
        
        return validated

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value with optional default."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a setting value with validation."""
        self._settings[key] = value
        self.save(self._settings) 