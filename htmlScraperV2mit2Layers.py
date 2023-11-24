"""
RULES: 

1. variable-name definition: data about the value (optional: + "_" + function of the value)

2. create as few side-effects as possible 

3.1. comment above block: describe the function of the code-block

3.2. comment after the line: describe the function of the line (for details)

"""


import numbers
from tokenize import String
from urllib import request
from bs4 import BeautifulSoup
import array as arr
import re
import datetime
import numpy
import ssl
from threading import Thread
import os
import time
import string as st





"""

def scrapeWikipediaLinks(url):
    urlDomain = re.search(r"\w+:\/\/\w+\.\w+\.\w+",url).group()
    wantedLinksContainer = list()
    noSSLverifiy = ssl._create_unverified_context()
    openedPage = urllib.request.urlopen(url,context=noSSLverifiy)
    wikipediaPageHTML = BeautifulSoup(openedPage, "html.parser")
    parentContainer = wikipediaPageHTML.find(class_="mw-parser-output")
    for sublink in parentContainer.find_all('a', href=True):
        sublinkHREF = sublink['href']
        wantedLinksContainer.append(sublinkHREF)
    wantedLinksContainer = list(set([f"{urlDomain}{sublinkHREF}" for sublinkHREF in wantedLinksContainer if (("/wiki/" in sublinkHREF) & ("Datei:" not in sublinkHREF) & ("Hilfe:" not in sublinkHREF) & ("Wikipedia:" not in sublinkHREF) & ("Spezial:" not in sublinkHREF) & ("https:" not in sublinkHREF))]))
    return wantedLinksContainer

def getImportantPageInfo(url):
    noSSLverifiy = ssl._create_unverified_context()
    openedPage = urllib.request.urlopen(url,context=noSSLverifiy)
    wikipediaPageHTML = BeautifulSoup(openedPage, "html.parser")
    parentContainer = wikipediaPageHTML.find(class_="mw-parser-output")
    descImg = f"https:{wikipediaPageHTML.find(class_='mw-file-element').get('src')}"
    descTxt = parentContainer.p.text
    allPageInfo = dict(descImg=descImg,descTxt=descTxt)
    return allPageInfo 

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
                nextLayAllItems_writeSublinks = [forEachElFunc(mainDict[preEl]) for preEl in currLayAllKeys_knowParentKeys] #applies the given function to every element of the current layer and stores the allLinks as a 2d-array/matrix
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
            print(mainDict)
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
              
"""
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

#def DOIT():
    #TADA = applyFuncRecurInDict(startUrl,scrapeWikipediaLinks,2)
    #TADA = applyFuncRecurInDict(123,divideWeirdly,5)
    #print(f"TADA: {TADA}")
    #saveDictToTXT(TADA,"TADA")

#DOIT()


URL = "https://de.wikipedia.org/wiki/Universum"


