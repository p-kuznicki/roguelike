from terrain import Door, Floor

import random as ra

class Room():
    def __init__(self, y_min,x_min, y_max, x_max):
        self.height = ra.randint(2, y_max-y_min-2)
        self.width = ra.randint(2, x_max-x_min-2)
        self.start_y = ra.randint(y_min+1, y_max-self.height-1)
        self.start_x = ra.randint(x_min+1, x_max-self.width-1)
        self.end_y = self.start_y + self.height
        self.end_x = self.start_x + self.width
        #self.door_b = None
        #self.door_u = None
        #self.door_r = None
        #self.door_l = None
        

    
    def carve_out_yx(self, level, terrain, room_y, room_x, max_y, max_x):
    
        for y in range(self.start_y, self.end_y):
            for x in range(self.start_x, self.end_x):
                level.map[y][x] = terrain()
                
        if room_y != 0 :
            self.door_u = Door(self.start_y-1, ra.randint(self.start_x, self.end_x-1))
            level.map[self.door_u.y][self.door_u.x] = self.door_u
        if room_y != max_y-1 :
            self.door_b = Door(self.end_y, ra.randint(self.start_x, self.end_x-1))
            level.map[self.door_b.y][self.door_b.x] = self.door_b
        if room_x != 0 :
            self.door_l = Door(ra.randint(self.start_y, self.end_y-1), self.start_x-1)
            level.map[self.door_l.y][self.door_l.x] = self.door_l
        if room_x != max_x-1 : 
            self.door_r = Door(ra.randint(self.start_y, self.end_y-1), self.end_x)
            level.map[self.door_r.y][self.door_r.x] = self.door_r
