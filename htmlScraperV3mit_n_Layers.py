import urllib.request
from bs4 import BeautifulSoup
import array as arr
import re

def scrapeLinks(url):
    linkArray = []

    open_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(open_page, "html.parser")
    #print(soup)

    mw_parser_output = soup.find_all(class_="mw-parser-output")

    for element in mw_parser_output:
        for a_tag in element.findAll('a', href=True):
            linkVar = a_tag['href']
            linkArray.append(linkVar)
    #print(linkArray)


    #verbotene Worte: Datei||Hilfe||Wikipedia||Spezial

    wantedLinks = set([link for link in linkArray if (("Datei:" not in link) & ("/wiki/" in link) & ("Hilfe:" not in link) & ("Wikipedia:" not in link) & ("Spezial:" not in link) & ("https:" not in link))])
    wantedLinksList = list(wantedLinks)
    #saveToTXT(wantedLinks)
    return wantedLinksList


def saveToTXT(wantedLinksList, topDoc):
    newTopDoc = re.sub('[^a-zA-Z0-9 \n\.]', '_', topDoc)
    with open(f'results/{newTopDoc}.txt', 'w') as temp_file:
            for item in wantedLinksList:
                temp_file.write("%s\n"                                                       % item)
                temp_file.close


#file = open('saveValues.txt', 'r')

def scrapeLinksNotOrdered(numberOfTimes, startLink):
    currentLinkArray = []
    previousLinkArray = []
    globalLinkArray = []
    previousLinkArray.append(startLink)
    globalLinkArray.append(startLink)
    for i in range(0, numberOfTimes):
         for i2 in range(0, len(previousLinkArray)):
              temp = scrapeLinks(previousLinkArray[i2])
              for i3 in range(0, len(globalLinkArray)):
                   if(globalLinkArray[i3] != temp):
                        previousLinkArray.append(temp)



layer1 = scrapeLinks("https://de.wikipedia.org/wiki/Chaos_Computer_Club")
#print(layer1)
for element in range(len(layer1)):
    saveToTXT(scrapeLinks(f"https://de.wikipedia.org{layer1[element]}"), layer1[element])
