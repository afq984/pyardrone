import unittest
from ctypes import sizeof

from pyardrone.navdata import options


class NavDataSizeTest(unittest.TestCase):

    '''
    Make sure the size of the data strcutures are the same as those in C
    '''

    @staticmethod
    def get_camelcased_name(name):
        return ''.join(sub.capitalize() for sub in name.split('_'))

    @staticmethod
    def trim_name(name):
        assert name.startswith('navdata_') and name.endswith('_t'), name
        return name[8:-2]

    @classmethod
    def get_option_class_by_original_name(cls, name):
        return getattr(options, cls.get_camelcased_name(cls.trim_name(name)))

    def assertSize(self, option_class, size):
        self.assertEqual(sizeof(option_class), size)

    def assertOptionSize(self, name, size):
        self.assertSize(self.get_option_class_by_original_name(name), size)

    def test_basic_type_size(self):
        self.assertSize(options.uint8_t, 1)
        self.assertSize(options.uint16_t, 2)
        self.assertSize(options.uint32_t, 4)
        self.assertSize(options.int16_t, 2)
        self.assertSize(options.bool_t, 4)
        self.assertSize(options.char, 1)
        self.assertSize(options.float32_t, 4)

    def test_container_type_size(self):
        self.assertSize(options._vector31_t, 12)
        self.assertSize(options._vector21_t, 8)
        self.assertSize(options._velocities_t, 12)
        self.assertSize(options._screen_point_t, 8)
        self.assertSize(options._matrix33_t, 36)

    def test_header_size(self):
        # self.assertSize("navdata_t", 20)
        # This is a special case, Navdata
        self.assertEqual(
            sizeof(options.Metadata) + sizeof(options.OptionHeader),
            20
        )

    def test_option_size(self):
        self.assertOptionSize('navdata_demo_t', 148)
        self.assertOptionSize('navdata_time_t', 8)
        self.assertOptionSize('navdata_raw_measures_t', 52)
        self.assertOptionSize('navdata_pressure_raw_t', 18)
        self.assertOptionSize('navdata_magneto_t', 75)
        self.assertOptionSize('navdata_wind_speed_t', 56)
        self.assertOptionSize('navdata_kalman_pressure_t', 72)
        self.assertOptionSize('navdata_zimmu_3000_t', 12)
        self.assertOptionSize('navdata_phys_measures_t', 46)
        self.assertOptionSize('navdata_gyros_offsets_t', 16)
        self.assertOptionSize('navdata_references_t', 88)
        self.assertOptionSize('navdata_trims_t', 16)
        self.assertOptionSize('navdata_rc_references_t', 24)
        self.assertOptionSize('navdata_pwm_t', 76)
        self.assertOptionSize('navdata_altitude_t', 56)
        self.assertOptionSize('navdata_vision_raw_t', 16)
        self.assertOptionSize('navdata_vision_t', 92)
        self.assertOptionSize('navdata_vision_perf_t', 108)
        self.assertOptionSize('navdata_trackers_send_t', 364)
        self.assertOptionSize('navdata_vision_detect_t', 328)
        self.assertOptionSize('navdata_vision_of_t', 44)
        self.assertOptionSize('navdata_watchdog_t', 8)
        self.assertOptionSize('navdata_adc_data_frame_t', 40)
        self.assertOptionSize('navdata_video_stream_t', 65)
        self.assertOptionSize('navdata_hdvideo_stream_t', 32)
        self.assertOptionSize('navdata_games_t', 12)
        self.assertOptionSize('navdata_wifi_t', 8)
        self.assertOptionSize('navdata_cks_t', 8)
