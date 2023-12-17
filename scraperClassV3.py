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
# import consolemenu







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
    
    def scrape(self, layerDepth = None, maxReadLinks = None, maxLinksPerLay = None):
        #scrapes a given link recursively, if the layerDepth is not defined as an integer in the parameter, the link will be scraped, until the next layer in the structure has no more elements
        
        #declaration of local functions
        def isInIter(value,iter):
            result = [i in value for i in iter].count(False) != 0
            return result
        
        #printing important information
        print(format("{_>80}\n"))
        print(f"Scraping of '{self.startURL}' at {datetime.datetime.now()} initiated...")
        print(f"layerDepth: {layerDepth}, maxReadLinks: {maxReadLinks}, maxLinksPerLay: {maxLinksPerLay}")
        # initiation of important variables
        self.isScraped = True
        startTime = time.perf_counter()
        mainDict = dict()
        allLinksCounter = 1
        layerConditions = {
            "0":lambda a,b : a < b,
            "1":lambda a,b : True
        }
        layerCondition = 1 if layerDepth >= 0 else 0
        #open and access the wanted Wikipedia Article
        currOpenedArticle = request.urlopen(self.startURL,context=ssl._create_unverified_context())
        wikipediaArticleHTML = BeautifulSoup(currOpenedArticle, "html.parser")
        #create and setup the dictionary
    
        firstEntryArticleTitle = wikipediaArticleHTML.find(class_="mw-page-title-main").text
        firstEntryDescImg = f"https:{wikipediaArticleHTML.find(class_='mw-file-element').get('src')}"
        firstEntryDescTxt = wikipediaArticleHTML.find(class_='mw-parser-output').p.text
        mainDict["0"] = dict(URL = self.startURL ,title=firstEntryArticleTitle,ArticleImg=firstEntryDescImg,ArticleTxt=firstEntryDescTxt)
        # initiate scraping
        layer = 0
        while(layerConditions[f"{layerCondition}"](layer,layerDepth)):  
            print(f"Current layer: {layer} | Working on layer: {layer+1}")
            #get items of current layer
            mainDictItems = [list(item) for item in list(mainDict.items())]
            currLayItems = [item for item in mainDictItems if self._getNumAmount(item[0]) == layer+1]
            if(len(currLayItems) == 0):
                break
            #create the items for the next layer
            layerItemCounter = 1
            currElIndex = 0
            for currURL in currLayItems:
                print(f"    Open current article number {currElIndex}...")
                currURL = str(currURL[1]['URL'])
                try:
                    currOpenedArticle = request.urlopen(currURL,context=ssl._create_unverified_context())
                except:
                    print("End of link structure has been reached")
                    return None 
                print(f"    Extract data...")
                currWikiArticle = BeautifulSoup(currOpenedArticle, "html.parser")
                nextURLContainer = currWikiArticle.find(class_="mw-parser-output")
                nextLay = [iterURL["href"] for iterURL in nextURLContainer.find_all("a",href=True)]
                maxReadLinks = maxReadLinks if maxReadLinks >= 0 else len(nextLay)
                nextElIndex = 0
                print(f"    Check next article number {nextElIndex}...")
                for nextURL in nextLay[:maxReadLinks]:
                    nextURL = f"{self.urlDomain}{nextURL}" if "https" not in nextURL else nextURL
                    print(f"        '{nextURL}' already exists?")
                    if(isInIter(nextURL,[val["URL"] for val in list(mainDict.values())])):
                        print(f"        Does not exist!")
                        print(f"            Is wanted article?")
                        # dbPrint(nextURL)
                        hasWantedWords = "/wiki/" in nextURL
                        # dbPrint(hasWantedWords)
                        hasBannedWords = [word in nextURL for word in self.bannedWordsInLink].count(True) != 0
                        # dbPrint(hasBannedWords)
                        isInNavRole = nextURL in str(currWikiArticle.find_all(role="navigation"))
                        # dbPrint(isInNavRole)
                        isInImgDesc = nextURL in str(currWikiArticle.find_all(class_="wikitable"))
                        # dbPrint(isInImgDesc)
                        isWantedURL = hasWantedWords and not hasBannedWords and not isInNavRole and not isInImgDesc
                        # dbPrint(isWantedURL)
                        if(isWantedURL):
                            print(f"            Is wanted!")
                            print(f"                Opening next article number {nextElIndex}")
                            nextOpenedArticle = request.urlopen(nextURL,context=ssl._create_unverified_context())
                            nextWikiArticle = BeautifulSoup(nextOpenedArticle, "html.parser")
                            print(f"                Extracting data...")
                            try:
                                articleTitle = nextWikiArticle.find(class_="mw-Article-title-main").text
                            except:
                                articleTitle = None 
                            try:
                                articleImg = f"https:{nextWikiArticle.find(class_='mw-file-element').get('src')}"
                            except:
                                articleImg = None
                            try:
                                articleTxt = nextWikiArticle.find(class_="mw-parser-output").p.text
                            except:
                                articleTxt = None
                            #print(f"   All processed URL: {allArticlesCounter} | Current scraped link: {layerItemCounter}/{len(currLayItems)}")
                            print(f"                Adding to main dict...")
                            nextElKey = f"{currLayItems[currElIndex][0]},{nextElIndex}"
                            mainDict[nextElKey] = dict(URL = nextURL, title = articleTitle, img = articleImg, txt = articleTxt)
                            print(f"                Done!")
                        else:
                            print(f"            Not wanted!")
                    else:
                        print(f"        Already exists!")
                    nextElIndex+=1
                currElIndex+=1                  #if the next layer doesn't contain any items, stop execution of this function and return the main dictionary and the layer, at which point execution was stopped
            layer+=1
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
                file.write(f"\n{fileName}\nExtraction of sublinks from '{self.startURL}' at {datetime.date.today()} {datetime.time}: \n\n")
            for itemIndex in range(len(self.resultDict)):
                file.write(f"{resultKeys[itemIndex]} : {resultVals[itemIndex]}\n")
        elif(fileType == "json"):
            file.write(json.dumps(self.resultDict))
        file.close()
        
    def plotlify(self):
        self._isObjectScraped()
        keysList = [item[0] for item in self.resultItems]
        pxElements = [item[1]["ArticleTitle"] for item in self.resultItems]
        pxParents = [""]
        pxParents[1:] = [self.resultDict[(lambda i : re.sub(r'(\,\d+|\d+)$','',i))(item[0])]["articleTitle"] for item in self.resultItems[1:]]
        pxValues = [1 for _ in range(len(self.resultItems))]
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


    

       

