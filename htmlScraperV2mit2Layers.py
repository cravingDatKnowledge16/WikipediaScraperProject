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
    
    allPre_layers = "0"
    pre_layer_elementsPositions = list()
    pre_layer_elementsPositions[0] = 0
    preLayerAllKeys = list()
    preLayerAllValues = list()
    currLayerHREF_matrix = list()
    mainDict = dict()
    mainDict[pre_layer_elementsPositions] = start_element
    for currLayer in range(layerDepth): #for every layer do:
        mainDict_keys = list(mainDict.keys()) #copy every key from mainDict to the list mainDict_keys

        for mainDict_key_index in range(len(mainDict_keys)): #for every key from the main dict do:
            if(extractNumberAmount(mainDict_keys[mainDict_key_index]) == currLayer+1): 
                preLayerAllKeys.append(mainDict_keys[mainDict_key_index]) #create a list for every element of the main dict, who's key indicates the same layer depth as the current layer we are on 
        for mainDict_key_index in preLayerAllKeys:
            preLayerAllValues.append(mainDict.get(mainDict_key_index))
        for currPositionOfPre_layer_elements in pre_layer_elementsPositions:
            currLayerHREF_matrix[currPositionOfPre_layer_elements] = scrapeLinks(preLayerAllKeys[currPositionOfPre_layer_elements])
            
        for preLayerHREF_element_index in range(len(currLayerHREF_matrix)):
            for currLayerHREF_element_index in currLayerHREF_matrix[preLayerHREF_element_index]:
                if(currLayerHREF_element_index):
                    mainDict[allPre_layers+f",{preLayerHREF_element_index}"+f",{currLayerHREF_element_index}"] = currLayerHREF_matrix[preLayerHREF_element_index][currLayerHREF_element_index]
                    
        for mainDict_items in list(mainDict.items()):
            mainDict_item_count = list(mainDict.values()).count(mainDict_items[1])
            if(mainDict_item_count >= 2): #if a value occurs more than 2 times
                toPopIndices = [i for i, x in enumerate(preLayerAllKeys) if x == mainDict_items[0]]
                for popElement in toPopIndices:
                    mainDict.pop(popElement)
                
        allPre_layers+=",0"
        pre_layer_elementsPositions = range(len(currLayerHREF_matrix))
        preLayerAllKeys = list()
        currLayerHREF_matrix = list()

                
def extractNumberAmount(text):
    allNumbers = re.findall(r"\d+",str(text))
    return len(allNumbers)

def listToString(list):
    return re.sub(r"[\s\[\]]","",str(list))
print(listToString(list((1,98,28,"njue"))))
#file = open('saveValues.txt', 'r')

#layer1 = scrapeLinks("https://de.wikipedia.org/wiki/Chaos_Computer_Club")
#print(layer1)
#for element in range(len(layer1)):
#    saveToTXT(scrapeLinks(f"https://de.wikipedia.org{layer1[element]}"), layer1[element])

obj = dict((name=213,un="ufeu"))
"""
print(extractNumberAmount("9079,083,9,1542,23"))
for x in obj:
    print(x)
#extractFromDictRecursivly("hoirhoifh",2)
"""
