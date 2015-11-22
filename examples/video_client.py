import cv2
from pyardrone.video import VideoClient

import logging

logging.basicConfig(level=logging.DEBUG)


client = VideoClient('192.168.1.1', 5555)
client.connect()
client.video_ready.wait()
try:
    while True:
        cv2.imshow('im', client.frame)
        if cv2.waitKey(10) == ord(' '):
            break
finally:
    client.close()
