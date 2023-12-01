"""
RULES: 

1. variable-name definition: data about the value (optional: + "_" + function of the value)

2. create as few side-effects as possible 

3.1. comment above block: describe the function of the code-block

3.2. comment after the line: describe the function of the line (for details)

"""


from ast import main
import imp
import numbers
from tokenize import String
from urllib import request
from bs4 import BeautifulSoup
import array as arr
import re
import datetime
import numpy as np
import ssl
from threading import Thread
import os
import time
import string as st
import json
import varname as vn
import imp




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
    open(f"results/{docName}.txt","x")
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
        self.resultDict = dict()
        self.resultItems = []
        self.scrapedLinksIter = 0
        self.isScraped = False
        self.bannedWordsInLink = ["Datei:","Hilfe:","Wikipedia:","Spezial:","https://"]
        self.returnedValue = None
        
    def __str__(self,returnedValue):
        self.returnedValue = returnedValue
        return self.returnedValue
    
    def isObjectScraped(self):
        if(not self.isScraped):
            raise ReferenceError("Link has not been scraped yet")
        
    def scrape(self, layerDepth = False, maxElPerLay = False):
        startTime = time.perf_counter()
        processCounter = 1
        print(f"Scraping of '{self.startURL} at {datetime.datetime.now()} initiated...")
        #scrapes a given link recursively, if the layerDepth is not defined as an integer in the parameter, the link will be scraped, until the next layer in the structure has no more elements
        self.isScraped = True
        def areObjectsInObject(self,value,checkList):
            #returns True, if an object 
            return [word not in value or word == value for word in checkList].count(False) != 0
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
            if(maxElPerLay is not False and maxElPerLay > 0):
               parentContainerAllLinks = parentContainerAllLinks[:maxElPerLay]
            for subLink in parentContainerAllLinks:
                hasWantedWords = "/wiki/" in subLink
                hasBannedWords = areObjectsInObject(self,subLink,self.bannedWordsInLink)
                isInNavRole = subLink in str(wikipediaPageHTML.find_all(role="navigation"))
                isInImgDesc = subLink in str(wikipediaPageHTML.find_all(class_="wikitable"))
                isWantedSubLink = hasWantedWords and not hasBannedWords and not isInNavRole and not isInImgDesc
                #dbPrint(subLink,hasWantedWords,hasBannedWords,isInImgDesc,isInNavRole,isWantedSubLink)
                if(isWantedSubLink):
                    subLink = f"{urlDomain}{subLink}"
                    #dbPrint(subLink)
                    openedChildPage = request.urlopen(subLink,context=ssl._create_unverified_context())
                    childWikiPage = BeautifulSoup(openedChildPage, "html.parser")
                    try:
                        descImg = f"https:{childWikiPage.find(class_='mw-file-element').get('src')}"
                    except:
                        descImg = None
                    try:
                        descTxt = childWikiPage.find(class_="mw-parser-output").p.text
                    except:
                        descTxt = None
                    wantedPageInfoContainer.append(dict(URL=subLink,descImg=descImg,descTxt=descTxt))
            return wantedPageInfoContainer
        
        #open and access the wanted Wikipedia page
        openedPage = request.urlopen(self.startURL,context=ssl._create_unverified_context())
        wikipediaPageHTML = BeautifulSoup(openedPage, "html.parser")
        #create and setup the dictionary
        mainDict = dict()
        firstEntryDescImg = f"https:{wikipediaPageHTML.find(class_='mw-file-element').get('src')}"
        firstEntryDescTxt = wikipediaPageHTML.find(class_='mw-parser-output').p.text
        mainDict["0"] = dict(URL=self.startURL,descImg=firstEntryDescImg,descTxt=firstEntryDescTxt)
        # setup for duplicate removal
        mainDictCheckList = [list(item) for item in list(mainDict.items())]
        itemToAppend = []
        appendToCheckList = True
        realNextElLayPos = 0
        # scrape the start-URL, if a max-layer is given
        print("Scraped element number:")
        if(layerDepth >= 0):
            for currLay in range(layerDepth): 
                print(f"Layer: {currLay}")
                #create the items for the next layer
                mainDictItems = [list(item) for item in list(mainDict.items())]
                currLayAllItems_knowItemParents = [item for item in mainDictItems if (extractNumberAmount(item[0]) == currLay+1)] #extracts every item in the main dictionary of the current layer
                currLayAllKeys_knowParentKeys = [item[0] for item in currLayAllItems_knowItemParents]
                #nextLayAllItems_writeSublinks = [scrapeWikipediaLink(self,preEl[1]["URL"]) for preEl in currLayAllItems_knowItemParents] #applies the given function to every element of the current layer and stores the allLinks as a 2d-array/matrix
                nextLayAllItems_writeSublinks = []
                for preEl in currLayAllItems_knowItemParents:
                    nextLayAllItems_writeSublinks.append(scrapeWikipediaLink(self,preEl[1]["URL"]))
                    print(processCounter)
                    processCounter+=1
                #dbPrint(nextLayAllItems_writeSublinks)
                #copy the next layer items onto the main dictionary
                for currLayKeyIndex in range(len(currLayAllKeys_knowParentKeys)):
                    realNextElLayPos = 0
                    for nextElLayPos in range(len(nextLayAllItems_writeSublinks[currLayKeyIndex])):
                        # prevent creation of duplicates and thereby infinite recursion
                        for checkItem in mainDictCheckList:
                            if(nextLayAllItems_writeSublinks[currLayKeyIndex][nextElLayPos]["URL"] == checkItem[1]["URL"]):
                                appendToCheckList = False
                                break
                        if(appendToCheckList):
                            itemToAppend = [f"{currLayAllKeys_knowParentKeys[currLayKeyIndex]},{realNextElLayPos}",nextLayAllItems_writeSublinks[currLayKeyIndex][nextElLayPos]] #appends every element of the next layer onto the main dictionary with a specific key as a its position
                            mainDictCheckList.append(itemToAppend)
                            mainDict[itemToAppend[0]] = itemToAppend[1]
                            realNextElLayPos+=1
                        else:
                            appendToCheckList = True
        # scrape the start-URL, if no max-layer is given
        else:
            currLay = 0
            while(True):
                mainDictItems = [list(item) for item in list(mainDict.items())]
                currLayAllItems_knowItemParents = [item for item in mainDictItems if (extractNumberAmount(item[0]) == currLay+1)]
                currLayAllKeys_knowParentKeys = [item[0] for item in currLayAllItems_knowItemParents]
                #scrape the links from the previous layer and write them onto a temporary matrix
                nextLayAllItems_writeSublinks = [scrapeWikipediaLink(self,preEl[1]["url"]) for preEl in enumerate(currLayAllKeys_knowParentKeys)] #applies the given function to every element of the current layer and stores the allLinks as a 2d-array/matrix
                #copy all links from current layer onto the main dictionairy
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
                    break
                currLay+=1
        self.resultDict = mainDict
        self.resultItems = [list(item) for item in list(mainDict.items())]
        return mainDict
  
    def getLayer(self,targetLayer):
        self.isObjectScraped()
        targetLayer = int(targetLayer)
        allLayEls = []
        preLayers = "".join("0," for _ in range(targetLayer))
        itemIndex = 0
        while(True):
            try:
                allLayEls.append([f"{preLayers}{itemIndex}",self.resultDict[f"{preLayers}{itemIndex}"]])
            except:
                break
        self.returnedValue = allLayEls
        return allLayEls
    
    def getParents(self,originLayer):
        self.isObjectScraped()
        originLayer = int(originLayer)
        allParentEls = []
        for item in self.resultItems:
            if(extractNumberAmount(item[0]) == originLayer):
                break  
            allParentEls.append(item)
        self.returnedValue = allParentEls
        return allParentEls
                    
    def getChildren(self,originLayer):
        self.isObjectScraped()
        originLayer = int(originLayer)
        preLayers = "".join("0," for _ in range(originLayer+1))
        
        
        
        allChildEls = [item for item in self.resultItems if (extractNumberAmount(item[0]) > originLayer)]
        self.returnedValue = allChildEls
        return allChildEls
    
    def save(self, fileName, fileType = ".txt", filePath = "results/"):
        self.isObjectScraped()
        fileName = re.sub(r"[\s\.,\/]", '', fileName).upper()
        resultKeys = [key for key in list(self.resultDict.keys())]
        resultVals = [val for val in list(self.resultDict.values())]
        fullFile = f"{filePath}{fileName}{fileType}"
        if(os.path.exists(fullFile)):
            os.remove(fullFile)
        file = open(fullFile,"x")
        file = open(fullFile,"a")
        file.write(f"\n{fileName}\nExtraction of sublinks from '{self.startURL}' at {datetime.date.today()} {datetime.time}: \n\n")
        for itemIndex in range(len(self.resultDict)):
            file.write(f"   {resultKeys[itemIndex]} : {resultVals[itemIndex]}\n")
        file.close()
        

def dbPrint(*values):
    for itemIndex in range(len(values)):    
        print(f"{vn.argname(f'values[{itemIndex}]')}: {values[itemIndex]}")
    

        
test = ScrapeLinks("https://de.wikipedia.org/wiki/Photon")
z = test.scrape(4,30)
y = test.save(f"test_{datetime.datetime.now()}")





print(test.returnedValue)
    
       




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




