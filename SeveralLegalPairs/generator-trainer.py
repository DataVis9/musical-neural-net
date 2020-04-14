from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.pyplot as plt
import tensorflow as tf
from tf import keras
import numpy as np
from keras.layers import Input, Dense, GaussianNoise
from keras.models import Model
import pandas as pd
import h5py
import io
from google.colab import files
uploaded = files.upload()
print(tf.__version__)

#Read in Data (4 note inputs) and Labels (77 item arrays of possible pair indices)
train_songs = pd.read_csv(io.BytesIO(uploaded['GenerateTrainData.csv']), skiprows=1)
test_songs = pd.read_csv(io.BytesIO(uploaded['GenerateTestData.csv']), skiprows=1)
train_labels = pd.read_csv(io.BytesIO(uploaded['GenerateTrainLabels.csv']), skiprows=1)
test_labels = pd.read_csv(io.BytesIO(uploaded['GenerateTestLabels.csv']), skiprows=1)

#Normalize data
divideNum = [18.0]
train_songs = np.divide(train_songs, divideNum)
test_songs = np.divide(test_songs, divideNum)

#Sanity check
print("train songs size:" + str(len(train_songs)) + str(train_songs.head()))
print("test songs size:" + str(len(test_songs)) + str(test_songs.head()))
print("train labels size:" + str(len(train_labels)) + str(train_labels.head()))
print("test labels size:" + str(len(test_labels)) + str(test_labels.head()))

#Build, compile, fit the model
a = Input(shape=(4,))
mid1 = Dense(30,activation='relu')(a)
b = Dense(77,activation='sigmoid')(mid1)
model = Model(inputs=a, outputs=b)

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(train_songs, train_labels, epochs=20, verbose=1, shuffle=True)

#Test accuracy
test_loss, test_acc = model.evaluate(test_songs,  test_labels, verbose=1)
train_loss, train_acc = model.evaluate(train_songs,  train_labels, verbose=1)

print('\nTest accuracy:', test_acc)
print('\nTrain accuracy:', train_acc)

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
    
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

#print model because i am a peasant and can't figure out how to save properly on google colab
print(model_json)

#close the file
json_file.close()


#end program
