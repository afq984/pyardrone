class StateMask:

    def __init__(self, bit, doc=None):
        self.bit = bit
        if doc is not None:
            self.__doc__ = 'bit {}.  {}'.format(bit, doc)

    def __get__(self, obj, type_=None):
        if obj is None:
            return self
        else:
            return bool(obj._data >> self.bit & 1)

    def __set__(self, obj, value):
        raise AttributeError('{!r} of {!r} is not settable'.format(self, obj))


class DroneState:

    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return '{self.__class__.__name__}(0b{self._data:b})'.format(self=self)

    fly_mask = StateMask(
        0,
        'FLY MASK : (0) ardrone is landed, (1) ardrone is flying'
    )

    video_mask = StateMask(
        1,
        'VIDEO MASK : (0) video disable, (1) video enable'
    )

    vision_mask = StateMask(
        2,
        'VISION MASK : (0) vision disable, (1) vision enable'
    )

    control_mask = StateMask(
        3,
        'CONTROL ALGO : (0) euler angles control, (1) angular speed control'
    )

    altitude_mask = StateMask(
        4,
        'ALTITUDE CONTROL ALGO : '
        '(0) altitude control inactive (1) altitude control active'
    )

    user_feedback_start = StateMask(
        5,
        'USER feedback : Start button state'
    )

    command_mask = StateMask(
        6,
        'Control command ACK : (0) None, (1) one received'
    )

    camera_mask = StateMask(
        7,
        'CAMERA MASK : (0) camera not ready, (1) Camera ready'
    )

    travelling_mask = StateMask(
        8,
        'Travelling mask : (0) disable, (1) enable'
    )

    usb_mask = StateMask(
        9,
        'USB key : (0) usb key not ready, (1) usb key ready'
    )

    navdata_demo_mask = StateMask(
        10,
        'Navdata demo : (0) All navdata, (1) only navdata demo'
    )

    navdata_bootstrap = StateMask(
        11,
        'Navdata bootstrap : '
        '(0) options sent in all or demo mode, (1) no navdata options sent'
    )

    motors_mask = StateMask(
        12,
        'Motors status : (0) Ok, (1) Motors problem'
    )

    com_lost_mask = StateMask(
        13,
        'Communication Lost : (1) com problem, (0) Com is ok'
    )

    software_fault = StateMask(
        14,
        'Software fault detected - user should land as quick as possible (1)'
    )

    vbat_low = StateMask(
        15,
        'VBat low : (1) too low, (0) Ok'
    )

    user_el = StateMask(
        16,
        'User Emergency Landing : (1) User EL is ON, (0) User EL is OFF'
    )

    timer_elapsed = StateMask(
        17,
        'Timer elapsed : (1) elapsed, (0) not elapsed'
    )

    magneto_needs_calib = StateMask(
        18,
        'Magnetometer calibration state : '
        '(0) Ok, no calibration needed, (1) not ok, calibration needed'
    )

    angles_out_of_range = StateMask(
        19,
        'Angles : (0) Ok, (1) out of range'
    )

    wind_mask = StateMask(
        20,
        'WIND MASK: (0) ok, (1) Too much wind'
    )

    ultrasound_mask = StateMask(
        21,
        'Ultrasonic sensor : (0) Ok, (1) deaf'
    )

    cutout_mask = StateMask(
        22,
        'Cutout system detection : (0) Not detected, (1) detected'
    )

    pic_version_mask = StateMask(
        23,
        'PIC Version number OK : '
        '(0) a bad version number, (1) version number is OK'
    )

    atcodec_thread_on = StateMask(
        24,
        'ATCodec thread ON : (0) thread OFF (1) thread ON'
    )

    navdata_thread_on = StateMask(
        25,
        'Navdata thread ON : (0) thread OFF (1) thread ON'
    )

    video_thread_on = StateMask(
        26,
        'Video thread ON : (0) thread OFF (1) thread ON'
    )

    acq_thread_on = StateMask(
        27,
        'Acquisition thread ON : (0) thread OFF (1) thread ON'
    )

    ctrl_watchdog_mask = StateMask(
        28,
        'CTRL watchdog : '
        '(1) delay in control execution (> 5ms), (0) control is well scheduled'
    )

    adc_watchdog_mask = StateMask(
        29,
        'ADC Watchdog : (1) delay in uart2 dsr (> 5ms), (0) uart2 is good'
    )

    com_watchdog_mask = StateMask(
        30,
        'Communication Watchdog : (1) com problem, (0) Com is ok'
    )

    emergency_mask = StateMask(
        31,
        'Emergency landing : (0) no emergency, (1) emergency'
    )
