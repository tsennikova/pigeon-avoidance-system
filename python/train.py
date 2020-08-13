#!/usr/bin/python3

import config
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.vgg19 import VGG19
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.optimizers import SGD
from tensorflow.keras.applications.vgg19 import preprocess_input
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.models import load_model

# For MAC OS, comment next 2 lines to run the script on Windows or Linux machine
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'


def define_model(num_of_classes):
    """
    Model Definition
    :param num_of_classes: number of classes to predict. type: int
    :return: compiled model
    """
    # load pretrained VGG19 with imagenet weights and without last layer
    model = VGG19(weights="imagenet",
                     include_top=False,
                     input_shape=(224, 224, 3))

    # freeze all the layers
    for layer in model.layers:
        layer.trainable = False

    # add new layers to the model
    flatten = Flatten()(model.layers[-1].output)
    classification = Dense(128, activation="relu")(flatten)
    dropout = Dropout(0.5)(classification)
    output = Dense(num_of_classes, activation="softmax")(dropout)
    model = Model(inputs=model.inputs, outputs=output)

    opt = SGD(lr=0.0001, momentum=0.9)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
    return model


def fit_model(model_1, train, val, epoch, steps, model_path, model_name):
    """
    Fit the configured model
    :param model_1: compiled Keras model
    :param train: training iterator. type: Iterator
    :param val: validation iterator. type: Iterator
    :param epoch: number of times the models sees the full dataset. type: int
    :param steps: number of image batches in a single epoch. type: int
    :param model_path: path to store the model. type: str
    :param model_name: file name for the model to store
    :return: history of the training. type: history object
    """
    es = EarlyStopping(monitor='accuracy', mode='max', verbose=1, patience=200)
    mc = ModelCheckpoint(model_path+model_name, monitor='val_loss', mode='min', verbose=1, save_best_only=True)
    print(">> Fiting the last layer")

    history = model_1.fit(x=train,
                        steps_per_epoch=steps,
                        validation_data=val,
                        epochs=epoch,
                        validation_steps=4,
                        verbose=1,
                        callbacks=[es, mc])
    return history


def run():
    """
    Reads the image data from the trainig directory specified in config.py: train_path, val_path.
    Preprocess data using fromat expected by ResNet50 via keras.applications.resnet50 preprocess_input.
    Creates iterators with the batch size specified in config.py.
    Runs fit_model method.
    :return:
    """
    model_name = 'best_model_1.h5'
    batch_size = config.batch_size
    epoch = config.epoch
    train_path = config.train_path
    val_path = config.validation_path
    model_path = config.model_path
    image_size = config.image_size
    num_of_classes = config.num_of_classes

    # create a data generators for training and test datasets,
    # keep it separate in case of augumentation of the training data
    train_datagen = ImageDataGenerator(dtype='float32',
                                       preprocessing_function=preprocess_input)

    test_datagen = ImageDataGenerator(dtype='float32',
                                      preprocessing_function=preprocess_input)

    # load and iterate over training dataset
    train = train_datagen.flow_from_directory(train_path,
                                              class_mode="categorical",
                                              target_size=image_size,
                                              color_mode='rgb',
                                              batch_size=batch_size,
                                              shuffle=True)
    # load and iterate over validation dataset
    val = test_datagen.flow_from_directory(val_path,
                                           class_mode="categorical",
                                           target_size=image_size,
                                           color_mode='rgb',
                                           batch_size=batch_size,
                                           shuffle=True)

    # calculate how many batches of images defines a single epoch
    steps = int(train.samples) // batch_size

    # define a model architecture
    model = define_model(num_of_classes)

    # fit the model
    fit_model(model, train, val, epoch, steps, model_path, config.model_name)
    return

if __name__ == "__main__":
    run()