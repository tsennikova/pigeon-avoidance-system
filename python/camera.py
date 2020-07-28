#!/usr/bin/python3

import config
from picamera import PiCamera
from datetime import datetime

# initialise camera
camera = PiCamera()

# my camera is flipped, therefore I need to rotate the images
camera.rotation = 180

# get path to store images from the configuration file
image_path = config.image_path


def take_pic():
	"""
	Takes pictures if motion was detected and stores it in img_path specified in config.py. With the name
	"%m-%d-%Y-%H-%M-%S.jpg"
	:return: image_path Name and location of the image. format: str
	"""
	now = datetime.now()
	current_time = now.strftime("%m-%d-%Y-%H-%M-%S")
	camera.start_preview()
	img_path = image_path + "img-" + current_time + ".jpg"
	camera.capture(img_path)
	camera.stop_preview()
	return img_path


