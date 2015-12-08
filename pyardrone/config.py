import collections
import weakref
import socket

from pyardrone import at
from pyardrone.abc import BaseClient


class ConfigClient(BaseClient):

    def __init__(self, host, port, at_client, timeout=3):
        self.host = host
        self.port = port
        self.at_client = at_client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', self.port))
        self.timeout = timeout

    @property
    def timeout(self):
        return self.sock.gettimeout()

    @timeout.setter
    def timeout(self, value):
        self.sock.settimeout(value)

    def _connect(self):
        self.sock.connect((self.host, self.port))

    def _close(self):
        self.sock.close()

    def get_raw_config(self):
        self.at_client.send(at.CTRL(mode=at.CTRL.mode.NO_CONTROL_MODE))
        self.at_client.send(at.CTRL(mode=at.CTRL.mode.CFG_GET_CONTROL_MODE))
        return self.sock.recv(65536)

    def set(self, key, value):
        self.at_client.send(at.CONFIG(key, value))

    def get(self, key):
        return dict(self.get_raw_config())


class Config(collections.ChainMap):

    '''
    .. attribute:: owner

        Proxy of the owner (:py:class:`~pyardrone.ARDrone`) of
        the config object.

    .. attribute:: data

        Cached dict of options from
        :py:meth:`~pyardrone.ARDrone.get_raw_config`.

    .. attribute:: updates

        Cached dict of options set by the user.
    '''

    def __init__(self, owner):
        self.owner = weakref.proxy(owner)
        self.data = LazyConfigDict(owner)
        self.updates = dict()
        super().__init__(self.updates, self.data)

    def __getattr__(self, name):
        return ConfigCategory(self, name)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.owner.send(at.CONFIG(key, value))

    def clear_cache(self):
        '''
        Clears the cached config options.
        '''
        self.updates.clear()
        self.data.clear()


class ConfigCategory:

    __slots__ = ('_context', '_name')

    def __init__(self, context, name):
        super().__setattr__('_context', weakref.proxy(context))
        super().__setattr__('_name', name)

    def __getattr__(self, name):
        return self._context[self._get_option_name(name)]

    def __setattr__(self, name, value):
        self._context[self._get_option_name(name)] = value

    def __repr__(self):
        return '<ConfigCategory {}>'.format(self._name)

    def _get_option_name(self, name):
        return '{}:{}'.format(self._name, name)


class LazyConfigDict(dict):

    __slots__ = ('owner', 'retrieved')

    def __init__(self, owner):
        super().__init__()
        self.owner = weakref.proxy(owner)
        self.retrieved = False

    def __getitem__(self, key):
        if not self.retrieved:
            self.retrieve()
        return super().__getitem__(key)

    def retrieve(self):
        self.retrieved = True
        raw_config = self.owner.get_raw_config()
        self.update(iter_config_file(raw_config))

    def clear(self):
        self.retrieved = False
        super().clear()


def unpack_value(value):
    if value == 'TRUE':
        return True
    elif value == 'FALSE':
        return False
    elif value.startswith('{') and value.endswith('}'):
        return [unpack_value(item) for item in value[1:-1].split()]
    elif value.isdigit():
        return int(value)
    else:
        try:
            return float(value)
        except:
            return value


def iter_config_file(confstr):
    for row in confstr.splitlines():
        name, raw_value = row.split(b' = ')
        yield name, unpack_value(raw_value)
