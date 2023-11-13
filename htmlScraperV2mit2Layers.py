"""
RULES: 

1. variable-name definition: data about the value (optional: + "_" + function of the value)

2. create as few side-effects as possible 

3.1. comment above block: describe the function of the code-block

3.2. comment after the line: describe the function of the line (for details)

"""


import urllib.request
from bs4 import BeautifulSoup
import array as arr
import re
import datetime

from numpy import iterable
#import highcharts



#url = "https://de.wikipedia.org/wiki/Chaos_Computer_Club"

def scrapeLinks(url):
    linkArray = []

    openPage = urllib.request.urlopen(url)
    soup = BeautifulSoup(openPage, "html.parser")
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
    newTopDoc = re.sub(r'[^a-zA-Z0-9 \n\.]', '_', topDoc)
    with open(f'results/{newTopDoc}.txt', 'w') as tempFile:
            for item in wantedLinksList:
                tempFile.write("%s\n"                                                       % item)
                tempFile.close()

def extractLinksRecursivly(startElement,forEachElFunc,layerDepth=False):
    #extracts the sublinks of a Wikipedia-link recusively
        currLayAllKeys_knowParentKeys = list()
        HREFmatrix_writeSublinks = list()
        mainDict = dict()
        mainDict["0"] = startElement
        
        for currLayer in range(layerDepth): #for every layer do:
            mainDictItems = [list(item) for item in list(mainDict.items())]
            currLayAllItems_knowItemParents = [item for item in mainDictItems if (extractNumberAmount(item[0]) == currLayer+1)]
            currLayAllKeys_knowParentKeys = [item[0] for item in currLayAllItems_knowItemParents]
            #scrape the links from the previous layer and write them onto a temporary matrix
            HREFmatrix_writeSublinks = [forEachElFunc(mainDict[preEl]) for preEl in currLayAllKeys_knowParentKeys]
            #copy all links from current layer onto the main dictionairies 
            for currLayKeyIndex in range(len(currLayAllKeys_knowParentKeys)):
                for nextLayPos in HREFmatrix_writeSublinks[currLayKeyIndex]:
                    mainDict[f"{currLayAllKeys_knowParentKeys[currLayKeyIndex]},{nextLayPos}"] = HREFmatrix_writeSublinks[currLayKeyIndex][nextLayPos]
            #eliminate all duplicates to avoid infinite recursion        
            for mainDictItem in list(mainDict.items()):
                mainDictItemCount = list(mainDict.values()).count(mainDictItem[1])
                if(mainDictItemCount >= 2): #if a value occurs more than 2 times
                    toPopList = [i for i, x in enumerate(currLayAllKeys_knowParentKeys) if x == mainDictItem[0]]
                    for elToPop in toPopList:
                        mainDict.pop(elToPop)
        return mainDict

                
def extractNumberAmount(text):
    allNumbers = re.findall(r"\d+",str(text))
    return len(allNumbers)

def listToString(list):
    return re.sub(r"[\s\[\]]","",str(list))
print(listToString(list((1,98,28,"njue"))))
#file = open('saveValues.txt', 'r')
obj = list((9,18,28))
print([el for el in enumerate(obj)])

#layer1 = scrapeLinks("https://de.wikipedia.org/wiki/Chaos_Computer_Club")
#print(layer1)
#for element in range(len(layer1)):
#    saveToTXT(scrapeLinks(f"https://de.wikipedia.org{layer1[element]}"), layer1[element])

fruits = ["0","0,0","0,1"]
newlist = fruits.sort()

print(newlist)
"""
print(extractNumberAmount("9079,083,9,1542,23"))
for x in obj:
    print(x)
#extractFromDictRecursivly("hoirhoifh",2)
"""
