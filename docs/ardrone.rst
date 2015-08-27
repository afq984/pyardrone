The ARDrone object
==================

.. class:: ARDrone(addr='192.168.1.1', at_port=5556, navdata_port=5554, video_port=5555, control_port=5559, interval=0.03, connect=True)

    The class representing a Parrot AR.Drone

    :param address: address of the drone
    :param at_port: AT command port
    :param navdata_port: NavData port
    :param video_port: Video port
    :param control_port: Control port
    :param interval: delay between subsequent commands in seconds
    :param connect: connect to the drone at init

    .. attribute:: config

        The config object of the drone, see :ref:`configuration`.

    .. method:: connect()

        Connect to the drone.

        :raises RuntimeError: if the drone is connected or closed already.

    .. method:: close()

        Exit all threads and disconnect the drone.

        This method has no effect if the drone is closed already or not connected yet.

    .. method:: takeoff(wait=False, discard=True)

    .. method:: land(wait=False, discard=True)

        drone takeoff / land

        If *wait* is True, wait for queued commands to complete before, taking off/landing.

        If *discard* is True, discard all queued commands after taking off/land.

    .. method:: register(command, with_event=True)

        Puts the *ATCommand* to the queue, does not block.

        :param ATCommand command: Command to register.
        :param bool with_event: If ``True``, returns an :py:class:`threading.Event` object, which can be used to indicate whether the job is done.

    .. method:: send(command)

        Puts the command to the queue, blocks until it is sent to the drone.

    .. method:: send_nowait(command)

        Sends the command to the drone immediately.

    .. method:: get_raw_config()

        Requests and returns the raw config file from the *control_port*.

        :rtype: bytes
