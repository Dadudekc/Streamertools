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
        # Initialize and normalize parameter definitions
        params = self.define_parameters()
        # Normalize dict return (name->props) into list of param dicts
        if isinstance(params, dict):
            normalized = []
            for name, props in params.items():
                # Copy props and include name
                prop = dict(props)
                prop['name'] = name
                # Infer type if not provided
                if 'type' not in prop:
                    default = prop.get('default')
                    if isinstance(default, bool):
                        prop['type'] = 'bool'
                    elif isinstance(default, (int,)) and not isinstance(default, bool):
                        prop['type'] = 'int'
                    elif isinstance(default, float):
                        prop['type'] = 'float'
                    else:
                        prop['type'] = 'str'
                # Assign a default step if not provided
                if 'step' not in prop:
                    prop['step'] = 1 if prop['type'] == 'int' else 0.1
                normalized.append(prop)
            self.parameters = normalized
        elif isinstance(params, list):
            self.parameters = params
        else:
            raise TypeError(f"define_parameters must return a dict or list, got {type(params)}")

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
