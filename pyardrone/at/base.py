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
        parameters = list()
        for key, value in namespace.items():
            if isinstance(value, Argument):
                value.name = key
                parameters.append(value)

        # update doc
        if '__doc__' in namespace:
            doc_updates = ['']
            indent = ''
            for line in namespace['__doc__'].splitlines():
                text = line.strip()
                if text:
                    indent = line.split(text)[0]
                    break

            for parameter in parameters:
                try:
                    type_hint = parameter.type_hint.__name__
                except AttributeError:
                    type_hint = ''
                doc_updates.append(
                    ':param {type} {name}: {desc}'.format(
                        type=type_hint,
                        name=parameter.name,
                        desc=parameter.description or 'no description'
                    )
                )

            doc_updates.append('')

            has_flags = False
            for parameter in parameters:
                if hasattr(parameter, '_flags'):
                    parameter._flags.__name__ = parameter.name
                    if not has_flags:
                        doc_updates.append('Flags:')
                    for flag in sorted(parameter._flags):
                        doc_updates.append(
                            '    * ``{flag!r}``'.format(
                                flag=flag
                            )
                        )
                doc_updates.append('')

            namespace['__doc__'] += ('\n' + indent).join(doc_updates)

        namespace['parameters'] = parameters
        self = type.__new__(cls, name, bases, dict(namespace))
        return self


class ATCommand(metaclass=ATCommandMeta):

    '''
    Base class of all ATCommands

    .. attribute:: parameters

        A list of parameters (:py:class:`~pyardrone.at.arguments.Argument`\ s)\
        of the command.

    .. attribute:: _args

        Dict of stored arguments.
    '''
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
        '''
        Two *ATCommand*\ s are compared equal if:
            * They are of the same class

            * They have the same arguments
        '''
        if isinstance(other, ATCommand):
            return type(self) == type(other) and self._args == other._args
        return NotImplemented

    def pack(self, seq='SEQUNSET'):
        '''
        Packs the command into *bytes*

        :param seq: sequence number
        :rtype: bytes
        '''

        # should use bytes.format, fix this after python3.5 is released
        return 'AT*{clsname}={seq},{argl}\r'.format(
            clsname=type(self).__name__,
            seq=seq,
            argl=b','.join(self._iter_packed()).decode()
        ).encode()

    def _iter_packed(self):
        for par in self.parameters:
            yield par.pack(getattr(self, par.name))
