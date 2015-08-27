import enum
import unittest
from pyardrone import at
from pyardrone.at import arguments, base
from pyardrone.utils import ieee754float


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

    def test_repr(self):
        self.assertEqual(repr(at.REF(3)), 'REF(input=3)')

    def test_equal(self):
        self.assertEqual(at.REF(20), at.REF(20))

    def test_different_commands_with_same_arguments_are_different(self):
        class REF2(base.ATCommand):

            input = arguments.Int32Arg()

        self.assertNotEqual(at.REF(3), REF2(3))

    def test_not_equal_to_other_type(self):
        self.assertNotEqual(at.REF(17), 17)

    def test_pack(self):
        self.assertEqual(at.REF(20).pack(100), b'AT*REF=100,20\r')


class CommandDefaultTest(unittest.TestCase):

    class FOO(base.ATCommand):
        argument = arguments.Int32Arg(default=20)

    def test_default(self):
        self.assertEqual(self.FOO().argument, 20)

    def test_default_overwrite(self):
        bar = self.FOO()
        bar.argument = 9
        self.assertEqual(bar.argument, 9)

        baz = self.FOO()
        baz.argument = 17
        self.assertEqual(baz.argument, 17)


class ArgumentReprTest(unittest.TestCase):

    class Bar(arguments.Argument):
        pass

    def test_repr_without_name(self):
        repr(self.Bar())

    def test_repr_with_name(self):
        bar = self.Bar()
        bar.name = 'parn'
        self.assertEqual(repr(bar), '<Bar:parn>')


class ArgumentCheckTest(unittest.TestCase):

    def test_int32_int_range(self):
        arguments.Int32Arg.check(2 ** 32 - 1)

    def test_int32_out_of_range(self):
        with self.assertRaises(ValueError):
            arguments.Int32Arg.check(2 ** 32)


class ArgumentPackTest(unittest.TestCase):

    def test_description(self):
        self.assertEqual(
            arguments.Int32Arg('hahaha').description,
            'hahaha'
        )

    def test_int_pack(self):
        self.assertEqual(
            arguments.Int32Arg.pack(100),
            b'100'
        )

    def test_int_pack_intenum(self):
        class SomeEnum(enum.IntEnum):
            some_flag = 10

        self.assertEqual(
            arguments.Int32Arg.pack(10),
            b'10'
        )

    def test_float_pack(self):
        # ieee754 specification is not the scope of this test
        self.assertIsInstance(
            arguments.FloatArg.pack(0.5),
            bytes
        )

    def test_float_pack_int(self):
        self.assertEqual(
            arguments.FloatArg.pack(10),
            str(ieee754float(10.)).encode(),
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


class ConstantTest(unittest.TestCase):

    def test_cfg_get_control_mode_is_4(self):
        '''
        Just make sure the range() enumeration is working properly

        8.1.2:
        ...with a mode parameter equaling 4 (CFG_GET_CONTROL_MODE)
        '''
        self.assertEqual(at.CTRL.Modes.CFG_GET_CONTROL_MODE, 4)


if __name__ == '__main__':
    unittest.main()
