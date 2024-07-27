import time
import curses
import random
from curses import wrapper

#import keyboard
#keyboard.press('f11')

#def ask_to_quit():
#    curses.flash()

class Terrain():
    def __init__(self, sign, solid=False):
        self.sign = sign
        self.solid = solid

        
class Monster():
    def __init__(self, sign):
        self.sign=sign
        
ground = Terrain(sign='_')
rock = Terrain(sign='#', solid=True) 
kobold = Monster(sign='k')


def main(stdscr):
    stdscr.clear()
#    stdscr.keypad(True)
#    stdscr.addstr("Press F11 to play...\n")
    
#    while True:
#        # Get user input
#        key = stdscr.getch()
         # Check if the key is F11
#        if key == 410:
#            break
    #rows, cols = stdscr.getmaxyx()
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
            row.append(['empty', rock]) if random.randint(0,3) == 0 else row.append(['empty',ground])
    stdscr.move(0,0)
    for row in mapcols:
        for terrain in row:
            stdscr.addch(terrain[1].sign)
        stdscr.addstr('\n')
        
    for i in range(7):
        my = random.randint(0,19)
        mx = random.randint(0,39)
        if mapcols[my][mx][1].solid == True or mapcols[my][mx][0] == 'occupied':
            continue
        else:
            stdscr.move(my,mx)
            stdscr.addch(kobold.sign)
            mapcols[my][mx][0] = 'occupied'
            
    while True:
        y = random.randint(0,19)
        x = random.randint(0,39)
        if mapcols[y][x][1].solid == True:
            continue
        else:
            stdscr.move(y,x)
            stdscr.addch("@")
            stdscr.move(y,x)
            break
            

   
    game = True
    while game:
        
        key = stdscr.getkey()
        if key == 'w':
            if y == 0 : continue
            if mapcols[y-1][x][1].solid==True: continue
            if mapcols[y-1][x][0] == 'occupied':
                mapcols[y-1][x][0] = 'empty'
                curses.beep()
                curses.flash()
                time.sleep(1)
                stdscr.move(y-1,x)
                stdscr.addch(mapcols[y-1][x][1].sign)
                stdscr.move(y,x)
                continue
            stdscr.addch(mapcols[y][x][1].sign)
            y -= 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 'a':
            if x == 0 : continue
            if mapcols[y][x-1][1].solid==True: continue
            if mapcols[y][x-1][0] == 'occupied':
                mapcols[y][x-1][0] = 'empty'
                curses.beep()
                stdscr.move(y,x-1)
                stdscr.addch(mapcols[y][x-1][1].sign)
                stdscr.move(y,x)
                continue
            stdscr.addch(mapcols[y][x][1].sign)
            x -= 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 's':
            #if y == rows -1 : continue
            
            if y == len(mapcols) -1 : continue
            if mapcols[y+1][x][1].solid==True: continue
            if mapcols[y+1][x][0] == 'occupied':
                mapcols[y+1][x][0] = 'empty'
                curses.beep()
                stdscr.move(y+1,x)
                stdscr.addch(mapcols[y+1][x][1].sign)
                stdscr.move(y,x)
                continue
            stdscr.addch(mapcols[y][x][1].sign)
            y += 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 'd':
            #if x == cols -1 : continue
            if x == len(maprow1) -1 : continue
            if mapcols[y][x+1][1].solid==True: continue
            if mapcols[y][x+1][0] == 'occupied':
                mapcols[y][x+1][0] = 'empty'
                curses.beep()
                stdscr.move(y,x+1)
                stdscr.addch(mapcols[y][x+1][1].sign)
                stdscr.move(y,x)
                continue
            stdscr.addch(mapcols[y][x][1].sign)
            x += 1
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
