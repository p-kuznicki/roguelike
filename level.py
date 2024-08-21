import random
#import curses

from terrain import *
from room import Room
from monster import *
from items import *

class Level():

    def __init__(self, width, height, density=None):
        
        self.name = ''
        self.width = width
        self.height = height
        self.density = density
        self.map = []
        self.monsters = []
        self.items = []
        
            
    def connect_doors_horizontally(self, door1, door2):
        turn = random.randint(door1.x+1, door2.x-1)
        for x in range(door1.x+1, turn+1):
            self.map[door1.y][x] = Floor()
        for x in range(turn,door2.x):
            self.map[door2.y][x] = Floor()
        if door1.y<door2.y: d = 1
        else: d = -1 
        for y in range(door1.y, door2.y, d):
            self.map[y][turn] = Floor()
            
    def connect_doors_vertically(self, door1, door2):
        turn = random.randint(door1.y+1, door2.y-1)
        for y in range(door1.y+1, turn+1):
            self.map[y][door1.x] = Floor()
        for y in range(turn,door2.y):
            self.map[y][door2.x] = Floor()
        if door1.x<door2.x: d = 1
        else: d = -1 
        for x in range(door1.x, door2.x, d):
            self.map[turn][x] = Floor()
    

    def fill_the_map(self, Terrain):
        for y in range(self.height):
            self.map.append([])
            for x in range(self.width): self.map[y].append(Terrain())


    def generate_yx_rooms(self, max_y, max_x, skip=None):
    
        skip_these_rooms = []
        for i in range(min(max_y-1, max_x-1)):
            skip_these_rooms.append(str(random.randint(0,max_y-1))+str(random.randint(0,max_x-1)))
    
        self.fill_the_map(Rock)
        
        limits_y = []
        limits_x = []
        
        for i in range(max_y+1): limits_y.append(int(i*(self.height/max_y)))
            
        for i in range(max_x+1): limits_x.append(int(i*(self.width/max_x)))
        
        # create rooms with position and dimensions
        rooms = []
        for y in range(max_y):
            rooms.append([])
            for x in range(max_x):
                rooms[y].append(Room(limits_y[y], limits_x[x], limits_y[y+1]-1, limits_x[x+1]-1))
        
        # actually put the rooms on the map (also create and place doors) 
        for y in range(max_y):
            for x in range(max_x):
                rooms[y][x].carve_out_yx(self, Floor, y, x, max_y, max_x)
                
        # connect pairs of doors bottom to upper       
        for y in range(max_y-1):
            for x in range(max_x):
                if (str(y)+str(x) in skip_these_rooms) or (str(y+1)+str(x) in skip_these_rooms):
                    # wall up the doors instead
                    by, bx = rooms[y][x].door_b.y, rooms[y][x].door_b.x 
                    self.map[by][bx] = Rock()
                    uy, ux = rooms[y+1][x].door_u.y, rooms[y+1][x].door_u.x 
                    self.map[uy][ux] = Rock()
                    rooms[y+1][x].door_u, rooms[y][x].door_b = None, None
                else:
                    self.connect_doors_vertically(rooms[y][x].door_b, rooms[y+1][x].door_u)
                
        # connect pairs of doors right to left
        for y in range(max_y):
            for x in range(max_x-1):
                if (str(y)+str(x) in skip_these_rooms) or (str(y)+str(x+1) in skip_these_rooms):
                    # wall up the doors instead
                    self.map[rooms[y][x].door_r.y][rooms[y][x].door_r.x] = Rock()
                    self.map[rooms[y][x+1].door_l.y][rooms[y][x+1].door_l.x] = Rock()
                    rooms[y][x+1].door_l, rooms[y][x].door_r = None, None
                else:
                    # connect the doors
                    self.connect_doors_horizontally(rooms[y][x].door_r, rooms[y][x+1].door_l)
        
        rooms_without_doors = []            
        for y in range(max_y):
            for room in rooms[y]:
                if not (room.door_l or room.door_r or room.door_u or room.door_b):
                    rooms_without_doors.append(room)
                    
        for room in rooms_without_doors:
            for y in range(room.start_y, room.end_y):
                for x in range(room.start_x, room.end_x):
                    self.map[y][x] = Rock()
                    self.special_place = True
                    
                    
                   

            
    def generate_random_rock_map(self):
        
        self.name = "random_rock_map"
        
        for y in range(self.height):   # generate map
            self.map.append([])
            for x in range(self.width):
                if random.randint(1,100) <= self.density: self.map[y].append(Rock())
                elif random.randint(0,3) == 0: self.map[y].append(Tree())
                else: self.map[y].append(Grass())
                
        for i in range(self.width//2):   # generate monsters
            monster = Kobold()
            self.monsters.append(monster)
            self.random_place_agent(monster)
            
            #items = [Dummy_Ring(), Short_Sword(), Iron_Shield(), Light_Armor(), Life_Necklace(), Murder_Mace(), Zweihander()]
            #for item in items:
            #    self.random_place_item(item)
            #    self.items.append(item)
            
                    

               
    def draw_single(self, y, x, map_win):
        method = map_win.addch if (y+1, x+1) != (self.height, self.width) else map_win.insch
        terrain = self.map[y][x]
        if not terrain.discovered: method(y, x, ' ')
        elif terrain.visible and terrain.occupied: method(y,x,terrain.occupied.sign)
        elif terrain.visible and terrain.loot: method(y,x,terrain.loot[-1].sign)
        else: method(y,x,terrain.sign,terrain.color)                      
      
            
    def draw_all(self, rays, player, map_win):  # CURRENTLY UNUSED, may be useful later
    
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
        
        map_win.clear()		
        for y in range(self.height):  #draw whole map
            for x in range(self.width):
                self.draw_single(y,x, map_win)
            map_win.move(y+1,0)
            
    def draw_rectangle_area(self, map_win, height, width):
        for y in range(height):
            #map_win.move(y,0)
            for x in range(width):
                self.draw_single(y,x, map_win)
       
            
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
    
        
    def hide_this(self, obj, map_win):
        y, x = obj.y, obj.x
        if self.map[y][x].visible:  #dissapear visible object
            map_win.addch(y, x, self.map[y][x].sign, self.map[y][x].color)
                                 
    def random_place_item(self, item):
        while True:
            y = random.randint(0,self.height-1)
            x = random.randint(0,self.width-1)
            if self.map[y][x].solid: continue
            else:
                self.map[y][x].loot.append(item)
                item.y = y
                item.x = x
                break
 
    
    
    def random_place_agent(self, agent):
        while True:
            y = random.randint(0,self.height-1)
            x = random.randint(0,self.width-1)
            if self.is_space_unavaible(y,x): continue
            else:
                self.map[y][x].occupied = agent
                agent.y = y
                agent.x = x
                break


    def is_beyond_map(self, y, x):
        return y < 0 or x < 0 or y >= self.height or x >= self.width
        
    def is_space_unavaible(self,y,x):
    	return self.is_beyond_map(y,x) or self.map[y][x].solid or self.map[y][x].occupied
        
    def make_visible(self, y, x):
        self.map[y][x].discovered = True
        self.map[y][x].visible = True


