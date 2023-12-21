import time as T
import curses as C


string = "niofnrenvner"
lstring = len(string)


S = C.initscr()
S.addstr(0,0,f"{string}\n")
S.getch()
C.endwin()
