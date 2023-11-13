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


def saveDictToTXT(dict, docName): 
    docName = re.sub(r"[\s\.,]", '', docName)
    dictKeys = [item[0] for item in list(dict.items())]
    dictValues = [item[1] for item in list(dict.items())]
    with open(f'results/{docName}.txt', 'w') as tempFile:
        for itemIndex in range(len(dict)):
            tempFile.write(f"  {dictKeys[itemIndex]} : {dictValues[itemIndex]}\n")

    
 
   

def storeFuncRecurInDict(startElement,forEachElFunc,layerDepth = -1):
    #extracts the elements of a dictionary recursively
        currLayAllKeys_knowParentKeys = list()
        nextLayAllItems_writeSublinks = list()
        mainDict = dict()
        mainDict["0"] = startElement
        for currLayer in range(layerDepth): #for every layer do:
            mainDictItems = [list(item) for item in list(mainDict.items())]
            print(f"mainDictItems {mainDictItems}")
            currLayAllItems_knowItemParents = [item for item in mainDictItems if (extractNumberAmount(item[0]) == currLayer+1)]
            print(f"currLayAllItems {currLayAllItems_knowItemParents}")
            currLayAllKeys_knowParentKeys = [item[0] for item in currLayAllItems_knowItemParents]
            print(f"currLayAllKeys {currLayAllKeys_knowParentKeys}")
            #scrape the links from the previous layer and write them onto a temporary matrix
            nextLayAllItems_writeSublinks = [forEachElFunc(mainDict[preEl]) for preEl in currLayAllKeys_knowParentKeys]
            print(f"nextLayAllItems {nextLayAllItems_writeSublinks}")
            #copy all links from current layer onto the main dictionairies 
            for currLayKeyIndex in range(len(currLayAllKeys_knowParentKeys)):
                print(f"currLayKeyIndex {currLayKeyIndex}")
                for nextLayPos in range(len(nextLayAllItems_writeSublinks[currLayKeyIndex])):
                    print(f"nextLayPos {nextLayPos}")
                    mainDict[f"{currLayAllKeys_knowParentKeys[currLayKeyIndex]},{nextLayPos}"] = nextLayAllItems_writeSublinks[currLayKeyIndex][nextLayPos]
                    print(f"mainDict {mainDict}")
            #eliminate all duplicates to avoid infinite recursion    
            mainDictItems = [list(item) for item in list(mainDict.items())]
            print("CHECK FOR DUPL")
            for mainDictItem in mainDictItems:
                mainDictItem = list(mainDictItem)
                print(f"mainDictItem {mainDictItem}")
                mainDictValues = list(mainDict.values())
                print(f"mainDictValues {mainDictValues}")
                mainDictKeys = list(mainDict.keys())
                print(f"mainDictKeys {mainDictKeys}")
                mainDictItemCount = mainDictValues.count(mainDictItem[1])
                print(f"mainDictItemCount {mainDictItemCount}")
                if(mainDictItemCount >= 2): #if a value occurs more than 2 times
                    toPopList = [item[0] for item in mainDictItems if item[1] == mainDictItem[1]]
                    toPopList.pop(0)
                    print(f"toPopList {toPopList}")
                    for keysToPop in toPopList:
                        pop = mainDict.pop(keysToPop)
                        print(f"POP {pop}")
            print("DUPL CHECK COMPLETE")
        return mainDict

                
def extractNumberAmount(text):
    allNumbers = re.findall(r"\d+",str(text))
    return len(allNumbers)

def listToString(list):
    return re.sub(r"[\s\[\]]","",str(list))

def getIndexByKey(key,dict):
    return list(dict.keys()).index(key)
    
print(listToString(list((1,98,28,"njue"))))
#file = open('saveValues.txt', 'r')
obj = list((9,18,28))
print([el for el in enumerate(obj)])
def divideWeirdly(el):
    return [el*(x/4) for x in range(1,4)]


TADA = storeFuncRecurInDict(123,divideWeirdly,10)

print(f"TADA: {TADA}")
saveDictToTXT(TADA,"TADA")

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
