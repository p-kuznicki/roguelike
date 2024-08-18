from terrain import Door, Floor

import random as r

class Room():
    def __init__(self, y_min,x_min, y_max, x_max, door_h, door_v):
        self.height = r.randint(2, y_max-y_min-2)
        self.width = r.randint(2, x_max-x_min-2)
        self.start_y = r.randint(y_min+1, y_max-self.height-1)
        self.start_x = r.randint(x_min+1, x_max-self.width-1)
        self.end_y = self.start_y + self.height
        self.end_x = self.start_x + self.width
        
        if door_h == "bottom":
            self.door_h = Door(self.end_y, r.randint(self.start_x, self.end_x-1))
        elif door_h == "upper":
            self.door_h = Door(self.start_y-1, r.randint(self.start_x, self.end_x-1))
        if door_v == "right":
            self.door_v = Door(r.randint(self.start_y, self.end_y-1), self.end_x)
        elif door_v == "left":
            self.door_v = Door(r.randint(self.start_y, self.end_y-1), self.start_x-1)
        
        
    def carve_out(self, level, terrain):
        for y in range(self.start_y, self.end_y):
            for x in range(self.start_x, self.end_x):
                level.map[y][x] = terrain()
        level.map[self.door_h.y][self.door_h.x] = self.door_h
        level.map[self.door_v.y][self.door_v.x] = self.door_v
