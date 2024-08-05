class Terrain():
    def __init__(self, name, sign, solid=False, discovered=False, visible = False):
        self.name = name
        self.sign = sign
        self.solid = solid
        self.discovered = discovered
        self.visible = visible
        self.occupied = False
        self.loot = False
        
   
#       def draw_ground(self):
#            stdscr.addch(self.loot.sign) if self.loot else stdscr.addch(self.sign)
