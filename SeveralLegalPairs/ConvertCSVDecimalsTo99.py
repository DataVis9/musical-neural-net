f=open("Datasets/GeneratorsTestLabels.csv", "r")
fprint=open("BinaryDatasets/GeneratorsTestLabels.csv", "w+")
fread=f.readlines()
for line in fread:
    notes = line.split(",")
    for note in notes:
        if (note=='0'):
            fprint.write(str(0)+",")
        else:
            fprint.write(str(0.99)+",")
    fprint.write("\n")


f2=open("Datasets/GeneratorsTrainLabels.csv", "r")
fprint2=open("BinaryDatasets/GeneratorsTrainLabels.csv", "w+")
fread2=f2.readlines()
for line in fread2:
    notes = line.split(",")
    for note in notes:
        if (note=='0'):
            fprint2.write(str(0)+",")
        else:
            fprint2.write(str(0.99)+",")
    fprint2.write("\n")


fprint.close()
fprint2.close()
