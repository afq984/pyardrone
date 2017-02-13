from pyardrone.utils import bits, logging
from pyardrone.at.base import ATCommand
from pyardrone.at import parameters
from pyardrone.abc import BaseClient

import threading
import socket


logger = logging.getLogger(__name__)


__all__ = (
    'REF', 'PCMD', 'PCMD_MAG', 'FTRIM', 'CONFIG',
    'CONFIG_IDS', 'COMWDG', 'CALIB', 'CTRL'
)


class REF_0_5(ATCommand):
    '''
    at.REF interface of version 0.5
    '''

    input = parameters.Int32(
        'an integer value, '
        'representing a 32 bit-wide bit-field controlling the drone')

    input._set_flags(
        default=bits(18, 20, 22, 24, 28),  # Always on
        start=bits(9),  # Takeoff / Land
        select=bits(8),  # Switch of emergency mode
    )


class REF(REF_0_5):
    '''
    Controls the basic behaviour of the drone (take-off/landing, emergency
    stop/reset)
    '''

    def __new__(cls, input=0, *, use_default_bits=True):
        if int.bit_length(input) > 32:
            raise ValueError(
                'value input {} should be less than 4 bytes'.format(input))
        if use_default_bits:
            input |= cls.input.default
        return super().__new__(cls, input)


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


class ATClient(BaseClient):

    connected = False

    def __init__(
        self,
        host='192.168.1.1',
        port=5556,
        watchdog_interval=0.5,
        log_comwdg=False
    ):
        self.host = host
        self.port = port
        self.watchdog_interval = watchdog_interval
        self.log_comwdg = log_comwdg
        self._closed = threading.Event()

    @property
    def closed(self):
        return self._closed.is_set()

    @closed.setter
    def closed(self, boolean):
        if boolean:
            self._closed.set()
        else:
            self._closed.clear()

    def _connect(self):
        self.sequence_number = 0
        self.sequence_number_mutex = threading.Lock()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._thread = threading.Thread(target=self._watchdog_job)
        self._thread.start()

    def _close(self):
        self._thread.join()
        self.sock.close()

    def send_bytes(self, bytez, *, log=True):
        self.sock.sendto(bytez, (self.host, self.port))
        if log:
            logger.debug('sent: {!r}', bytez)

    def send(self, command, *, log=True):
        '''
        :param pyardrone.at.base.ATCommand command: command to send

        Sends the command to the drone,
        with an internal increasing sequence number.
        this method is thread-safe.
        '''
        with self.sequence_number_mutex:
            self.sequence_number += 1
            packed = command._pack(self.sequence_number)
            self.send_bytes(packed, log=log)

    def _watchdog_job(self):
        while not self.closed:
            self.send(COMWDG(), log=self.log_comwdg)
            self._closed.wait(timeout=self.watchdog_interval)
