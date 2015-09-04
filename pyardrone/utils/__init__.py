import struct


def repack_to_int(float_):
    return struct.unpack('i', struct.pack('f', float_))[0]


def bits(*args):
    return sum(1 << bit for bit in args)


def noop(obj):
    return obj
