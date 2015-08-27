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
