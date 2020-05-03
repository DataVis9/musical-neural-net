# ~ WRITE DATA TO TRAIN FSC GENERATOR ~
#
# Print prompting two intervals and the following third interval to a file.
# This will train the net to distinguish the best FSC interval to output given any two inputs.
#
# Created 2/25/2020 by Emily Wasylenko
# Modified 4/14/2020 by Emily Wasylenko


validPairs=[(0,4),(0,5),(0,7),(0,9),(0,11),(0,12),          #6
            (1,6),(1,8),(1,10),(1,12),(1,13),               #11
            (2,4),(2,6),(2,7),(2,9),(2,11),(2,13),(2,14),   #18
            (3,5),(3,7),(3,8),(3,10),(3,12),(3,14),(3,15),  #25
            (4,6),(4,8),(4,9),(4,11),(4,13),(4,15),(4,16),  #32
            (5,7),(5,10),(5,12),(5,14),(5,16),(5,17),       #etc
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

#[String => List(Pair)]
InputMap = dict([])

#Print them 2 intervals at a time, saving the 3rd interval
f=open("Datasets/SongPairs.csv", "r")
fTrainDataPrint=open("Datasets/GeneratorsTrainData.csv", "w+")
fTrainLblPrint=open("Datasets/GeneratorsTrainLabels.csv", "w+")
fTestDataPrint=open("Datasets/GeneratorsTestData.csv", "w+")
fTestLblPrint=open("Datasets/GeneratorsTestLabels.csv", "w+")

f1 = f.readlines()

#Read through every line in file
for line in f1:
    notes = line.split(",")
    #Read through each pair in the line
    for index, pair in enumerate(notes, start=0):
        #Start at index=2 to guarantee a 2-interval, 4-note pattern
        if(2 <= index <= 8) & (pair!="\n"):
            
            #get the previous 2 interval pairs (The last 4 notes)
            prevPrevCP = int((notes[index-2]).split("~")[0])
            prevPrevCF = int((notes[index-2]).split("~")[1])
            prevCP = int((notes[index-1]).split("~")[0])
            prevCF = int((notes[index-1]).split("~")[1])

            #Concat these 4 notes into a key: String
            fourNoteKey = str(prevPrevCP) + str(prevPrevCF) + str(prevCP) + str(prevCF)

            #get the current pair
            cp = int(pair.split("~")[0])
            cf = int(pair.split("~")[1])

            #determine value index
            valueIndex = validPairs.index((cp,cf))

            #if it's not in map, add it as 1, make all others 0
            if fourNoteKey not in InputMap.keys():
                InputMap[fourNoteKey] = []
                for i in range(0, 77):
                    if(i!=valueIndex):
                        InputMap[fourNoteKey].append(0)
                    else:
                        InputMap[fourNoteKey].append(1)
            else:
                #SUM OPTION: Get sum of all data points : Increment corresponding value (pair index) to key in map
                InputMap[fourNoteKey][valueIndex] = InputMap[fourNoteKey][valueIndex]+1

                """
                BINARY OPTION, set all pairs seen to 0.99 :
                InputMap[fourNoteKey][valueIndex] = 0.99
                """

#read through file again, printing keys to data file and values to label file
unfound = 0
f=open("Datasets/SongPairs.csv", "r")
f2 = f.readlines()

for overallIndex, line in enumerate(f2, start=0):
    notes = line.split(",")
    
    for index, pair in enumerate(notes, start=0):
        if(2 <= index <= 8) & (pair!="\n"):
            #get the last 2 interval pairs (The last 4 notes)
            prevCP = int((notes[index-1]).split("~")[0])
            prevCF = int((notes[index-1]).split("~")[1])
            cp = int(pair.split("~")[0])
            cf = int(pair.split("~")[1])

            #save notes to string, print to data file
            fourNoteKey = str(prevPrevCP) + str(prevPrevCF) + str(prevCP) + str(prevCF)

            #print data
            
            if(overallIndex < 19000):
                fTestDataPrint.write(str(prevCP) + ","
                             + str(prevCF) + ","
                             + str(cp) + ","
                             + str(cf) + "\n")
            else:
                fTrainDataPrint.write(str(prevCP) + ","
                             + str(prevCF) + ","
                             + str(cp) + ","
                             + str(cf) + "\n")
            """
            fTestDataPrint.write(str(prevCP) + ","
                             + str(prevCF) + ","
                             + str(cp) + ","
                             + str(cf) + "\n")
            """
            #print labels
            """
            if fourNoteKey not in InputMap.keys():
                unfound = unfound+1

                for i in range(0, 77):
                    if(overallIndex<5000):
                        fTestLblPrint.write(str(0) + ",")
                    elif(5000 <= overallIndex < 20000):
                        fTrainLblPrint.write(str(0) + ",")
            else:
                value = InputMap[fourNoteKey]

                for v in value:
                    if(overallIndex<5000):
                        fTestLblPrint.write(str(v) + ",")
                    elif(5000 <= overallIndex < 20000):
                        fTrainLblPrint.write(str(v) + ",")
            if(overallIndex<5000):
                fTestLblPrint.write("\n")
            elif(5000 <= overallIndex < 20000):
                fTrainLblPrint.write("\n")
                """
            if fourNoteKey not in InputMap.keys():
                unfound = unfound+1
                if(overallIndex < 19000):
                    for i in range(0, 77):
                        fTestLblPrint.write(str(0) + ",")
                    fTestLblPrint.write("\n")
                else:
                    for i in range(0, 77):
                        fTrainLblPrint.write(str(0) + ",")
                    fTrainLblPrint.write("\n")
            else:
                value = InputMap[fourNoteKey]
                if(overallIndex < 19000):
                    for v in value:
                        fTestLblPrint.write(str(v) + ",")
                    fTestLblPrint.write("\n")
                else:
                    for v in value:
                        fTrainLblPrint.write(str(v) + ",")
                    fTrainLblPrint.write("\n")
        
print(unfound)
fTestDataPrint.close()
fTestLblPrint.close()
fTrainDataPrint.close()
fTrainLblPrint.close()
