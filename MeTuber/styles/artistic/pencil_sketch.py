import cv2
import numpy as np
from styles.base import Style


class PencilSketch(Style):
    """
    A style that creates a pencil sketch effect on live webcam feeds.
    """
    name = "Pencil Sketch"
    category = "Artistic"
    parameters = [
        {
            "name": "blur_intensity",
            "type": "int",
            "default": 21,
            "min": 1,
            "max": 51,
            "step": 2,
            "label": "Blur Intensity",
        }
    ]

    def define_parameters(self):
        return self.parameters

    def apply(self, image, params=None):
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a valid NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input must be a 3-channel BGR image.")

        # Validate and sanitize parameters
        params = self.validate_params(params or {})
        blur_intensity = params["blur_intensity"]

        # Ensure blur intensity is odd
        if blur_intensity % 2 == 0:
            blur_intensity += 1

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Invert the grayscale image
        inverted_gray = cv2.bitwise_not(gray)

        # Apply Gaussian blur to the inverted image
        blurred = cv2.GaussianBlur(inverted_gray, (blur_intensity, blur_intensity), 0)

        # Invert the blurred image
        inverted_blur = cv2.bitwise_not(blurred)

        # Combine the grayscale and inverted blur to create the pencil sketch effect
        sketch = cv2.divide(gray, inverted_blur, scale=256.0)

        # Convert single-channel sketch to BGR for compatibility with video feeds
        sketch_bgr = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

        return sketch_bgr


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
