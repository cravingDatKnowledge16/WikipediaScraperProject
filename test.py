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
import curses
from time import sleep
import re

# file_dir = os.path.dirname(os.path.realpath('__file__'))
# file = os.path.join(file_dir,"results/TETETE.txt")

if(True):
    x = 9
print(x)


os.abort()

def d():
    t = 3
    def a():
        nonlocal t
        t = 3
        def r():
            nonlocal t
   # t = 9
            print(t)
        r()
        print(t)
    a()
    print(t)
d()