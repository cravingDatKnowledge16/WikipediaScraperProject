import re
import numpy as np
import time
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

wc = WordCloud(width=1920, height=1080).generate(text)
plt.axis("off")
plt.imshow(wc, interpolation="bilinear")

zeitpunkt2 = time.perf_counter()
print(f"Dauer: {zeitpunkt2 - zeitpunkt1} sekunden")

plt.show()