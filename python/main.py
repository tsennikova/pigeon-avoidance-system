#!/usr/bin/python3

import syslog


def logger(message):
    """
    Write status into a log file located in /var/log/messages
    :param message: Message to write into the log file. format: str
    :return:
    """
    syslog.syslog(message)
    print(message)
    return


logger("INFO: main.py started")

import RPi.GPIO as GPIO
import config
import time
from camera import take_pic
from stepping_motor import rotate_motor
import inference

# set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# pin of a motion sensor
pin_motion = config.pin_motion

# flag to check if the main pipeline is already running
pap_flag = 0

# rotation time of a stepping motor
rotation_time = config.rotation_time

# setup GPIO ports as an input
GPIO.setup(pin_motion, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# load the classification model
model = inference.load_pretrained_model()
logger("INFO: Model Loaded")


def motion():
    """
    Runs a motion detection for GPIO.RISING. Runs a main_pipeline as a callback function at the same time while
    motion detection.
    :return:
    """
    GPIO.add_event_detect(pin_motion,
                          GPIO.RISING,
                          callback=main_pipeline)
    return


def main_pipeline(port):
    """
    Runs main pipeline: motion -> take picture -> classify -> action if the input on pin_motion is raising high.
    :param port: pin of the motion sensor. In this case pin_motion. format: int
    :return:
    """
    global pap_flag

    logger("INFO: motion detected")

    if pap_flag:
        logger("WARNING: main_pipeline is already running")
        return

    pap_flag = 1
    img = take_pic()
    predicted_class = inference.predict(img, model)

    if predicted_class == 2:
        logger("INFO: pigeon detected")
        rotate_motor(rotation_time)
    if predicted_class == 0:
        logger("INFO: human detected")
        time.sleep(180)
    if predicted_class == 1:
        logger("INFO: no one detected")

    inference.save_image(img, predicted_class)
    pap_flag = 0

    return


# run a motion detection on the background
motion()
try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
