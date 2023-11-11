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

    open_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(open_page, "html.parser")
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
    with open(f'results/{newTopDoc}.txt', 'w') as temp_file:
            for item in wantedLinksList:
                temp_file.write("%s\n"                                                       % item)
                temp_file.close

def extractFromDictRecursivly(start_element,layerDepth):
    allPre_layers = "0"
    pre_layer_elementsPositions = list((0))
    currLayerElement_key_list = list()
    currLayerHREF_list = list()
    mainDict = dict()
    mainDict[pre_layer_elementsPositions] = start_element
    for currLayer in range(layerDepth): #for every layer do:
        mainDict_keys = list(mainDict.keys()) #copy every key from mainDict to the list mainDict_keys

        for mainDict_key_index in range(len(mainDict_keys)): #for every key from the main dict do:
            if(extractNumberAmount(mainDict_keys[mainDict_key_index]) == currLayer+1): 
                currLayerElement_key_list.append(mainDict_keys[mainDict_key_index]) #create a list for every element of the main dict, who's key indicates the same layer depth as the current layer we are on 

        for currPositionOfPre_layer_elements in pre_layer_elementsPositions:
            currLayerHREF_list[currPositionOfPre_layer_elements] = scrapeLinks(currLayerElement_key_list[currPositionOfPre_layer_elements])
        for preLayerHREF_element_index in range(len(currLayerHREF_list)):
            for currLayerHREF_element_index in currLayerHREF_list[preLayerHREF_element_index]:
                mainDict[allPre_layers+f",{preLayerHREF_element_index}"+f",{currLayerHREF_element_index}"] = currLayerHREF_list[preLayerHREF_element_index][currLayerHREF_element_index]
        allPre_layers+=",0"
        pre_layer_elementsPositions = range(len(currLayerHREF_list))

                
def extractNumberAmount(text):
    allNumbers = re.findall(r"\d+",str(text))
    return len(allNumbers)

def listToString(list):
    return re.sub(r"[\s\[\]]","",str(list))

#file = open('saveValues.txt', 'r')

#layer1 = scrapeLinks("https://de.wikipedia.org/wiki/Chaos_Computer_Club")
#print(layer1)
#for element in range(len(layer1)):
#    saveToTXT(scrapeLinks(f"https://de.wikipedia.org{layer1[element]}"), layer1[element])
obj = {
    "1":"tzt",
    "3":"jkjl"
}

print(extractNumberAmount("9079,083,9,1542,23"))
for x in obj:
    print(x)
#extractFromDictRecursivly("hoirhoifh",2)
