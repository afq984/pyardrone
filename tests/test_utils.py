import unittest
from pyardrone.utils import repack_to_int, bits, noop


class IEEE754Test(unittest.TestCase):

    def test_mdot8(self):
        '''
        According to ARDrone Developer Guide chapter 6.3,
        -0.8 can be considered as holding the 32-bit integer value −1085485875
        '''
        self.assertEqual(repack_to_int(-0.8), -1085485875)


class BitsTest(unittest.TestCase):

    def test_bit_0_is_1(self):
        self.assertEqual(bits(0), 1)

    def test_bit_4_is_0x10(self):
        self.assertEqual(bits(4), 0x10)

    def test_bits_accepts_multiple_arguments(self):
        self.assertEqual(bits(1) + bits(13) + bits(6), bits(1, 13, 6))


class NoopTest(unittest.TestCase):

    def test_whatever(self):
        self.assertEqual(noop(3 + 4), 7)
        self.assertEqual(noop(1), True)
