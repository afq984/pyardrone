Getting Started
===============

~ `Github <https://github.com/afg984/pyardrone>`_ ~
`PyPI <https://pypi.python.org/pypi/pyardrone>`_ ~
`Online Docs <http://pyardrone.readthedocs.org>`_ ~

Requirements
------------

* Python 3.4 or later
* opencv 3.0 or later (for video support)

Installation
------------

.. code-block:: bash

    pip install pyardrone

Basic Usage
-----------

.. code-block:: python3

    import time
    from pyardrone import ARDrone
    drone = ARDrone()
    drone.navdata_ready.wait()  # wait until NavData is ready
    while not drone.state.fly_mask:
        drone.takeoff()
    time.sleep(20)              # hover for a while
    while drone.state.fly_mask:
        drone.land()
