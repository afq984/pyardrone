import struct
import io
import reprlib


header = 0x55667788


class NavData:

    def __init__(self, bytes_):
        flo = io.BytesIO(bytes_)
        (
            self.header,
            self.drone_state,
            self.sequence_number,
            self.version_flag
        ) = struct.unpack('<IIII', flo.read(16))
        self.options = []
        while flo.tell() != len(bytes_):
            self.options.append(NavOption(flo))

    def __repr__(self):
        return (
            '{self.__class__.__name__}'
            '(drone_state={self.drone_state}, '
            'sequence_number={self.sequence_number}, '
            'version_flag={self.version_flag}, options={options})').format(
            self=self,
            options=reprlib.repr(self.options)
        )


class NavOption:

    def __init__(self, flo):
        self.id, self.size = struct.unpack('<HH', flo.read(4))
        self.data = flo.read(self.size)

    def __repr__(self):
        return (
            '{self.__class__.__name__}'
            '(id={self.id}, size={self.size})').format(self=self)


def compute_checksum(bytes_):
    return sum(bytes_[:-8]) & 0xffffffff
