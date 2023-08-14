Drone States
------------

.. module:: pyardrone.navdata.states

The ARDrone SDK 2.0.1 defines the following drone states in
``ARDroneLib/Soft/Common/config.h``

These states are presented as :class:`DroneState` attributes in the library.

.. autoclass:: DroneState

    .. autoattribute:: fly_mask

    .. autoattribute:: video_mask

    .. autoattribute:: vision_mask

    .. autoattribute:: control_mask

    .. autoattribute:: altitude_mask

    .. autoattribute:: user_feedback_start

    .. autoattribute:: command_mask

    .. autoattribute:: camera_mask

    .. autoattribute:: travelling_mask

    .. autoattribute:: usb_mask

    .. autoattribute:: navdata_demo_mask

    .. autoattribute:: navdata_bootstrap

    .. autoattribute:: motors_mask

    .. autoattribute:: com_lost_mask

    .. autoattribute:: software_fault

    .. autoattribute:: vbat_low

    .. autoattribute:: user_el

    .. autoattribute:: timer_elapsed

    .. autoattribute:: magneto_needs_calib

    .. autoattribute:: angles_out_of_range

    .. autoattribute:: wind_mask

    .. autoattribute:: ultrasound_mask

    .. autoattribute:: cutout_mask

    .. autoattribute:: pic_version_mask

    .. autoattribute:: atcodec_thread_on

    .. autoattribute:: navdata_thread_on

    .. autoattribute:: video_thread_on

    .. autoattribute:: acq_thread_on

    .. autoattribute:: ctrl_watchdog_mask

    .. autoattribute:: adc_watchdog_mask

    .. autoattribute:: com_watchdog_mask

    .. autoattribute:: emergency_mask

