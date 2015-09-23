from ctypes import sizeof
from types import SimpleNamespace

from pyardrone.navdata.options import Metadata, OptionHeader, index


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
    Container of navdata :py:class:`~pyardrone.navdata.types.Option`\ s.

    To fetch an option:

        >>> nav.demo
        Demo(altitude=0, ctrl_state=131072, detection_camera_rot=...)
    '''

    def __init__(self, buffer):
        super().__init__()

        self.checksum = compute_checksum(memoryview(buffer)[:-8])

        self.add_option(Metadata, buffer, 0)

        option_header_size = sizeof(OptionHeader)
        offset = sizeof(Metadata)
        while offset < len(buffer):
            header = OptionHeader.from_buffer_copy(buffer, offset)
            offset += option_header_size
            if header.size:
                option_class = index[header.tag]
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
