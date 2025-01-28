# styles/base.py
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod
import numpy as np


class Style(ABC):
    """
    Abstract base class for all styles.
    """
    name = "BaseStyle"
    category = "Base"

    def __init__(self):
        self.parameters = self.define_parameters()

    @abstractmethod
    def define_parameters(self) -> List[Dict[str, Any]]:
        """
        Define the parameters required for the style.
        Must be implemented by subclasses.
        """
        return []

    def apply(self, frame: Optional[np.ndarray], params: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Apply the style to the given frame using the provided parameters.

        Args:
            frame (numpy.ndarray): The input video frame.
            params (dict): Parameters for the style.

        Returns:
            numpy.ndarray: The styled video frame.
        """
        if frame is None or not isinstance(frame, np.ndarray):
            raise ValueError("Invalid frame provided. Expected a NumPy array.")

        # Use default parameters if params are not provided
        params = self.validate_params(params or {})

        # Default behavior is to return the original frame (no-op)
        return frame

    def validate_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and set default values for parameters.

        Args:
            params (dict): Parameters to validate.

        Returns:
            dict: Validated parameters with defaults applied.
        """
        validated = {}
        for param in self.parameters:
            name = param["name"]
            value = params.get(name, param.get("default"))

            # Validate range for numeric parameters
            if param["type"] in ["int", "float"]:
                min_val = param.get("min", float("-inf"))
                max_val = param.get("max", float("inf"))
                if not (min_val <= value <= max_val):
                    raise ValueError(
                        f"Parameter '{name}' must be between {min_val} and {max_val}."
                    )

            # Validate options for string parameters
            if param["type"] == "str" and "options" in param:
                if value not in param["options"]:
                    raise ValueError(
                        f"Parameter '{name}' must be one of {param['options']}."
                    )

            validated[name] = value
        return validated

    def describe(self) -> str:
        """
        Provide a human-readable description of the style and its parameters.

        Returns:
            str: Description of the style and its parameters.
        """
        description = f"Style: {self.name}\nCategory: {self.category}\nParameters:\n"
        for param in self.parameters:
            description += (
                f"  - {param['name']}: {param['type']} "
                f"(Default: {param.get('default')}, Min: {param.get('min')}, Max: {param.get('max')}, Step: {param.get('step')})\n"
            )
        return description
