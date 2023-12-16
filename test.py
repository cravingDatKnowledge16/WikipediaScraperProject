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
func = 5


print(t := 0)

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