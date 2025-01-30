import cv2
import numpy as np
import threading
from styles.base import Style


class AdvancedPencilSketch(Style):
    """
    An enhanced Pencil Sketch effect with improved edge detection and adaptive blending.
    """
    name = "Advanced Pencil Sketch"
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
        },
        {
            "name": "stroke_thickness",
            "type": "int",
            "default": 3,
            "min": 1,
            "max": 7,
            "step": 1,
            "label": "Stroke Thickness",
        },
        {
            "name": "detail_preservation",
            "type": "float",
            "default": 0.5,
            "min": 0.1,
            "max": 1.0,
            "step": 0.1,
            "label": "Detail Preservation",
        },
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
        stroke_thickness = params["stroke_thickness"]
        detail_preservation = params["detail_preservation"]

        # Ensure blur intensity is odd
        if blur_intensity % 2 == 0:
            blur_intensity += 1

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply bilateral filtering to enhance details while reducing noise
        filtered_gray = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

        # Invert the grayscale image
        inverted_gray = cv2.bitwise_not(filtered_gray)

        # Apply Gaussian blur to the inverted image
        blurred = cv2.GaussianBlur(inverted_gray, (blur_intensity, blur_intensity), 0)

        # Invert the blurred image
        inverted_blur = cv2.bitwise_not(blurred)

        # Create a pencil sketch effect
        sketch = cv2.divide(filtered_gray, inverted_blur, scale=256.0)

        # Edge refinement using adaptive thresholding
        edges = cv2.adaptiveThreshold(
            filtered_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, stroke_thickness
        )

        # Blend the sketch with detected edges for a refined stroke effect
        combined_sketch = cv2.addWeighted(sketch, detail_preservation, edges, (1 - detail_preservation), 0)

        # Convert to BGR for compatibility with video processing
        sketch_bgr = cv2.cvtColor(combined_sketch, cv2.COLOR_GRAY2BGR)

        return sketch_bgr


# =========================
# **🔹 Multi-Threaded Webcam Processing**
# =========================
class WebcamPencilSketchProcessor:
    """
    Processes live webcam feed with the Advanced Pencil Sketch effect.
    Runs in a separate thread for optimal performance.
    """

    def __init__(self):
        self.pencil_sketch = AdvancedPencilSketch()
        self.params = {
            "blur_intensity": 21,
            "stroke_thickness": 3,
            "detail_preservation": 0.5,
        }
        self.cap = cv2.VideoCapture(0)
        self.running = True

    def update_params(self, new_params):
        """Update parameters dynamically while running."""
        self.params.update(new_params)

    def process_frame(self):
        """Capture and process frames in real-time."""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame from webcam.")
                break

            # Apply the Advanced Pencil Sketch effect
            sketch_frame = self.pencil_sketch.apply(frame, self.params)

            # Display the processed frame
            cv2.imshow("Advanced Pencil Sketch - Webcam", sketch_frame)

            # Check for user input to quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.running = False

        # Release the webcam and close all windows
        self.cap.release()
        cv2.destroyAllWindows()

    def start(self):
        """Start processing the webcam feed in a separate thread."""
        processing_thread = threading.Thread(target=self.process_frame)
        processing_thread.daemon = True
        processing_thread.start()


if __name__ == "__main__":
    # Initialize and start the webcam processor
    sketch_processor = WebcamPencilSketchProcessor()
    sketch_processor.start()

    # Simulate live parameter adjustments (For testing)
    import time
    for i in range(10):
        new_params = {
            "blur_intensity": 15 + (i % 5) * 2,
            "stroke_thickness": 2 + (i % 3),
            "detail_preservation": 0.3 + (i % 5) * 0.1,
        }
        print(f"Updating parameters: {new_params}")
        sketch_processor.update_params(new_params)
        time.sleep(2)  # Simulating UI updates
