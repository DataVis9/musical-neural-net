from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.layers import Input, Dense, GaussianNoise
from keras.models import Model
import pandas as pd
import h5py
import io
from google.colab import files
uploaded = files.upload()
import keras.backend as K

print(tf.__version__)

@tf.function
def euclidean_distance_loss(y_true, y_pred):
    """
    Euclidean distance loss
    https://en.wikipedia.org/wiki/Euclidean_distance
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    if(K.sqrt(K.sum(K.square(y_pred - y_true))) < 0):
      print("Returned Negative!")
      print("y_pred:",y_pred.eval())
      print("y_true:",y_true.eval())

    return K.sqrt(K.sum(K.square(y_pred - y_true)))

#Read in Data (4 note inputs) and Labels (77 item arrays of possible pair indices)
train_songs = pd.read_csv('https://github.com/DataVis9/musical-neural-net/blob/master/SeveralLegalPairs/Datasets/GeneratorsTrainData.csv'), skiprows=1)
test_songs = pd.read_csv('https://github.com/DataVis9/musical-neural-net/blob/master/SeveralLegalPairs/Datasets/GeneratorsTestData.csv'), skiprows=1)
train_labels = pd.read_csv('https://github.com/DataVis9/musical-neural-net/blob/master/SeveralLegalPairs/Datasets/GeneratorsTrainLabels.csv'), skiprows=1)
test_labels = pd.read_csv('https://github.com/DataVis9/musical-neural-net/blob/master/SeveralLegalPairs/Datasets/GeneratorsTestLabels.csv'), skiprows=1)


#Normalize data
divideNum = [18.0]
train_songs = np.divide(train_songs, divideNum)
test_songs = np.divide(test_songs, divideNum)

divideNum = [52.0]
train_labels = np.divide(train_labels, divideNum)
test_labels = np.divide(test_labels, divideNum)

#Kill extra last column
#train_labels = train_labels.drop(columns=[77])
#test_labels = test_labels.drop(columns=[77])
"""
zeroCount = 0.0
totalCount = 0.0
for (colName, colData) in train_labels.iteritems():
  for x in colData:
    totalCount = totalCount + 1
    if x == 0:
      zeroCount = zeroCount + 1
"""
#print("Total: " + str(totalCount) + ", Zeroes: " + str(zeroCount) + ", Fraction: " + str(zeroCount/totalCount))

#Sanity check
"""
print("train songs size:" + str(len(train_songs)) + "\n" + str(train_songs.head()) + "\n")
print("test songs size:" + str(len(test_songs)) + "\n" + str(test_songs.head()) + "\n")
print("train labels size:" + str(len(train_labels)) + "\n" + str(train_labels.head()) + "\n")
print("test labels size:" + str(len(test_labels)) + "\n" + str(test_labels.head()) + "\n")
"""
#Build, compile, fit the model
a = Input(shape=(4,))
mid1 = Dense(100,activation='relu')(a)
mid2 = Dense(50,activation='relu')(mid1)
b = Dense(77,activation='relu')(mid2)
model = Model(inputs=a, outputs=b)

#TODO: rerun with new data (using RELU or SOFTMAX. NOO sigmoid)
#TODO: make custom metrics - Recognizer - FINAL OUTPUT SHOULDN'T BE SIGMOID
model.compile(loss=euclidean_distance_loss, optimizer='adam', metrics=['categorical_accuracy'])
model.fit(train_songs, train_labels, epochs=5, verbose=1, shuffle=True)

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

print(model_json)

#close the file
json_file.close()


print("end program")