class ScrapeLinks:
    def __init__(self,startURL):
        self.startURL = startURL
        self.iter = 0
        self.allLinks = dict()
        self.allLinksItems = []
        self.scrapedLinksIter = 0
        self.isScraped = False
        self.bannedWordsInLink = ["Datei:","Hilfe:","Wikipedia:","Spezial:","https://"]
        self.returnedValue = str()
    def __str__(self,returnedValue):
        self.returnedValue = returnedValue
        return self.returnedValue
    
    def isObjectScraped(self):
        if(len(self.allLinksItems) == 0):
            raise ReferenceError("Link has not been scraped yet")
        
    def scrape(self, layerDepth = False, maxElPerLay = False):
        #scrapes a given link recursively, if the layerDepth is not defined as an integer in the parameter, the link will be scraped, until the next layer in the structure has no more elements
        def areObjectsInObject(self,value,checkList):
            #returns True, if an object 
            return [word not in value for word in checkList].count(False) != 0
        def scrapeWikipediaLink(self,URL):
            try:
                openedParentPage = request.urlopen(URL,context=ssl._create_unverified_context())
            except:
                print("End of link structure has been reached")
                os.abort()
            parentWikiPage = BeautifulSoup(openedParentPage, "html.parser")
            parentContainer = parentWikiPage.find(class_="mw-parser-output")
            urlDomain = re.search(r"\w+:\/\/\w+\.\w+\.\w+",self.startURL).group()
            parentContainerAllLinks = [subLink["href"] for subLink in parentContainer.find_all("a",href=True)]
            wantedPageInfoContainer = []
            if(maxElPerLay is numbers.Number):
               parentContainerAllLinks = parentContainerAllLinks[:maxElPerLay-1]
            for subLink in parentContainerAllLinks:
                hasWantedWords = "/wiki/" in subLink
                hasBannedWords = areObjectsInObject(self,subLink,self.bannedWordsInLink)
                isInNavRole = subLink in str(wikipediaPageHTML.find_all(role="navigation"))
                isInImgDesc = subLink in str(wikipediaPageHTML.find_all(class_="wikitable"))
                if(hasWantedWords and not hasBannedWords and not isInNavRole and not isInImgDesc):
                    #wantedLinksContainer.append(f"{urlDomain}{subLink}")
                    subLink = f"{urlDomain}{subLink}"
                    openedChildPage = request.urlopen(subLink,context=ssl._create_unverified_context())
                    childWikiPage = BeautifulSoup(openedChildPage, "html.parser")
                    try:
                        descImg = f"https:{childWikiPage.find(class_='mw-file-element').get('src')}"
                    except:
                        descImg = "None"
                    #descTxt = childWikiPage.find(class_="mw-parser-output").p.text
                    descTxt = "Currently None"
                    wantedPageInfoContainer.append(dict(URL=subLink,descImg=descImg,descTxt=descTxt))
            print("wantedPageInfoContainer: ",wantedPageInfoContainer)
            return wantedPageInfoContainer
        
        #open and access the wanted Wikipedia page
        openedPage = request.urlopen(self.startURL,context=ssl._create_unverified_context())
        wikipediaPageHTML = BeautifulSoup(openedPage, "html.parser")
        #create and setup the dictionary
        mainDict = dict()
        firstEntryDescImg = f"https:{wikipediaPageHTML.find(class_='mw-file-element').get('src')}"
        firstEntryDescTxt = wikipediaPageHTML.find(class_='mw-parser-output').p.text
        mainDict["0"] = dict(URL=self.startURL,descImg=firstEntryDescImg,descTxt=firstEntryDescTxt)
        #
        if(layerDepth >= 0):
            for currLay in range(layerDepth): 
                #create the items for the next layer
                mainDictItems = [list(item) for item in list(mainDict.items())]
                currLayAllItems_knowItemParents = [item for item in mainDictItems if (extractNumberAmount(item[0]) == currLay+1)] #extracts every item in the main dictionary of the current layer
                print("currLayAllItems_knowItemParents: ",currLayAllItems_knowItemParents)
                currLayAllKeys_knowParentKeys = [item[0] for item in currLayAllItems_knowItemParents]
                nextLayAllItems_writeSublinks = [scrapeWikipediaLink(self,preEl[1]["URL"]) for preEl in currLayAllItems_knowItemParents] #applies the given function to every element of the current layer and stores the allLinks as a 2d-array/matrix
                #copy the next layer items onto the main dictionary
                for currLayKeyIndex in range(len(currLayAllKeys_knowParentKeys)):
                    for nextElLayPos in range(len(nextLayAllItems_writeSublinks[currLayKeyIndex])):
                        mainDict[f"{currLayAllKeys_knowParentKeys[currLayKeyIndex]},{nextElLayPos}"] = nextLayAllItems_writeSublinks[currLayKeyIndex][nextElLayPos] #appends every element of the next layer onto the main dictionary with a specific key as a its position
                        self.scrapedLinksIter+=1
                        print(f"Process state: {self.iter}, {nextElLayPos}, {currLayKeyIndex}")
                #eliminate all duplicates to avoid infinite recursion    
                mainDictItems = [list(item) for item in list(mainDict.items())]
                self.iter = 0
                for mainDictItem in mainDictItems:
                    mainDictItem = list(mainDictItem)
                    mainDictValues = list(mainDict.values())
                    mainDictItemCount = mainDictValues.count(mainDictItem[1])
                    if(mainDictItemCount >= 2): #if a value occurs more than 2 times
                        toPopList = [item[0] for item in mainDictItems if item[1] == mainDictItem[1]]
                        toPopList.pop(0)
                        for keyToPop in toPopList:
                            pop = mainDict.pop(keyToPop)  
            print("DONE")
            return mainDict
        else:
            currLay = 0
            while(True):
                mainDictItems = [list(item) for item in list(mainDict.items())]
                currLayAllItems_knowItemParents = [item for item in mainDictItems if (extractNumberAmount(item[0]) == currLay+1)]
                currLayAllKeys_knowParentKeys = [item[0] for item in currLayAllItems_knowItemParents]
                #scrape the links from the previous layer and write them onto a temporary matrix
                nextLayAllItems_writeSublinks = [scrapeWikipediaLink(self,preEl[1]["url"]) for preEl in enumerate(currLayAllKeys_knowParentKeys)] #applies the given function to every element of the current layer and stores the allLinks as a 2d-array/matrix
                #copy all links from current layer onto the main dictionairies 
                for currLayKeyIndex in range(len(currLayAllKeys_knowParentKeys)):
                    for nextElLayPos in range(len(nextLayAllItems_writeSublinks[currLayKeyIndex])):
                        mainDict[f"{currLayAllKeys_knowParentKeys[currLayKeyIndex]},{nextElLayPos}"] = nextLayAllItems_writeSublinks[currLayKeyIndex][nextElLayPos]
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
                #if the next layer doesn't contain any items, stop execution of this function and return the main dictionary and the layer, at which point execution was stopped
                if(len(nextLayAllItems_writeSublinks) == 0):
                    self.allLinksItems = list(mainDict.items())
                    return dict(dict = mainDict,stopLayer = currLay)
                currLay+=1
    def getLayer(self,targetLayer):
        self.isObjectScraped()
        targetLayer = int(targetLayer)
        allTargetLayElements = []
        layerIsFound = False
        for allLinksItem in self.allLinksItems:
            if(extractNumberAmount(allLinksItem[0]) == targetLayer):
                layerIsFound = True
                allTargetLayElements.append(allLinksItem)
            # break out of the loop, when all items of the wanted layer have been copied
            elif(extractNumberAmount(allLinksItem[0]) != targetLayer and layerIsFound == True):
                break
        return allTargetLayElements
    
    def getParents(self,originLayer):
        self.isObjectScraped()
        originLayer = int(originLayer)
        allParentElements = []
        for allLinksItem in self.allLinksItems:
            if(extractNumberAmount(allLinksItem[0]) == originLayer):
                break  
            allParentElements.append(allLinksItem)
        return allParentElements
                    
    def getChildren(self,originLayer):
        self.isObjectScraped()
        originLayer = int(originLayer)
        manipulatedAllLinks = [item for item in self.allLinksItems if (extractNumberAmount(item[0]) > item[0])]
        return manipulatedAllLinks


        
        
        
test = ScrapeLinks("https://de.wikipedia.org/wiki/Universum")
z = test.scrape(2,10)

print(z)
    
       




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




