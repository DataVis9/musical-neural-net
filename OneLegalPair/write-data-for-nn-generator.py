# ~ WRITE DATA TO TRAIN FSC GENERATOR ~
#
# Print prompting two intervals and the following third interval to a file.
# This will train the net to distinguish the best FSC interval to output given any two inputs.
#
# Created 2/25/2020 by Emily Wasylenko
# Modified 4/14/2020 by Emily Wasylenko


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

#Print them 2 intervals at a time, saving the 3rd interval
f=open("Datasets/FSongPairs.csv", "r")
fprint=open("Datasets/GeneratorsTestData.csv", "w+")
LblPrint=open("Datasets/GeneratorsTestLabels.csv", "w+")
f1 = f.readlines()
for line in f1:
    notes = line.split(",")
    index = 0
    for pair in notes:
        if(index>0) & (pair!="\n") & (index <= 7):
            
            #get the last 2 intervals (The last 4 notes)
            prevCP = int((notes[index-1]).split("~")[0])
            prevCF = int((notes[index-1]).split("~")[1])
            cp = int(pair.split("~")[0])
            cf = int(pair.split("~")[1])
            fprint.write(str(prevCP) + ","
                         + str(prevCF) + ","
                         + str(cp) + ","
                         + str(cf) + "\n")
        if(index>=2) & (index<=8):

            #get the index of the resulting pair
            labelIndex = validPairs.index((cp,cf))
            for i in range(0, 77):
                if(i!=labelIndex):
                    LblPrint.write(str(0) + ",")
                else:
                    LblPrint.write(str(0.99) + ",")
            LblPrint.write("\n")
        index=index+1
fprint.close()
LblPrint.close()
