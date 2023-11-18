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

print(range(len([1,4,2,5])))

def test(value):
    return ("/wiki/" in value) & ("Datei:" not in value) & ("Hilfe:" not in value) & ("Wikipedia:" not in value) & ("Spezial:" not in value) & ("https:" not in value)

def test2(value):
    bannedWords = ["t","i","o"]
    return [el not in value for el in bannedWords].count(False) != 0

print(test2("tno"))


list = [[0,1],[89,5],[20,7]]

print([enumerate(el) for el in list])