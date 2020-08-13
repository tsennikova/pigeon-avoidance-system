#!/usr/bin/python3

import RPi.GPIO as GPIO
import config
import time
from datetime import datetime
from math import sin

# set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# pins of the stepping motor
motor_ports = config.motor_ports

# setup GPIO ports as an output
for port in motor_ports:
    GPIO.setup(port, GPIO.OUT)


def stop_motor():
    """
    Stops rotation of the stepping motor
    :return:
    """

    global motor_ports

    for port in motor_ports:
        GPIO.output(port, 0)
    return


def rotate_motor(rotation_time):
    """
    Rotates the stepping motor
    :param: rotation_time - interval when motor is rotating in sec. type: int
    :return:
    """

    global motor_ports

    # drive_sequence = [[0],[0,1],[1],[1,2],[2],[2,3],[3],[3,0]] #indices of motor ports
    stop_motor()

    # define clockwise rotation sequence
    drive_sequence = [[0], [1], [2], [3]]
    current_position = 1
    drive_delay_ms = 20

    # define rotation angle
    # the lower the number, the bigger the angle
    drive_delay_arc_speed = 0.6

    start_time = datetime.now()
    delta_time = 0

    try:

        while delta_time < rotation_time:
            active_motor_indices = drive_sequence[current_position - 1]

            for port in range(len(motor_ports)):

                if port in active_motor_indices:
                    GPIO.output(motor_ports[port], 1)
                else:
                    GPIO.output(motor_ports[port], 0)

            if drive_delay_ms > 0:
                current_position += 1
            else:
                current_position -= 1

            if current_position > len(drive_sequence):
                current_position = 1
            if current_position == 0:
                current_position = len(drive_sequence)

            # drive delay automation part
            curr_time = datetime.now()
            delta_time = (curr_time - start_time).total_seconds()

            # we want to drive the motor nicely and smoothly to impress the pigeons
            drive_speed = sin(delta_time * drive_delay_arc_speed)

            drive_delay_ms = 2.0 # 50 is very slow and 2 is the fastest

            if drive_speed < 0:
                drive_delay_ms = drive_delay_ms * -1

            time.sleep(abs(float(drive_delay_ms)) / 1000.0)
        stop_motor()

    except KeyboardInterrupt:
        GPIO.cleanup()
    return


