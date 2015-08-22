import unittest
from pyardrone.at import commands, arguments


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


class ArgumentTest(unittest.TestCase):

    def test_int_pack(self):
        self.assertEqual(
            arguments.Int32Arg.pack(100),
            b'100'
        )

    def test_float_pack(self):
        # ieee754 specification is not the scope of this test
        self.assertIsInstance(
            arguments.FloatArg.pack(0.5),
            bytes
        )

    def test_str_pack_int(self):
        self.assertEqual(
            arguments.StringArg.pack(6543),
            b'"6543"'
        )

    def test_str_pack_float(self):
        self.assertEqual(
            arguments.StringArg.pack(0.5),
            b'"0.5"',
        )

    def test_str_pack_str(self):
        self.assertEqual(
            arguments.StringArg.pack('ertb3'),
            b'"ertb3"',
        )

    def test_str_pack_true(self):
        self.assertEqual(
            arguments.StringArg.pack(True),
            b'"TRUE"'
        )

    def test_str_pack_false(self):
        self.assertEqual(
            arguments.StringArg.pack(False),
            b'"FALSE"'
        )


if __name__ == '__main__':
    unittest.main()
