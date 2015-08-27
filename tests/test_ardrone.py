import unittest
import pyardrone


class ARDroneIntervalTest(unittest.TestCase):

    def setUp(self):
        self.drone = pyardrone.ARDrone(connect=False)

    def testSetInterval(self):
        self.drone.interval = 200
        self.assertEqual(self.drone.interval, 200)
        self.assertEqual(self.drone._at_executor.interval, 200)

    def testSetExecutorInterval(self):
        self.drone._at_executor.interval = 30
        self.assertEqual(self.drone.interval, 30)
