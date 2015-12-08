NavData
=======


To access navdata:

.. code-block:: python3

    >>> from pyardrone import ARDrone, at
    >>> drone = ARDrone()
    >>> drone.navdata_ready.wait()  # wait for first navdata
    >>> drone.navdata
    NavData(checksum=928, cks=Cks(value=928), metadata=Metadata(header=1432778632, state=1333790928, sequence_number=79367, vision_flag=1))
    >>> drone.navdata.metadata
    Metadata(header=1432778632, state=1333790928, sequence_number=79367, vision_flag=1)

For navdata demo data, according to the Developer Guide from parrot, you have to send an AT*CONFIG command,
which is:

.. code-block:: python3

    >>> drone.send(at.CONFIG('general:navdata_demo', True))

in pyardrone.

And drone.navdata.demo will be available then.

A higher level API for configuring ARDrone will be available in future versions, though.

The NavData Class
-----------------

.. automodule:: pyardrone.navdata
    :members:
    :show-inheritance:


List of navdata Options
-----------------------

.. automodule:: pyardrone.navdata.options
    :members:
    :member-order:
    :undoc-members:
