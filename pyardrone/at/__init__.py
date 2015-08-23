'''
AT Commands
'''


from enum import IntEnum
from pyardrone.at.base import ATCommand
from pyardrone.at.arguments import Int32Arg, FloatArg, StringArg
from pyardrone.utils import bits


class REF(ATCommand):

    '''
    Controls the basic behaviour of the drone (take-off/landing, emergency
    stop/reset)
    '''

    input = Int32Arg(
        'an integer value, '
        'representing a 32 bit-wide bit-field controlling the drone')

    class Flags(IntEnum):
        default = bits(18, 20, 22, 24, 28)  # Always on
        start = bits(9)  # Takeoff / Land
        select = bits(8)  # Switch of emergency mode


class PCMD(ATCommand):

    '''
    Send progressive commands - makes the drone move (translate/rotate).
    '''

    flag = Int32Arg(
        'flag enabling the use of progressive commands and/or the Combined'
        'Yaw mode (bitfield)')
    roll = FloatArg('drone left-right tilt, [-1...1]')
    pitch = FloatArg('drone front-back tilt, [-1...1]')
    gaz = FloatArg('drone vertical speed, [-1...1]')
    yaw = FloatArg('drone angular speed, [-1...1]')

    class Flags(IntEnum):
        absolute_control = bits(2)
        combined_yaw = bits(1)


class PCMD_MAG(ATCommand):

    '''
    Send progressive commands - makes the drone move (translate/rotate).
    '''

    flag = Int32Arg(
        'flag enabling the use of progressive commands and/or the Combined'
        'Yaw mode (bitfield)')
    roll = FloatArg('drone left-right tilt, [-1...1]')
    pitch = FloatArg('drone front-back tilt, [-1...1]')
    gaz = FloatArg('drone vertical speed, [-1...1]')
    yaw = FloatArg('drone angular speed, [-1...1]')
    psi = FloatArg('magneto psi, [-1...1]')
    psi_accuracy = FloatArg('magneto psi accuracy, [-1...1]')


class FTRIM(ATCommand):

    '''
    Flat trims - Tells the drone it is lying horizontally
    '''


class CONFIG(ATCommand):

    '''
    Sets an configurable option on the drone
    '''

    key = StringArg('the name of the option to set')
    value = StringArg('the option value')


class CONFIG_IDS(ATCommand):

    '''
    Identifiers for the next AT*CONFIG command
    '''

    session = StringArg()
    user = StringArg()
    application_ids = StringArg()


class COMWDG(ATCommand):

    '''
    reset communication watchdog
    '''


class CALIB(ATCommand):

    '''
    Magnetometer calibration - Tells the drone to calibrate its magnetometer
    '''

    device_number = Int32Arg(
        'Identifier of the device to calibrate - '
        'Choose this identifier from ardrone_calibration_device_t.')
