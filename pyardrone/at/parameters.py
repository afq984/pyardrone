import enum
import functools
import json
import io
import operator

from pyardrone.utils import ieee754float


class Parameter:

    '''
    Base class of all at command parameters.

    :param description: description of the parameter, stored in __doc__
    :param default: default value of the parameter
    '''

    def __init__(self, description='', default=None, name=None, index=None):
        self.__doc__ = description
        self._default = default
        self._name = name
        self._index = index

    def __repr__(self):
        if hasattr(self, '_name'):
            return '<{self.__class__.__name__}:{self._name}>'.format(self=self)
        else:
            return super().__repr__()

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:
            return obj[self._index]

    def __set__(self, obj, value):
        raise AttributeError(
            '{} of {} not settable, please use {}._replace'.format(
                self._name, obj, obj.__class__.__name__))

    @staticmethod
    def _check(value):
        '''
        Checks the value on :py:class:`~pyardrone.at.base.ATCommand`\ 's init.
        Subclasses can optionally define this method.

        :rtype: bool

        '''
        pass

    @staticmethod
    def _pack(value):
        '''
        Packs the value.
        Subclasses should define this method.

        :rtype: bytes

        '''


class Int32(Parameter):

    '''
    Argument representing an 32bit integer.
    '''

    @staticmethod
    def _check(value):
        if int.bit_length(value) > 32:
            raise ValueError(
                'value {} should be less than 4 bytes'.format(value)
            )

    @staticmethod
    def _pack(value):
        return str(int(value)).encode()

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == '_name' and hasattr(self, '_flags'):
            self._flags.__name__ = value

    def _set_flags(self, **flags):
        '''
        Set the flags of this argument.

        Example: ``int_param._set_flags(a=1, b=2, c=4, d=8)``
        '''
        self._flags = enum.IntEnum('_flags', flags)
        self.__dict__.update(self._flags.__members__)
        self._patch_flag_doc()

    def _patch_flag_doc(self):
        patch = io.StringIO()
        patch.write('\n\n:Flags:\n')
        for key, value in sorted(
            self._flags.__members__.items(),
            key=operator.itemgetter(1)
        ):
            patch.write('    * ``{}`` = *{:d}*\n'.format(
                key, value))
        self.__doc__ = self.__doc__.rstrip() + patch.getvalue()


class Float(Parameter):

    'Argument representing a float'

    __slots__ = ()

    @staticmethod
    def _check(value):
        float(value)

    @staticmethod
    def _pack(value):
        return str(ieee754float(value)).encode()


class String(Parameter):

    'Argument representing a string'

    __slots__ = ()

    @staticmethod
    def _check(value):
        if not isinstance(value, (str, bytes, float, int, bool)):
            raise TypeError(
                '{} is of type {}, which is unsupported'.format(
                    value,
                    type(value)
                )
            )

    @functools.singledispatch
    def _pack(value):
        '''
        packing rule:

        =========== ============
        Value       Packes into
        =========== ============
        ``True``    ``b'TRUE'``
        ``False``   ``b'FALSE'``
        ``65535``   ``b'65535'``
        ``0.32``    ``b'0.32'``
        ``'hello'`` ``b'hello'``
        =========== ============
        '''
        return json.dumps(str(value)).encode()

    @_pack.register(bool)
    def _pack_bool(value):
        return b'"TRUE"' if value else b'"FALSE"'

    @_pack.register(bytes)
    def _pack_bytes(value):
        return json.dumps(value.decode()).encode()

    _pack = staticmethod(_pack)
