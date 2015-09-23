/*
 *  generate test data for navdata structures
 */

#include <stdio.h>
#include <navdata_common.h>

#define assert_size(name) printf("self.assertSize(options.%s, %lu)\n", #name, sizeof(name))
#define _assert_size(name) printf("self.assertSize(options._%s, %lu)\n", #name, sizeof(name))
#define assert_option_size(name) printf("self.assertOptionSize(\'%s\', %lu)\n", #name, sizeof(name))

int main(int argc, char** argv)
{
    assert_size(uint8_t);
    assert_size(uint16_t);
    assert_size(uint32_t);
    assert_size(int16_t);
    assert_size(bool_t);
    assert_size(char);
    assert_size(float32_t);

    putchar('\n');

    _assert_size(vector31_t);
    _assert_size(vector21_t);
    _assert_size(velocities_t);
    _assert_size(screen_point_t);
    _assert_size(matrix33_t);

    putchar('\n');

    assert_option_size(navdata_t);

    putchar('\n')

    assert_option_size(navdata_demo_t);
    assert_option_size(navdata_time_t);
    assert_option_size(navdata_raw_measures_t);
    assert_option_size(navdata_pressure_raw_t);
    assert_option_size(navdata_magneto_t);
    assert_option_size(navdata_wind_speed_t);
    assert_option_size(navdata_kalman_pressure_t);
    assert_option_size(navdata_zimmu_3000_t);
    assert_option_size(navdata_phys_measures_t);
    assert_option_size(navdata_gyros_offsets_t);
    assert_option_size(navdata_references_t);
    assert_option_size(navdata_trims_t);
    assert_option_size(navdata_rc_references_t);
    assert_option_size(navdata_pwm_t);
    assert_option_size(navdata_altitude_t);
    assert_option_size(navdata_vision_raw_t);
    assert_option_size(navdata_vision_t);
    assert_option_size(navdata_vision_perf_t);
    assert_option_size(navdata_trackers_send_t);
    assert_option_size(navdata_vision_detect_t);
    assert_option_size(navdata_vision_of_t);
    assert_option_size(navdata_watchdog_t);
    assert_option_size(navdata_adc_data_frame_t);
    assert_option_size(navdata_video_stream_t);
    assert_option_size(navdata_hdvideo_stream_t);
    assert_option_size(navdata_games_t);
    assert_option_size(navdata_wifi_t);
    assert_option_size(navdata_cks_t);

    return 0;
}
