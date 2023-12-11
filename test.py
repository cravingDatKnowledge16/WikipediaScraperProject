from typing import LiteralString
import urllib.request
from bs4 import BeautifulSoup
import array as arr
import re
import datetime
import random
import string as st
import dis
import os


def _isLayPos(value):
    valStr = st.Formatter()
    print(valStr)
    val2 = valStr.isalnum()
    print(val2)
    return value.strip(",").isalnum()

print(_isLayPos("0,0,0"))
u = {
    "m":0,
    "r":1,
    "t":5
} 
print(3 in u.values())

os.abort()

def d():
    t = 3
    def a():
        nonlocal t
        t = 5
        def r():
            nonlocal t
   # t = 9
            print(t)
        r()
        print(t)
    a()
    print(t)
d()