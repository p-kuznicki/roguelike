import random

class Player():

    def __init__(self, name):
        self.name = name
        self.sign = '@'
        self.y = None
        self.x = None
        self.inventory= []
        
                
    def move(self, level, y, x):
        ny = self.y + y
        nx = self.x + x
        if level.is_beyond_map(ny,nx) or level.map[ny][nx].solid: return
        elif level.map[ny][nx].occupied:
            #level.map[ny][nx].occupied.die(level)
            level.remove_monster(level.map[ny][nx].occupied)
        else: 
            level.map[self.y][self.x].occupied = False
            self.y = ny
            self.x = nx
            level.map[self.y][self.x].occupied = self
            
    def get_loot(self, level):
        if level.map[self.y][self.x].loot:
            self.inventory.append(level.map[self.y][self.x].loot)
            level.map[self.y][self.x].loot = False
    
