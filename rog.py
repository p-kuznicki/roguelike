import time
import curses
import random
from curses import wrapper

#import keyboard
#keyboard.press('f11')

#def ask_to_quit():
#    curses.flash()

class Terrain():
    def __init__(self, name, sign, solid=False):
        self.name = name
        self.sign = sign
        self.solid = solid
        self.occupied = False

        
class Monster():
    def __init__(self, name, sign, y, x):
        self.name = name
        self.sign = sign
        self.y = y
        self.x = x
        
#ground = Terrain(sign='_')
#rock = Terrain(sign='#', solid=True) 
#kobold = Monster(sign='k')

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


def is_blocked (y,x):
    return mapcols[y][x].solid or mapcols[y][x].occupied  

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
    for row in mapcols:
        for i in range(40):
 #           row.append(['empty', rock]) if random.randint(0,3) == 0 else row.append(['empty',ground])
             row.append(Terrain(name = 'rock', sign='#', solid = True)) if random.randint(0,3) == 0 else row.append(Terrain(name = 'grass', sign='_', solid=False))
    stdscr.move(0,0)
    for row in mapcols:
        for terrain in row:
            stdscr.addch(terrain.sign)
        stdscr.addstr('\n')
    monsters = []
    while len(monsters) < 7:
        y = random.randint(0,19)
        x = random.randint(0,39)
        if mapcols[y][x].solid == True or mapcols[y][x].occupied == True:
            continue
        else:
            monsters.append(Monster(name='kobold', sign='k', y=y, x=x))
            stdscr.move(y,x)
            stdscr.addch(monsters[-1].sign)
            mapcols[y][x].occupied = True
            
    while True:
        y = random.randint(0,19)
        x = random.randint(0,39)
        if mapcols[y][x].solid == True:
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
            if mapcols[y-1][x].solid: continue
            if mapcols[y-1][x].occupied:
                mapcols[y-1][x].occupied = False
                curses.beep()
                curses.flash()
                time.sleep(1)
                stdscr.move(y-1,x)
                stdscr.addch(mapcols[y-1][x].sign)
                stdscr.move(y,x)
                continue
            stdscr.addch(mapcols[y][x].sign)
            y -= 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 'a':
            if x == 0 : continue
            if mapcols[y][x-1].solid: continue
            if mapcols[y][x-1].occupied:
                mapcols[y][x-1].occupied = False
                curses.beep()
                stdscr.move(y,x-1)
                stdscr.addch(mapcols[y][x-1].sign)
                stdscr.move(y,x)
                continue
            stdscr.addch(mapcols[y][x].sign)
            x -= 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 's':
            #if y == rows -1 : continue
            
            if y == len(mapcols) -1 : continue
            if mapcols[y+1][x].solid: continue
            if mapcols[y+1][x].occupied:
                mapcols[y+1][x].occupied = False
                curses.beep()
                stdscr.move(y+1,x)
                stdscr.addch(mapcols[y+1][x].sign)
                stdscr.move(y,x)
                continue
            stdscr.addch(mapcols[y][x].sign)
            y += 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 'd':
            #if x == cols -1 : continue
            if x == len(maprow1) -1 : continue
            if mapcols[y][x+1].solid==True: continue
            if mapcols[y][x+1].occupied:
                mapcols[y][x+1].occupied = False
                curses.beep()
                stdscr.move(y,x+1)
                stdscr.addch(mapcols[y][x+1].sign)
                stdscr.move(y,x)
                continue
            stdscr.addch(mapcols[y][x].sign)
            x += 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)

        elif key == 'q':
            game = False
            break
    
        for monster in monsters:
            directionx = monster.x
            if monster.x > x:
                directionx -=1
            if monster.x < x:
                directionx +=1
            directiony = monster.y
            if monster.y > y:
                directiony -=1
            if monster.y < y:
                directiony +=1
            if directiony == y and  directionx == x: continue
            if is_blocked(directiony, directionx):
                if x == directionx and not is_blocked(directiony, directionx+1):
                    directionx +=1
                elif x == directionx and not is_blocked(directiony, directionx-1):
                    directionx -=1
                elif y == directiony and not is_blocked(directiony+1, directionx):
                    directiony +=1
                elif y == directiony and not is_blocked(directiony-1, directionx):
                    directiony -=1
                elif directionx != x and directiony !=y and not is_blocked(directiony,x):
                    directionx = monster.x
                elif directionx != x and directiony !=y and not is_blocked(y,directionx):
                    directiony = monster.y
                else: continue
            stdscr.move(monster.y, monster.x)
            stdscr.addch(mapcols[monster.y][monster.x].sign)            
            mapcols[monster.y][monster.x].occupied = False
            mapcols[directiony][directionx].occupied = True
            stdscr.move(directiony, directionx)
            stdscr.addch(monster.sign)
            monster.x = directionx
            monster.y = directiony
            stdscr.move(y,x)
             
 
            
        
        

wrapper(main)

#import curses
#stdscr = curses.initscr()
#    stdscr.refresh()
#curses.has_colors()
#curses.start_color()
#curses.flash()
#curses.beep()
#curses.endwin()
