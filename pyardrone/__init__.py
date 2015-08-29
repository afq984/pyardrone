import collections
import itertools
import logging
import socket
import threading

from pyardrone.config import Config
from pyardrone import at
from pyardrone.utils import noop
from pyardrone.utils.object_executor import ObjectExecutor


__version__ = '0.2.0dev1'

__all__ = ('ARDrone',)


logger = logging.getLogger(__name__)


QueuedCommand = collections.namedtuple('QueuedCommand', 'command event')


class ARDrone:

    '''
    The class representing a Parrot AR.Drone

    :param address: address of the drone
    :param at_port: AT command port
    :param navdata_port: NavData port
    :param video_port: Video port
    :param control_port: Control port
    :param interval: delay between subsequent commands in seconds
    :param connect: connect to the drone at init

    .. attribute:: config

        The config object of the drone, see :ref:`configuration`.
    '''

    def __init__(
        self,
        *,
        addr='192.168.1.1',
        at_port=5556,
        navdata_port=5554,
        video_port=5555,  # 5553?
        control_port=5559,
        interval=0.03,
        connect=True
    ):
        self.addr = addr
        self.at_port = at_port
        self.navdata_port = navdata_port
        self.video_port = video_port
        self.control_port = control_port

        # sequence number required by ATCommands
        # DevGuide: send 1 as the sequence number of the first sent command
        self.seq_num = 0
        self.seq_lock = threading.Lock()

        self._at_executor = ObjectExecutor(
            self.send_nowait,
            interval,
            at.COMWDG()
        )

        self.config = Config(self)

        self.connected = False
        self.closed = False

        if connect:
            self.connect()

    @property
    def interval(self):
        return self._at_executor.interval

    @interval.setter
    def interval(self, value):
        self._at_executor.interval = value

    @property
    def state(self):
        '''
        The latest state from *NavData*.

            >>> drone.state.fly_mask
            True  # drone is flying
            >>> drone.state.video
            True  # video is enabled

        See :py:class:`~pyardrone.navdata.states.DroneState`
        for the full list of states.
        '''
        raise NotImplementedError

    def takeoff(wait=False, discard=True):
        '''
        Drone takeoff.

        :param wait: if True, wait for queued commands to complete before\
        taking off.
        :param discard: if True, discard all queued commands after taking off.
        '''
        raise NotImplementedError

    def land(wait=False, discard=True):
        '''
        Drone land.

        Parameters same as :py:meth:`~pyardrone.ARDrone.takeoff`
        '''
        raise NotImplementedError

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
        self._at_executor.start()

    def close(self):
        '''
        Exit all threads and disconnect the drone.

        This method has no effect if the drone is closed already or not
        connected yet.
        '''
        if self.closed or not self.connected:
            return
        self.closed = True
        self._at_executor.stop(True)
        self._close_sockets()

    def register(self, command, with_event=True):
        '''
        Puts the *ATCommand* to the queue, does not block.

        :param ATCommand command: Command to register.
        :param bool with_event: If ``True``, returns an \
        :py:class:`threading.Event` object, which can be used to \
        indicate whether the job is done.
        '''
        return self._at_executor.put(command, with_event)

    def send(self, command):
        '''
        Puts the command to the queue, blocks until it is sent to the drone.
        '''
        self._at_executor.put(command, True).wait()

    def send_nowait(self, command):
        '''
        Sends the command to the drone immediately.
        '''
        with self.seq_lock:
            self.seq_num += 1
            packed = command._pack(self.seq_num)
            bytes_sent = self.at_sock.sendto(packed, (self.addr, self.at_port))
            logger.debug(
                'sent %d bytes to "%s:%d", %r',
                bytes_sent,
                self.addr,
                self.at_port,
                packed
            )

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
        self.at_sock.bind(('', self.at_port))

        self.navdata_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.navdata_sock.bind(('', self.navdata_port))

        self.control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_sock.bind(('', self.control_port))

    def _close_sockets(self):
        self.at_sock.close()
        self.navdata_sock.close()
        self.control_sock.close()
