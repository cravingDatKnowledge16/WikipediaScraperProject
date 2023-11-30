from typing import LiteralString
import urllib.request
from bs4 import BeautifulSoup
import array as arr
import re
import datetime
import random
import string as st

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

print([1,4,2,9,0,4,6][:3])


def areObjectsInObject(value,checkList): 
    #returns True, if an object 
    return [word not in value for word in checkList].count(False) != 0

def areObjectsInObject2(value,checkList):
    #returns True, if an object 
    checkList = [word not in value or word == value for word in checkList]
    print(checkList)
    return checkList.count(False) != 0

# print(areObjectsInObject("/wiki/Hilfe:Wikimedia_Commons",["Datei:","Hilfe:","Wikipedia:","Spezial:","https://"]))

# print(areObjectsInObject2("/wiki/Hilfe:Wikimedia_Commons",["Datei:","Hilfe:","Wikipedia:","Spezial:","https://"]))
r = None
t = ["0," for i in range(4)]

print("".join(t))