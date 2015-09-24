The ARDrone object
==================

.. automodule:: pyardrone

    .. autoclass:: pyardrone.ARDrone
        :members:
        :inherited-members:


        The class representing a Parrot AR.Drone

        :param address:         address of the drone
        :param at_port:         AT command port
        :param navdata_port:    NavData port
        :param video_port:      Video port
        :param control_port:    Control port
        :param watchdog_interval:  seconds between each
                                   :py:class:`~pyardrone.at.COMWDG`
                                   sent in background
        :param bind:            whether to :py:meth:`~socket.socket.bind`
                                the sockets; this option exists for testing
        :param connect:         connect to the drone at init

        .. py:attribute:: navdata

            Latest navdata from drone.
