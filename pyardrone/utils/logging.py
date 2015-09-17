import logging
import collections


class MessageDict(collections.UserDict):

    def __init__(self, data):
        self.data = data

    def __getitem__(self, name):
        return self.data.pop(name)


class Message(str):

    def __new__(self, fmt, args, kwargs):
        return fmt.format(*args, **kwargs)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self)


class StyleAdapter(logging.LoggerAdapter):

    def __init__(self, logger, extra=None):
        super(StyleAdapter, self).__init__(logger, extra or {})

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            message = Message(msg, args, MessageDict(kwargs))
            self.logger._log(level, message, (), **kwargs)


def getLogger(name):
    return StyleAdapter(logging.getLogger(name))
