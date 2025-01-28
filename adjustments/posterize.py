import numpy as np
from styles.base import Style


class Posterize(Style):
    name = "Posterize"
    parameters = [
        {
            "name": "bits",
            "type": "int",
            "default": 6,
            "min": 1,
            "max": 8,
            "step": 1,
            "label": "Bits"
        }
    ]

    def apply(self, image, params=None):
        if params is None:
            params = {}
        params = self.validate_params(params)

        bits = params["bits"]
        shift = 8 - bits
        poster
