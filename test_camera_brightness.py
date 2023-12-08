import unittest
import cv2
import numpy as np
from videostream_switcher import calculate_brightness  # Import the function from your script

class TestCameraScript(unittest.TestCase):

    def test_calculate_brightness(self):
        # Create a dummy image with known brightness
        dummy_image = np.full((100, 100, 3), fill_value=127, dtype=np.uint8)  # A gray image
        hsv_image = cv2.cvtColor(dummy_image, cv2.COLOR_BGR2HSV)
        expected_brightness = hsv_image[...,2].mean()
        print(f"Expected brightness: {expected_brightness}")

        # Test the calculate_brightness function
        calculated_brightness = calculate_brightness(dummy_image)
        print(f"Calculated brightness: {calculated_brightness}")
        self.assertAlmostEqual(calculated_brightness, expected_brightness, places=2)

if __name__ == '__main__':
    unittest.main()
