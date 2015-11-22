import cv2
from pyardrone import ARDrone

import logging

logging.basicConfig(level=logging.DEBUG)


client = ARDrone()
client.video_ready.wait()
try:
    while True:
        cv2.imshow('im', client.frame)
        if cv2.waitKey(10) == ord(' '):
            break
finally:
    client.close()
