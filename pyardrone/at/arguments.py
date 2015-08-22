import collections
import functools
import json
import warnings
from pyardrone.utils import ieee754float


def packer(func):
    def wrapper(self):
        return func(self.value)
    return wrapper


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


class ATCommandMeta(type):

    @classmethod
    def __prepare__(cls, name, bases):
        return collections.OrderedDict()

    def __new__(cls, name, bases, namespace):
        self = type.__new__(cls, name, bases, dict(namespace))
        self.parameters = list()
        for key, value in namespace.items():
            if isinstance(value, Argument):
                value.name = key
                self.parameters.append(value)
        return self


class ATCommand(metaclass=ATCommandMeta):
    __slots__ = '_args'

    def __init__(self, *args, **kwargs):
        self._args = dict()
        if len(args) > len(self.parameters):
            raise TypeError('__init__ got {} arguments, expected {}'.format(
                len(args), len(self.parameters)
            ))
        for arg, par in zip(args, self.parameters):
            setattr(self, par.name, arg)
        for key, value in kwargs.items():
            if key in self._args:
                raise TypeError(
                    'Argument {!r} given by name and position'.format(
                        key
                    )
                )
            setattr(self, key, value)

    def __repr__(self):
        return '{clsname}({argl})'.format(
            clsname=type(self).__name__,
            argl=', '.join(
                '{}={!r}'.format(par.name, getattr(self, par.name).value)
                for par in self.parameters
            )
        )

    def pack(self, seq='SEQUNSET'):
        # should use bytes.format, fix this after python3.5 is released
        return 'AT*{clsname}={seq},{argl}\r'.format(
            clsname=type(self).__name__,
            seq=seq,
            argl=b','.join(self._iter_packed()).decode()
        ).encode()

    def _iter_packed(self):
        for par in self.parameters:
            yield par.pack(getattr(self, par.name))
