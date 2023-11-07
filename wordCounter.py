import re
import numpy as np
import time

#

zeitpunkt1 = time.perf_counter()
#1. Text lesen, bei jedem Leerzeichen neuen Array Punkt erstellen
with open('test.txt', 'r') as file:
    text = file.read()
#text = ""
#text = input("Text eingeben: ")
wordArray = text.split()
finalWordArray = []
for i in range (0, len(wordArray)):
    finalWordArray.append(re.sub(r"[^a-zA-Z0-9 äöüÄÖÜ]", "", wordArray[i]))

# 2. Matrix erstellen, in der je die Zahl und dann das Wort steht.
# Bei jedem hinzufügen eines Wortes wird geschaut, ob dieses schon in der Matrix ist.
#  a) schon in der Matrix
#     Das Wort wird gefunden und die Zahl wird um 1 erhöht
#  b) noch nicht in der Matrix
#     Das Wort wird der Matrix hinzugefügt und die Zahl wird auf 1 gesetzt
anzahlDerVergleiche = 0
wordMatrix = []
#für jedes Wort
for i1 in range (0, len(finalWordArray)):
    #für jedes Wort in der Wortmatrix
    trigger = False
    matrixIndex = 0
    for i2 in range (0, len(wordMatrix)):
        anzahlDerVergleiche +=1
        if finalWordArray[i1] == wordMatrix[i2][1]:
            trigger = True
            matrixIndex = i2
    if trigger == True:
        wordMatrix[matrixIndex][0] += 1
    else:
        wordMatrix.append([1,finalWordArray[i1]])

sortedWordMatrix = sorted(wordMatrix, key=lambda x: x[0], reverse=True)

print("ERGEBNIS:")
for i in range(0, 50):
    print(f"{sortedWordMatrix[i][0]} x {sortedWordMatrix[i][1]}")

#print(wordMatrix)

zeitpunkt2 = time.perf_counter()
print(f"Dauer: {zeitpunkt2 - zeitpunkt1} sekunden | Anzahl der Operationen: {anzahlDerVergleiche}")