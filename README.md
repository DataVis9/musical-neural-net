# musical-neural-net
A rule-based system that generates musical data in the style of First Species Counterpoint (FSC), a neural net trained to recognize FSC, and a neural net trained to generate its own FSC.

# How to run:
0. Use the stuff in the SeveralLegalPairs directory
1. Run `rulebased-fsc-generator.py` to print data to SongPairs.csv
2. Run `write-data-for-nn-generator.py` to 
    - print training data to GenerateTrainData.csv
    - print testing data to GenerateTestData.csv
    - print training labels to GenerateTrainLabels.csv
    - print testing labels to GenerateTestLabels.csv
3. Make a new Notebook in Google Colab: https://colab.research.google.com/
3. Copy code in `generator-trainer.py` and paste it into your Google Colab notebook
4. Click the triangle to run the neural net. Scroll down until you see an upload prompt. Use it to upload the needed files, located in .../SeveralLegalPairs/Datasets
    - GenerateTrainData.csv
    - GenerateTestData.csv
    - GenerateTrainLabels.csv
    - GenerateTestLabels.csv
