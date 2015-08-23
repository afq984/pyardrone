'''
ATCommand Base Class
'''


import collections
from pyardrone.at.arguments import Argument


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
                '{}={!r}'.format(par.name, getattr(self, par.name))
                for par in self.parameters
            )
        )

    def __eq__(self, other):
        if isinstance(other, ATCommand):
            return self._args == other._args
        return NotImplemented

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
