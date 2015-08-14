import struct


header = struct.pack('<i', 0x55667788)


class NavOption:

    def __init__(self, ib):
        self.tag, self.size = struct.unpack('<hh')
        self.data = struct.unpack('<' + 'b' * self.size)


class NavData:

    def __init__(self, ib):
        (
            self.drone_state, self.seq_num, self.vision_flag
        ) = struct.unpack('<iii', ib)
