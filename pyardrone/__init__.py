from pyardrone import at
from pyardrone.at import ATClient
from pyardrone.navdata import NavDataClient
from pyardrone.navdata.states import DroneState
from pyardrone.utils import logging
from pyardrone.abc import BaseClient

# import VideoMixin only if opencv is available
try:
    import cv2
except ImportError:
    class DummyVideoMixin:
        pass
    VideoMixin = DummyVideoMixin
    VIDEO = False
else:
    del cv2
    from pyardrone.video import VideoMixin
    VIDEO = True


__version__ = '0.6.0'

__all__ = ('ARDrone',)


logger = logging.getLogger(__name__)


class ARDroneBase(BaseClient):

    def __init__(
        self,
        *,
        host='192.168.1.1',
        at_port=5556,
        navdata_port=5554,
        video_port=5555,
        watchdog_interval=0.5,
        timeout=0.01,
        bind=True,
        connect=True
    ):
        self.host = host
        self.at_port = at_port
        self.navdata_port = navdata_port
        self.video_port = video_port
        self.watchdog_interval = watchdog_interval
        self.timeout = timeout
        self.bind = bind

        if connect:
            self.connect()

    @property
    def navdata(self):
        return self.navdata_client.navdata

    @property
    def state(self):
        '''
        The latest state from :py:class:`~pyardrone.navdata.NavData`.

            >>> drone.state.fly_mask
            True  # drone is flying
            >>> drone.state.video
            True  # video is enabled

        See :py:class:`~pyardrone.navdata.states.DroneState`
        for the full list of states.
        '''
        return DroneState(self.navdata.metadata.state)

    @property
    def navdata_ready(self):
        return self.navdata_client.navdata_ready

    def send(self, command):
        '''
        :param ~pyardrone.at.base.ATCommand command: command to send

        Sends the command to the drone,
        with an internal increasing sequence number.
        this method is thread-safe.
        '''
        self.at_client.send(command)

    def _connect(self):
        self.at_client = ATClient(self.host, self.at_port)
        self.navdata_client = NavDataClient(self.host, self.navdata_port)
        self.at_client.connect()
        self.navdata_client.connect()

    def _close(self):
        self.at_client.close()
        self.navdata_client.close()


class HelperMixin:

    def takeoff(self):
        '''
        Sends the takeoff command.
        '''
        self.send(at.REF(at.REF.input.start))

    def land(self):
        '''
        Sends the land command.
        '''
        self.send(at.REF())

    def emergency(self):
        '''
        Sends the emergency command.
        '''
        self.send(at.REF(at.REF.input.select))

    def _move(self, roll=0, pitch=0, gaz=0, yaw=0):
        '''
        Same as sending :py:class:`~pyardrone.at.PCMD` command with progressive
        flag.
        '''
        self.send(at.PCMD(at.PCMD.flag.progressive, roll, pitch, gaz, yaw))

    def move(
            self, *,
            forward=0, backward=0,
            left=0, right=0,
            up=0, down=0,
            cw=0, ccw=0):
        '''
        Moves the drone.

        To move the drone forward at 0.8x speed:

        >>> drone.move(forward=0.8)

        To move the drone right at 0.5x speed and upward at full speed:

        >>> drone.move(right=0.5, up=1)

        To rotate clockwise at 0.7x speed:

        >>> drone.move(cw=0.7)

        :param forward:  speed for moving forward
        :param backward: speed for moving backward
        :param left:     speed for moving left
        :param right:    speed for moving right
        :param up:       speed for moving up
        :param down:     speed for moving down
        :param cw:       speed for rotating clockwise
        :param ccw:      speed for rotating counter-clockwise
        '''
        self._move(
            roll=right-left,
            pitch=backward-forward,
            gaz=up-down,
            yaw=cw-ccw
        )

    def hover(self):
        '''
        Sends the hover command.
        '''
        self.send(at.PCMD(flag=0))


class ARDrone(HelperMixin, VideoMixin, ARDroneBase):
    pass
