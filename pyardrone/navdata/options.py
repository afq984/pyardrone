'''
This module corresponds to ARDroneLib/Soft/Common/navdata_common.h
'''

import ctypes
import functools

from pyardrone.utils.structure import Structure


uint8_t = ctypes.c_uint8
uint16_t = ctypes.c_uint16
uint32_t = ctypes.c_uint32
int16_t = ctypes.c_int16
int32_t = ctypes.c_int32
bool_t = ctypes.c_uint32  # ARDroneTool's bool is 4 bytes
char = ctypes.c_char
float32_t = ctypes.c_float


NB_GYROS = 3
NB_ACCS = 3
NB_NAVDATA_DETECTION_RESULTS = 4

NB_CORNER_TRACKERS_WIDTH = 5
NB_CORNER_TRACKERS_HEIGHT = 4

DEFAULT_NB_TRACKERS_WIDTH = NB_CORNER_TRACKERS_WIDTH + 1
DEFAULT_NB_TRACKERS_HEIGHT = NB_CORNER_TRACKERS_HEIGHT + 1

NAVDATA_MAX_CUSTOM_TIME_SAVE = 20


_vector31_t = float32_t * 3
_velocities_t = _vector31_t
_vector21_t = float32_t * 2
_screen_point_t = int32_t * 2
_matrix33_t = float32_t * 3 * 3


class OptionHeader(dict):

    def register(self, tag):
        return functools.partial(self._register, tag)

    def _register(self, tag, function):
        if tag in self:
            raise KeyError('Key {!r} conflict with existing item {}'.format(
                tag, self[tag]))
        self[tag] = function
        return function


index = OptionHeader()


class Metadata(Structure):

    '''
    Header of :py:class:`~pyardrone.navdata.NavData`.

    Available via :py:class:`~pyardrone.navdata.NavData`.metadata

    Corresponds to C struct ``navdata_t``.
    '''

    _pack_ = 1

    _attrname = 'metadata'

    header = uint32_t  #: Should be 0x55667788

    #: raw drone state,
    #: see also: :py:class:`~pyardrone.navdata.states.DroneState`
    state = uint32_t

    sequence_number = uint32_t  #:
    vision_flag = uint32_t  #:


class OptionHeader(Structure):

    _pack_ = 1

    tag = uint16_t
    size = uint16_t


@index.register(0)
class Demo(OptionHeader):

    '''
    Minimal navigation data for all flights.

    Corresponds to C struct ``navdata_demo_t``.
    '''

    _attrname = 'demo'

    #: Flying state (landed, flying, hovering, etc.)
    #: defined in CTRL_STATES enum.
    ctrl_state = uint32_t

    vbat_flying_percentage = uint32_t  #: battery voltage filtered (mV)

    theta = float32_t  #: UAV's pitch in milli-degrees
    phi = float32_t  #: UAV's roll  in milli-degrees
    psi = float32_t  #: UAV's yaw   in milli-degrees

    altitude = int32_t  #: UAV's altitude in centimeters

    vx = float32_t  #: UAV's estimated linear velocity
    vy = float32_t  #: UAV's estimated linear velocity
    vz = float32_t  #: UAV's estimated linear velocity

    #: streamed frame index   Not used -> To integrate in video stage.
    num_frames = uint32_t

    # Camera parameters compute by detection
    detection_camera_rot = _matrix33_t  #: Deprecated ! Don't use !
    detection_camera_trans = _vector31_t  #: Deprecated ! Don't use !
    detection_tag_index = uint32_t  #: Deprecated ! Don't use !

    detection_camera_type = uint32_t  #: Type of tag searched in detection

    # Camera parameters compute by drone
    drone_camera_rot = _matrix33_t  #: Deprecated ! Don't use !
    drone_camera_trans = _vector31_t  #: Deprecated ! Don't use !


@index.register(1)
class Time(OptionHeader):

    '''
    Timestamp

    Corresponds to C struct ``navdata_time_t``.
    '''

    _attrname = 'time'

    #: 32 bit value where the 11 most significant bits represents the seconds,
    #: and the 21 least significant bits are the microseconds.
    time = uint32_t


