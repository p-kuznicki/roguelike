import curses

class Terrain():
    def __init__(self, name, sign, color, solid=False, discovered=False, visible = False):
        self.name = name
        self.sign = sign
        self.color = color
        self.solid = solid
        self.discovered = discovered
        self.visible = visible
        self.occupied = False
        self.loot = []

class Grass(Terrain):
    def __init__(self):
        super().__init__(name = 'grass', sign = '\"', color = curses.color_pair(2))
        
class Tree(Terrain):
    def __init__(self):
        super().__init__(name = 'tree', sign = 'T', color = curses.color_pair(2))

        
class Rock(Terrain):
    def __init__(self):
        super().__init__(name = 'rock', sign = '#', color = curses.color_pair(1), solid = False)
        
class Floor(Terrain):
    def __init__(self):
        super().__init__(name = 'floor', sign = '.', color = curses.color_pair(1))

class Door(Terrain):
    def __init__(self, y=None, x=None):
        super().__init__(name = 'door', sign = '/', solid=False, color = curses.color_pair(4))
        self.y = y
        self.x = x
        
class Stairs(Terrain):
    def __init__(self, direction, y, x):
        self.y = y
        self.x = x
        if direction == "down" :
            self.sign = ">"
        else:
            self.sign = "<"
        
        super().__init__(name = 'stairs', sign = self.sign, color = curses.color_pair(1))
     
        
    def activate(self, player, levels):
        if self.sign == ">":
            levels[player.depth].go_down(player, levels)
        else: 
            levels[player.depth].go_up(player, levels)
        
