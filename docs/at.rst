ATCommands
==========

The (in)complete description of ATCommands is documented in Parrot's AR.Drone Developer Guide chapter 6.5, please refer to it for detailed description of each command.

Using ATCommands
----------------

Creating an ATCommand
~~~~~~~~~~~~~~~~~~~~~

To create an :class:`~pyardrone.at.base.ATCommand`, you have to call the command class with the corresponding arguments.

For example, to create an ``"AT*PCMD"`` command with the progressive flag and vertical speed = 0.8:

    >>> from pyardrone import at
    >>> cmd = at.PCMD(at.PCMD.flag.progressive, 0, 0.8, 0, 0)
    >>> cmd
    PCMD(flag=<flag.progressive: 1>, roll=0, pitch=0.8, gaz=0, yaw=0)

or using keyword arguments, just like a function:

    >>> at.PCMD(at.PCMD.flag.progressive, gaz=0.8)
    PCMD(flag=<flag.progressive: 1>, roll=0, pitch=0.8, gaz=0, yaw=0)

ATCommands are :py:func:`collections.namedtuple` subclasses, so reading it is just as easy.

    >>> cmd
    PCMD(flag=<flag.progressive: 1>, roll=0, pitch=0.8, gaz=0, yaw=0)
    >>> cmd.roll
    0
    >>> cmd.pitch
    0.8
    >>> cmd[0]
    <flag.progressive: 1>
    >>> cmd[2]
    0.8
    >>> list(cmd)
    [<flag.progressive: 1>, 0, 0.8, 0, 0]

Additionally :py:meth:`~pyardrone.at.base.ATCommand._pack` packs the command into bytes

    >>> cmd._pack(10)  # pack with sequence number = 10
    b'AT*PCMD=10,1,0,1061997773,0,0\r'

Sending an ATCommand
~~~~~~~~~~~~~~~~~~~~

To send a AT\*PCMD command with the progressive flag and vertical speed = 0.8, use :py:meth:`pyardrone.ARDrone.send`

    >>> # drone is an ARDrone instance here
    >>> drone.send(at.PCMD(at.PCMD.flag.progressive, 0, 0.8, 0, 0))

:py:meth:`~pyardrone.ARDrone.send` provides the sequence number for the :py:meth:`~pyardrone.at.base.ATCommand._pack` function automatically.

Defining ATCommand subclasses
-----------------------------

If you want to use an ATCommand not defined in the library, you can define it yourself.

For example, to define a "AT*EXAMPLE" command with three arguments: options, speed, comment, which is a integer, a float, and a string respectively:

.. code-block:: python

    from pyardrone.at import base, parameters

    class EXAMPLE(base.ATCommand):

        options = parameters.Int32()
        speed = parameters.Float()
        comment = parameters.String(default='nothing')

        options._set_flags(
            eat=0b1,
            sleep=0b10,
            wander=0b100
        )

The created *EXAMPLE* class can then be used just like other ATCommand classes:

    >>> cmd = EXAMPLE(EXAMPLE.options.sleep, 3.5, 'hello')
    >>> cmd
    EXAMPLE(options=<options.sleep: 2>, speed=3.5, comment='hello')
    >>> cmd._pack()
    b'AT*EXAMPLE=SEQUNSET,2,1080033280,"hello"\r'
    >>> EXAMPLE(options=EXAMPLE.options.wander, speed=6.7)
    EXAMPLE(options=<options.wander: 4>, speed=6.7, comment='nothing')

The base ATCommand Class
------------------------

Subclasses share the following methods:

.. autoclass:: pyardrone.at.base.ATCommand
    :members:
    :private-members:

List of ATCommands
------------------

.. automodule:: pyardrone.at
    :members:
    :member-order:

Parameters
----------

.. currentmodule:: pyardrone.at.parameters

.. autoclass:: Parameter
    :members:
    :private-members:

Parameter types
~~~~~~~~~~~~~~~

.. autoclass:: Int32(...)
    :members:
    :private-members:

.. autoclass:: Float(...)
    :members:

.. autoclass:: String(...)
    :members:
    :private-members:

