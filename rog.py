import curses
from curses import wrapper
#import keyboard

#keyboard.press('f11')



def ask_to_quit():
    curses.flash()


def main(stdscr):
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    maprow1 = []
    maprow2 = []
    maprow3 = []
    maprow4 = []
    maprow5 = []
    maprow6 = []
    maprow7 = []
    maprow8 = []
    maprow9 = []
    maprow10 = []
    maprow11 = []
    maprow12 = []
    maprow13 = []
    maprow14 = []
    maprow15 = []
    maprow16 = []
    maprow17 = []
    maprow18 = []
    maprow19 = []
    maprow20 = []
    mapcols = [maprow1,maprow2,maprow3,maprow4,maprow5,maprow6,maprow7,maprow8,maprow9,maprow10,maprow11,maprow12,maprow13,maprow14,maprow15,maprow16,maprow17,maprow18,maprow19,maprow20]
    for row in mapcols:
        for i in range(40):
            row.append('T') if i%2==0 else row.append('=')
    for row in mapcols:
        for sign in row:
            stdscr.addch(sign)
        stdscr.addstr('\n')
    y = 10
    x = 30
    stdscr.move(y,x)
#    stdscr.addstr("@")
    game = True
    while game:
        key = stdscr.getkey()
        if key == 'w':
            if y == 0 : continue
            y -= 1
            stdscr.addch(mapcols[y-1][x])
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 'a':
            if x == 0 : continue
            x -= 1
            stdscr.addch(mapcols[y-1][x-1])
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 's':
            #if y == rows -1 : continue
            if y == len(mapcols) -1 : continue
            y += 1
            stdscr.addch(mapcols[y-1][x])
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 'd':
            #if x == cols -1 : continue
            if x == len(maprow1) -1 : continue
            x += 1
            stdscr.addch(mapcols[y-1][x-1])
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)

        elif key == 'q':
            game = False

wrapper(main)

#import curses
#stdscr = curses.initscr()
#    stdscr.refresh()
#curses.has_colors()
#curses.start_color()
#curses.flash()
#curses.beep()
#curses.endwin()
