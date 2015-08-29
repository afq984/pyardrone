from pyardrone.utils import bits
from pyardrone.at.base import ATCommand
from pyardrone.at import parameters


__all__ = (
    'REF', 'PCMD', 'PCMD_MAG', 'FTRIM', 'CONFIG',
    'CONFIG_IDS', 'COMWDG', 'CALIB', 'CTRL'
)


class REF(ATCommand):

    '''
    Controls the basic behaviour of the drone (take-off/landing, emergency
    stop/reset)
    '''

    input = parameters.Int32(
        'an integer value, '
        'representing a 32 bit-wide bit-field controlling the drone')

    input._set_flags(
        default=bits(18, 20, 22, 24, 28),  # Always on
        start=bits(9),  # Takeoff / Land
        select=bits(8),  # Switch of emergency mode
    )


class PCMD(ATCommand):

    '''
    Send progressive commands - makes the drone move (translate/rotate).
    '''

    flag = parameters.Int32(
        'flag enabling the use of progressive commands and/or the Combined'
        'Yaw mode (bitfield)')
    roll = parameters.Float('drone left-right tilt, [-1...1]', default=0)
    pitch = parameters.Float('drone front-back tilt, [-1...1]', default=0)
    gaz = parameters.Float('drone vertical speed, [-1...1]', default=0)
    yaw = parameters.Float('drone angular speed, [-1...1]', default=0)

    flag._set_flags(
        absolute_control=bits(2),
        combined_yaw=bits(1),
        progressive=bits(0),
    )


class PCMD_MAG(ATCommand):

    '''
    Send progressive commands - makes the drone move (translate/rotate).
    '''

    flag = parameters.Int32(
        'flag enabling the use of progressive commands and/or the Combined'
        'Yaw mode (bitfield)')
    roll = parameters.Float('drone left-right tilt, [-1...1]')
    pitch = parameters.Float('drone front-back tilt, [-1...1]')
    gaz = parameters.Float('drone vertical speed, [-1...1]')
    yaw = parameters.Float('drone angular speed, [-1...1]')
    psi = parameters.Float('magneto psi, [-1...1]')
    psi_accuracy = parameters.Float('magneto psi accuracy, [-1...1]')


class FTRIM(ATCommand):

    '''
    Flat trims - Tells the drone it is lying horizontally
    '''


class CONFIG(ATCommand):

    '''
    Sets an configurable option on the drone
    '''

    key = parameters.String('the name of the option to set')
    value = parameters.String('the option value')


class CONFIG_IDS(ATCommand):

    '''
    Identifiers for the next AT*CONFIG command
    '''

    session = parameters.String()
    user = parameters.String()
    application_ids = parameters.String()


class COMWDG(ATCommand):

    '''
    reset communication watchdog
    '''


class CALIB(ATCommand):

    '''
    Magnetometer calibration - Tells the drone to calibrate its magnetometer
    '''

    device_number = parameters.Int32(
        'Identifier of the device to calibrate - '
        'Choose this identifier from ardrone_calibration_device_t.')


class CTRL(ATCommand):

    '''
    Not documented in developer guide, change control mode
    '''

    mode = parameters.Int32()

    mode._set_flags(
        NO_CONTROL_MODE=0,  # Doing nothing
        ARDRONE_UPDATE_CONTROL_MODE=1,  # Not used
        PIC_UPDATE_CONTROL_MODE=2,  # Not used
        LOGS_GET_CONTROL_MODE=3,  # Not used

        CFG_GET_CONTROL_MODE=4,
        # Send active configuration file to a client through the
        # 'control' socket UDP 5559 */

        ACK_CONTROL_MODE=5,  # Reset command mask in navdata

        CUSTOM_CFG_GET_CONTROL_MODE=6,
        # Requests the list of custom configuration IDs
    )

    zero = parameters.Int32(default=0)
