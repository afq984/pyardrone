import unittest
from pyardrone import at
from pyardrone.at import arguments


class CommandTest(unittest.TestCase):

    def test_init_by_arg(self):
        cmd = at.REF(3)
        self.assertEqual(cmd.input, 3)

    def test_init_by_kwarg(self):
        cmd = at.REF(input=3)
        self.assertEqual(cmd.input, 3)

    def test_defaults_to_none(self):
        cmd = at.REF()
        self.assertIs(cmd.input, None)

    def test_argument_updatable(self):
        cmd = at.REF()
        cmd.input = 20
        self.assertEqual(cmd.input, 20)
        cmd.input = 14
        self.assertEqual(cmd.input, 14)

    def test_too_many_arguments_raises_TypeError(self):
        with self.assertRaises(TypeError):
            at.REF(3, 7)

    def test_duplicate_value_raises_TypeError(self):
        with self.assertRaises(TypeError):
            at.REF(3, input=7)

    def test_wrong_type_raises_TypeError(self):
        with self.assertRaises(TypeError):
            at.REF(0.5)


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

    def test_str_pack_bytes(self):
        self.assertEqual(
            arguments.StringArg.pack(b'jgoi'),
            b'"jgoi"'
        )


class ArgumentAPITest(unittest.TestCase):

    def assert200(self, value):
        self.assertEqual(value, b'200')

    def test_pack_with_class(self):
        self.assert200(arguments.Int32Arg.pack(200))

    def test_pack_with_instance(self):
        self.assert200(arguments.Int32Arg().pack(200))


if __name__ == '__main__':
    unittest.main()
