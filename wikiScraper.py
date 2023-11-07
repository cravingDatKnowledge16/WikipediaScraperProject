import re
import numpy as np
import time
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import urllib.request
from bs4 import BeautifulSoup
import array 

url = input("Enter url: ")
openPage = urllib.request.urlopen(url)
preText = BeautifulSoup(openPage, "html.parser")

