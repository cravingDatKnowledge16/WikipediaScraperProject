import re
import numpy as np
import time
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import urllib.request
from bs4 import BeautifulSoup
import ssl

zeitpunkt1 = time.perf_counter()

url = input("Link eingeben: ")

SSLnoverify = ssl._create_unverified_context()
openPage = urllib.request.urlopen(url,context=SSLnoverify)
preText = BeautifulSoup(openPage, "html.parser")

print(type(preText))

# Extrahiere den Text aus dem ResultSet-Objekt
text = ""
for element in preText:
    print(f"element {len(element)}")
    text += element.get_text()
    

# Entferne unerwünschte Zeichen
text = re.sub(r"[^a-zA-Z0-9 äöüÄÖÜ]", "", text)

wc = WordCloud(width=3840, height=2160, background_color = "white", colormap = "magma").generate(text)
plt.axis("off")
plt.imshow(wc, interpolation="bilinear")

zeitpunkt2 = time.perf_counter()
print(f"Dauer: {zeitpunkt2 - zeitpunkt1} sekunden")


plt.show()