import cv2
from styles.base import Style


class OilPainting(Style):
    """
    Applies an oil painting effect to the image.
    """

    name = "Oil Painting"
    category = "Artistic"
    parameters = [
        {
            "name": "size",
            "type": "int",
            "default": 7,
            "min": 1,
            "max": 15,
            "step": 2,
            "label": "Size",
        },
        {
            "name": "dyn_ratio",
            "type": "int",  # Updated to integer to align with OpenCV's requirement
            "default": 1,
            "min": 0,
            "max": 2,
            "step": 1,
            "label": "Dyn Ratio",
        },
    ]

    def define_parameters(self):
        """
        Define the parameters for this style.
        Returns:
            list: List of parameter dictionaries.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Applies an oil painting effect to the image using OpenCV's stylization.

        Args:
            image (numpy.ndarray): The input image in BGR format.
            params (dict, optional): Parameters for oil painting effect.

        Returns:
            numpy.ndarray: The oil painting-stylized image.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Validate and sanitize parameters
        params = self.validate_params(params)

        size = params["size"]
        dyn_ratio = max(1, int(params["dyn_ratio"]))  # Ensure dyn_ratio is an int >= 1

        # Apply oil painting effect
        try:
            oil_painting = cv2.xphoto.oilPainting(image, size=size, dynRatio=dyn_ratio)
        except cv2.error as e:
            raise RuntimeError(f"OpenCV error during oil painting effect: {e}")

        return oil_painting
