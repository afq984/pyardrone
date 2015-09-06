import unittest
import pyardrone


class ARDroneConnectExceptionTest(unittest.TestCase):

    def setUp(self):
        self.drone = pyardrone.ARDrone(connect=False)

    def tearDown(self):
        self.drone.close()

    def test_connected_already(self):
        self.drone.connect()
        with self.assertRaises(RuntimeError):
            self.drone.connect()

    def test_disconnected(self):
        self.drone.connect()
        self.drone.close()
        with self.assertRaises(RuntimeError):
            self.drone.connect()
