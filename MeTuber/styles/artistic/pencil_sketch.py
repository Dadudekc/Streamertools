import cv2
import numpy as np
from styles.base import Style


class PencilSketch(Style):
    """
    A style that creates a pencil sketch effect on live webcam feeds.
    """
    def __init__(self):
        super().__init__()
        self.name = "Pencil Sketch"
        self.category = "Artistic"

    def define_parameters(self):
        """Define parameters for pencil sketch effect."""
        return {
            "blur_intensity": {"default": 15, "min": 1, "max": 51},
            "contrast": {"default": 1.5, "min": 0.5, "max": 5.0}
        }

    def apply(self, image, params=None):
        """Apply pencil sketch effect to the image.
        
        Args:
            image (numpy.ndarray): Input image in BGR format
            params (dict, optional): Parameters for the effect
                - blur_intensity: Intensity of the blur effect
                - contrast: Contrast adjustment for the sketch
        
        Returns:
            numpy.ndarray: Image with pencil sketch effect in grayscale format
        """
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array")

        # Use default parameters if none provided
        if params is None:
            params = {name: param["default"] for name, param in self.define_parameters().items()}

        # Get and validate parameters
        blur_intensity = params.get("blur_intensity", 15)
        if not 1 <= blur_intensity <= 51:
            raise ValueError("Parameter 'blur_intensity' must be between 1 and 51.")

        contrast = params.get("contrast", 1.5)
        if not 0.5 <= contrast <= 5.0:
            raise ValueError("Parameter 'contrast' must be between 0.5 and 5.0.")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (blur_intensity, blur_intensity), 0)

        # Apply adaptive threshold
        sketch = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )

        # Adjust contrast
        sketch = cv2.convertScaleAbs(sketch, alpha=contrast, beta=0)

        return sketch


# Live webcam feed integration
def process_webcam_feed():
    """
    Processes live webcam feed with the Pencil Sketch effect.
    """
    # Initialize the PencilSketch style
    pencil_sketch = PencilSketch()

    # Default parameters
    params = {"blur_intensity": 21}

    # Start webcam capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # Apply the PencilSketch effect
        sketch_frame = pencil_sketch.apply(frame, params)

        # Display the processed frame
        cv2.imshow("Pencil Sketch - Webcam", sketch_frame)

        # Check for user input to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    process_webcam_feed()
