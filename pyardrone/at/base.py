import collections
from pyardrone.at.parameters import Parameter


class ATCommandMeta(type):

    @classmethod
    def __prepare__(cls, name, bases):
        return collections.OrderedDict()

    def __new__(cls, name, bases, namespace):
        parameters = list()

        param_index = 0

        for key, value in namespace.items():
            if isinstance(value, Parameter):
                value._name = key
                value._index = param_index
                parameters.append(value)
                param_index += 1

        namespace['_parameters'] = parameters

        bases += cls._get_superclass_injections(name, parameters)

        return type.__new__(cls, name, bases, dict(namespace))

    @staticmethod
    def _get_superclass_injections(class_name, parameters):
        if class_name == 'ATCommand':
            return ()
        if parameters:
            param_names, defaults = zip(*(
                (param._name, param._default) for param in parameters
            ))
        else:
            param_names = defaults = ()

        middleclass = collections.namedtuple(
            '{}Namespace'.format(class_name),
            param_names
        )
        middleclass.__new__.__defaults__ = tuple(defaults)
        return (middleclass,)


class ATCommand(metaclass=ATCommandMeta):

    '''
    Base class of all ATCommands

    .. data:: _parameters

        A list of :py:class:`~pyardrone.at.parameters.Parameter`\ s of the
        command.
    '''

    def __init__(self, *args, **kwargs):
        for param, arg in zip(self._parameters, self):
            param._check(arg)

    def __eq__(self, other):
        '''
        Two commands are considered equal if they have the same arguments and
        they are of the same class
        '''
        return (type(self) is type(other)) and tuple.__eq__(self, other)

    def __ne__(self, other):
        return not self == other

    def _pack(self, seq='SEQUNSET'):
        '''
        Packs the command into *bytes*

        :param seq: sequence number
        :rtype: bytes
        '''

        # should use bytes.format, fix this after python3.5 is released
        return 'AT*{clsname}={seq}{argl_wc}\r'.format(
            clsname=type(self).__name__,
            seq=seq,
            argl_wc=b''.join(self._iter_packed_with_comma()).decode()
        ).encode()

    def _iter_packed_with_comma(self):
        for param, arg in zip(self._parameters, self):
            yield b','
            yield param._pack(arg)
