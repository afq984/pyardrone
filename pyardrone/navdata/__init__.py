from ctypes import sizeof
from types import SimpleNamespace
import socket
import threading

from pyardrone.navdata.options import Metadata, OptionHeader, index
from pyardrone.abc import BaseClient


header = 0x55667788


class NavDataError(Exception):
    pass


class ChecksumError(NavDataError):
    pass


class IncorrectChecksum(ChecksumError):
    pass


class ChecksumNotPresent(ChecksumError):
    pass


class InvalidSize(NavDataError):
    pass


def compute_checksum(buffer):
    return sum(buffer) & 0xffffffff


class NavData(SimpleNamespace):

    '''
    Container of navdata options.

    NavData of :py:class:`~pyardrone.ARDrone` is available after
    :py:attr:`~pyardrone.ARDrone.navdata_ready`.is_set() is ``True``.

    You can call :py:attr:`~pyardrone.ARDrone.navdata_ready`.wait() to wait for
    it.

    To fetch an option:

        >>> drone.navdata.demo
        Demo(altitude=0, ctrl_state=131072, detection_camera_rot=...)
    '''

    def __init__(self, buffer):
        super().__init__()

        self.checksum = compute_checksum(memoryview(buffer)[:-8])

        self.add_option(Metadata, buffer, 0)

        offset = sizeof(Metadata)
        while offset < len(buffer):
            header = OptionHeader.from_buffer_copy(buffer, offset)
            if header.size:
                option_class = index[header.tag]
                if header.size != sizeof(option_class):
                    raise InvalidSize(
                        'Option: {!r}, calculated: {}, reported: {}'.format(
                            option_class, sizeof(option_class), header.size
                        )
                    )
                self.add_option(option_class, buffer, offset)
                offset += sizeof(option_class)

        if not hasattr(self, 'cks'):
            raise ChecksumNotPresent
        if self.checksum != self.cks.value:
            raise IncorrectChecksum('calculated: {}, reported: {}'.format(
                self.checksum,
                self.cks.value
            ))

    def add_option(self, option_class, buffer, offset):
        option = option_class.from_buffer_copy(buffer, offset)
        setattr(self, option_class._attrname, option)


class NavDataClient(BaseClient):

    def __init__(self, host, port, timeout=0.01):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.navdata_ready = threading.Event()

    def _listener_job(self):
        while not self.closed:
            try:
                data, addr = self.sock.recvfrom(4096)
            except socket.timeout:
                pass
            else:
                if addr == (self.host, self.port):
                    self.navdata_received(data)
                    self.navdata_ready.set()

    def _connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout)

        self.sock.sendto(
            b'\x01\x00\x00\x00',
            (self.host, self.port)
        )
        self._thread = threading.Thread(target=self._listener_job)
        self._thread.start()

    def _close(self):
        self._thread.join()
        self.sock.close()

    def navdata_received(self, data):
        self.navdata = NavData(data)
