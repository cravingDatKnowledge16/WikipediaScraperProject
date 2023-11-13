import urllib.request
from bs4 import BeautifulSoup
import array as arr
import re
import datetime

from numpy import iterable

obj = dict(name=1,tru=3,ihi=1)
objKeys = list(obj.items())
objInd = [x for x in enumerate(objKeys)]

def dictToList(dict):
    return [list(el) for el in list(dict.items())]

def dictNoDuplVal(dict):
    dictVal = list(dict.values())
    pass 

print(dictToList(obj))

print(set(list((11,2,5,676))))