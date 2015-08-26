The ARDrone object
==================

.. class:: ARDrone(addr='192.168.1.1', at_port=5556, navdata_port=5554, video_port=5555, control_port=5559, interval=0.03)

    The class representing a Parrot AR.Drone

    *interval*: delay between subsequent commands in seconds

    .. attribute:: config

        The config object of the drone, see the configuration topic.

    .. method:: takeoff(interrupt=False)

    .. method:: land(interrupt=False)

        drone takeoff / land

        If *interrupt* is True, abort the queued *ATCommand*\ s and takeoff/land immediately; wait for the queued commands otherwise.

    .. method:: register(command, event=None)

        Puts the *ATCommand* to the queue, does not block.

    .. method:: send(command)

        Puts the *ATCommand* to the queue, blocks until it is sent to the drone.

    .. method:: send_nowait(command)

        Sends the *ATCommand* to the drone immediately.

    .. method:: get_raw_config(self):

        Requests and returns the raw config file from the *control_port*.
