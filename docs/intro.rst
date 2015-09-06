Getting Started
===============

THIS SECTION IS WIP.

Requirements
------------

* Python 3.4 or later

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
    while not drone.state.fly_mask:
        drone.takeoff()
    time.sleep(10)
    while drone.state.fly_mask:
        drone.land()
