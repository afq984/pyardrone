import struct


def ieee754float(value):
    return struct.unpack('i', struct.pack('f', value))[0]
