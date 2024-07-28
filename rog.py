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
        self.loot = False

        
class Monster():
    def __init__(self, name, sign, y, x):
        self.name = name
        self.sign = sign
        self.corpse_sign = '%'
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
   # if y > len(mapcols) or y < 0 or x > len(maprow1) or x < 0: return True
    return y > (len(mapcols)-1) or y < 0 or x > (len(maprow1)-1) or x < 0 or mapcols[y][x].solid or mapcols[y][x].occupied


        
        

def main(stdscr):
    def move_random(monster):
        directiony = monster.y + random.randint(-1,1)
        directionx = monster.x + random.randint(-1,1)
        if not is_blocked(directiony, directionx):
            stdscr.move(monster.y, monster.x)
            stdscr.addch(mapcols[monster.y][monster.x].sign)            
            mapcols[monster.y][monster.x].occupied = False
            mapcols[directiony][directionx].occupied = True
            stdscr.move(directiony, directionx)
            stdscr.addch(monster.sign)
            monster.x = directionx
            monster.y = directiony
            stdscr.move(y,x)
    stdscr.clear()
    
#    stdscr.keypad(True)
#    stdscr.addstr("Press F11 to play...\n")
#    while True:
#        key = stdscr.getch()
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
            mapcols[y][x].occupied = monsters[-1]
            
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
            
    def kill_monster_at(y, x):
                curses.beep()
                mapcols[y][x].loot = mapcols[y][x].occupied.corpse_sign
                monsters.remove(mapcols[y][x].occupied)
                mapcols[y][x].occupied = False
                stdscr.move(y,x)
                stdscr.addch(mapcols[y][x].loot)
                
    def draw_ground_at(y, x):
        stdscr.addch(mapcols[y][x].loot) if mapcols[y][x].loot else stdscr.addch(mapcols[y][x].sign)
                        

   
    game = True
    while game:
        
        key = stdscr.getkey()
        if key == 'w':
            if y == 0 : continue
            if mapcols[y-1][x].solid: continue
            if mapcols[y-1][x].occupied:
                kill_monster_at(y-1, x)
                stdscr.move(y,x)
                continue
            draw_ground_at(y,x)
            y -= 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 'a':
            if x == 0 : continue
            if mapcols[y][x-1].solid: continue
            if mapcols[y][x-1].occupied:
                kill_monster_at(y, x-1)
                stdscr.move(y,x)
                continue
            draw_ground_at(y,x)
            x -= 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 's':
            #if y == rows -1 : continue
            
            if y == len(mapcols) -1 : continue
            if mapcols[y+1][x].solid: continue
            if mapcols[y+1][x].occupied:
                kill_monster_at(y+1, x)
                stdscr.move(y,x)
                continue
            draw_ground_at(y,x)
            y += 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)
        if key == 'd':
            #if x == cols -1 : continue
            if x == len(maprow1) -1 : continue
            if mapcols[y][x+1].solid==True: continue
            if mapcols[y][x+1].occupied:
                kill_monster_at(y, x+1)
                stdscr.move(y,x)
                continue
            draw_ground_at(y,x)
            x += 1
            stdscr.move(y,x)
            stdscr.addch('@')
            stdscr.move(y,x)

        elif key == 'q':
            game = False
            break
    
        for monster in monsters:
            if abs(monster.x - x) + abs(monster.y - y) > 5:
                move_random(monster)
                continue
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
            if directiony == y and  directionx == x: continue			      # if tries to go into player - do nothing
            if is_blocked(directiony, directionx):
                if x == directionx and not is_blocked(directiony, directionx+1):      # if is in the same column as player and diagonal right is open, go diag-right
                    directionx +=1
                elif x == directionx and not is_blocked(directiony, directionx-1):    # if is in the same column as player and diagonal left is open, go diag-left
                    directionx -=1
                elif y == directiony and not is_blocked(directiony+1, directionx):    # if is in the same row as player and diagonal down is open, go diag-down
                    directiony +=1
                elif y == directiony and not is_blocked(directiony-1, directionx):    # if is in the same row as player and diagonal up is open, go diag-up
                    directiony -=1
                elif directionx != x and directiony !=y and not is_blocked(directiony,x):  # if tries to go diagonal, and path along x axis is open go along x
                    directionx = monster.x
                elif directionx != x and directiony !=y and not is_blocked(y,directionx):  # if tries to go diagonal, and path along y axis is open go along y
                    directiony = monster.y
                else: continue								   # if non apply, do nothing	
            stdscr.move(monster.y, monster.x)
            #stdscr.addch(mapcols[monster.y][monster.x].sign)
            draw_ground_at(monster.y, monster.x)            
            mapcols[monster.y][monster.x].occupied = False
            mapcols[directiony][directionx].occupied = monster
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
