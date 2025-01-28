```markdown
# OBS Live Filter and Overlay Library

This project is a Python-based library designed to easily apply various image filters and overlays to live Twitch feeds through OBS. With a growing variety of styles and effects, it’s built to be modular, expandable, and user-friendly for streamers who want to add creative flair to their live streams.

## Key Features

- **Filters:** Apply visually stunning effects like vibrant colors, black and white, sepia tones, and more.
- **Overlays:** Create artistic overlays, including halftones, glitch effects, and light leaks.
- **Bitwise Operations:** Perform advanced effects using bitwise AND, OR, and XOR.
- **Customizable:** Modify existing styles or add new filters with ease.
- **Modular Design:** Designed for scalability with a focus on adding new effects quickly.
- **Seamless OBS Integration:** Built to work seamlessly with OBS for live stream customization.
- **Comprehensive Testing:** 80%+ test coverage ensures reliability and stability.
```

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Dadudekc/Streamertools.git
    cd Streamertools
    ```

2. Set up a Python virtual environment:
   ```bash
   python -m venv myenv
   source myenv/bin/activate       # On Windows: myenv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests to verify the setup:
   ```bash
   pytest -n auto --cov=styles tests/
   ```

## Usage

### Example: Applying a Vibrant Color Filter
To apply a vibrant color filter to an image, follow these steps:

```python
import cv2
from styles.basic.vibrant_color import VibrantColor

# Load your image
image = cv2.imread("input.jpg")

# Apply vibrant color filter
vibrant = VibrantColor()
params = {"intensity": 2.0}
result = vibrant.apply(image, params)

# Save the result
cv2.imwrite("output.jpg", result)
```

### Example: Adding a Halftone Overlay
```python
from styles.distortions.halftone import Halftone

# Load your image
image = cv2.imread("input.jpg")

# Apply halftone effect
halftone = Halftone()
params = {"dot_size": 5, "threshold": 100}
result = halftone.apply(image, params)

# Save the result
cv2.imwrite("halftone_output.jpg", result)
```

## Expanding the Library
The library is modular and designed for easy expansion. To add a new style:
1. Create a new file in the appropriate `styles/` subfolder.
2. Define a new class inheriting from `Style` in `base.py`.
3. Implement the `apply` method to process the image and define any parameters.
4. Add unit tests to ensure functionality and reliability.

## Testing

This project includes comprehensive tests with `pytest`. To run all tests:
```bash
pytest -n auto --cov=styles tests/
```

## Contributing

Contributions are welcome! Please fork the repository, make changes, and submit a pull request. Ensure your code follows PEP 8 guidelines and is well-documented.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

Special thanks to the Twitch and OBS communities for inspiring this project. We hope this tool enhances creativity and elevates live streaming experiences!

---

Get started and make your streams shine with personalized filters and overlays! 🚀
