# ~ RULE-BASED FIRST SPECIES COUNTERPOINT GENERATOR ~
#
# This script generates musical data in the style of First Species Counterpoint (FSC).
# FSC is comprised of note pairs, called intervals: (counterpoint, cantus firmus).
# Cantus firmus = cf, counterpoint = cp
#
# Each interval is held for 4 beats, and should follow standard FSC style guidelines. 
# Each song is 10 notes long, all naturals, limited to C Major. 
#
# Created 2/8/2020 by Emily Wasylenko


import random
from random import choice


#The CounterNoteLookup dictionary maps CF notes to all viable CPs.
#Comments show the note and octave corresponding to the map key (for example, 7 = Middle C = C4). There's a music pun in there somewhere.
CounterNoteLookup = dict([ 
                 (4, [0,2]),                  #G3
                 (5, [0,3]),                  #A4
                 (6, [1,2,4]),                #B4
                 (7, [0,2,3,5]),              #C4
                 (8, [1,3,4,6]),              #D4
                 (9, [0,2,4,7]),              #E4
                 (10, [1,3,5,8]),             #F4
                 (11, [0,2,4,6,7,9]),         #G4
                 (12, [0,1,3,5,7,8,10]),      #A5
                 (13, [1,2,4,6,8,9,11]),      #B5
                 (14, [2,3,5,7,9,10,12]),     #C5
                 (15, [3,4,6,8,10,11,13]),    #D5
                 (16, [4,5,7,9,11,12,14]),    #E5
                 (17, [5,8,10,12,13,15]),     #F5
                 (18, [6,7,9,11,13,14,16])])  #G5


# Generate all valid options for the current note pair, given the current CF and the previous two intervals.
# Returns: Int
def getCounterpoint(cf, prevInterval, prevPrevInterval):
  counterpointBlacklist = []

  #repeated note check
  counterpointBlacklist.append(prevInterval[0])

  #fifth check
  if((prevInterval[1]-prevInterval[0])>=4):
    counterpointBlacklist.append(cf+4)
    counterpointBlacklist.append(cf-4)

  #octave check
  if((prevInterval[1]-prevInterval[0])>=7):
    counterpointBlacklist.append(cf-7)
    counterpointBlacklist.append(cf+7)

  #parallel motion to fifth/octave check
  #parallel upward motion
  if(cf-prevInterval[1] > 0):
    if(prevInterval[0]<(cf-7)):
      counterpointBlacklist.append(cf-7)
    if(prevInterval[0]<(cf-4)):
      counterpointBlacklist.append(cf-4)
  #parallel downward motion
  elif(cf-prevInterval[1] < 0):
    if(prevInterval[0]>(cf-7)):
      counterpointBlacklist.append(cf-7)
    if(prevInterval[0]>(cf-4)):
      counterpointBlacklist.append(cf-4)

  #large leap going up check
  slope=prevInterval[0]-prevPrevInterval[0]
  if(slope>0 & (abs(slope)>=4)):
    for i in range(prevInterval[0]+4,19):
      counterpointBlacklist.append(i)

  #large leap going down check
  if(slope<0 & (abs(slope)>=4)):
    for i in range(0,prevInterval[0]-3):
      counterpointBlacklist.append(i)

  #find set difference of possibleNotes and BlackList
  possibleCpNotes = list(set(CounterNoteLookup[cf]) - set(counterpointBlacklist))

  if len(possibleCpNotes) == 0:
    #There is no valid pairing
    cp = -1
  else:
    #Randomly choose one of the valid pairings
    cp = possibleCpNotes[random.randrange(0, len(possibleCpNotes))]

  return cp


# Helper dictionaries for first interval.
CFNoteLookup = [7,14]
CPNoteLookup = [0,7,14]

# Choose a valid CF for the first interval.
# Returns: Int
def findValidCF():
  index = random.randrange(0,2)
  return CFNoteLookup[index]

# Choose a valid CP for the first interval.
# Returns: Int
def findValidCounterpoint():
  index = random.randrange(0,3)
  return CPNoteLookup[index]


# This function generates FSC data.
# Returns: a list of Pairs: [(Int, Int)]
# TODO: clean it up, put CF blacklisting into its own function.
def musicGenerator():

  #song, array(pair), holds all intervals as pairs (cp, cf)
  song = []

  #cfBlackList, array(Int), holds all currently illegal cf notes
  cfBlackList = []
  
  #add first note
  cp = findValidCounterpoint()
  cf = findValidCF()
  song.append((cp, cf))

  #generate the cantus firmus and obtain corresponding cp
  for i in range(1,9):
    prevInterval = song[i-1]

    #remove second to last CF note to prevent duplicates
    if(i>1):
      cfBlackList.append(song[i-2][1])
    
    #remove last CF note to prevent duplicates
    cfBlackList.append(prevInterval[1])
    
    if(len(song) >= 2):
      prevPrevInterval = song[i-2]
    else:
      prevPrevInterval = (0,0)

    #remove melodic tritones 
    if((prevInterval[1] == 3) | (prevInterval[1] == 10) | (prevInterval[1] == 17)):
      cfBlackList.append(6)
      cfBlackList.append(13)
    elif((prevInterval[1] == 6) | (prevInterval[1] == 13)):
      cfBlackList.append(3)
      cfBlackList.append(10)
      cfBlackList.append(17)

    cf = choice([j for j in range(4,18) if j not in cfBlackList])
    cp = getCounterpoint(cf, prevInterval, prevPrevInterval)    

    #failure case
    if(cp == -1):
      return -1
    
    song.append((cp, cf))

    #reset blacklist
    cfBlackList = []
    
  #Last counterpoint note must be tonic or tonic 3rd - choose tonic 3rd because it sounds pretty
  song.append((14, 9))
    
  return song


# Write music information to file
f = open("Datasets/SongPairs.csv","w+")
failedCount = 0
numSongsToGenerate = 1000

for j in range(0, numSongsToGenerate):
  song = musicGenerator()
  if (song == -1):
    failedCount = failedCount+1
  else:
    for i in range(0, len(song)):
      f.write(str(song[i][0]) + "~" + str(song[i][1]))
      f.write(",")
    f.write("\n")
f.close()
print("Fail rate: ",failedCount,"/",numSongsToGenerate,"=",failedCount/numSongsToGenerate)




# BELOW: JUST FOR FUN 


#This dictionary maps notes (0 -> 18) to their corresponding MIDI tones (48 -> 79). Useful for listening to the songs.
NoteToMIDITone = {
    0: 48,  #C3
    1: 50,  #D3
    2: 52,  #E3
    3: 53,  #F3
    4: 55,  #G3
    5: 57,  #A4
    6: 59,  #B4
    7: 60,  #C4
    8: 62,  #D4
    9: 64,  #E4
    10: 65, #F4
    11: 67, #G4
    12: 69, #A5
    13: 71, #B5
    14: 72, #C5
    15: 74, #D5
    16: 76, #E5
    17: 77, #F5
    18: 79  #G5
}


# Print a song in MIDI format
# Returns: nothin
def convertToMIDI(song):
  cfToMIDI = [i[0] for i in song]
  cntrptToMIDI = [i[1] for i in song]
  for i in range(0,10):
    print("[" + str(2*i) + ", " + str(NoteToMIDITone[cfToMIDI[i]]) + ", 127, 4],")
    print("[" + str(2*i) + ", " + str(NoteToMIDITone[cntrptToMIDI[i]]) + ", 127, 4],")

