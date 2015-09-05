import collections
import functools
import io
import itertools
import struct
import types

from pyardrone.utils.dochelper import DocFile


def _grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


class Type:

    def get_size(self):
        return struct.calcsize(self.code)

    def __getitem__(self, item):
        return ArrayType(self, item)

    def __repr__(self):
        return '<{self.__class__.__name__} {self.name!r}>'.format(self=self)


class ValueType(Type):

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def unpack(self, buffer):
        return struct.unpack(self.code, buffer)[0]

    def unpack_file(self, file):
        return self.unpack(file.read(struct.calcsize(self.code)))


bool_t = ValueType('?', 'bool_t')
char = ValueType('c', 'char')
int8_t = ValueType('b', 'int8_t')
int16_t = ValueType('h', 'int16_t')
int32_t = ValueType('i', 'int32_t')
int64_t = ValueType('q', 'int64_t')
uint8_t = ValueType('B', 'uint8_t')
uint16_t = ValueType('H', 'uint16_t')
uint32_t = ValueType('I', 'uint32_t')
uint64_t = ValueType('Q', 'uint64_t')
float32_t = ValueType('f', 'float32_t')
float64_t = ValueType('d', 'float64_t')


class Embed:

    def __init__(self, option):
        self.option = option


class ContainerType(Type):

    def unpack_file(self, file):
        return self.unpack(file.read(struct.calcsize(self.code)))


class MatrixType(ContainerType):

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.count = a * b
        self.code = 'f' * self.count

    @property
    def name(self):
        return 'matrix{self.a}{self.b}_t'.format(self=self)

    def unpack(self, buffer):
        return tuple(_grouper(struct.unpack(self.code, buffer), self.a))


class VectorType(ContainerType):

    def __init__(self, name, vargs, type=float32_t):
        count = len(vargs)
        self.code = type.code * count
        self.name = name
        self.container = collections.namedtuple(
            name,
            vargs
        )

    def unpack(self, buffer):
        return self.container(*struct.unpack(self.code, buffer))


class ArrayType(ContainerType):

    def __init__(self, value_type, count):
        self.value_type = value_type
        self.count = count
        self.code = self.value_type.code * count

    @property
    def name(self):
        return '{}[{}]'.format(self.value_type.name, self.count)

    def unpack(self, buffer):
        return struct.unpack(self.code, buffer)


class OptionNamespace(dict):

    def __init__(self):
        self['_fields'] = []

    def __setitem__(self, key, value):
        if isinstance(value, Type):
            self['_fields'].append((key, value))
        elif isinstance(value, Embed):
            self['_fields'].extend(value.option._fields)
        super().__setitem__(key, value)


class OptionType(type, Type):

    @classmethod
    def __prepare__(cls, name, bases):
        return OptionNamespace()

    def __new__(cls, name, bases, namespace):
        cls.update_doc(namespace)
        return type.__new__(cls, name, bases, dict(namespace))

    def unpack(self, buffer):
        return self.unpack_file(io.BytesIO(buffer))

    def unpack_file(self, file):
        obj = super().__call__()
        for name, type_ in self._fields:
            setattr(obj, name, type_.unpack_file(file))
        return obj

    @staticmethod
    def update_doc(namespace):
        # TODO: This should be done by a sphinx extension instead of a
        #       metaclass hack
        if '__doc__' not in namespace or '_attrname' not in namespace:
            return
        df = DocFile(namespace['__doc__'])
        df.write('\n')
        df.writeline(
            "available via :py:class:`~pyardrone.navdata.NavData`'s "
            "attribute: ``{}``".format(
                namespace['_attrname']
            )
        )
        namespace['__doc__'] = df.getvalue()

    @property
    def code(self):
        return ''.join(field[1].code for field in self._fields)

    __call__ = unpack


class Option(types.SimpleNamespace, metaclass=OptionType):

    '''
    Base class of all NavData options.

    Corresponds to C struct ``navdata_option_t``.

    .. py:data:: attrname

        The attribute name the get this option from
        :py:class:`~pyardrone.navdata.NavData`
    '''


class OptionHeader(Option):

    tag = uint16_t
    size = uint16_t


class OptionIndex(dict):

    def register(self, tag):
        return functools.partial(self._register, tag)

    def _register(self, tag, function):
        if tag in self:
            raise KeyError('Key {!r} conflict with existing item {}'.format(
                tag, self[tag]))
        self[tag] = function
        return function
