'''
High level ARDrone API
'''

import socket
import logging

from pyardrone.config import Config


logger = logging.getLogger(__name__)


class ARDrone:

    def __init__(
        self,
        addr='192.168.1.1',
        at_port=5556,
        navdata_port=5554,
        video_port=5559
    ):
        self.addr = addr
        self.at_port = at_port
        self.navdata_port = navdata_port
        self.video_port = video_port

        # sequence number required by ATCommands
        # DevGuide: send 1 as the sequence number of the first sent command
        self.seq_num = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.config = Config(self)

    def send(self, command):
        self.seq_num += 1
        packed = command.pack(self.seq_num)
        bytes_sent = self.sock.sendto(packed, (self.addr, self.at_port))
        logger.debug(
            'sent %d bytes to "%s:%d", %r',
            bytes_sent,
            self.addr,
            self.at_port,
            packed
        )

    def get_raw_config(self):
        with open('/home/afg/Downloads/conf_file_example.txt') as f:
            return f.read()
