import unittest
from unittest import mock

from pyardrone import ARDrone, at, config


config_file_example = '''\
some:config = TRUE
a:number = 3.71
i:am = tired
'''


class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.drone = ARDrone(connect=False)
        self.drone.get_raw_config = mock.Mock(
            spec=self.drone.get_raw_config,
            return_value=config_file_example,
        )
        self.drone.send = mock.Mock(spec=self.drone.send)

    def tearDown(self):
        self.drone.close()

    def test_read_config_by_attribute(self):
        self.assertEqual(self.drone.config.some.config, True)
        self.assertEqual(self.drone.config.a.number, 3.71)
        self.assertEqual(self.drone.config.i.am, 'tired')

    def test_read_config_by_getitem(self):
        self.assertEqual(self.drone.config['some:config'], True)
        self.assertEqual(self.drone.config['a:number'], 3.71)
        self.assertEqual(self.drone.config['i:am'], 'tired')

    def test_set_config_by_attribute(self):
        self.drone.config.a.b = 100
        self.assertEqual(self.drone.config.a.b, 100)
        self.assertEqual(self.drone.config['a:b'], 100)

    def test_set_config_by_setitem(self):
        self.drone.config['a:b'] = 200
        self.assertEqual(self.drone.config.a.b, 200)
        self.assertEqual(self.drone.config['a:b'], 200)

    def test_set_config_sends_command(self):
        self.drone.config.a.b = 32
        self.drone.send.assert_called_once_with(at.CONFIG('a:b', 32))

    def test_config_is_lazy(self):
        self.assertFalse(self.drone.get_raw_config.call_count)

    def test_config_is_cached(self):
        self.drone.config.some.config
        self.drone.config.i.am
        self.assertEqual(self.drone.get_raw_config.call_count, 1)

    def test_config_is_lazy_after_cache_cleared(self):
        self.drone.config.some.config
        self.drone.config.clear_cache()
        self.assertEqual(self.drone.get_raw_config.call_count, 1)

    def test_config_is_updated_again_after_cache_cleared(self):
        self.drone.config.some.config
        self.drone.config.clear_cache()
        self.drone.config.some.config
        self.assertEqual(self.drone.get_raw_config.call_count, 2)

    def test_manually_set_config_is_cached(self):
        self.drone.config.some.config = 1
        self.drone.config.some.config
        self.assertFalse(self.drone.get_raw_config.call_count)

    def test_config_category_repr(self):
        reprs = repr(self.drone.config.QzEw)
        self.assertIn('ConfigCategory', reprs)
        self.assertIn('QzEw', reprs)


class RawConfigUnpackTest(unittest.TestCase):

    def assertUnpacks(self, raw, value):
        unpacked = config.unpack_value(raw)
        self.assertEqual(unpacked, value)
        self.assertEqual(type(unpacked), type(value))

    def test_unpack_int(self):
        self.assertUnpacks('2345', 2345)

    def test_unpack_float(self):
        self.assertUnpacks('3.14', 3.14)

    def test_unpack_float2(self):
        self.assertUnpacks('1e-23', 1e-23)

    def test_unpack_list_of_floats(self):
        self.assertUnpacks('{ 1.5 2.4 3.8 4.8 }', [1.5, 2.4, 3.8, 4.8])

    def test_unpack_string(self):
        self.assertUnpacks('My ARDrone', 'My ARDrone')

    def test_unpack_true(self):
        self.assertUnpacks('TRUE', True)

    def test_unpack_false(self):
        self.assertUnpacks('FALSE', False)


class ConfigFileIterTest(unittest.TestCase):

    def test_iter(self):
        self.assertEqual(
            list(config.iter_config_file(config_file_example)),
            [
                ('some:config', True),
                ('a:number', 3.71),
                ('i:am', 'tired')
            ]
        )
