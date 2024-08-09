import random
import curses

from terrain import Terrain
from monster import Monster
from item import Item

class Level():

    def __init__(self, name, width=40, height=20, density=25):
        
        self.name = name
        self.width = width
        self.height = height
        self.density = density
        self.map = []
        self.monsters = []
        
        for y in range(height):
            self.map.append([])
            for x in range(width):
                if random.randint(1,100) <= self.density:
                    self.map[y].append(Terrain(name = 'rock', sign='#', solid = True))
                else:
                    self.map[y].append(Terrain(name = 'grass', sign='\"'))
                    
                    
    def draw_single(self, y, x, map_win):
        terrain = self.map[y][x]
        if not terrain.discovered: map_win.addch(y, x, ' ')
        elif terrain.visible and terrain.occupied: map_win.addch(y,x,terrain.occupied.sign)
        elif terrain.visible and terrain.loot: map_win.addch(y,x,terrain.loot.sign)
        else:
            if terrain.name == 'grass': map_win.addch(y,x,terrain.sign, curses.color_pair(1))
            else: map_win.addch(y,x,terrain.sign)                    
                    
    def check_visibility(self, rays, player):
    
        for row in self.map:         # reset visibility to False for the whole map            
            for terrain in row: terrain.visible = False
            
        for y in range(player.y-1, player.y+2):      # make terrain adjencent to player visible 
            for x in range(player.x-1, player.x+2):
                if not self.is_beyond_map(y,x): self.make_visible(y,x)
                            
        for ray in rays:			# check visibility in concentric rays from player position, stop when solid
            for i in range(1, len(ray)):
                if not self.is_beyond_map(ray[i][0]+player.y,ray[i][1]+player.x) and not self.map[ray[i-1][0]+player.y][ray[i-1][1]+player.x].solid:
    	            self.make_visible(ray[i][0]+player.y,ray[i][1]+player.x)
                else: break          
                
            
    def draw(self, map_win):
        map_win.clear()
        for row in (self.map):
            for terrain in row:
                if not terrain.discovered: map_win.addch(' ')
                elif terrain.visible and terrain.occupied: map_win.addch(terrain.occupied.sign)
                elif terrain.visible and terrain.loot: map_win.addch(terrain.loot.sign)
                else:
                    if terrain.name == 'grass': map_win.addch(terrain.sign, curses.color_pair(1))
                    else: map_win.addch(terrain.sign)
            map_win.addch('\n')    # map_win.move(y+1,0)
            
    def draw_visible(self, rays, player, map_win):
           
        for row in self.map:         # reset visibility to False for the whole map            
            for terrain in row: terrain.visible = False
            
        for y in range(player.y-1, player.y+2):      # make terrain adjencent to player visible AND DRAW IT
            for x in range(player.x-1, player.x+2):
                if not self.is_beyond_map(y,x):
                    self.make_visible(y,x)
                    self.draw_single(y,x, map_win)
                            
        for ray in rays:			# check visibility in concentric rays from player position, THEN DRAW, stop when solid
            for i in range(1, len(ray)):
                if not self.is_beyond_map(ray[i][0]+player.y,ray[i][1]+player.x) and not self.map[ray[i-1][0]+player.y][ray[i-1][1]+player.x].solid:
    	            self.make_visible(ray[i][0]+player.y, ray[i][1]+player.x)
    	            self.draw_single(ray[i][0]+player.y, ray[i][1]+player.x, map_win)
                else: break
        

    def random_place(self, agent):
        while True:
            y = random.randint(0,self.height-1)
            x = random.randint(0,self.width-1)
            #if self.map[y][x].solid or self.map[y][x].occupied: continue
            if self.is_space_unavaible(y,x): continue
            else:
                self.map[y][x].occupied = agent
                agent.y = y
                agent.x = x
                break
                
    def generate_monsters(self):
        for i in range(self.width//2):
            monster = Monster(name='kobold', sign='k')
            self.monsters.append(monster)
            self.random_place(monster)
    
            
    def is_beyond_map(self, y, x):
        return y < 0 or x < 0 or y >= self.height or x >= self.width
        
    def is_space_unavaible(self,y,x):
    	return self.is_beyond_map(y,x) or self.map[y][x].solid or self.map[y][x].occupied
        
    def make_visible(self, y, x):
        self.map[y][x].discovered = True
        self.map[y][x].visible = True


    
    #def remove_monster(self, monster):
    #    curses.beep()
    #    self.map[monster.y][monster.x].loot = Item(name = 'corpse', sign = '%')
    #    self.map[monster.y][monster.x].occupied = False
    #    self.monsters.remove(monster)
