import functools
import json
import warnings
from pyardrone.utils import ieee754float


class Argument:

    __slots__ = ('name', 'description')

    def __init__(self, description=None):
        self.description = None

    def __get__(self, obj, type_=None):
        try:
            return obj._args[self.name]
        except KeyError:
            return None

    def __set__(self, obj, value):
        if hasattr(self, 'check'):
            self.check(value)
        obj._args[self.name] = value

    def __repr__(self):
        if hasattr(self, 'name'):
            return '<{}:{}>'.format(type(self).__name__, self.name)
        else:
            return super().__repr__()


class Int32Arg(Argument):

    def check(self, value):
        if int.bit_length(value) > 32:
            raise ValueError(
                'value {} should be less than 4 bytes'.format(value)
            )

    @staticmethod
    def pack(value):
        return str(value).encode()


class FloatArg(Argument):

    def check(self, value):
        if not isinstance(value, float):
            raise TypeError('{:r} should be a float, not {}'.format(
                value, type(value)
            ))

    @staticmethod
    def pack(value):
        return str(ieee754float(value)).encode()


class StringArg(Argument):

    def check(self, value):
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
        return json.dumps(str(value)).encode()

    @pack.register(bool)
    def _pack_bool(value):
        return b'"TRUE"' if value else b'"FALSE"'

    @pack.register(bytes)
    def _pack_bytes(value):
        return json.dumps(value.decode()).encode()

    pack = staticmethod(pack)
