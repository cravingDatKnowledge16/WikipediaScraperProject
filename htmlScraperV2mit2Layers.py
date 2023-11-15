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
import numpy
import ssl


startUrl = "https://de.wikipedia.org/wiki/Universum"

def scrapeWikipediaLinks(url,extraInfo = False):
    urlDomain = re.search(r"\w+:\/\/\w+\.\w+\.\w+",url).group()
    sublinkContainer = list()
    noSSLverifiy = ssl._create_unverified_context()
    openedPage = urllib.request.urlopen(url,context=noSSLverifiy)
    wikipediaPageHTML = BeautifulSoup(openedPage, "html.parser")
    print("Test")
    parentContainer = wikipediaPageHTML.find(class_="mw-parser-output")
    print(f"parentContainer {parentContainer}")
    return
    if(extraInfo == True):
        headerImage = f"https:{wikipediaPageHTML.find(class_='mw-file-element').get('src')}"
        headerParagraph = parentContainer.find("p")
    for sublink in parentContainer.find_all('a', href=True):
        sublinkHREF = sublink['href']
        sublinkContainer.append(sublinkHREF)
    sublinkContainer = list(set([f"{urlDomain}{sublinkHREF}" for sublinkHREF in sublinkContainer if (("/wiki/" in sublinkHREF) & ("Datei:" not in sublinkHREF) & ("Hilfe:" not in sublinkHREF) & ("Wikipedia:" not in sublinkHREF) & ("Spezial:" not in sublinkHREF) & ("https:" not in sublinkHREF))]))
    return sublinkContainer

def applyFuncRecurInDict(startElement,forEachElFunc,layerDepth = -1):
    #applies a function to an element (startElement) recursivly and stores it in a dictionary, where the key corresponds to the index of the element in a tree structure 
        mainDict = dict()
        mainDict["0"] = startElement
        if(layerDepth >= 0):
            for currLay in range(layerDepth): 
                #create the items for the next laye.#r
                mainDictItems = [list(item) for item in list(mainDict.items())]
                currLayAllItems_knowItemParents = [item for item in mainDictItems if (extractNumberAmount(item[0]) == currLay+1)] #extracts every item in the main dictionary of the current layer
                currLayAllKeys_knowParentKeys = [item[0] for item in currLayAllItems_knowItemParents]
                nextLayAllItems_writeSublinks = [forEachElFunc(mainDict[preEl]) for preEl in currLayAllKeys_knowParentKeys] #applies the given function to every element of the current layer and stores the result as a 2d-array/matrix
                #copy the next layer items onto the main dictionary
                for currLayKeyIndex in range(len(currLayAllKeys_knowParentKeys)):
                    for nextElLayPos in range(len(nextLayAllItems_writeSublinks[currLayKeyIndex])):
                        mainDict[f"{currLayAllKeys_knowParentKeys[currLayKeyIndex]},{nextElLayPos}"] = nextLayAllItems_writeSublinks[currLayKeyIndex][nextElLayPos] #appends every element of the next layer onto the main dictionary with a specific key as a its position
                #eliminate all duplicates to avoid infinite recursion    
                mainDictItems = [list(item) for item in list(mainDict.items())]
                for mainDictItem in mainDictItems:
                    mainDictItem = list(mainDictItem)
                    mainDictValues = list(mainDict.values())
                    mainDictItemCount = mainDictValues.count(mainDictItem[1])
                    if(mainDictItemCount >= 2): #if a value occurs more than 2 times
                        toPopList = [item[0] for item in mainDictItems if item[1] == mainDictItem[1]]
                        toPopList.pop(0)
                        for keysToPop in toPopList:
                            pop = mainDict.pop(keysToPop)          
        else:
            currLay = 0
            while(True):
                mainDictItems = [list(item) for item in list(mainDict.items())]
                #print(f"mainDictItems {mainDictItems}")
                currLayAllItems_knowItemParents = [item for item in mainDictItems if (extractNumberAmount(item[0]) == currLay+1)]
                #print(f"currLayAllItems {currLayAllItems_knowItemParents}")
                currLayAllKeys_knowParentKeys = [item[0] for item in currLayAllItems_knowItemParents]
                #print(f"currLayAllKeys {currLayAllKeys_knowParentKeys}")
                #scrape the links from the previous layer and write them onto a temporary matrix
                nextLayAllItems_writeSublinks = [forEachElFunc(mainDict[preEl]) for preEl in currLayAllKeys_knowParentKeys]
                #print(f"nextLayAllItems {nextLayAllItems_writeSublinks}")
                #copy all links from current layer onto the main dictionairies 
                for currLayKeyIndex in range(len(currLayAllKeys_knowParentKeys)):
                    #print(f"currLayKeyIndex {currLayKeyIndex}")
                    for nextElLayPos in range(len(nextLayAllItems_writeSublinks[currLayKeyIndex])):
                        #print(f"nextElLayPos {nextElLayPos}")
                        mainDict[f"{currLayAllKeys_knowParentKeys[currLayKeyIndex]},{nextElLayPos}"] = nextLayAllItems_writeSublinks[currLayKeyIndex][nextElLayPos]
                        #print(f"mainDict {mainDict}")
                #eliminate all duplicates to avoid infinite recursion    
                mainDictItems = [list(item) for item in list(mainDict.items())]
                #print("CHECK FOR DUPL")
                for mainDictItem in mainDictItems:
                    mainDictItem = list(mainDictItem)
                    #print(f"mainDictItem {mainDictItem}")
                    mainDictValues = list(mainDict.values())
                    #print(f"mainDictValues {mainDictValues}")
                    mainDictKeys = list(mainDict.keys())
                    #print(f"mainDictKeys {mainDictKeys}")
                    mainDictItemCount = mainDictValues.count(mainDictItem[1])
                    #print(f"mainDictItemCount {mainDictItemCount}")
                    if(mainDictItemCount >= 2): #if a value occurs more than 2 times
                        toPopList = [item[0] for item in mainDictItems if item[1] == mainDictItem[1]]
                        toPopList.pop(0)
                        #print(f"toPopList {toPopList}")
                        for keysToPop in toPopList:
                            pop = mainDict.pop(keysToPop)
                            #print(f"POP {pop}")
                #print("DUPL CHECK COMPLETE")
                if(len(nextLayAllItems_writeSublinks) == 0):
                    return dict(dict = mainDict,stopLayer = currLay)
                currLay+=1
        return mainDict
              
