'''
High level ARDrone API
'''

import collections
import itertools
import logging
import socket
import threading

from pyardrone.config import Config
from pyardrone import at
from pyardrone.utils import noop
from pyardrone.utils.object_executor import ObjectExecutor


logger = logging.getLogger(__name__)


QueuedCommand = collections.namedtuple('QueuedCommand', 'command event')


class ARDrone:

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

    def connect(self):
        if self.closed:
            raise RuntimeError("The drone's connection is closed already")
        if self.connected:
            raise RuntimeError('The drone is connected already')
        self.connected = True
        self._init_sockets()
        self._at_executor.start()

    def close(self):
        if self.closed or not self.connected:
            return
        self.closed = True
        self._at_executor.stop(True)
        self._close_sockets()

    def register(self, command, with_event=True):
        return self._at_executor.put(command, with_event)

    def send(self, command):
        self._at_executor.put(command, True).wait()

    def send_nowait(self, command):
        with self.seq_lock:
            self.seq_num += 1
            packed = command.pack(self.seq_num)
            bytes_sent = self.at_sock.sendto(packed, (self.addr, self.at_port))
            logger.debug(
                'sent %d bytes to "%s:%d", %r',
                bytes_sent,
                self.addr,
                self.at_port,
                packed
            )

    def get_raw_config(self):
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
