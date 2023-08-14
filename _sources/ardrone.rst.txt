.. _ardrone:

High Level API
==============

The ARDrone Object
------------------

.. automodule:: pyardrone

    .. autoclass:: pyardrone.ARDrone

        The class representing a Parrot AR.Drone

        :param host:            address of the drone
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

        .. automethod:: takeoff

        .. automethod:: land

        .. automethod:: hover

        .. automethod:: move

        .. py:attribute:: navdata_ready

            A :py:class:`threading.Event` indicating whether
            :py:attr:`~pyardrone.ARDrone.navdata` and :py:attr:`~pyardrone.ARDrone.state`
            is ready.

            .. code-block:: python

                drone.navdata_ready.is_set() # bool: whether navdata is ready
                drone.navdata_ready.wait()   # wait until navdata is ready

        .. py:attribute:: navdata

            Latest :py:class:`~pyardrone.navdata.NavData` from drone.

            This is an attribute which gets updated each time the drone sends
            navdata back to the computer.

            .. seealso::

                :py:class:`pyardrone.navdata.NavData`

        .. autoattribute:: state

            Latest :py:class:`~pyardrone.navdata.states.DroneState` from drone.

        .. automethod:: send


Video Support
-------------

The following functions are available to the :py:class:`~pyardrone.ARDrone` class
if opencv 3.0 (cv2) is installed.

.. autoclass:: pyardrone.video.VideoMixin
    :members:
