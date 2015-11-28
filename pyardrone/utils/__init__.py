'''
Utility functions
=================
'''


import struct
import time


def repack_to_int(value):
    '''
    Converts the passed in float *value* to interger as ieee754 specification.

    Same as *\*(int\*)&value* in C, or *reinterpret_cast<int>value* in C++.
    '''
    return struct.unpack('i', struct.pack('f', value))[0]


def bits(*args):
    '''
    >>> bits(7)
    128
    >>> bits(1, 3, 5) == 0b101010
    True
    '''
    return sum(1 << bit for bit in args)


def noop(obj):
    '''
    Returns the passed in argument.

        >>> noop(10)
        10
        >>> noop(list)
        <class 'list'>
    '''
    return obj


def every(secs):
    '''
    Generator that yields for every *secs* seconds.

    Example:

        >>> for _ in every(0.1):
        ...     print('Hello')

    You get ``Hello`` output every 0.1 seconds.
    '''
    time_stated = time.monotonic()
    while True:
        time_yielded = time.monotonic()
        yield time_yielded - time_stated
        time.sleep(max(0, secs + time_yielded - time.monotonic()))


def get_free_udp_port():
    '''
    Get a free UDP port.

    Note this is vlunerable to race conditions.
    '''
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    addr = sock.getsockname()
    sock.close()
    return addr[1]
