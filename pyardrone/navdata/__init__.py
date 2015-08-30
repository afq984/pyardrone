import io
import collections

from pyardrone.navdata.options import Metadata, Checksum, index
from pyardrone.navdata.types import OptionHeader, OptionType



header = 0x55667788


def compute_checksum(buffer):
    return sum(buffer) & 0xffffffff


class NavData(collections.OrderedDict):

    '''
    Container of navdata :py:class:`~pyardrone.navdata.types.Option`\ s.

    To fetch a option, use the option class as the key:

        >>> nav[options.Demo]
        Demo(altitude=0, ctrl_state=131072, detection_camera_rot=...)
    '''

    def __init__(self, buffer):
        super().__init__()

        self.checksum = compute_checksum(buffer[:-8])

        file = io.BytesIO(buffer)

        self.add_option(Metadata, file.read(Metadata.get_size()))

        header_size = OptionHeader.get_size()
        while True:
            hb = file.read(header_size)
            if not hb:
                break
            header = OptionHeader.unpack(hb)
            if header.size:
                option_class = index[header.tag]
                data = file.read(header.size - 4)
                self.add_option(option_class, data)

    def is_valid(self):
        '''
        Checks if this NavData is valid:
            1. Header matches 0x55667788
            2. Checksum is the last item and is correct

        :rtype: bool
        '''
        return (
            self[Metadata].header == header
            and Checksum in self
            and self[Checksum].value == self.checksum
        )

    def __repr__(self):
        return '{self.__class__.__name__}({objv})'.format(
            self=self,
            objv=', '.join(map(repr, self.values()))
        )

    def add_option(self, option_class, data):
        option = option_class.unpack(data)
        self[option_class] = option