def extractNumberAmount(text):
    allNumbers = re.findall(r"\d+",str(text))
    return len(allNumbers)

def listToString(list):
    return re.sub(r"[\s\[\]]","",str(list))

def getIndexByKey(key,dict):
    return list(dict.keys()).index(key)

def saveDictToTXT(dict, docName): 
    docName = re.sub(r"[\s\.,]", '', docName)
    dictKeys = [item[0] for item in list(dict.items())]
    dictValues = [item[1] for item in list(dict.items())]
    with open(f'results/{docName}.txt', 'w') as tempFile:
        for itemIndex in range(len(dict)):
            tempFile.write(f"  {dictKeys[itemIndex]} : {dictValues[itemIndex]}\n")
    
def divideWeirdly(el):
    return [el*0.5,el*1.5]

def squareShit(x):
     return [pow(x,0),pow(x,2)]


scrapeWikipediaLinks(startUrl)


def DOIT():
    #TADA = applyFuncRecurInDict(startUrl,scrapeWikipediaLinks,2)
    TADA = applyFuncRecurInDict(123,divideWeirdly,5)
    print(f"TADA: {TADA}")
    saveDictToTXT(TADA,"TADA")





"""
Storage:

def storeFuncRecurInDict(startElement,forEachElFunc,layerDepth = -1):
    #extracts the elements of a dictionary recursively
        currLayAllKeys_knowParentKeys = list()
        nextLayAllItems_writeSublinks = list()
        mainDict = dict()
        mainDict["0"] = startElement
        if(layerDepth >= 0):
            for currLay in range(layerDepth): #for every layer do:
                mainDictItems = [list(item) for item in list(mainDict.items())]
                #print(f"mainDictItems {mainDictItems}")
                currLayAllItems_knowItemParents = [item for item in mainDictItems if (extractNumberAmount(item[0]) == currLay+1)]
                #print(f"currLayAllItems {currLayAllItems_knowItemParents}")
                currLayAllKeys_knowParentKeys = [item[0] for item in currLayAllItems_knowItemParents]
                #print(f"currLayAllKeys {currLayAllKeys_knowParentKeys}")
                #scrape the links from the previous layer and write them onto a temporary matrix
                nextLayAllItems_writeSublinks = [forEachElFunc(mainDict[preEl]) for preEl in currLayAllKeys_knowParentKeys]
                #print(f"nextLayAllItems {nextLayAllItems_writeSublinks}")
                #copy all links from current layer onto the main dictionairies 
                for currLayKeyIndex in range(len(currLayAllKeys_knowParentKeys)):
                    #print(f"currLayKeyIndex {currLayKeyIndex}")
                    for nextElLayPos in range(len(nextLayAllItems_writeSublinks[currLayKeyIndex])):
                        #print(f"nextElLayPos {nextElLayPos}")
                        mainDict[f"{currLayAllKeys_knowParentKeys[currLayKeyIndex]},{nextElLayPos}"] = nextLayAllItems_writeSublinks[currLayKeyIndex][nextElLayPos]
                        #print(f"mainDict {mainDict}")
                #eliminate all duplicates to avoid infinite recursion    
                mainDictItems = [list(item) for item in list(mainDict.items())]
                #print("CHECK FOR DUPL")
                for mainDictItem in mainDictItems:
                    toPopList = [item[0] for item in mainDictItems if item[1] == mainDictItem[1]]
                    for keysToPop in toPopList[1:]:
                        pop = mainDict.pop(keysToPop)
                #print("DUPL CHECK COMPLETE")

"""

