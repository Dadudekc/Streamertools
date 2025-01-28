import cv2
import numpy as np
from styles.base import Style


class Mosaic(Style):
    """
    A style that applies a mosaic effect to the image by resizing down and back up.
    """

    name = "Mosaic"
    category = "Distortions"
    parameters = [
        {
            "name": "tile_size",
            "type": "int",
            "default": 10,
            "min": 2,
            "max": 50,
            "step": 1,
            "label": "Tile Size",
        }
    ]

    def define_parameters(self):
        """
        Define the parameters for the Mosaic effect.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Apply the mosaic effect using the validated parameters.

        Args:
            image (numpy.ndarray): Input BGR image.
            params (dict, optional): Parameters for the mosaic effect.

        Returns:
            numpy.ndarray: The image with a mosaic effect applied.

        Raises:
            ValueError: If the input image is None or invalid.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        # Validate and sanitize parameters
        params = self.validate_params(params)

        tile_size = params["tile_size"]
        h, w = image.shape[:2]

        # Ensure tile_size does not exceed the image dimensions
        if tile_size > min(h, w):
            raise ValueError(f"Tile size ({tile_size}) cannot exceed the smaller image dimension ({min(h, w)}).")

        # Resize down to create larger "tiles"
        mosaic_image = cv2.resize(
            image, 
            (w // tile_size, h // tile_size), 
            interpolation=cv2.INTER_AREA
        )

        # Resize back up to original size to create the mosaic effect
        mosaic_image = cv2.resize(
            mosaic_image, 
            (w, h), 
            interpolation=cv2.INTER_NEAREST
        )

        return mosaic_image


# Example usage
if __name__ == "__main__":
    # Create a dummy image for testing
    dummy_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
    dummy_image = cv2.rectangle(dummy_image, (25, 25), (75, 75), (0, 255, 0), -1)

    # Initialize Mosaic style
    mosaic = Mosaic()

    # Print style description
    print(mosaic.describe())

    # Apply mosaic effect with a tile size of 5
    try:
        mosaic_image = mosaic.apply(dummy_image, {"tile_size": 5})

        # Display the result
        cv2.imshow("Mosaic Effect", mosaic_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error applying mosaic effect: {e}")
