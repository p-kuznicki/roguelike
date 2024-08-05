import curses
import random
import math
from curses import wrapper
from fov_algo import Visual

TERRAIN_DENSITY = 3

####### RAY CREATION

visual = Visual(N=12, R=6)

rays = visual.create_rays()

#######

def main(stdscr):

##################################
####### CLASSES AND FUNCTIONS
##################################

    def is_beyond_map (y, x):
        return y < 0 or x < 0 or y >= len(mapcols) or x >= len(mapcols[0]) 

    def is_blocked (y,x):
        return is_beyond_map(y,x) or mapcols[y][x].solid or mapcols[y][x].occupied
        
    def visible (y,x):
        return abs(x - player.x) + abs(y - player.y) < 9
        
    def make_visible(y,x):
        mapcols[y][x].discovered = True
        mapcols[y][x].visible = True

    def check_visibility():
    
        for row in mapcols:         # reset visibility in the whole map            
            for terrain in row: terrain.visible = False
            
        for y in range(player.y-1, player.y+2):             # make terrain around player visible 
            for x in range(player.x-1, player.x+2):
                if not is_beyond_map(y,x): make_visible(y,x)
                            
        for ray in rays:
            for i in range(1, len(ray)):
                if not is_beyond_map(ray[i][0]+player.y,ray[i][1]+player.x) and not mapcols[ray[i-1][0]+player.y][ray[i-1][1]+player.x].solid:
    	            make_visible(ray[i][0]+player.y,ray[i][1]+player.x)
                else: break    
 

    def print_map():
        stdscr.move(0,0)
        for y, row in enumerate(mapcols):         # print map
            for terrain in row:
                if not terrain.discovered: stdscr.addch(' ')
                elif terrain.visible and terrain.occupied: stdscr.addch(terrain.occupied.sign)
                elif terrain.visible and terrain.loot: stdscr.addch(terrain.loot.sign)
                else:
                    if terrain.name == 'grass': stdscr.addch(terrain.sign, curses.color_pair(1))
                    elif terrain.name == 'rock': stdscr.addch(terrain.sign)
            stdscr.move(y+1,0)
    
    
    class Terrain():
    
        def __init__(self, name, sign, solid=False):
            self.name = name
            self.sign = sign
            self.solid = solid
            self.discovered = False
            self.visible = False
            self.occupied = False
            self.loot = False
            
        def draw_ground(self):
            stdscr.addch(self.loot.sign) if self.loot else stdscr.addch(self.sign)

        
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
        
        def draw_if_visible(self, y , x):
            if abs(x - player.x) + abs(y - player.y) < 13:
                stdscr.move(y, x)
                stdscr.addch(self.sign)
        
        def complete_movement(self, directiony, directionx):          
            mapcols[self.y][self.x].occupied = False
            mapcols[directiony][directionx].occupied = self
            self.x = directionx
            self.y = directiony
            
        def move_random(self):
            directiony = self.y + random.randint(-1,1)
            directionx = self.x + random.randint(-1,1)
            if not is_blocked(directiony, directionx): self.complete_movement(directiony, directionx)

        def get_closer(self):
            directionx = self.x                         # create direction and assume monster is on the same row as player
            if self.x > player.x: directionx -=1        # if player is on earlier row adjust direction by x-1
            elif self.x < player.x: directionx +=1      # if player is on later row adjust direction by x+1
            directiony = self.y                         # create direction and assume monster is on the same column as player
            if self.y > player.y: directiony -=1        # if player is on earlier column adjust direction by y-1
            elif self.y < player.y: directiony +=1      # if player is on later column adjust direction by y+1
            
            if directiony == player.y and  directionx == player.x: return	    	# if tries to go into player - do nothing... for now ]:->
            
            if is_blocked(directiony, directionx):					# if direct path blocked try other:
                if player.x == directionx and not is_blocked(directiony, directionx+1): directionx +=1          # if is in the same column as player and diagonal right is open, go diag-right   
                elif player.x == directionx and not is_blocked(directiony, directionx-1): directionx -=1        # if is in the same column as player and diagonal left is open, go diag-left
                elif player.y == directiony and not is_blocked(directiony+1, directionx): directiony +=1        # if is in the same row as player and diagonal down is open, go diag-down
                elif player.y == directiony and not is_blocked(directiony-1, directionx): directiony -=1        # if is in the same row as player and diagonal up is open, go diag-up
                elif directionx != player.x and directiony !=player.y and not is_blocked(directiony,x): directionx = self.x # if tries to go diagonal, and path along x axis is open go along x
                elif directionx != player.x and directiony !=player.y and not is_blocked(y,directionx): directiony = self.y # if tries to go diagonal, and path along y axis is open go along y
                else: return								                                    # if non apply, do nothing	
            self.complete_movement(directiony, directionx)
            
        def die(self):
            curses.beep()
            mapcols[self.y][self.x].loot = Item(name = 'corpse', sign = self.corpse_sign)
            monsters.remove(self)
            mapcols[self.y][self.x].occupied = False




    class Player():
    
        def __init__(self, y, x):
            self.y = y
            self.x = x
            self.sign = '@'
            self.inventory = []
            
        def move(self, modifier_y, modifier_x):
            new_y = self.y + modifier_y
            new_x = self.x + modifier_x
            if is_beyond_map(new_y, new_x) or mapcols[new_y][new_x].solid: return
            if mapcols[new_y][new_x].occupied:
                mapcols[new_y][new_x].occupied.die()
                return
            mapcols[self.y][self.x].occupied = False
            self.y = new_y
            self.x = new_x
            mapcols[self.y][self.x].occupied = self
            
        def get_loot(self):
            self.inventory.append(mapcols[self.y][self.x].loot)
            mapcols[self.y][self.x].loot = False


####################################
#### MAP SETUP
####################################


    stdscr.clear()
    
    mapcols = []		# generate map
    for i in range(20):
        mapcols.append([])
    
    for row in mapcols:         
        for i in range(40):
             row.append(Terrain(name = 'rock', sign='#', solid = True)) if random.randint(0,TERRAIN_DENSITY) == 0 else row.append(Terrain(name = 'grass', sign='\"'))
    stdscr.move(0,0)
    

    while True:                 # generate player and print
        y = random.randint(0,19)
        x = random.randint(0,39)
        if mapcols[y][x].solid or mapcols[y][x].occupied: continue
        else:
            player = Player(y,x)
            mapcols[y][x].occupied = player
            break
        
    monsters = []               # generate monsters and print if visible
    while len(monsters) < len(mapcols)/2:
        y = random.randint(0,len(mapcols)-1)
        x = random.randint(0,len(mapcols[0])-1)
        if mapcols[y][x].solid or mapcols[y][x].occupied: continue
        else:
            monsters.append(Monster(name='kobold', sign='k', y=y, x=x))
            mapcols[y][x].occupied = monsters[-1]           
            
      
#######################################                        
#####  MAIN GAME LOOP
#######################################
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
    game = True
    
    while game:
    
        check_visibility()
    
        print_map()
        
        stdscr.move(player.y, player.x) 	# center cursor on player
        
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
            if abs(monster.x - player.x) + abs(monster.y - player.y) > 3: monster.move_random()
            else: monster.get_closer()
       
wrapper(main)
