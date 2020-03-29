import random
from linereader import getline

# Open data/labels files
fgood = open("Datasets/SongPairs.csv", "r")
fprintData = open("Datasets/TestDataSet.csv", "w+")
fprintLabels = open("Datasets/TestLabelsSet.csv", "w+")

# Set variables
goodSongIndex = 0
numDataPoints = 10000
numLinesInFile = 90000

# Generate data points, randomized so roughly 50% are valid FSCs 
for i in range(0, numDataPoints):
    indicator = random.randrange(0,2)
    if (indicator == 1):

        #generate a good song
        lineReader=fgood.readlines()
        filename = "Datasets/SongPairs.csv"
        line = getline(filename, (numLinesInFile - goodSongIndex))
        notes = line.split(",")

        #Go through all pairs in the line
        for pair in notes:
            if(pair!="\n"):
                cp = int(pair.split("~")[0])
                cf = int(pair.split("~")[1])
                fprintData.write(str(cp) + "," + str(cf) + ",")
        fprintData.write("\n")
        fprintLabels.write("1\n")
        goodSongIndex = goodSongIndex+1
        if(goodSongIndex == 59000):
            goodSongIndex = 0
    else:
        #generate a bad song
        for j in range(0, 20):
            fprintData.write(str(random.randrange(0,19)) + ",")
        fprintData.write("\n")
        fprintLabels.write("0\n")

fprintData.close()
fprintLabels.close()
