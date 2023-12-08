import unittest
from videostream_switcher import switch_camera  # Import the function from your script

class TestCameraSwitching(unittest.TestCase):

    def test_switch_to_camera_2(self):
        # Test switching to camera 2 when brightness exceeds the threshold
        self.assertEqual(switch_camera(1, 101, 100), 2)

    def test_stay_on_camera_1(self):
        # Test staying on camera 1 when brightness is below the threshold
        self.assertEqual(switch_camera(1, 99, 100), 1)

    def test_switch_back_to_camera_1(self):
        # Test switching back to camera 1 when on camera 2 and brightness drops below threshold
        self.assertEqual(switch_camera(2, 99, 100), 1)

    def test_stay_on_camera_2(self):
        # Test staying on camera 2 when on camera 2 and brightness is above the threshold
        self.assertEqual(switch_camera(2, 101, 100), 2)

if __name__ == '__main__':
    unittest.main()
