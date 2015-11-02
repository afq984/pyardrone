from pyardrone.utils.structure import Structure
from pyardrone.utils import get_free_udp_port
import ctypes
import socket
import threading

import cv2


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


class VideoMixin:
    '''
    Mixin of ARDrone that provides video functionality
    '''

    def _video_client_job(self):
        rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rsock.connect((self.address, self.video_port))
        ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not self.closed.is_set():
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
        while not self.closed.is_set():
            ret, im = capture.read()
            self.frame_recieved(im)

    def connect(self):
        super().connect()
        self.redirect_port = get_free_udp_port()
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

    def close(self):
        super().close()

    def frame_recieved(self, im):
        self.frame = im
