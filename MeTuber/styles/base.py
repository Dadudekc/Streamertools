import numpy as np
from typing import List, Dict, Optional, Any


class Style:
    """
    Base class for all styles.
    """
    name: str = "Base Style"
    category: str = "Uncategorized"
    parameters: List[Dict[str, Any]] = []

    def __init__(self):
        # Initialize default parameters dynamically based on the class definition
        self.default_params: Dict[str, Any] = {
            param["name"]: param.get("default", None) for param in self.parameters
        }

    def validate_params(self, params):
        """
        Validates and sanitizes the input parameters against the defined parameters.
        :param params: Dictionary of input parameters.
        :return: Validated parameter dictionary.
        """
        validated_params = {}
        for param in self.parameters:
            name = param["name"]
            param_type = param["type"]
            value = params.get(name, self.default_params.get(name))

            # Ensure the parameter value respects its type and constraints
            if param_type == "int":
                if value < param["min"] or value > param["max"]:
                    raise ValueError(f"Parameter '{name}' must be between {param['min']} and {param['max']}.")
                value = int(value)
            elif param_type == "float":
                if value < param["min"] or value > param["max"]:
                    raise ValueError(f"Parameter '{name}' must be between {param['min']} and {param['max']}.")
                value = float(value)
            elif param_type == "str":
                if "options" in param and value not in param["options"]:
                    raise ValueError(f"Parameter '{name}' must be one of {param['options']}.")

            validated_params[name] = value

        return validated_params

    def apply(self, image: Optional[np.ndarray], params: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Apply the style to the image.
        :param image: Input BGR image.
        :param params: Dictionary of parameters.
        :return: Processed image.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image provided. Expected a NumPy array.")

        if params is None:
            params = {}
        params = self.validate_params(params)

        return image

    def describe(self) -> str:
        """
        Provide a human-readable description of the style and its parameters.
        :return: String describing the style.
        """
        description = f"Style: {self.name}\nCategory: {self.category}\nParameters:\n"
        for param in self.parameters:
            description += f"  - {param['name']}: {param['type']} (Default: {param.get('default')}, Min: {param.get('min')}, Max: {param.get('max')}, Step: {param.get('step')})\n"
        return description
