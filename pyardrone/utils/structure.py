import ctypes

try:
    import numpy
except ImportError:
    NUMPY = False
else:
    NUMPY = True


# make sure ctypes.Structure does not have a special __prepare__ method
assert type(type(ctypes.Structure).__prepare__()) is dict


def first_in_other(a, b):
    b_set = set(b)
    return next(i for i in a if i in b_set)


CData = first_in_other(ctypes.Structure.mro(), ctypes.c_int.mro())
assert CData is not object
assert isinstance(CData, type)


_ctypes_StrcutureMeta = type(ctypes.Structure)


class StructureNamespace(dict):

    def __setitem__(self, key, value):
        if isinstance(value, type) and issubclass(value, CData):
            self.setdefault('_fields_', []).append((key, value))
        else:
            super().__setitem__(key, value)


class StructureMeta(_ctypes_StrcutureMeta):

    @classmethod
    def __prepare__(self, name, bases):
        return StructureNamespace()

    def __new__(cls, name, bases, namespace):
        return _ctypes_StrcutureMeta.__new__(cls, name, bases, dict(namespace))


class Structure(ctypes.Structure, metaclass=StructureMeta):

    def __repr__(self):
        return '{clsname}({fields})'.format(
            clsname=self.__class__.__name__,
            fields=', '.join(
                '{}={}'.format(name, getattr(self, name))
                for name, _ in self._fields_
            )
        )

    if NUMPY:
        def __getattribute__(self, name):
            res = super().__getattribute__(name)
            if isinstance(res, ctypes.Array):
                return numpy.asarray(res)
            return res
