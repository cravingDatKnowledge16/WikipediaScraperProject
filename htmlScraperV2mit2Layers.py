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
                tempFile.close

def extractLinksRecursivly(start_element,layerDepth):
    
    #extracts the sublinks of a Wikipedia-link recusively
    
    allPreLayers_getPos = "0"
    preLayElemPos_writeNextLay = list()
    preLayElemPos_writeNextLay.append(0)
    preLayAllKeys_knowParentKeys = list()
    preLayAllValues_knowParentValues = list()
    HREFmatrix_writeSublinks = list()
    mainDict = dict()
    mainDict[allPreLayers_getPos] = start_element
    for currLayer in range(layerDepth): #for every layer do:
        mainDictItems = [list(item) for item in list(mainDict.items())]
        preLayAllItems_knowItemParents = [item for item in mainDictItems if (extractNumberAmount(item[0]) == currLayer+1)]
        preLayAllKeys_knowParentKeys = [item[0] for item in preLayAllItems_knowItemParents]
        preLayAllValues_knowParentKeys = [item[1] for item in preLayAllItems_knowItemParents]
    
        #return preLayAllKeys_knowParentKeys
      
        #scrape the links from the previous layer and write them onto a temporary matrix
        for currPositionOfPre_layer_elements in preLayElemPos_writeNextLay:
            HREFmatrix_writeSublinks[currPositionOfPre_layer_elements] = scrapeLinks(preLayAllKeys_knowParentKeys[currPositionOfPre_layer_elements])
            
        HREFmatrix_writeSublinks = [scrapeLinks(preLayElemPos_writeNextLay[preEl]) for preEl in preLayElemPos_writeNextLay]
        #copy all links from current layer onto the main dictionairies 
        for preLayerHREF_element_index in range(len(HREFmatrix_writeSublinks)):
            for currLayerHREF_element_index in HREFmatrix_writeSublinks[preLayerHREF_element_index]:
                if(currLayerHREF_element_index):
                    mainDict[allPreLayers_getPos+f",{preLayerHREF_element_index}"+f",{currLayerHREF_element_index}"] = HREFmatrix_writeSublinks[preLayerHREF_element_index][currLayerHREF_element_index]
        #eliminate all duplicates to avoid recursion collision         
        for mainDict_items in list(mainDict.items()):
            mainDict_item_count = list(mainDict.values()).count(mainDict_items[1])
            if(mainDict_item_count >= 2): #if a value occurs more than 2 times
                toPopIndices = [i for i, x in enumerate(preLayAllKeys_knowParentKeys) if x == mainDict_items[0]]
                for popElement in toPopIndices:
                    mainDict.pop(popElement)
                
        allPreLayers_getPos+=",0"
        preLayElemPos_writeNextLay = range(len(HREFmatrix_writeSublinks))
        preLayAllKeys_knowParentKeys = list()
        HREFmatrix_writeSublinks = list()

                
def extractNumberAmount(text):
    allNumbers = re.findall(r"\d+",str(text))
    return len(allNumbers)

def listToString(list):
    return re.sub(r"[\s\[\]]","",str(list))
print(listToString(list((1,98,28,"njue"))))
#file = open('saveValues.txt', 'r')

print(extractLinksRecursivly("fbirbi",2))

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
