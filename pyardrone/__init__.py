import itertools
import socket
import threading

from pyardrone import at
from pyardrone.config import Config
from pyardrone.navdata import NavData
from pyardrone.navdata.states import DroneState
from pyardrone.utils import noop, logging


__version__ = '0.3.1dev1'

__all__ = ('ARDrone',)


logger = logging.getLogger(__name__)


class ARDroneBase:

    def __init__(
        self,
        *,
        address='192.168.1.1',
        at_port=5556,
        navdata_port=5554,
        video_port=5555,  # 5553?
        control_port=5559,
        watchdog_interval=0.5,
        bind=True,
        connect=True
    ):
        self.address = address
        self.at_port = at_port
        self.navdata_port = navdata_port
        self.video_port = video_port
        self.control_port = control_port
        self.watchdog_interval = watchdog_interval
        self._watchdog_thread = threading.Thread(target=self._watchdog_job)
        self.bind = bind

        self.config = Config(self)

        self.connected = False
        self.closed = threading.Event()

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

    def send(self, command):
        '''
        :param pyardrone.at.base.ATCommand command: command to send

        Sends the command to the drone,
        with an internal increasing sequence number.
        this method is thread-safe.
        '''
        with self.sequence_number_mutex:
            self.sequence_number += 1
            packed = command._pack(self.sequence_number)
            self.send_bytes(packed)

    def navdata_received(self, data):
        '''
        Called when navdata received.

        :param bytes data: navdata received.
        '''
        self.navdata = NavData(data)


class IOMixin:

    def connect(self):
        '''
        Connect to the drone.

        :raises RuntimeError: if the drone is connected or closed already.
        '''
        if self.closed.is_set():
            raise RuntimeError("The drone's connection is closed already")
        if self.connected:
            raise RuntimeError('The drone is connected already')

        self.connected = True

        # sequence number required by ATCommands
        # DevGuide: send 1 as the sequence number of the first sent command
        self.sequence_number = 0
        self.sequence_number_mutex = threading.Lock()

        self._init_sockets()
        self._init_threads()

    def close(self):
        '''
        Exit all threads and disconnect the drone.

        This method has no effect if the drone is closed already or not
        connected yet.
        '''
        if self.closed.is_set() or not self.connected:
            return
        self.closed.set()
        self._close_threads()
        self._close_sockets()

    def send_bytes(self, bytez):
        self.at_sock.sendto(bytez, (self.address, self.at_port))
        logger.debug('sent: {!r}', bytez)

    def get_raw_config(self):
        '''
        Requests and returns the raw config file from the *control_port*.
        '''
        self.send(at.CTRL(at.CTRL.Modes.CFG_GET_CONTROL_MODE))
        return b''.join(
            itertools.dropwhile(noop, self.control_sock.recv(4096))
        ).encode()

    def _init_sockets(self):

        self.at_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.navdata_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.bind:
            self.at_sock.bind(('', self.at_port))
            self.navdata_sock.bind(('', self.navdata_port))
            self.control_sock.bind(('', self.control_port))

        self.navdata_sock.setblocking(False)

    def _close_sockets(self):
        self.at_sock.close()
        self.navdata_sock.close()
        self.control_sock.close()

    def _watchdog_job(self):
        while not self.closed.is_set():
            self.send(at.COMWDG())
            self.closed.wait(timeout=self.watchdog_interval)

    def _init_threads(self):
        self._watchdog_thread.start()

    def _close_threads(self):
        self._watchdog_thread.join()


class HelperMixin:

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


class ARDrone(HelperMixin, IOMixin, ARDroneBase):
    pass
