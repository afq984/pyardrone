from abc import ABCMeta, abstractmethod


class BaseClient(metaclass=ABCMeta):

    connected = False
    closed = False

    def connect(self):
        '''
        Connect to the drone.

        :raises RuntimeError: if the drone is connected or closed already.
        '''
        if self.connected:
            raise RuntimeError(
                '{} is connected already'.format(self.__class__.__name__))
        if self.closed:
            raise RuntimeError(
                '{} is closed already'.format(self.__class__.__name__))
        self.connected = True
        self._connect()

    def close(self):
        '''
        Exit all threads and disconnect the drone.

        This method has no effect if the drone is closed already or not
        connected yet.
        '''
        if not self.connected:
            return
        if self.closed:
            return
        self.closed = True
        self._close()

    @abstractmethod
    def _connect(self):
        raise NotImplementedError

    @abstractmethod
    def _close(self):
        raise NotImplementedError
