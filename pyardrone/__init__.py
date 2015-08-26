'''
High level ARDrone API
'''

import collections
import itertools
import logging
import queue
import socket
import threading
import time

from pyardrone.config import Config
from pyardrone import at
from pyardrone.utils import noop


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
        interval=0.03
    ):
        self.addr = addr
        self.at_port = at_port
        self.navdata_port = navdata_port
        self.video_port = video_port
        self.control_port = control_port
        self.interval = interval

        self.init_sockets()

        # sequence number required by ATCommands
        # DevGuide: send 1 as the sequence number of the first sent command
        self.seq_num = 0

        self.seq_lock = threading.Lock()
        self.queued_commands = queue.Queue()
        self._at_thread = threading.Thread(target=self._at_job)
        self._at_stop = threading.Event()

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

    def register(self, command, *, event=None):
        self.queued_commands.put_nowait(QueuedCommand(command, event))
        return event

    def send(self, command):
        self.register(command, event=threading.Event()).wait()

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

    def _at_job(self):
        while not self._at_stop.isSet():
            try:
                qcmd = self.queued_commands.get_nowait()
                call_task_done = True
            except queue.Empty:
                qcmd = QueuedCommand(at.COMWDG(), event=None)
                call_task_done = False
            self.send_nowait(qcmd.command)
            if qcmd.event is not None:
                qcmd.event.set()
            if call_task_done:
                self.queued_commands.task_done()
            time.sleep(self.interval)
