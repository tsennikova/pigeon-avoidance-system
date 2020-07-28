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

import config
import numpy as np
import time
import os

from keras.models import load_model
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array


def load_image(filename):
    """
    Loads images taken by the camera when the motion was detected.
    :param filename: image path. type: str
    :return: img: image converted into array. type: 3D Numpy array of float32.
    """
    start_time = time.time()
    img = load_img(filename, target_size=config.image_size) # convert to array
    img = img_to_array(img)
    img = img.astype('float32')
    runtime = time.time() - start_time
    logger("INFO: Loading image took " + str(runtime) + "s to run")
    return img


def load_pretrained_model():
    """
    Loads pretrained calssification model.
    :return: pretrained model type: h5
    """
    return load_model(config.model_path + config.model_name)


def save_image(image_path, predicted_class):
    """
    Adds a class name to the original image and stores it in image_path
    :param image_path: path of the original image. type: str
    :param predicted_class: predicted class. type: int
    :return:
    """
    if predicted_class == 0:
        os.rename(image_path, image_path + '_human.jpg')
    if predicted_class == 1:
        os.rename(image_path, image_path + '_nothing.jpg')
    if predicted_class == 2:
        os.rename(image_path, image_path + '_pigeon.jpg')
    return


def predict(image_path, model):
    """
    Loads image, preprocesses it in the same way as the images in the training loop, generates a prediction.
    :param image_path: path of the original image. type: str
    :param model: pretrained model. type: h5
    :return: predicted class type: int
    """
    start_time = time.time()
    image = load_image(image_path)
    image = np.expand_dims(image, axis=0)
    image = image.astype(float)
    image = preprocess_input(image)
    scores = model.predict(image)
    runtime = time.time() - start_time
    logger("INFO: Prediction took " + str(runtime) + "s to run")
    return np.argmax(scores)

