"""
RULES: 

1. variable-name definition: data about the value (optional: + "_" + function of the value)

2. create as few side-effects as possible 

3.1. comment above block: describe the function of the code-block

3.2. comment after the line: describe the function of the line (for details)

"""


from ast import main
import imp
import imp
import numbers
from tkinter.tix import Tree
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
import plotly.express as px
import translate 





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



URL = "https://de.wikipedia.org/wiki/Universum"


class ScrapeURL:
    def __init__(self,startURL):
        self.startURL = startURL
        self.urlDomain = re.search(r"\w+:\/\/\w+\.\w+\.\w+",self.startURL).group()
        self.iter = 0
        self.resultDict = dict()
        self.resultList = []
        self.layers = None
        self.isScraped = False
        self.bannedWordsInLink = ["Datei:","Hilfe:","Wikipedia:","Spezial:","https://"]
        self.returnedValue = None
        
    def __str__(self,returnedValue):
        self.returnedValue = returnedValue
        return self.returnedValue
    
    def _isObjectScraped(self):
        if(not self.isScraped):
            raise ReferenceError("Link has not been scraped yet")
        
    def _getNumberAmount(self,text):
            return len(re.findall(r"\d+",str(text)))
    def scrape(self, layerDepth = None, maxReadLinks = None, maxURLPerLay = None):
        #scrapes a given link recursively, if the layerDepth is not defined as an integer in the parameter, the link will be scraped, until the next layer in the structure has no more elements
        
        # initiation of important variables
        startTime = time.perf_counter()
        self.isScraped = True
        mainDict = dict()
        layerConditions = {
            "0":lambda a,b : a < b,
            "1":lambda a,b : True
        }
        layerCondition = 1 if layerDepth >= 0 else 0
        currLayKeyIndex = 0
        currLayAllItems = []
        currLayAllKeys = []
        mainDictCheckList = [list(item) for item in list(mainDict.items())]
        itemToAppend = []
        appendToChecklist = True
        currLayDuplCounter = 0
        layerItemCounter = 1
        allArticlesCounter = 1
        realNextElLayPos = 0
        currLay = 0
        
        #declaration of local functions
        
        def areObjectsInObject(self,value,checkList):
            return [word not in value or word == value for word in checkList].count(False) != 0
        def isWantedURL(self,checkURL,wikiPage):
            hasWantedWords = "/wiki/" in checkURL
            hasBannedWords = areObjectsInObject(self,checkURL,self.bannedWordsInLink)
            isInNavRole = checkURL in str(wikiPage.find_all(role="navigation"))
            isInImgDesc = checkURL in str(wikiPage.find_all(class_="wikitable"))
            isWantedURL = hasWantedWords and not hasBannedWords and not isInNavRole and not isInImgDesc
            return isWantedURL
        def getPageInfo(self,URL):
            pageURL = f"{self.urlDomain}{URL}"
            openedPage = request.urlopen(pageURL,context=ssl._create_unverified_context())
            wikiPage = BeautifulSoup(openedPage, "html.parser")
            try:
                articleTitle = wikiPage.find(class_="mw-page-title-main").text
            except:
                print("dafuq")
                print(pageURL)
                os.abort()
            try:
                articleImg = f"https:{wikiPage.find(class_='mw-file-element').get('src')}"
            except:
                articleImg = None
            try:
                articleTxt = wikiPage.find(class_="mw-parser-output").p.text
            except:
                articleTxt = None
            return dict(URL=URL,articleTitle=articleTitle,articleImg=articleImg,articleTxt=articleTxt)
        
        def getSublinks(self,URL):
            nonlocal maxReadLinks
            print(f"   Open page...")
            try:
                openedPage = request.urlopen(URL,context=ssl._create_unverified_context())
            except:
                print("End of link structure has been reached")
                return None 
            print(f"   Extract data...")
            wikiPage = BeautifulSoup(openedPage, "html.parser")
            parentContainer = wikiPage.find(class_="mw-parser-output")
            maxReadLinks = maxReadLinks if maxReadLinks >= 0 else len(parentContainer)
            parentContainerAllURLs = [iterURL["href"] for iterURL in parentContainer.find_all("a",href=True)[:maxReadLinks]]
            print(f"   Scrape URLs...")
            wantedPageInfoContainer = [getPageInfo(self,iterURL) for iterURL in parentContainerAllURLs if isWantedURL(self,iterURL,wikiPage)]
            return wantedPageInfoContainer
        
        def printStartTerminalInfo(self):
            print(f"{''.join('-' for _ in range(100))}\n")
            print(f"Scraping of '{self.startURL}' at {datetime.datetime.now()} initiated...")
            print(f"layerDepth: {layerDepth}, maxReadLinks: {maxReadLinks}, maxURLPerLay: {maxURLPerLay}")
        def predefineDict(self):
            nonlocal mainDict
            #open and access the wanted Wikipedia page
            openedPage = request.urlopen(self.startURL,context=ssl._create_unverified_context())
            wikipediaPageHTML = BeautifulSoup(openedPage, "html.parser")
            #create and setup the dictionary
            firstEntryPageTitle = wikipediaPageHTML.find(class_="mw-page-title-main").text
            firstEntryDescImg = f"https:{wikipediaPageHTML.find(class_='mw-file-element').get('src')}"
            firstEntryDescTxt = wikipediaPageHTML.find(class_='mw-parser-output').p.text
            mainDict["0"] = dict(URL=self.startURL,articleTitle=firstEntryPageTitle,articleImg=firstEntryDescImg,articleTxt=firstEntryDescTxt)
        
        printStartTerminalInfo(self)
        predefineDict(self)
        
        mainDictItems = currLayAllItems = nextLayAllItems = []
        def initiateScraping(self):
            nonlocal currLay
            while(layerConditions[f"{layerCondition}"](currLay,layerDepth)):  
                print(f" Current layer: {currLay} | Working on layer: {currLay+1}")
                getCurrLayEls(self)
                createNextLayEls()
                initiateAppendingNextLayEls()
                if(len(nextLayAllItems) == 0):
                    break
                currLay+=1
            self.resultDict = mainDict
            self.layers = currLay
            self.resultList = [list(item) for item in list(mainDict.items())]
        def getCurrLayEls(self):
            print(f"  Getting current layer...")
            nonlocal mainDictItems,currLayAllItems
            mainDictItems = [list(item) for item in list(mainDict.items())]
            currLayAllItems = [item for item in mainDictItems if (self._getNumberAmount(item[0]) == currLay+1)]
            currLayAllKeys = [item[0] for item in currLayAllItems]
        def createNextLayEls():
            print(f"  Creating next layer...")
            nonlocal allArticlesCounter,layerItemCounter,nextLayAllItems
            nextLayAllItems = []
            layerItemCounter = 1
            for currEl in currLayAllItems:
                nextLayAllItems.append(getSublinks(self,currEl[1]["URL"]))
                print(f"   All processed URL: {allArticlesCounter} | Current scraped link: {layerItemCounter}/{len(currLayAllItems)}")
                allArticlesCounter+=1
                layerItemCounter+=1
        def initiateAppendingNextLayEls():
            print(f"  Initiating appending of next layer...")
            nonlocal currLayDuplCounter,realNextElLayPos,maxURLPerLay,itemToAppend,mainDictCheckList,mainDict,currLayKeyIndex
            #copy the next layer items onto the main dictionary
            maxURLPerLay = maxURLPerLay if maxURLPerLay >= 0 else len(nextLayAllItems)
            currLayDuplCounter = 0
            for currLayKeyIndex in range(len(currLayAllItems)):
                realNextElLayPos = 0
                for nextElLayPos in range(len(nextLayAllItems[:maxURLPerLay][currLayKeyIndex])):
                    isInResultDict(self,nextElLayPos)
                    appendToResultDict(self,nextElLayPos)  
            print(f"  Amount of duplicates in layer: {currLayDuplCounter}")
                
        def isInResultDict(self,elInd):
            print(f"   Checking if duplicate...")
            nonlocal appendToChecklist 
            for checkItem in mainDictCheckList:
                if(nextLayAllItems[currLayKeyIndex][elInd]["URL"] == checkItem[1]["URL"]):
                    appendToChecklist = False
                    print(f"   Is duplicate, no appending")
                    break
            if(appendToChecklist):
                print(f"   Not a duplicate")
                
        def appendToResultDict(self,elInd):
            nonlocal currLayDuplCounter,realNextElLayPos,maxURLPerLay,itemToAppend,mainDictCheckList,mainDict,appendToChecklist
            # prevent creation of duplicates and thereby infinite recursion
            if(appendToChecklist):
                print(f"   Appending...")
                itemToAppend = [f"{currLayAllKeys[elInd]},{realNextElLayPos}",nextLayAllItems[currLayKeyIndex][elInd]] #appends every element of the next layer onto the main dictionary with a specific key as a its position
                mainDictCheckList.append(itemToAppend)
                mainDict[itemToAppend[0]] = itemToAppend[1]
                realNextElLayPos+=1
            else:
                print(f"   Not appending...")
                appendToChecklist = True
                currLayDuplCounter+=1
        
        initiateScraping(self)



  
    def getLayer(self,targetLayer):
        self._isObjectScraped()
        targetLayer = int(targetLayer)
        allLayEls = [item for item in self.resultList if (self._getNumberAmount(item[0])-1 == targetLayer)]
        self.returnedValue = allLayEls
        return allLayEls
    
    def getParents(self,originLayer,extraLayers = None):
        self._isObjectScraped()
        originLayer = int(originLayer)
        if(extraLayers == None):
            extraLayers = originLayer
        allParentEls = [item for item in self.resultList if (self._getNumberAmount(item[0])-1 < originLayer and self._getNumberAmount(item[0])-1 >= originLayer-extraLayers)]   
        self.returnedValue = allParentEls
        return allParentEls
                    
    def getChildren(self,originLayer,extraLayers = None):
        self._isObjectScraped()
        originLayer = int(originLayer)
        allChildEls = []
        if(extraLayers == None):
            allChildEls = [item for item in self.resultList if (self._getNumberAmount(item[0])-1 > originLayer)]
        elif(type(extraLayers)==type(1)):    
            allChildEls = [item for item in self.resultList if (self._getNumberAmount(item[0])-1 > originLayer and self._getNumberAmount(item[0])-1 <= originLayer+extraLayers)]
        self.returnedValue = allChildEls
        return allChildEls
    
    def save(self, fileName, fileType = "txt", filePath = "results/", extraInfo = False):
        self._isObjectScraped()
        fileName = re.sub(r"[\s\.,\/]", '', fileName).upper()
        resultKeys = list(self.resultDict.keys()).copy()
        resultVals = list(self.resultDict.values()).copy()
        fullFilePath = f"{filePath}{fileName}.{fileType}"
        if(os.path.exists(fullFilePath)):
            os.remove(fullFilePath)
        file = open(fullFilePath,"x")
        file = open(fullFilePath,"a")
        if(fileType == "txt"):
            if(extraInfo):
                file.write(f"\n{fileName}\nExtraction of URLs from '{self.startURL}' at {datetime.date.today()} {datetime.time}: \n\n")
            for itemIndex in range(len(self.resultDict)):
                file.write(f"{resultKeys[itemIndex]} : {resultVals[itemIndex]}\n")
        elif(fileType == "json"):
            file.write(json.dumps(self.resultDict))
        file.close()
        
    def plotlify(self):
        self._isObjectScraped()
        keysList = [item[0] for item in self.resultList]
        pxElements = [item[1]["articleTitle"] for item in self.resultList]
        pxParents = [""]
        pxParents[1:] = [self.resultDict[(lambda i : re.sub(r'(\,\d+|\d+)$','',i))(item[0])]["articleTitle"] for item in self.resultList[1:]]
        pxValues = [1 for _ in range(len(self.resultList))]
        dbPrint(pxElements,len(pxElements),pxParents,len(pxParents))
        pxData= dict(
            el = pxElements,
            par = pxParents,
            #val = pxValues        
        )
        fig = px.sunburst(
            pxData,
            names="el",
            parents="par",
            #values="val"
            
        )
        fig.show()

def dbPrint(*values):
    for itemIndex in range(len(values)):    
        print(f"{vn.argname(f'values[{itemIndex}]')}: {values[itemIndex]}")
    

        
test = ScrapeURL("https://de.wikipedia.org/wiki/Photon")
z = test.scrape(3,15,20)
# y = test.save(f"test_{datetime.datetime.now()}")
test.getChildren(1)
test.plotlify()
os.abort()

dbPrint(test.returnedValue)

test.getLayer(1)

dbPrint(test.returnedValue)

test.getParents(2)

dbPrint(test.returnedValue)


    

       

