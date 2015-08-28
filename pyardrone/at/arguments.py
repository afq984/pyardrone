'''
ATCommand Argument Classes
'''

import enum
import functools
import json
import warnings
from pyardrone.utils import ieee754float


class Argument:

    '''
    Base class of all arguments.

    :param description: stored, used to generate documentation.

    :param default: used to provide a default value for the argument for the \
                    :class:`~pyardrone.at.base.ATCommand`.
    '''

    __slots__ = ('name', 'description', 'default')

    def __init__(self, description=None, *, default=None):
        self.description = description
        self.default = default

    def __get__(self, obj, type_=None):
        if obj is None:
            return None
        else:
            try:
                return obj._args[self.name]
            except KeyError:
                return self.default

    def __set__(self, obj, value):
        if obj is None:
            raise AttributeError('{!r} is not settable'.format(self))
        if hasattr(self, 'check'):
            self.check(value)
        obj._args[self.name] = value

    def __repr__(self):
        if hasattr(self, 'name'):
            return '<{}:{}>'.format(type(self).__name__, self.name)
        else:
            return super().__repr__()

    @staticmethod
    def pack(value):
        '''
        Packs the value into bytes

        :rtype: bytes

        Subclasses should define this method.
        '''

        raise NotImplementedError


class Int32Arg(Argument):

    '''
    Argument representing an 32bit integer.
    '''

    __slots__ = ('_flags',)

    type_hint = int

    def __get__(self, obj, type_=None):
        if obj is None:
            return getattr(self, '_flags', None)
        else:
            return super().__get__(obj, type_)

    @staticmethod
    def check(value):
        if int.bit_length(value) > 32:
            raise ValueError(
                'value {} should be less than 4 bytes'.format(value)
            )

    @staticmethod
    def pack(value):
        return str(int(value)).encode()

    def set_flags(self, **flags):
        '''
        Set the flags of this arguments
        '''
        self._flags = enum.IntEnum('_flags', flags)


class FloatArg(Argument):

    'Argument representing a float'

    __slots__ = ()

    type_hint = float

    @staticmethod
    def pack(value):
        return str(ieee754float(value)).encode()


class StringArg(Argument):

    'Argument representing a string'

    __slots__ = ()

    type_hint = str

    @staticmethod
    def check(value):
        if not isinstance(value, (str, bytes, float, int, bool)):
            warnings.warn(
                '{} is of type {}, which may be unsupported py ARDrone'.format(
                    value,
                    type(value)
                ),
                stacklevel=3
            )

    @functools.singledispatch
    def pack(value):
        '''
        packing rule:
            * ``True`` => ``b'TRUE'``
            * ``False`` => ``b'FALSE'``
            * ``65535`` => ``b'65535'``
            * ``0.32`` => ``b'0.32'``
            * ``'hello, world'`` => ``b'hello, world'``
        '''
        return json.dumps(str(value)).encode()

    @pack.register(bool)
    def _pack_bool(value):
        return b'"TRUE"' if value else b'"FALSE"'

    @pack.register(bytes)
    def _pack_bytes(value):
        return json.dumps(value.decode()).encode()

    pack = staticmethod(pack)
