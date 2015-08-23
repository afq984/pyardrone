import struct


def ieee754float(value):
    return struct.unpack('i', struct.pack('f', value))[0]


def bits(*args):
    return sum(1 << bit for bit in args)


def noop(obj):
    return obj
