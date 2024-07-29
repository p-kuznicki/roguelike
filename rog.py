import curses
import random
from curses import wrapper

def main(stdscr):

##################################
####### CLASSES AND FUNCTIONS
##################################

    mapcols = []
    for i in range(20):
        mapcols.append([])

    def is_solid (y,x):
        return y > (len(mapcols)-1) or y < 0 or x > (len(mapcols[0])-1) or x < 0 or mapcols[y][x].solid

    def is_blocked (y,x):
          return y > (len(mapcols)-1) or y < 0 or x > (len(mapcols[0])-1) or x < 0 or mapcols[y][x].solid or mapcols[y][x].occupied

    class Terrain():
        def __init__(self, name, sign, solid=False):
            self.name = name
            self.sign = sign
            self.solid = solid
            self.occupied = False
            self.loot = False
        
    class Item():
         def __init__(self, name, sign):
             self.name = name
             self.sign = sign

    class Monster():
        def __init__(self, name, sign, y, x):
            self.name = name
            self.sign = sign
            self.corpse_sign = '%'
            self.y = y
            self.x = x
            
        def complete_movement(self, directiony, directionx):
            stdscr.move(self.y, self.x)
            stdscr.addch(mapcols[self.y][self.x].sign)            
            mapcols[self.y][self.x].occupied = False
            mapcols[directiony][directionx].occupied = self
            stdscr.move(directiony, directionx)
            stdscr.addch(self.sign)
            self.x = directionx
            self.y = directiony
            stdscr.move(player.y,player.x)
            
        def move_random(self):
            directiony = self.y + random.randint(-1,1)
            directionx = self.x + random.randint(-1,1)
            if not is_blocked(directiony, directionx): self.complete_movement(directiony, directionx)

        def get_closer(self):
            directionx = self.x                         # assume monster is on the same row as player
            if self.x > player.x: directionx -=1        # if player is on earlier row adjust direction by -1
            if self.x < player.x: directionx +=1        # if player is on later row adjust direction by +1
            directiony = self.y                         # assume monster is on the same column as player
            if self.y > player.y: directiony -=1        # if player is on earlier column adjust direction by -1
            if self.y < player.y: directiony +=1        # if player is on later column adjust direction by +1
            if directiony == player.y and  directionx == player.x: return	    # if tries to go into player - do nothing
            if is_blocked(directiony, directionx):
                if player.x == directionx and not is_blocked(directiony, directionx+1): directionx +=1          # if is in the same column as player and diagonal right is open, go diag-right   
                elif player.x == directionx and not is_blocked(directiony, directionx-1): directionx -=1        # if is in the same column as player and diagonal left is open, go diag-left
                elif player.y == directiony and not is_blocked(directiony+1, directionx): directiony +=1        # if is in the same row as player and diagonal down is open, go diag-down
                elif player.y == directiony and not is_blocked(directiony-1, directionx): directiony -=1        # if is in the same row as player and diagonal up is open, go diag-up
                elif directionx != player.x and directiony !=player.y and not is_blocked(directiony,x): directionx = self.x # if tries to go diagonal, and path along x axis is open go along x
                elif directionx != player.x and directiony !=player.y and not is_blocked(y,directionx): directiony = self.y # if tries to go diagonal, and path along y axis is open go along y
                else: return								                                                    # if non apply, do nothing	
            self.complete_movement(directiony, directionx)

    def kill_monster_at(y, x):
                curses.beep()
                mapcols[y][x].loot = Item(name = 'corpse', sign = mapcols[y][x].occupied.corpse_sign)
                monsters.remove(mapcols[y][x].occupied)
                mapcols[y][x].occupied = False
                stdscr.move(y,x)
                stdscr.addch(mapcols[y][x].loot.sign)
                
    def draw_ground_at(y, x):
        stdscr.addch(mapcols[y][x].loot.sign) if mapcols[y][x].loot else stdscr.addch(mapcols[y][x].sign)
    
    class Player():
        def __init__(self, y, x):
            self.y = y
            self.x = x
            self.sign = '@'
            self.inventory = []
        def move(self, modifier_y, modifier_x):
            new_y = self.y + modifier_y
            new_x = self.x + modifier_x
            if is_solid(new_y, new_x): return
            if mapcols[new_y][new_x].occupied:
                kill_monster_at(new_y, new_x)
                stdscr.move(self.y,self.x)
                return
            draw_ground_at(self.y,self.x)
            self.y = new_y
            self.x = new_x
            stdscr.move(self.y,self.x)
            stdscr.addch(self.sign)
            stdscr.move(self.y,self.x)
        def get_loot(self):
            self.inventory.append(mapcols[self.y][self.x].loot)
            mapcols[self.y][self.x].loot = False

####################################
#### MAP SETUP
####################################

    stdscr.clear()
    
    for row in mapcols:         # generate map
        for i in range(40):
             row.append(Terrain(name = 'rock', sign='#', solid = True)) if random.randint(0,3) == 0 else row.append(Terrain(name = 'grass', sign='_', solid=False))
    stdscr.move(0,0)
    
    for row in mapcols:         # print map
        for terrain in row:
            stdscr.addch(terrain.sign)
        stdscr.addch('\n')
        
    monsters = []               # generate monsters
    while len(monsters) < 7:
        y = random.randint(0,19)
        x = random.randint(0,39)
        if mapcols[y][x].solid == True or mapcols[y][x].occupied == True: continue
        else:
            monsters.append(Monster(name='kobold', sign='k', y=y, x=x))
            stdscr.move(y,x)
            stdscr.addch(monsters[-1].sign)
            mapcols[y][x].occupied = monsters[-1]
            
    while True:                 # generate player
        y = random.randint(0,19)
        x = random.randint(0,39)
        if mapcols[y][x].solid == True:
            continue
        else:
            player = Player(y,x)
            stdscr.move(player.y, player.x)
            stdscr.addch(player.sign)
            stdscr.move(player.y,player.x)
            break
            

#######################################                        
#####  MAIN GAME LOOP
#######################################

    game = True
    
    while game:
        
        key = stdscr.getkey()
        if key == 'e' and mapcols[player.y][player.x].loot: player.get_loot()          
        if key == 'w': player.move(-1, 0)
        if key == 'a': player.move(0, -1)
        if key == 's': player.move(1, 0)
        if key == 'd': player.move(0, 1)
        if key == 'q':
            game = False
            break
    
        for monster in monsters:
            if abs(monster.x - player.x) + abs(monster.y - player.y) > 5: monster.move_random()
            else: monster.get_closer()
       
wrapper(main)

