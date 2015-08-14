import unittest
from pyardrone.at import commands


class CommandTest(unittest.TestCase):

    def test_init_by_arg(self):
        cmd = commands.REF(3)
        self.assertEqual(cmd.input.value, 3)

    def test_init_by_kwarg(self):
        cmd = commands.REF(input=3)
        self.assertEqual(cmd.input.value, 3)

    def test_defaults_to_none(self):
        cmd = commands.REF()
        self.assertIs(cmd.input.value, None)

    def test_argument_updatable(self):
        cmd = commands.REF()
        cmd.input = 20
        self.assertEqual(cmd.input.value, 20)
        cmd.input = 14
        self.assertEqual(cmd.input.value, 14)

    def test_too_many_arguments_raises_TypeError(self):
        with self.assertRaises(TypeError):
            commands.REF(3, 7)

    def test_duplicate_value_raises_TypeError(self):
        with self.assertRaises(TypeError):
            commands.REF(3, input=7)

    def test_wrong_type_raises_TypeError(self):
        with self.assertRaises(TypeError):
            commands.REF(0.5)


if __name__ == '__main__':
    unittest.main()
