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
        
        
    def generate_room(self):
        self.name = "random_room"
        room_height = random.randint(5,9)
        room_width = random.randint(5,9)
        room_start_y = random.randint(0,self.height-10)
        room_start_x = random.randint(0,self.width-10)
        room_end_y = room_start_y + room_height
        room_end_x = room_start_x + room_width
        while True:
            door_side = random.randint(0,3)
            if door_side == 0:
                 door_y, door_x = room_start_y, random.randint(room_start_x+1, room_end_x-1)
                 door_direction = (-1, 0)
            elif door_side == 1:
                 door_y, door_x = room_end_y, random.randint(room_start_x+1, room_end_x-1)
                 door_direction = (+1, 0)
            elif door_side == 2:
                 door_x, door_y = room_start_x, random.randint(room_start_y+1, room_end_y-1)
                 door_direction = (0, -1)
            elif door_side == 3:
                 door_x, door_y = room_end_x, random.randint(room_start_y+1, room_end_y-1)
                 door_direction = (0, +1)
            if not (door_y == 0 or door_y == self.height or door_x == 0 or door_x == self.width): break
        for y in range(self.height):   # generate map
            self.map.append([])
            for x in range(self.width):
               if y == door_y and x == door_x: self.map[y].append(Door())
               elif x > room_start_x and x < room_end_x and y > room_start_y and y < room_end_y:
                   self.map[y].append(Floor())
               else: self.map[y].append(Rock())
        i = 0
        while True:
            i += 1 
            y = door_y + i*door_direction[0]
            x = door_x + i*door_direction[1]
            if not self.is_beyond_map(y, x):
                self.map[y][x] = Floor()
            else: break
        
    def generate_2_rooms(self):                
        for y in range(self.height):   # fill the map with rocks
            self.map.append([])
            for x in range(self.width): self.map[y].append(Rock())
        
        room_height = random.randint(3,6)
        room_width = random.randint(3,6)
        room_start_y = random.randint(1,self.height//2-8)
        room_start_x = random.randint(1,(self.width//2)-8)
        room_end_y = room_start_y + room_height
        room_end_x = room_start_x + room_width
        
        for y in range(room_start_y,room_end_y+1):
            for x in range(room_start_x,room_end_x+1): self.map[y][x] = Floor()
            
        door1_y, door1_x = random.randint(room_start_y,room_end_y), room_end_x+1
        self.map[door1_y][door1_x] = Door()
        
        
        room_height = random.randint(3,6)
        room_width = random.randint(3,6)
        room_start_y = random.randint(1,self.height//2-8)
        room_start_x = random.randint(self.width//2,self.width-8)
        room_end_y = room_start_y + room_height
        room_end_x = room_start_x + room_width
        
        for y in range(room_start_y,room_end_y+1):
            for x in range(room_start_x,room_end_x+1): self.map[y][x] = Floor()
            
        door2_y, door2_x = random.randint(room_start_y,room_end_y), room_start_x-1
        self.map[door2_y][door2_x] = Door()
        
        turn_x = random.randint(door1_x+1,door2_x-1)
        for x in range(door1_x+1, turn_x+1):
            self.map[door1_y][x] = Floor()
            
        for x in range(turn_x,door2_x):
            self.map[door2_y][x] = Floor()
        
        if door1_y<door2_y: d =1
        else: d = -1 
        for y in range(door1_y,door2_y,d):
            self.map[y][turn_x] = Floor()
            
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
        
    def generate_4_rooms(self):
        self.fill_the_map(Rock)
        room00 = Room(0, 0, self.height//2, self.width//2, b=1, r=1)
        room01 = Room(0, self.width//2+1, self.height//2, self.width, b=1, l=1)
        room10 = Room(self.height//2+1, 0, self.height, self.width//2, u=1, r=1)
        room11 = Room(self.height//2+1, self.width//2+1, self.height, self.width, u=1, l=1)
        
        rooms = [room00, room01, room10, room11]
        for room in rooms:
            room.carve_out(self, Floor)
            
        self.connect_doors_horizontally(room00.door_r, room01.door_l)
        self.connect_doors_horizontally(room10.door_r, room11.door_l)
        self.connect_doors_vertically(room00.door_b, room10.door_u)
        self.connect_doors_vertically(room01.door_b, room11.door_u)
        
    def generate_9_rooms(self):
        self.fill_the_map(Rock)
        room00 = Room(0, 0, self.height//3, self.width//3, b=1, r=1)
        room01 = Room(0, self.width//3+1, self.height//3, 2*self.width//3, b=1, l=1, r=1)
        room02 = Room(0, 2*self.width//3+1, self.height//3, self.width, b=1, l=1)
        room10 = Room(self.height//3+1, 0, 2*self.height//3, self.width//3, b=1, u=1, r=1)
        room11 = Room(self.height//3+1, self.width//3+1, 2*self.height//3, 2*self.width//3, b=1, u=1, r=1, l=1)
        room12 = Room(self.height//3+1, 2*self.width//3+1, 2*self.height//3, self.width, b=1, u=1, l=1)
        room20 = Room(2*self.height//3+1, 0, self.height, self.width//3, u=1, r=1)
        room21 = Room(2*self.height//3+1, self.width//3+1, self.height, 2*self.width//3, u=1, r=1, l=1)
        room22 = Room(2*self.height//3+1, 2*self.width//3+1, self.height, self.width, u=1, l=1)
        
        rooms = [room00, room01, room02, room10, room11, room12, room20, room21, room22]
        for room in rooms:
            room.carve_out(self, Floor)
            
        self.connect_doors_horizontally(room00.door_r, room01.door_l)
        self.connect_doors_horizontally(room10.door_r, room11.door_l)
        self.connect_doors_horizontally(room20.door_r, room21.door_l)
        self.connect_doors_horizontally(room01.door_r, room02.door_l)
        self.connect_doors_horizontally(room11.door_r, room12.door_l)
        self.connect_doors_horizontally(room21.door_r, room22.door_l)
        
        self.connect_doors_vertically(room00.door_b, room10.door_u)
        self.connect_doors_vertically(room01.door_b, room11.door_u)
        self.connect_doors_vertically(room02.door_b, room12.door_u)
        self.connect_doors_vertically(room10.door_b, room20.door_u)
        self.connect_doors_vertically(room11.door_b, room21.door_u)
        self.connect_doors_vertically(room12.door_b, room22.door_u)

    def generate_9_rooms_alt(self):
    
        self.fill_the_map(Rock)
        
        rows = [0, self.height//3, 2*self.height//3, self.height]
        columns = [0, self.width//3, 2*self.width//3, self.width]
        
        rooms = []
        for r in range(3):
            rooms.append([])
            for c in range(3):
                rooms[r].append(Room(rows[r],columns[c],rows[r+1]-1,columns[c+1]-1))
        
        for y in range(3):
            for x in range(3):
                rooms[y][x].carve_out_alt(self, Floor, y, x)
                 
        for y in range(3):
            for x in range(2):
                self.connect_doors_horizontally(rooms[y][x].door_r, rooms[y][x+1].door_l)
                
        for y in range(2):
            for x in range(3):
                self.connect_doors_vertically(rooms[y][x].door_b, rooms[y+1][x].door_u)

    def generate_yx_rooms(self, max_y, max_x):
    
        self.fill_the_map(Rock)
        
        limits_y = []
        limits_x = []
        
        for i in range(max_y+1): limits_y.append(int(i*(self.height/max_y)))
            
        for i in range(max_x+1): limits_x.append(int(i*(self.width/max_x)))
        
        rooms = []
        for y in range(max_y):
            rooms.append([])
            for x in range(max_x):
                rooms[y].append(Room(limits_y[y], limits_x[x], limits_y[y+1]-1, limits_x[x+1]-1))
        
        for y in range(max_y):
            for x in range(max_x):
                rooms[y][x].carve_out_yx(self, Floor, y, x, max_y, max_x)
                 
        for y in range(max_y):
            for x in range(max_x-1):
                self.connect_doors_horizontally(rooms[y][x].door_r, rooms[y][x+1].door_l)
                
        for y in range(max_y-1):
            for x in range(max_x):
                self.connect_doors_vertically(rooms[y][x].door_b, rooms[y+1][x].door_u)


            
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


    
    #def remove_monster(self, monster):
    #    curses.beep()
    #    self.map[monster.y][monster.x].loot = Item(name = 'corpse', sign = '%')
    #    self.map[monster.y][monster.x].occupied = False
    #    self.monsters.remove(monster)
