The ARDrone object
==================

.. class:: ARDrone(addr='192.168.1.1', at_port=5556, navdata_port=5554, video_port=5555, control_port=5559, interval=0.03, connect=True)

    The class representing a Parrot AR.Drone

    *interval*: delay between subsequent commands in seconds

    *connect*: connect to the drone at init

    .. attribute:: config

        The config object of the drone, see the configuration topic.

    .. method:: connect()

        Connect to the drone.

    .. method:: disconnect()

        Disconnect the drone.

    .. method:: takeoff(wait=False, discard=True)

    .. method:: land(wait=False, discard=True)

        drone takeoff / land

        If *wait* is True, wait for queued commands to complete before, taking off/landing.

        If *discard* is True, discard all queued commands after taking off/land.

    .. method:: register(command, event=None)

        Puts the *ATCommand* to the queue, does not block.

    .. method:: send(command)

        Puts the *ATCommand* to the queue, blocks until it is sent to the drone.

    .. method:: send_nowait(command)

        Sends the *ATCommand* to the drone immediately.

    .. method:: get_raw_config()

        Requests and returns the raw config file from the *control_port*.
