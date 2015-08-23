import unittest
from pyardrone.utils import ieee754float


class IEEE754Test(unittest.TestCase):

    def test_mdot8(self):
        '''
        According to ARDrone Developer Guide chapter 6.3,
        -0.8 can be considered as holding the 32-bit integer value −1085485875
        '''
        self.assertEqual(ieee754float(-0.8), -1085485875)


if __name__ == '__main__':
    unittest.main()
