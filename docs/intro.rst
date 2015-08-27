Getting Started
===============

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

    >>> import time
    >>> from pyardrone import ARDrone
    >>> drone = ARDrone()
    >>> drone.takeoff()
    >>> time.sleep(10)
    >>> drone.land()
