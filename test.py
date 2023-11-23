import urllib.request
from bs4 import BeautifulSoup
import array as arr
import re
import datetime

from numpy import iterable

obj = dict(name=1,tru=3,ihi=1)
objKeys = list(obj.items())
objInd = [x for x in enumerate(objKeys)]


#print(dictToList(obj))

#print(range(len([1,4,2,5])))

def test(value):
    return ("/wiki/" in value) or ("Datei:" not in value) or ("Hilfe:" not in value) or ("Wikipedia:" not in value) or ("Spezial:" not in value) or ("https:" not in value)

def test2(value):
    bannedWords = ["t","i","o"]
    return [el not in value for el in bannedWords].count(False) != 0

#print(test2("tno"))




def areObjectsInObject(value,checkList):
    #returns True, if an object 
    return [word not in value for word in checkList].count(False) != 0

print(areObjectsInObject("de.wikipedia.org/wiki/Universum",["Datei:","Hilfe:","Wikipedia:","Spezial:","https://"]))

list = [[0,1],[89,5],[20,7]]

print([enumerate(el) for el in list])