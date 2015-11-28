from pyardrone import ARDrone
from contextlib import suppress


drone = ARDrone()

drone.navdata_ready.wait()
with suppress(KeyboardInterrupt):
    while True:
        print(drone.state)
drone.close()
