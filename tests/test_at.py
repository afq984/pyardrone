import enum
import unittest
from pyardrone import at
from pyardrone.at import parameters, base
from pyardrone.utils import ieee754float


class CommandTest(unittest.TestCase):

    def test_init_by_arg(self):
        cmd = at.REF(3)
        self.assertEqual(cmd.input, 3)

    def test_init_by_kwarg(self):
        cmd = at.REF(input=3)
        self.assertEqual(cmd.input, 3)

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

    def test_unequal_different_argument(self):
        self.assertNotEqual(at.REF(10), at.REF(12))

    def test_different_commands_with_same_arguments_are_different(self):
        class REF2(base.ATCommand):

            input = parameters.Int32()

        self.assertNotEqual(at.REF(3), REF2(3))

    def test_not_equal_to_other_type(self):
        self.assertNotEqual(at.REF(17), 17)

    def test_pack(self):
        self.assertEqual(at.REF(20)._pack(100), b'AT*REF=100,20\r')

    def test_command_arguments_can_not_be_assigned(self):
        with self.assertRaises(AttributeError):
            at.REF(10).input = 11

    def test_attributes_which_are_not_arguments_can_be_assigned(self):
        at.REF(11).some_attribute = 20


class CommandDefaultTest(unittest.TestCase):

    class FOO(base.ATCommand):
        argument = parameters.Int32(default=20)

    def test_default(self):
        self.assertEqual(self.FOO().argument, 20)


class ArgumentReprTest(unittest.TestCase):

    class Bar(parameters.Parameter):
        pass

    def test_repr_without_name(self):
        repr(self.Bar())

    def test_repr_with_name(self):
        bar = self.Bar()
        bar._name = 'parn'
        self.assertEqual(repr(bar), '<Bar:parn>')


class ArgumentCheckTest(unittest.TestCase):

    def test_int32_int_range(self):
        parameters.Int32._check(2 ** 32 - 1)

    def test_int32_out_of_range(self):
        with self.assertRaises(ValueError):
            parameters.Int32._check(2 ** 32)


class ArgumentPackTest(unittest.TestCase):

    def test_description(self):
        self.assertEqual(
            parameters.Int32('hahaha').__doc__,
            'hahaha'
        )

    def test_int_pack(self):
        self.assertEqual(
            parameters.Int32._pack(100),
            b'100'
        )

    def test_int_pack_intenum(self):
        class SomeEnum(enum.IntEnum):
            some_flag = 10

        self.assertEqual(
            parameters.Int32._pack(10),
            b'10'
        )

    def test_float_pack(self):
        # ieee754 specification is not the scope of this test
        self.assertIsInstance(
            parameters.Float._pack(0.5),
            bytes
        )

    def test_float_pack_int(self):
        self.assertEqual(
            parameters.Float._pack(10),
            str(ieee754float(10.)).encode(),
        )

    def test_str_pack_int(self):
        self.assertEqual(
            parameters.String._pack(6543),
            b'"6543"'
        )

    def test_str_pack_float(self):
        self.assertEqual(
            parameters.String._pack(0.5),
            b'"0.5"',
        )

    def test_str_pack_str(self):
        self.assertEqual(
            parameters.String._pack('ertb3'),
            b'"ertb3"',
        )

    def test_str_pack_true(self):
        self.assertEqual(
            parameters.String._pack(True),
            b'"TRUE"'
        )

    def test_str_pack_false(self):
        self.assertEqual(
            parameters.String._pack(False),
            b'"FALSE"'
        )

    def test_str_pack_bytes(self):
        self.assertEqual(
            parameters.String._pack(b'jgoi'),
            b'"jgoi"'
        )


class ArgumentAPITest(unittest.TestCase):

    def assert200(self, value):
        self.assertEqual(value, b'200')

    def test_pack_with_class(self):
        self.assert200(parameters.Int32._pack(200))

    def test_pack_with_instance(self):
        self.assert200(parameters.Int32()._pack(200))


class ConstantTest(unittest.TestCase):

    def test_cfg_get_control_mode_is_4(self):
        '''
        Just make sure the range() enumeration is working properly

        8.1.2:
        ...with a mode parameter equaling 4 (CFG_GET_CONTROL_MODE)
        '''
        self.assertEqual(at.CTRL.mode.CFG_GET_CONTROL_MODE, 4)


if __name__ == '__main__':
    unittest.main()
