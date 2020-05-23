#a recognizer?! YESYESYESYESYES

#How many songs are actually FSC?



#Emily Wasylenko

import numpy as numpy
import itertools
# function takes a song, an array of pairs
# and tells whether or not it is in 1st species counterpoint form


FirstCPInvalid = 0
FirstCFInvalid = 0
repeats = 0
crossover = 0
unison = 0
second = 0
seventh = 0
parallelFifths = 0
parallelOctaves = 0
largeLeap = 0

validFSCs = 0


def recognizer(song):

    isFSC = True
    global FirstCPInvalid
    global FirstCFInvalid
    global repeats
    global crossover
    global unison
    global second
    global seventh
    global parallelFifths
    global parallelOctaves
    global largeLeap

    global validFSCs

    #test first cp
    if ((song[0][0] != 0) & (song[0][0] != 7) & (song[0][0] != 14)):
        isFSC = False
        FirstCPInvalid = FirstCPInvalid+1
    #test first cf
    if ((song[0][1] != 7) & (song[0][1] != 14)):
        isFSC = False
        FirstCFInvalid = FirstCFInvalid+1
    #test middle intervals
    for i in range(1, len(song)-1):
        #same consecutive pair
        if((song[i+1][0]==song[i-1][0]) & (song[i+1][1]==song[i-1][1])):
            isFSC = False
            repeats = repeats + 1
        if((song[i][0]==song[i-1][0]) & (song[i][1]==song[i-1][1])):
            isFSC = False
            repeats = repeats + 1
        #voice crossover (cp above cf)
        if(song[i][0]>song[i][1]):
            isFSC = False
            crossover = crossover + 1
        #unison 
        if((song[i][1]-song[i][0]) == 0):
            isFSC = False
            unison = unison + 1
        #second
        if((song[i][1]-song[i][0]) == 1):
            isFSC = False
            second = second + 1
        #seventh
        if((song[i][1]-song[i][0]) == 6):
            isFSC = False
            seventh = seventh + 1
        #parallel fifths
        if((song[i][1] - song[i][0] == 4) & (song[i-1][1]-song[i-1][0] == 4)):
            isFSC = False
            parallelFifths = parallelFifths + 1
        #parallel octaves
        if((song[i][1] - song[i][0] == 7) & (song[i-1][1]-song[i-1][0] == 7)):
            isFSC = False
            parallelOctaves = parallelOctaves + 1
        #large leap going up/down 
        if(i>=2):
            prevSlope = song[i-1][0] - song[i-2][0]
            slope = song[i][0] - song[i-1][0]
            if((numpy.sign(prevSlope)==numpy.sign(slope)) & (abs(song[i][0] - song[i-1][0])>=4) & (abs(song[i-1][0] - song[i-2][0])>=4)):
                #isFSC = False
                largeLeap = largeLeap + 1

    if(isFSC):
        validFSCs = validFSCs + 1
        print(list(itertools.chain(*song)))
    return isFSC



songs = []

fgood=open("Datasets/Book4.csv", "r")

lineReader=fgood.readlines()

for line in lineReader:
    notes = line.split(",")
    cp = 0
    cf = 0
    index = 0
    song = []
    for n in notes:    
        if( index%2==0) & (n!='\n'):
            cp = int(n)
        elif (index%2!=0)  & (n!='\n'):
            cf = int(n)
            song.append((cp, cf))
        index = index + 1
    songs.append(song)

for s in songs:
    recognizer(s)
        

print("FirstCPInvalid: ", FirstCPInvalid)
print("FirstCFInvalid: ", FirstCFInvalid)
print("repeats: ", repeats)
print("crossover: ", crossover)
print("unison: ", unison)
print("second: ", second) 
print("seventh: ", seventh)
print("parallelFifths: ", parallelFifths)
print("parallelOctaves: ", parallelOctaves)
print("largeLeap: ", largeLeap)
print("\nValid FSCs generated: ",validFSCs)
