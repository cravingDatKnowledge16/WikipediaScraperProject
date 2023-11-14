from ast import For
import imp
from os import error
import urllib
from bs4 import BeautifulSoup
import array as arr
import re
import time
import sys
from requests import HTTPError
import colorama
from colorama import Fore, Style

errorCounter = 0
#from multiprocessing import Pool, cpu_count
#p = Pool

zeitpunkt1 = time.perf_counter()
def scrapeLinks(url):
    linkArray = []

    try:
        open_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(open_page, "html.parser")

        mw_parser_output = soup.find_all(class_="mw-parser-output")

        for element in mw_parser_output:
            for a_tag in element.findAll('a', href=True):
                linkVar = a_tag['href']
                linkArray.append(linkVar)
    except urllib.error.HTTPError:
        print(Fore.RED + f"Couldn't load {url}, skipping file.")
        errorCounter = errorCounter+1
        return []

    #verbotene Worte: Datei||Hilfe||Wikipedia||Spezial

    wantedLinks = set([link for link in linkArray if (("Datei:" not in link) & ("/wiki/" in link) & ("Hilfe:" not in link) & ("Wikipedia:" not in link) & ("Spezial:" not in link) & ("https:" not in link))])
    wantedLinksList = list(wantedLinks)
    
    return wantedLinksList


def saveToTXT(wantedLinksList, topDoc):
    newTopDoc = re.sub('[^a-zA-Z0-9 \n\.]', '_', topDoc)
    with open(f'results/{newTopDoc}.txt', 'w') as temp_file:
            for item in wantedLinksList:
                temp_file.write("%s\n"                                                       % item)
                temp_file.close


def scrapeLinksNotOrdered(numberOfTimes, startLink):
    #Arrays erstellen
    currentLinkArray = []
    previousLinkArray = []
    globalLinkSet = set()
    previousLinkArray.append(startLink)
    globalLinkSet.add(startLink)
    numberOfScrapedLinks = 0
    
    #Äußere for Schleife pro Layer: 
    for i in range(0, numberOfTimes):
        #Alle Links aus den in der vorherigen Layer gescrapeden
        #Websites nacheinander auswählen
        for prevLink in previousLinkArray:
            print(f"[Layer {i+1}/{numberOfTimes}, schon {numberOfScrapedLinks} von {len(previousLinkArray)} mal] " + Fore.BLUE + f"{prevLink}" + Fore.WHITE)
            temp = scrapeLinks(f"https://de.wikipedia.org{prevLink}")
            numberOfScrapedLinks = numberOfScrapedLinks+1
            #Den einzelnen Link mit dem globalLinkArray abgleichen,
            #wenn er nicht schon drin ist, wird er hinzugefügt:
            for temp_entry in temp:
                if temp_entry not in globalLinkSet:
                    currentLinkArray.append(temp_entry)
                    globalLinkSet.add(temp_entry)
        #current in previous pushen
        previousLinkArray = currentLinkArray.copy()
        currentLinkArray = []
        numberOfScrapedLinks = 0
    saveToTXT(globalLinkSet, "ScraperV3Result-no1")


scrapeLinksNotOrdered(2, "/wiki/New_Urbanism")
zeitpunkt2 = time.perf_counter()
print(f"Dauer: {zeitpunkt2-zeitpunkt1} Fehler: {errorCounter} ({round((zeitpunkt2-zeitpunkt1)/60, ndigits=3)}min)")