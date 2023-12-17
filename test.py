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

t = curses.initscr()

t.addstr(0,0,"tnietnbuiluivenuiveruv")
t.refresh()
curses.endwin()


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