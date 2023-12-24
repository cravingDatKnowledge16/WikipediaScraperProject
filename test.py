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
import time
import re

import timeit

def isValInIter(value,iter):
    for i in iter:
        if(value in i):
            return True
    return False

print(isValInIter("a",["pka","ikni"]))