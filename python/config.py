#!/usr/bin/python3

# training setup:
batch_size = 8
epoch = 50
image_size = (224, 224)
num_of_classes = 3

# pretrained classification model path
model_path = "/usr/local/pigeon-avoidance-system/python/models/"
model_name = "best_model_1.h5"

# path for the images taken
image_path = "/usr/local/pigeon-avoidance-system/images/"

# path for images that should to be removed
trash_path = "/usr/local/pigeon-avoidance-system/labeled/trash"

# images older then max_file_age will be removed
max_file_age = 7

# pin of a motion sensor
pin_motion = 23

# pins of the motor
motor_ports = [12,16,20,21]

# rotation time of a stepping motor
rotation_time = 10


