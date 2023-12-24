"""
RULES: 

1. variable-name definition: data about the value (optional: + "_" + function of the value)

2. create as few side-effects as possible 

3.1. comment above block: describe the function of the code-block

3.2. comment after the line: describe the function of the line (for details)

"""


from ast import main
import numpy as num
# from tkinter.tix import Tree
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
import plotly.express as px
import curses as cur
import timeit
# import consolemenu



URL = "https://de.wikipedia.org/wiki/Universum"


class ScrapeLinks:
    def __init__(self,startURL):
        self.startURL = startURL
        self.urlDomain = re.search(r"\w+:\/\/\w+\.\w+\.\w+",self.startURL).group()
        self.iter = 0
        self.resultDict = dict()
        self.resultItems = []
        self.layers = None
        self.isScraped = False
        self.bannedWordsInLink = ["Datei:","Hilfe:","Wikipedia:","Spezial:"]
        self.returnedValue = None
        
    def __str__(self):
        print("works")
        return ""


    def _isObjectScraped(self):
        if(not self.isScraped):
            raise ReferenceError("Link has not been scraped yet")

    def _getNumAmount(self,text:str):
        return len(re.findall(r"\d+",text))
        
        
    def scrape(self, layerDepth = None, maxReadLinks = None, maxLinksPerLay = None, constSave = True, fileData = None):
        #scrapes a given link recursively, if the layerDepth is not defined as an integer in the parameter, the link will be scraped, until the next layer in the structure has no more elements
        startTime = time.perf_counter()
    
        #declaration of local functions
        def isValInIter(value,iter):
            for i in iter:
                if(value in i):
                    return True
            return False
        def isIterInVal(value,iter):
            for i in iter:
                if(i in value):
                    return True
            return False
        
        #printing important information
        screenBuffer = 0
        screen = cur.initscr()
        # cur.endwin()
        screenWidth = screen.getmaxyx()[1]
        # cur.noecho()
        screen.clear()
        screen.addstr(0,0,"".rjust(100,"-"))
        screen.addstr(1,0,f"Scraping of '{self.startURL}' at {datetime.datetime.now()} initiated...")
        screen.addstr(2,0,f"layerDepth: {layerDepth}, maxReadLinks: {maxReadLinks}, maxLinksPerLay: {maxLinksPerLay}")
        screenBuffer = 4
        # initiation of important variables
        self.isScraped = True
        mainDict = dict()
        allLinksCounter = 1
        layerConditions = {
            "0":lambda a,b : a < b,
            "1":lambda a,b : True
        }
        layerCondition = 1 if layerDepth >= 0 else 0
        # initiation of constant saving
        if (type(fileData) == dict):
            fileData["givenName"] = fileData["givenName"] if f"{os.path.dirname(__file__)}{''}" else ''
            pass
        if(constSave):
            fileName = str(datetime.datetime.now()).replace(":","_")
            file = open(f"{os.path.dirname(__file__)}/results/{fileName}.txt","a")
            
        #open and access the wanted Wikipedia Article
        currOpenedArticle = request.urlopen(self.startURL,context=ssl._create_unverified_context())
        wikipediaArticleHTML = BeautifulSoup(currOpenedArticle, "html.parser")
        #create and setup the dictionary
        firstEntryArticleTitle = wikipediaArticleHTML.find(class_="mw-page-title-main").text
        firstEntryDescImg = f"https:{wikipediaArticleHTML.find(class_='mw-file-element').get('src')}"
        firstEntryDescTxt = wikipediaArticleHTML.find(class_='mw-parser-output').p.text
        firstEntry = dict(URL = self.startURL ,title=firstEntryArticleTitle,img=firstEntryDescImg,txt=firstEntryDescTxt)
        mainDict["0"] = firstEntry
        file.write(f"0 : {firstEntry}\n")
        # initiate scraping
        layer = 0
        processSpeed = 0
        totalScrapedURLs = 0
        while(layer <= layerDepth):  
            #get items of current layer
            mainDictItems = [list(item) for item    in list(mainDict.items())]
            currLayItems = [item for item in mainDictItems if self._getNumAmount(item[0]) == layer+1]
            if(len(currLayItems) == 0):
                break
            layerItemCounter = 1
            currElIndex = 0
            for currURL in currLayItems:
                currURL = str(currURL[1]['URL'])
                try:
                    currOpenedArticle = request.urlopen(currURL,context=ssl._create_unverified_context())
                except Exception as err:
                    screenBuffer+=1
                    screen.addstr(layer+screenBuffer,0,f"ERROR SKIPPED: {err}")
                    screenBuffer+=1
                    return None 
                currWikiArticle = BeautifulSoup(currOpenedArticle, "html.parser")
                nextURLContainer = currWikiArticle.find(class_="mw-parser-output")
                nextLay = [iterURL["href"] for iterURL in nextURLContainer.find_all("a",href=True)]
                if(type(maxReadLinks) is not type(1)):
                    maxReadLinks = len(nextLay)
                nextElIndex = 0
                realNextElIndex = 0
                unWantedURLs = 0
                nextLay = nextLay[:maxReadLinks]
                doAppend = True
                URLsubdir = ""
                for nextURL in nextLay:
                    startTime = time.perf_counter()
                    nextURL = f"{self.urlDomain}{nextURL}" if "https" not in nextURL else nextURL
                    allURLs = [val["URL"] for val in list(mainDict.values())]
                    try:
                        URLsubdir = re.search(r"(?<=wiki\/).+",nextURL).group()
                    except:
                        URLsubdir = ""
                        doAppend = False
                    if(doAppend):
                        if(not isValInIter(URLsubdir,allURLs)):
                            hasBannedWords = isIterInVal(nextURL,self.bannedWordsInLink)
                            isInNavRole = isValInIter(nextURL,currWikiArticle.find_all(role="navigation"))
                            isInImgDesc = isValInIter(nextURL,currWikiArticle.find_all(role="wikitable"))
                            isWantedURL = not hasBannedWords and not isInNavRole and not isInImgDesc
                            if(isWantedURL):
                                screen.refresh()
                                nextOpenedArticle = request.urlopen(nextURL,context=ssl._create_unverified_context())
                                nextWikiArticle = BeautifulSoup(nextOpenedArticle, "html.parser")
                                try:
                                    articleTitle = nextWikiArticle.find(class_="mw-page-title-main").text
                                except:
                                    articleTitle = None 
                                try:
                                    articleImg = f"https:{nextWikiArticle.find(class_='mw-file-element').get('src')}"
                                except:
                                    articleImg = None
                                try:
                                    articleTxt = nextWikiArticle.find(class_="mw-parser-output").p.text.replace("\\n","")
                                except:
                                    articleTxt = None
                                nextElKey = f"{currLayItems[currElIndex][0]},{realNextElIndex}"
                                mainDict[nextElKey] = dict(URL = nextURL, title = articleTitle, img = articleImg, txt = articleTxt)
                                if(constSave):
                                    file.write(f"{nextElKey} : {mainDict[nextElKey]}\n")
                                realNextElIndex += 1
                                endTime = time.perf_counter()
                            else:
                                unWantedURLs += 1
                        else:
                            unWantedURLs += 1
                    else:
                        unWantedURLs += 1
                    doAppend = True
                    endTime = time.perf_counter()
                    deltaTime = endTime - startTime
                    processSpeed += deltaTime
                    averageProcSpeed = format(processSpeed / float(1+totalScrapedURLs), ".4f")
                    displayMessage = f"[Current layer: {layer} | Scraping current article {currElIndex+1}/{len(currLayItems)} | Scraping next article {nextElIndex+1}/{len(nextLay)} | # unwanted URLs {unWantedURLs}/{len(nextLay)} | Average URL process speed {averageProcSpeed}]\n"
                    screen.addstr(layer+screenBuffer,0,displayMessage)
                    nextElIndex+=1
                    totalScrapedURLs+=1
                currElIndex+=1                  
            layer+=1
        file.close()
        screen.addstr(layer+screenBuffer,0,"\n")
        screen.refresh()
        # cur.echo()
        screen.getch()
        cur.endwin()
        self.resultDict = mainDict
        self.layers = layer
        self.resultItems = [list(item) for item in list(mainDict.items())]
        return mainDict

  
    def getLayer(self,targetLayer):
        self._isObjectScraped()
        targetLayer = int(targetLayer)
        allLayEls = [item for item in self.resultItems if  self._getNumAmount(item[0])-1 == targetLayer]
        self.returnedValue = allLayEls
        return allLayEls
    
    def getParents(self,originLayer,extraLayers = None):
        self._isObjectScraped()
        originLayer = int(originLayer)
        if(extraLayers == None):
            extraLayers = originLayer
        allParentEls = [item for item in self.resultItems if  self._getNumAmount(item[0])-1 < originLayer and self._getNumAmount(item[0])-1 >= originLayer-extraLayers]   
        self.returnedValue = allParentEls
        return allParentEls
                    
    def getChildren(self,originLayer,extraLayers = None):
        self._isObjectScraped()
        originLayer = int(originLayer)
        allChildEls = []
        if(extraLayers == None):
            allChildEls = [item for item in self.resultItems if  self._getNumAmount(item[0])-1 > originLayer]
        elif(type(extraLayers)==type(1)):    
            allChildEls = [item for item in self.resultItems if  self._getNumAmount(item[0])-1 > originLayer and self._getNumAmount(item[0])-1 <= originLayer+extraLayers]
        self.returnedValue = allChildEls
        return allChildEls
    
    def save(self, fileName, fileType = "txt", filePath = os.path.dirname(__file__), extraInfo = False):
        self._isObjectScraped()
        fileName = re.sub(r"[\s\.,\/]", '', fileName)
        resultKeys = list(self.resultDict.keys())
        resultVals = list(self.resultDict.values())
        fullFilePath = f"{filePath}{fileName}.{fileType}".replace(":","_")
        if(os.path.exists(fullFilePath)):
            os.remove(fullFilePath)
        file = open(fullFilePath,"x")
        file = open(fullFilePath,"a")
        if(fileType == "txt"):
            if(extraInfo):
                file.write(f"\n{fileName}\nExtraction of sublinks from '{self.startURL}' at {datetime.date.today()} {datetime.time}: \n\n")
            for itemIndex in range(len(self.resultDict)):
                file.write(f"{resultKeys[itemIndex]} : {resultVals[itemIndex]}\n")
        elif(fileType == "json"):
            file.write(json.dumps(self.resultDict))
        file.close()
        
    def plotlify(self):
        self._isObjectScraped()
        keysList = [item[0] for item in self.resultItems]
        pxElements = [item[1]["title"] for item in self.resultItems]
        pxParents = [""]
        pxParents[1:] = [self.resultDict[(lambda i : re.sub(r'(\,\d+|\d+)$','',i))(item[0])]["title"] for item in self.resultItems[1:]]
        pxValues = [1 for _ in self.resultItems]
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
        print(f"{vn.argname(f'values[{itemIndex}]')}: {values[itemIndex]}\n")
    

        
test = ScrapeLinks("https://de.wikipedia.org/wiki/Photon")
# z = test.scrape(10,constSave=True)
# test.getChildren(1)
# test.plotlify() 
os.abort()

dbPrint(test.returnedValue)

test.getLayer(1)

dbPrint(test.returnedValue)

test.getParents(2)

dbPrint(test.returnedValue)


    

       

