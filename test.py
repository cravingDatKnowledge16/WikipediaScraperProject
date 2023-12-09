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


t = z = o = 2
print(t)

z=0
print(t)

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