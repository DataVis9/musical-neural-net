# ~ TRAIN/TEST DATA PRINTER FOR RECOGNIZER ~
#
# This script prints data to the train/test files (currently set up for test data).
# Data is comprised of 10-interval songs.
# Roughly half are valid FSCs, the other are random notes.
# Each song has its corresponding label printed to the label file:
#   Valid FSC >> 1
#   Random song >> 0
#
# Created 2/25/2020 by Emily Wasylenko
# Modified 3/29/2020 by Emily Wasylenko



import random
from linereader import getline

# Init files
inputFilePath = "Datasets/SongPairs.csv"
outputDataFilePath = "Datasets/TestDataSet.csv"
outputLabelsFilePath = "Datasets/TestLabelsSet.csv"

fgood = open(inputFilePath, "r")
fprintData = open(outputDataFilePath, "w+")
fprintLabels = open(outputLabelsFilePath, "w+")

# Set variables
goodSongIndex = 0
numDataPoints = 10000
numLinesInFile = 90000

# Generate data points, randomized so roughly 50% are valid FSCs 
for i in range(0, numDataPoints):
    indicator = random.randrange(0,2)
    if (indicator == 1):

        # Generate a good song
        lineReader=fgood.readlines()
        filename = "Datasets/SongPairs.csv"
        line = getline(filename, (numLinesInFile - goodSongIndex))
        notes = line.split(",")

        # Go through all pairs in the line
        for pair in notes:
            if(pair!="\n"):
                cp = int(pair.split("~")[0])
                cf = int(pair.split("~")[1])
                fprintData.write(str(cp) + "," + str(cf) + ",")
        fprintData.write("\n")
        fprintLabels.write("1\n")
        goodSongIndex = goodSongIndex+1

        # If index exceeds current line in valid data file, start over (impossible, but just in case)
        if(goodSongIndex == numLinesInFile):
            goodSongIndex = 0
    else:
        #generate a bad song
        for j in range(0, 20):
            fprintData.write(str(random.randrange(0,19)) + ",")
        fprintData.write("\n")
        fprintLabels.write("0\n")

fprintData.close()
fprintLabels.close()
