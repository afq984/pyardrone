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
        PCMD(flag=at.PCMD.Flags.progressive, roll=0.0, pitch=0.8, gaz=0.0, yaw=0.0)
        >>> # or with keyword arguments, just use it like a function
        >>> at.PCMD(at.PCMD.Flags.progressive, gaz=0.8)
        PCMD(flag=at.PCMD.Flags.progressive, roll=0.0, pitch=0.8, gaz=0.0, yaw=0.0)

Packing an *ATCommand*
~~~~~~~~~~~~~~~~~~~~~~

*ATCommand.pack* can be used to pack the command into *bytes*, if you want to manipulate it manually (you don't have to do this):

* *pack* takes an optional argument seq (sequence number), which defaults to ``'SEQUNSET'``

        >>> cmd.pack()
        b'AT*PCMD=SEQUNSET,2,0,1061997773,0,0\r'
        >>> cmd.pack(100)
        b'AT*PCMD=100,2,0,1061997773,0,0\r'

Sending an *ATCommand*
~~~~~~~~~~~~~~~~~~~~~~

To send a AT\*PCMD command with the progressive flag and vertical speed = 0.8, use the following:

    .. code-block:: python3

        >>> # drone is an ARDrone instance here
        >>> drone.send(at.PCMD(at.PCMD.Flags.progressive, 0, 0.8, 0, 0))

The library provides the sequence number for the *pack()* function automatically.

Defining an *ATCommand* class
-----------------------------

If you want to use an *ATCommand* not defined in the library, you can define it yourself.

For example, to define a "AT*EXAMPLE" command with three arguments: number, speed, comment, which is a integer, a float, and a string respectively:

    .. code-block:: python

        from pyardrone.at.base import ATCommand
        from pyardrone.at.arguments imoprt Int32Arg, FloatArg, StringArg

        class EXAMPLE(ATCommand):

            number = Int32Arg(default=15)
            speed = FloatArg()
            comment = StringArg()

The created *EXAMPLE* class can then be used just like other ATCommand classes:

    .. code-block:: python

        >>> cmd = EXAMPLE(4, 3.5, 'nothing')
        >>> cmd
        EXAMPLE(number=4, speed=3.5, comment='nothing')
        >>> cmd.pack()
        b'AT*EXAMPLE=SEQUNSET,4,1080033280,"nothing"\r'
        >>> EXAMPLE(speed=6.7, comment='QAQ')
        EXAMPLE(number=15, speed=6.7, comment='QAQ')

ATCommand API
-------------

.. class:: ATCommand(*args, **kwargs)

    Base class of all *ATCommand*\ s

    .. method:: __eq__(other)

        Two *ATCommand*\ s are compared equal if:
            * They are of the same class

            * They have the same arguments

    .. method:: pack(seq='SEQUNSET')

        Pack the command into bytes for sockets.

    .. attribute:: parameters

        A list of *Arguments* of the command.

    .. attribute:: _args

        Dict of stored arguments.

.. class:: Argument(description=None, *, default=None)

    Base class of all arguments.

    *description* is stored, but has no effect.

    *default* is used to provide a default value for the argument for the *ATCommand*.

.. class:: Int32Arg(...)

.. class:: FloatArg(...)

.. class:: StringArg(...)

    .. staticmethod:: pack(value)

        Pack the value into bytes.
