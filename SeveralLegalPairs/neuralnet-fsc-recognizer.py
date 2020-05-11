# This script trains a simple neural net to distinguish First Species Counterpoint data from random notes.
# Average accuracy: 98%
#
# Created 2/25/2020 by Emily Wasylenko
# Modified 3/28/2020 by Emily Wasylenko

import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import h5py
import io

from __future__ import absolute_import, division, print_function, unicode_literals
#TODO: change these imports (next 3)
from keras.layers import Input, Dense, GaussianNoise
from keras.models import Model
from tensorflow import keras
from google.colab import files

print(tf.__version__)


#Load datasets and labels
uploaded = files.upload()
train_songs = pd.read_csv(io.BytesIO(uploaded['TrainDataSet.csv']), skiprows=1)
test_songs = pd.read_csv(io.BytesIO(uploaded['TestDataSet.csv']), skiprows=1)
train_labels = pd.read_csv(io.BytesIO(uploaded['TrainLabelsSet.csv']), skiprows=1)
test_labels = pd.read_csv(io.BytesIO(uploaded['TestLabelsSet.csv']), skiprows=1)


#Normalize data
divideNum = [18.0]
train_songs = np.divide(train_songs, divideNum)
test_songs = np.divide(test_songs, divideNum)


#Sanity check
print("train songs size:" + str(len(train_songs)) + str(train_songs.head()))
print("test songs size:" + str(len(test_songs)) + str(test_songs.head()))
print("train labels size:" + str(len(train_labels)) + str(train_labels.head()))
print("test labels size:" + str(len(test_labels)) + str(test_labels.head()))


#Build the net
a = Input(shape=(20,))
mid1 = Dense(30,activation='relu')(a)
b = Dense(1,activation='sigmoid')(mid1)
model = Model(inputs=a, outputs=b)

model.compile(optimizer='adam',
              #loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              loss=keras.losses.BinaryCrossentropy(),
              metrics=['accuracy'])

model.fit(train_songs, train_labels, epochs=20, verbose=1, shuffle=True)

test_loss, test_acc = model.evaluate(test_songs,  test_labels, verbose=1)
train_loss, train_acc = model.evaluate(train_songs,  train_labels, verbose=1)

print('\nTest accuracy:', test_acc)
print('\nTrain accuracy:', train_acc)


#Serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
    
#Serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

print(model_json)

json_file.close()
