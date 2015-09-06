import itertools
import logging
import socket
import threading

from pyardrone import at
from pyardrone.config import Config
from pyardrone.navdata import NavData
from pyardrone.navdata.states import DroneState
from pyardrone.utils import noop


__version__ = '0.3.0dev1'

__all__ = ('ARDrone',)


logger = logging.getLogger(__name__)


class ARDrone:

    '''
    The class representing a Parrot AR.Drone

    :param address:         address of the drone
    :param at_port:         AT command port
    :param navdata_port:    NavData port
    :param video_port:      Video port
    :param control_port:    Control port
    :param watchdog_interval:  seconds between each
                               :py:class:`~pyardrone.at.COMWDG`
                               sent in background
    :param bind:            whether to :py:meth:`~socket.socket.bind`
                            the sockets; this option exists for testing
    :param connect:         connect to the drone at init

    .. attribute:: config

        The config object of the drone, see :ref:`configuration`.
    '''

    def __init__(
        self,
        *,
        address='192.168.1.1',
        at_port=5556,
        navdata_port=5554,
        video_port=5555,  # 5553?
        control_port=5559,
        watchdog_interval=0.03,
        bind=True,
        connect=True
    ):
        self.address = address
        self.at_port = at_port
        self.navdata_port = navdata_port
        self.video_port = video_port
        self.control_port = control_port
        self.watchdog_interval = watchdog_interval
        self.bind = bind

        # sequence number required by ATCommands
        # DevGuide: send 1 as the sequence number of the first sent command
        self.sequence_number = 0
        self.sequence_number_mutex = threading.Lock()

        self.config = Config(self)

        self.connected = False
        self.closed = False

        if connect:
            self.connect()

    @property
    def state(self):
        '''
        The latest state from :py:class:`~pyardrone.navdata.NavData`.

            >>> drone.state.fly_mask
            True  # drone is flying
            >>> drone.state.video
            True  # video is enabled

        See :py:class:`~pyardrone.navdata.states.DroneState`
        for the full list of states.
        '''
        return DroneState(self.navdata.metadata.state)

    def takeoff(self):
        '''
        Sends the takeoff command.
        '''
        self.send(at.REF(at.REF.input.default | at.REF.input.start))

    def land(self):
        '''
        Sends the land command.
        '''
        self.send(at.REF(at.REF.input.default))

    def connect(self):
        '''
        Connect to the drone.

        :raises RuntimeError: if the drone is connected or closed already.
        '''
        if self.closed:
            raise RuntimeError("The drone's connection is closed already")
        if self.connected:
            raise RuntimeError('The drone is connected already')
        self.connected = True
        self._init_sockets()

    def close(self):
        '''
        Exit all threads and disconnect the drone.

        This method has no effect if the drone is closed already or not
        connected yet.
        '''
        if self.closed or not self.connected:
            return
        self.closed = True
        self._close_sockets()

    def send(self, command):
        '''
        :param pyardrone.at.ATCommand command: command to send

        Sends the command to the drone,
        with an internal increasing sequence number.
        this method is thread-safe.
        '''
        with self.sequence_number_mutex:
            self.sequence_number += 1
            self.at_sock.send(
                command._pack(self.sequence_number)
            )

    def get_raw_config(self):
        '''
        Requests and returns the raw config file from the *control_port*.
        '''
        self.send(at.CTRL(at.CTRL.Modes.CFG_GET_CONTROL_MODE))
        return b''.join(
            itertools.dropwhile(noop, self.control_sock.recv(4096))
        ).encode()

    def get_new_and_latest_navdata(self):
        navb = None
        while True:
            try:
                navb = self.navdata_sock.recv(1024)
            except BlockingIOError:
                return navb

    def update_navdata(self):
        navb = self.get_new_and_latest_navdata()
        if navb is not None:
            self.navdata = NavData(navb)

    def _init_sockets(self):

        self.at_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.navdata_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.bind:
            self.at_sock.bind(('', self.at_port))
            self.navdata_sock.bind(('', self.navdata_port))
            self.control_sock.bind(('', self.control_port))

        self.at_sock.connect((self.address, self.at_port))
        self.navdata_sock.connect((self.address, self.navdata_port))
        # self.control_sock.connect((self.address, self.navdata_port))

        self.navdata_sock.setblocking(False)

    def _close_sockets(self):
        self.at_sock.close()
        self.navdata_sock.close()
        self.control_sock.close()
