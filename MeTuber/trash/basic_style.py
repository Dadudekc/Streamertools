import cv2
import numpy as np
from ..styles.base import Style

class Grayscale(Style):
    """
    A style that converts the image to grayscale.
    """
    name = "Grayscale"
    category = "Basic Styles"
    parameters = []

    def apply(self, image, params=None):
        """
        Convert the image to grayscale.
        :param image: Input BGR image.
        :param params: Unused for this style.
        :return: Grayscale image.
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

class Original(Style):
    """
    A style that returns the original image unmodified.
    """
    name = "Original"
    category = "Basic Styles"
    parameters = []

    def apply(self, image, params=None):
        """
        Return the original image as-is.
        :param image: Input BGR image.
        :param params: Unused for this style.
        :return: Original image.
        """
        return image

class Sepia(Style):
    """
    A style that applies a sepia tone to the image.
    """
    name = "Sepia"
    category = "Basic Styles"
    parameters = [
        {
            "name": "sepia_intensity",
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 2.0,
            "step": 0.1,
            "label": "Sepia Intensity"
        }
    ]

    def apply(self, image, params=None):
        """
        Apply a sepia tone to the image using the specified intensity.
        :param image: Input BGR image.
        :param params: Dictionary of parameters.
        :return: Sepia-toned image.
        """
        if params is None:
            params = {}
        params = self.validate_params(params)

        intensity = params.get("sepia_intensity", 1.0)

        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])

        sepia_image = cv2.transform(image, sepia_filter)
        sepia_image = np.clip(sepia_image * intensity, 0, 255).astype(np.uint8)

        return sepia_image

# Example usage
if __name__ == "__main__":
    import numpy as np

    # Create a dummy image for testing
    dummy_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
    dummy_image = cv2.rectangle(dummy_image, (25, 25), (75, 75), (0, 0, 255), -1)

    grayscale = Grayscale()
    print(grayscale.describe())
    gray_image = grayscale.apply(dummy_image)

    sepia = Sepia()
    print(sepia.describe())
    sepia_image = sepia.apply(dummy_image, {"sepia_intensity": 1.5})

    # Display the results
    cv2.imshow("Grayscale", gray_image)
    cv2.imshow("Sepia", sepia_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
