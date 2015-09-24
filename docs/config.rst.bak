.. highlight:: pycon3

.. _configuration:

Configuration
=============

Configuration is done by sending :py:class:`~pyardrone.at.CONFIG` commands to the drone and reading from :py:class:`~pyardrone.ARDrone`.control_port.

See ARDrone Developer Guide chapters 8.4 - 8.14 for detailed information of each option.

Using the config object
-----------------------

:py:class:`~pyardrone.ARDrone` provides a config object to simplify configuration: :py:attr:`pyardrone.ARDrone.config`.

Writing configuration
~~~~~~~~~~~~~~~~~~~~~

To set ``"general:navdata_demo"`` to ``"TRUE"``:

    >>> drone.config.general.navdata_demo = True

which is equivalent to:

    >>> drone.config['general:navdata_demo'] = True

or even:

    >>> drone.send(at.CONFIG('general:navdata_demo', True))

Reading configuration
~~~~~~~~~~~~~~~~~~~~~

The usage is similiar to writing.

Attribute access:

    >>> drone.config.general.ardrone_name
    'My ARDrone'

or __getitem__:

.. code-block:: pycon3

    >>> drone.config["general:ardrone_name"]
    'My ARDrone'


If the requested configuration option does not exist, :py:exc:`KeyError` will be raised

.. note::

    1. The config object uses :py:meth:`pyardrone.ARDrone.get_raw_config` to retrieve the config file from the drone and caches it, when requested to read a option.

    2. Options set by the user are also cached.

    So :py:meth:`~pyardrone.ARDrone.get_raw_config` is called only if:
        * the option is not set previously

        * it is not called previously

    Still, the cache can be cleared by calling :py:meth:`~pyardrone.config.Config.clear_cache`

The Config Class
----------------

.. autoclass:: pyardrone.config.Config
    :members:
