# ~ GENERATE SONGS WITH TRAINED MODEL ~
#
# Net model is fed two intervals and outputs the following third interval to a file.
# It outputs the 8 middle intervals of a song. First and last note are added manually.
#
# Created 2/25/2020 by Emily Wasylenko
# Modified 4/14/2020 by Emily Wasylenko


#generator based on imported Model
from __future__ import absolute_import, division, print_function, unicode_literals
import h5py
import io
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import io
import csv
from google.colab import files
uploaded = files.upload()

#setup
validPairs=[(0,4),(0,5),(0,7),(0,9),(0,11),(0,12),          
            (1,6),(1,8),(1,10),(1,12),(1,13),               
            (2,4),(2,6),(2,7),(2,9),(2,11),(2,13),(2,14),   
            (3,5),(3,7),(3,8),(3,10),(3,12),(3,14),(3,15),  
            (4,6),(4,8),(4,9),(4,11),(4,13),(4,15),(4,16),  
            (5,7),(5,10),(5,12),(5,14),(5,16),(5,17),       
            (6,8),(6,11),(6,13),(6,15),(6,18),
            (7,9),(7,11),(7,12),(7,14),(7,16),(7,18),
            (8,10),(8,12),(8,13),(8,15),(8,17),
            (9,11),(9,13),(9,14),(9,16),(9,18),
            (10,12),(10,14),(10,15),(10,17),
            (11,13),(11,15),(11,16),(11,18),
            (12,14),(12,16),(12,17),
            (13,15),(13,17),(13,18),
            (14,16),(14,18),
            (15,17),
            (16,18)]

##this will return the list of input numbers
def prepare(input_arr):
  divideNum = [18.0]
  input_arr = np.divide(input_arr, divideNum)
  newArray = np.reshape(input_arr, (1,4))
  return newArray


#Reading the model from JSON file
with open('model3.json', 'r') as json_file:
    json_savedModel= json_file.read()
#load the model architecture 
model = tf.keras.models.model_from_json(json_savedModel)
model.summary()

#read first 4 notes in
InputIntervals = pd.read_csv(io.BytesIO(uploaded['InputIntervals.csv']), skiprows=0)

#open file we will write to
with open('data.csv', mode='w') as songFile:
    songWriter = csv.writer(songFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#loop through all intros
for j in range(0, InputIntervals.shape[0]):
  #inputNotes = the intervals of each song we generate. The 4 most recently generated are fed into net.
  inputNotes = []
  for note in InputIntervals.values.tolist()[j]:
    inputNotes.append(note)

  #create 8 middle intervals of a song
  for k in range(0, 7):
    #Generate prediction based on previous 4 notes
    prediction = model.predict(prepare(inputNotes[(2*k):(2*k)+4]))

    #format data to find the max 
    listy = np.array2string(prediction[0]).split()

    intervals = []
    for i in range(1, len(listy) - 1):
      intervals.append(listy[i])

    maxNum = max(intervals)
    maxIndex = intervals.index(maxNum)

    outputInterval = validPairs[maxIndex]
    inputNotes.append(outputInterval[0])
    inputNotes.append(outputInterval[1])

  #last note is manually generated
  inputNotes.append(9)
  inputNotes.append(14)

  #Write notes to file
  #songWriter.writerow(inputNotes)  
  for t in range(0, len(inputNotes)):
    print(inputNotes[t],end='')
    print(",",end='')
  print("")

  inputNotes = []
