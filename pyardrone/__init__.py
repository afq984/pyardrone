'''
High level ARDrone API
'''

import socket
import logging
import itertools

from pyardrone.config import Config
from pyardrone import at
from pyardrone.utils import noop


logger = logging.getLogger(__name__)


class ARDrone:

    def __init__(
        self,
        *,
        addr='192.168.1.1',
        at_port=5556,
        navdata_port=5554,
        video_port=5555,  # 5553?
        control_port=5559,
        interval=0.03
    ):
        self.addr = addr
        self.at_port = at_port
        self.navdata_port = navdata_port
        self.video_port = video_port
        self.control_port = control_port
        self.interval = interval

        # sequence number required by ATCommands
        # DevGuide: send 1 as the sequence number of the first sent command
        self.seq_num = 0

        self.init_sockets()

        self.config = Config(self)

    def init_sockets(self):

        self.at_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.at_sock.bind(('', self.at_port))

        self.navdata_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.navdata_sock.bind(('', self.navdata_port))

        self.control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_sock.bind(('', self.control_port))

    def close_sockets(self):
        self.at_sock.close()
        self.navdata_sock.close()
        self.control_sock.close()

    def send(self, command):
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
