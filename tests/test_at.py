import enum
import unittest
from pyardrone import at
from pyardrone.at import parameters, base
from pyardrone.utils import repack_to_int


class CommandTest(unittest.TestCase):

    def test_init_by_arg(self):
        cmd = at.REF_0_5(3)
        self.assertEqual(cmd.input, 3)

    def test_init_by_kwarg(self):
        cmd = at.REF_0_5(input=3)
        self.assertEqual(cmd.input, 3)

    def test_too_many_arguments_raises_TypeError(self):
        with self.assertRaises(TypeError):
            at.REF_0_5(3, 7)

    def test_duplicate_value_raises_TypeError(self):
        with self.assertRaises(TypeError):
            at.REF_0_5(3, input=7)

    def test_wrong_type_raises_TypeError(self):
        with self.assertRaises(TypeError):
            at.REF_0_5(0.5)

    def test_repr(self):
        self.assertEqual(repr(at.REF_0_5(3)), 'REF(input=3)')

    def test_equal(self):
        self.assertEqual(at.REF_0_5(20), at.REF_0_5(20))

    def test_unequal_different_argument(self):
        self.assertNotEqual(at.REF_0_5(10), at.REF_0_5(12))

    def test_different_commands_with_same_arguments_are_different(self):
        class REF_0_52(base.ATCommand):

            input = parameters.Int32()

        self.assertNotEqual(at.REF_0_5(3), REF_0_52(3))

    def test_not_equal_to_other_type(self):
        self.assertNotEqual(at.REF_0_5(17), 17)

    def test_pack(self):
        self.assertEqual(at.REF_0_5(20)._pack(100), b'AT*REF=100,20\r')

    def test_command_arguments_can_not_be_assigned(self):
        with self.assertRaises(AttributeError):
            at.REF_0_5(10).input = 11

    def test_attributes_which_are_not_arguments_can_be_assigned(self):
        at.REF_0_5(11).some_attribute = 20

    def test_parameterless_pack_does_not_end_with_comma(self):
        self.assertEqual(
            at.COMWDG()._pack(100),
            b'AT*COMWDG=100\r'
        )


class CommandDefaultTest(unittest.TestCase):

    class FOO(base.ATCommand):
        argument = parameters.Int32(default=20)

    def test_default(self):
        self.assertEqual(self.FOO().argument, 20)


class ParameterClassTest(unittest.TestCase):

    def test_pack_required(self):
        with self.assertRaises(NotImplementedError):
            parameters.Parameter._pack(10)

    def test_check_optional(self):
        parameters.Parameter._check(10)


class ParameterReprTest(unittest.TestCase):

    class Bar(parameters.Parameter):
        pass

    def test_repr_without_name(self):
        obj = self.Bar()
        self.assertEqual(object.__repr__(obj), repr(obj))

    def test_repr_with_name(self):
        bar = self.Bar()
        bar._name = 'parn'
        self.assertEqual(repr(bar), '<Bar:parn>')


class ParameterCheckTest(unittest.TestCase):

    def test_int32_int_range(self):
        parameters.Int32._check(2 ** 32 - 1)

    def test_int32_out_of_range(self):
        with self.assertRaises(ValueError):
            parameters.Int32._check(2 ** 32)


class ParameterPackTest(unittest.TestCase):

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
            str(repack_to_int(10.)).encode(),
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


class ParameterAPITest(unittest.TestCase):

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


class AtREFDefaults(unittest.TestCase):

    def test_defaults_are_added(self):
        self.assertEqual(at.REF(60).input, 60 | at.REF.input.default)

    def test_defaults_can_be_disabled(self):
        self.assertEqual(at.REF(60, use_default_bits=False).input, 60)

    def test_pack_equal(self):
        self.assertEqual(
            at.REF()._pack(4),
            at.REF_0_5(at.REF_0_5.input.default)._pack(4))

    def test_pack_default(self):
        # issue 16
        self.assertEqual(
            b'AT*REF=26,290718208\r',
            at.REF(at.REF.input.start)._pack(26)
        )


if __name__ == '__main__':
    unittest.main()
