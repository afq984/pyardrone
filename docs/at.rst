*ATCommand*\ s
==============

The (in)complete description of *ATCommand*\ s is documented in Parrot's AR.Drone Developer Guide chapter 6.5, please refer to it for detailed description of each command.

Using *ATCommand*\s
-------------------

Creating an *ATCommand* instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create an *ATCommand* instance, you have to call the command class with the corresponding arguments.

For example, to create an ``"AT*PCMD"`` command with the progressive flag and vertical speed = 0.8:

    .. code-block:: python3

        >>> from pyardrone import at
        >>> cmd = at.PCMD(at.PCMD.Flags.progressive, 0, 0.8, 0, 0)
        PCMD(flag=<flags.progressive: 1>, roll=0, pitch=0.8, gaz=0, yaw=0)
        >>> # or with keyword arguments, just use it like a function
        >>> at.PCMD(at.PCMD.flag.progressive, gaz=0.8)
        PCMD(flag=<flags.progressive: 1>, roll=0, pitch=0.8, gaz=0, yaw=0)

Sending an *ATCommand*
~~~~~~~~~~~~~~~~~~~~~~

To send a AT\*PCMD command with the progressive flag and vertical speed = 0.8, use the following:

    .. code-block:: python3

        >>> # drone is an ARDrone instance here
        >>> drone.send(at.PCMD(at.PCMD.flag.progressive, 0, 0.8, 0, 0))

The library provides the sequence number for the *pack()* function automatically.

Defining an *ATCommand* class
-----------------------------

If you want to use an *ATCommand* not defined in the library, you can define it yourself.

For example, to define a "AT*EXAMPLE" command with three arguments: options, speed, comment, which is a integer, a float, and a string respectively:

    .. code-block:: python

        from pyardrone.at.base import ATCommand
        from pyardrone.at.arguments imoprt Int32Arg, FloatArg, StringArg

        class EXAMPLE(ATCommand):

            options = Int32Arg()
            speed = FloatArg()
            comment = StringArg(default='nothing')

            options.set_flags(
                eat=0b1,
                sleep=0b10,
                wander=0b100
            )

The created *EXAMPLE* class can then be used just like other ATCommand classes:

    .. code-block:: python

        >>> cmd = EXAMPLE(EXAMPLE.options.sleep, 3.5, 'hello')
        >>> cmd
        EXAMPLE(number=<flags.sleep: 2>, speed=3.5, comment='hello')
        >>> cmd.pack()
        b'AT*EXAMPLE=SEQUNSET,2,1080033280,"hello"\r'
        >>> EXAMPLE(number=EXAMPLE.options.wander, speed=6.7)
        EXAMPLE(number=<flags.wander: 4>, speed=6.7, comment='nothing')

ATCommand API
-------------

.. autoclass:: pyardrone.at.base.ATCommand
    :members:
    :special-members:

List of ATCommands
------------------

.. automodule:: pyardrone.at
    :members:

Argument Classes
----------------

.. currentmodule:: pyardrone.at.arguments

.. autoclass:: Argument
    :members:

.. autoclass:: Int32Arg
    :members: set_flags

.. autoclass:: FloatArg

.. autoclass:: StringArg
    :members: pack