@index.register(2)
class RawMeasures(OptionHeader):

    '''
    Raw sensors measurements

    Corresponds to C struct ``navdata_raw_measures_t``.
    '''

    _attrname = 'raw_measures'

    # +12 bytes
    raw_accs = uint16_t * NB_ACCS  #: filtered accelerometers
    raw_gyros = int16_t * NB_GYROS  #: filtered gyrometers
    raw_gyros_110 = int16_t * 2  #: gyrometers  x/y 110 deg/s
    vbat_raw = uint32_t  #: battery voltage raw (mV)
    us_debut_echo = uint16_t
    us_fin_echo = uint16_t
    us_association_echo = uint16_t
    us_distance_echo = uint16_t
    us_courbe_temps = uint16_t
    us_courbe_valeur = uint16_t
    us_courbe_ref = uint16_t
    flag_echo_ini = uint16_t
    # TODO:   uint16_t  frame_number  from ARDrone_Magneto
    nb_echo = uint16_t
    sum_echo = uint32_t
    alt_temp_raw = int32_t
    gradient = int16_t


@index.register(21)
class PressureRaw(OptionHeader):

    'Corresponds to C struct ``navdata_pressure_raw_t``.'

    _attrname = 'pressure_raw'

    up = int32_t
    ut = int16_t
    Temperature_meas = int32_t
    Pression_meas = int32_t


@index.register(22)
class Magneto(OptionHeader):

    'Corresponds to C struct ``navdata_magneto_t``.'

    _attrname = 'magneto'

    mx = int16_t
    my = int16_t
    mz = int16_t
    magneto_raw = _vector31_t  #: magneto in the body frame, in mG
    magneto_rectified = _vector31_t
    magneto_offset = _vector31_t
    heading_unwrapped = float32_t
    heading_gyro_unwrapped = float32_t
    heading_fusion_unwrapped = float32_t
    magneto_calibration_ok = char
    magneto_state = uint32_t
    magneto_radius = float32_t
    error_mean = float32_t
    error_var = float32_t


@index.register(23)
class WindSpeed(OptionHeader):

    'Corresponds to C struct ``navdata_wind_speed_t``.'

    _attrname = 'wind_speed'

    wind_speed = float32_t  #: estimated wind speed [m/s]

    #: estimated wind direction in North-East frame [rad] e.g.
    #: if wind_angle is pi/4, wind is from South-West to North-East
    wind_angle = float32_t

    wind_compensation_theta = float32_t
    wind_compensation_phi = float32_t
    state_x1 = float32_t
    state_x2 = float32_t
    state_x3 = float32_t
    state_x4 = float32_t
    state_x5 = float32_t
    state_x6 = float32_t
    magneto_debug1 = float32_t
    magneto_debug2 = float32_t
    magneto_debug3 = float32_t


@index.register(24)
class KalmanPressure(OptionHeader):

    'Corresponds to C struct ``navdata_kalman_pressure_t``.'

    _attrname = 'kalman_pressure'

    offset_pressure = float32_t
    est_z = float32_t
    est_zdot = float32_t
    est_bias_PWM = float32_t
    est_biais_pression = float32_t
    offset_US = float32_t
    prediction_US = float32_t
    cov_alt = float32_t
    cov_PWM = float32_t
    cov_vitesse = float32_t
    bool_effet_sol = bool_t
    somme_inno = float32_t
    flag_rejet_US = bool_t
    u_multisinus = float32_t
    gaz_altitude = float32_t
    Flag_multisinus = bool_t
    Flag_multisinus_debut = bool_t


@index.register(27)
class Zimmu3000(OptionHeader):

    'Corresponds to C struct ``navdata_zimmu_3000_t``.'

    _attrname = 'zimmu_3000'

    vzimmuLSB = int32_t
    vzfind = float32_t


@index.register(3)
class PhysMeasures(OptionHeader):

    'Corresponds to C struct ``navdata_phys_measures_t``.'

    _attrname = 'phys_measures'

    accs_temp = float32_t
    gyro_temp = uint16_t
    phys_accs = float32_t * NB_ACCS
    phys_gyros = float32_t * NB_GYROS
    alim3V3 = uint32_t  #: 3.3volt alim [LSB]
    vrefEpson = uint32_t  #: ref volt Epson gyro [LSB]
    vrefIDG = uint32_t  #: ref volt IDG gyro [LSB]


@index.register(4)
class GyrosOffsets(OptionHeader):

    'Corresponds to C struct ``navdata_gyros_offsets_t``.'

    _attrname = 'gyros_offsets'

    offset_g = float32_t * NB_GYROS


@index.register(5)
class EulerAngles(OptionHeader):

    'Corresponds to C struct ``navdata_euler_angles_t``.'

    _attrname = 'eular_angles'

    theta_a = float32_t
    phi_a = float32_t


@index.register(6)
class References(OptionHeader):

    'Corresponds to C struct ``navdata_references_t``.'

    _attrname = 'references'

    ref_theta = int32_t
    ref_phi = int32_t
    ref_theta_I = int32_t
    ref_phi_I = int32_t
    ref_pitch = int32_t
    ref_roll = int32_t
    ref_yaw = int32_t
    ref_psi = int32_t

    vx_ref = float32_t
    vy_ref = float32_t
    theta_mod = float32_t
    phi_mod = float32_t

    k_v_x = float32_t
    k_v_y = float32_t
    k_mode = uint32_t

    ui_time = float32_t
    ui_theta = float32_t
    ui_phi = float32_t
    ui_psi = float32_t
    ui_psi_accuracy = float32_t
    ui_seq = int32_t


@index.register(7)
class Trims(OptionHeader):

    'Corresponds to C struct ``navdata_trims_t``.'

    _attrname = 'trims'

    angular_rates_trim_r = float32_t
    euler_angles_trim_theta = float32_t
    euler_angles_trim_phi = float32_t


@index.register(8)
class RcReferences(OptionHeader):

    'Corresponds to C struct ``navdata_rc_references_t``.'

    _attrname = 'rc_references'

    rc_ref_pitch = int32_t
    rc_ref_roll = int32_t
    rc_ref_yaw = int32_t
    rc_ref_gaz = int32_t
    rc_ref_ag = int32_t


@index.register(9)
class Pwm(OptionHeader):

    'Corresponds to C struct ``navdata_pwm_t``.'

    _attrname = 'pwm'

    motor1 = uint8_t
    motor2 = uint8_t
    motor3 = uint8_t
    motor4 = uint8_t
    sat_motor1 = uint8_t
    sat_motor2 = uint8_t
    sat_motor3 = uint8_t
    sat_motor4 = uint8_t
    gaz_feed_forward = float32_t
    gaz_altitude = float32_t
    altitude_integral = float32_t
    vz_ref = float32_t
    u_pitch = int32_t
    u_roll = int32_t
    u_yaw = int32_t
    yaw_u_I = float32_t
    u_pitch_planif = int32_t
    u_roll_planif = int32_t
    u_yaw_planif = int32_t
    u_gaz_planif = float32_t
    current_motor1 = uint16_t
    current_motor2 = uint16_t
    current_motor3 = uint16_t
    current_motor4 = uint16_t
    # WARNING: new navdata (FC 26/07/2011)
    altitude_prop = float32_t
    altitude_der = float32_t


@index.register(10)
class Altitude(OptionHeader):

    'Corresponds to C struct ``navdata_altitude_t``.'

    _attrname = 'altitude'

    altitude_vision = int32_t
    altitude_vz = float32_t
    altitude_ref = int32_t
    altitude_raw = int32_t

    obs_accZ = float32_t
    obs_alt = float32_t
    obs_x = _vector31_t
    obs_state = uint32_t
    est_vb = _vector21_t
    est_state = uint32_t


@index.register(11)
class VisionRaw(OptionHeader):

    'Corresponds to C struct ``navdata_vision_raw_t``.'

    _attrname = 'vision_raw'

    vision_tx_raw = float32_t
    vision_ty_raw = float32_t
    vision_tz_raw = float32_t


@index.register(13)
class Vision(OptionHeader):

    'Corresponds to C struct ``navdata_vision_t``.'

    _attrname = 'vision'

    vision_state = uint32_t
    vision_misc = int32_t
    vision_phi_trim = float32_t
    vision_phi_ref_prop = float32_t
    vision_theta_trim = float32_t
    vision_theta_ref_prop = float32_t

    new_raw_picture = int32_t
    theta_capture = float32_t
    phi_capture = float32_t
    psi_capture = float32_t
    altitude_capture = int32_t
    time_capture = uint32_t  #: time in TSECDEC format (see config.h)
    body_v = _velocities_t

    delta_phi = float32_t
    delta_theta = float32_t
    delta_psi = float32_t

    gold_defined = uint32_t
    gold_reset = uint32_t
    gold_x = float32_t
    gold_y = float32_t


@index.register(14)
class VisionPerf(OptionHeader):

    'Corresponds to C struct ``navdata_vision_perf_t``.'

    _attrname = 'vision_perf'

    time_szo = float32_t
    time_corners = float32_t
    time_compute = float32_t
    time_tracking = float32_t
    time_trans = float32_t
    time_update = float32_t
    time_custom = float32_t * NAVDATA_MAX_CUSTOM_TIME_SAVE


@index.register(15)
class TrackersSend(OptionHeader):

    'Corresponds to C struct ``navdata_trackers_send_t``.'

    _attrname = 'trackers_send'

    locked = int32_t * (DEFAULT_NB_TRACKERS_WIDTH * DEFAULT_NB_TRACKERS_HEIGHT)
    point = _screen_point_t * (
        DEFAULT_NB_TRACKERS_WIDTH * DEFAULT_NB_TRACKERS_HEIGHT
    )


@index.register(16)
class VisionDetect(OptionHeader):

    'Corresponds to C struct ``navdata_vision_detect_t``.'

    # Change the function 'navdata_server_reset_vision_detect()'
    # if this structure is modified

    _attrname = 'vision_detect'

    nb_detected = uint32_t
    type = uint32_t * NB_NAVDATA_DETECTION_RESULTS
    xc = uint32_t * NB_NAVDATA_DETECTION_RESULTS
    yc = uint32_t * NB_NAVDATA_DETECTION_RESULTS
    width = uint32_t * NB_NAVDATA_DETECTION_RESULTS
    height = uint32_t * NB_NAVDATA_DETECTION_RESULTS
    dist = uint32_t * NB_NAVDATA_DETECTION_RESULTS
    orientation_angle = float32_t * NB_NAVDATA_DETECTION_RESULTS
    rotation = _matrix33_t * NB_NAVDATA_DETECTION_RESULTS
    translation = _vector31_t * NB_NAVDATA_DETECTION_RESULTS
    camera_source = uint32_t * NB_NAVDATA_DETECTION_RESULTS


@index.register(12)
class VisionOf(OptionHeader):

    'Corresponds to C struct ``navdata_vision_of_t``.'

    _attrname = 'vision_of'

    of_dx = float32_t * 5
    of_dy = float32_t * 5


@index.register(17)
class Watchdog(OptionHeader):

    'Corresponds to C struct ``navdata_watchdog_t``.'

    _attrname = 'watchdog'

    # +4 bytes
    watchdog = int32_t


@index.register(18)
class AdcDataFrame(OptionHeader):

    'Corresponds to C struct ``navdata_adc_data_frame_t``.'

    _attrname = 'adc_data_frame'

    version = uint32_t
    data_frame = uint8_t * 32


@index.register(19)
class VideoStream(OptionHeader):

    'Corresponds to C struct ``navdata_video_stream_t``.'

    _attrname = 'video_stream'

    quant = uint8_t  #: quantizer reference used to encode frame [1:31]
    frame_size = uint32_t  #: frame size (bytes)
    frame_number = uint32_t  #: frame index
    atcmd_ref_seq = uint32_t  #: atmcd ref sequence number

    #: mean time between two consecutive atcmd_ref (ms)
    atcmd_mean_ref_gap = uint32_t

    atcmd_var_ref_gap = float32_t
    atcmd_ref_quality = uint32_t  #: estimator of atcmd link quality

    # drone2

    #: measured out throughput from the video tcp socket
    out_bitrate = uint32_t

    #: last frame size generated by the video encoder
    desired_bitrate = uint32_t

    # misc temporary data
    data1 = int32_t
    data2 = int32_t
    data3 = int32_t
    data4 = int32_t
    data5 = int32_t

    # queue usage
    tcp_queue_level = uint32_t
    fifo_queue_level = uint32_t


@index.register(25)
class HdvideoStream(OptionHeader):

    'Corresponds to C struct ``navdata_hdvideo_stream_t``.'

    _attrname = 'hdvideo_stream'

    hdvideo_state = uint32_t
    storage_fifo_nb_packets = uint32_t
    storage_fifo_size = uint32_t
    usbkey_size = uint32_t  #: USB key in kbytes - 0 if no key present

    #: USB key free space in kbytes - 0 if no key present
    usbkey_freespace = uint32_t

    #: 'frame_number' PaVE field of the frame starting to be encoded for the
    #: HD stream
    frame_number = uint32_t

    usbkey_remaining_time = uint32_t  #: time in seconds


@index.register(20)
class Games(OptionHeader):

    'Corresponds to C struct ``navdata_games_t``.'

    _attrname = 'games'

    double_tap_counter = uint32_t
    finish_line_counter = uint32_t


@index.register(26)
class Wifi(OptionHeader):

    'Corresponds to C struct ``navdata_wifi_t``.'

    _attrname = 'wifi'

    link_quality = uint32_t


@index.register(0xFFFF)
class Cks(OptionHeader):

    'Corresponds to C struct ``navdata_cks_t``.'

    _attrname = 'cks'

    value = uint32_t  #: Value of the checksum
