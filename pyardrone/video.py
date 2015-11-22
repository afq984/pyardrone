from pyardrone.utils.structure import Structure
from pyardrone.utils import get_free_udp_port, logging
from pyardrone.abc import BaseClient
import ctypes
import socket
import threading

import cv2


logger = logging.getLogger(__name__)


uint8_t = ctypes.c_int8
uint16_t = ctypes.c_int16
uint32_t = ctypes.c_int32


class PaVE(Structure):

    HEADER = b'PaVE'

    signature = uint8_t * 4  #: "PaVE" - used to identify the start of frame
    version = uint8_t  #: Version code
    video_codec = uint8_t  #: Codec of the following frame
    header_size = uint16_t  #: Size of the parrot_video_encapsulation_t
    payload_size = uint32_t  #: Amount of data following this PaVE
    encoded_stream_width = uint16_t  #: ex: 640
    encoded_stream_height = uint16_t  #: ex: 368
    display_width = uint16_t  #: ex: 640
    display_height = uint16_t  #: ex: 360

    frame_number = uint32_t  #: Frame position inside the current stream

    timestamp = uint32_t  #: In milliseconds

    total_chuncks = uint8_t
    #: Number of UDP packets containing the current decodable payload -
    #: currently unused

    chunck_index = uint8_t
    #: Position of the packet - first chunk is #0 - currenty unused

    frame_type = uint8_t
    #: I-frame, P-frame - parrot_video_encapsulation_frametypes_t

    control = uint8_t
    #: Special commands like end-of-stream or advertised frames

    stream_byte_position_lw = uint32_t
    #: Byte position of the current payload in the encoded stream - lower
    #: 32-bit word

    stream_byte_position_uw = uint32_t
    #: Byte position of the current payload in the encoded stream - upper
    #: 32-bit word

    stream_id = uint16_t
    #: This ID indentifies packets that should be recorded together

    total_slices = uint8_t
    #: number of slices composing the current frame

    slice_index = uint8_t
    #: position of the current slice in the frame

    header1_size = uint8_t
    #: H.264 only : size of SPS inside payload - no SPS present if value is
    #: zero

    header2_size = uint8_t
    #: H.264 only : size of PPS inside payload - no PPS present if value is
    #: zero

    reserved2 = uint8_t * 2
    #: Padding to align on 48 bytes

    advertised_size = uint32_t
    #: Size of frames announced as advertised frames

    reserved3 = uint8_t * 12
    #: Padding to align on 64 bytes


class VideoClient(BaseClient):
    '''
    Independent ARDrone Video Client
    '''

    def __init__(self, host, video_port, redirect_port=None):
        self.host = host
        self.video_port = video_port
        self.redirect_port = redirect_port
        self.video_ready = threading.Event()

    def _video_client_job(self):
        rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rsock.connect((self.host, self.video_port))
        logger.info(
            'Connected to video port {}'.format(self.host, self.video_port))
        ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not self.closed:
            data = rsock.recv(4096)
            if data.startswith(PaVE.HEADER):
                data = data[ctypes.sizeof(PaVE):]
            ssock.sendto(data, ('localhost', self.redirect_port))
        rsock.close()
        ssock.close()

    def _video_opencv_job(self):
        capture = cv2.VideoCapture(
            'udp://localhost:{port}'.format(port=self.redirect_port)
        )
        logger.info('initiated VideoCapture at port {}'.format(
            self.redirect_port))
        while not self.closed:
            ret, im = capture.read()
            self.frame_recieved(im)
            self.video_ready.set()

    def _connect(self):
        if self.redirect_port is None:
            self.redirect_port = get_free_udp_port()
            logger.info('Selected free udp port {}'.format(self.redirect_port))
        self._video_client_thread = threading.Thread(
            target=self._video_client_job,
            daemon=True
        )
        self._video_opencv_thread = threading.Thread(
            target=self._video_opencv_job,
            daemon=True
        )

        self._video_client_thread.start()
        self._video_opencv_thread.start()

    def _close(self):
        pass

    def frame_recieved(self, im):
        self.frame = im


class VideoMixin:
    '''
    Mixin of ARDrone that provides video functionality
    '''

    def _connect(self):
        super()._connect()
        self.video_client = VideoClient(self.host, self.video_port)
        self.video_client.connect()

    def _close(self):
        self.video_client.close()
        super()._close()

    @property
    def frame(self):
        '''
        The latest frame from ARDrone, in opencv's format.
        '''
        return self.video_client.frame

    @property
    def video_ready(self):
        '''
        A :py:class:`threading.Event` object indicating whether video is ready.
        '''
        return self.video_client.video_ready
