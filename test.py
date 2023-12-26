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
import signal
import sys
import time
import threading


"""
def STORAGE():
    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        # sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')
    forever = threading.Event()
    forever.wait()
    print("lol")
    
"""


import asyncio

async def main():
    print('Hello ...')
    time.sleep(1)
    print('... World!')

asyncio.run(main())


def p(n):
    for i in range(n,10+n):
        print(i)
        
p(2)
p(3)
        
# asyncio.run(p(2))
# asyncio.run(p(5))
