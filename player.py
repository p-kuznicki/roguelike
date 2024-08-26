import curses
import random
import time

from color import get_col
from items import *

class Player():

    def __init__(self, name, to_hit, base_damage, defense, hp):
        self.name = name
        self.sign = '@'
        self.kills = 0
        self.inventory= [LightArmor(), ShortSword(), MurderMace(), HellfireStaff()]
        self.carry_limit = 10
        self.to_hit = to_hit
        self.unarmed = Fists()
        self.defense = defense
        self.initiative = 100
        
        self.hp = hp
        self.max_hp = hp
        self.regen_interval = 200/self.max_hp
        self.regen_counter = 0
 
        self.hit = False
        self.message = []
        self.attributes_changed = True
        self.changed_levels = False
        self.y = None
        self.x = None
        self.depth = 0
        
        class Equipment():
            def __init__(self, max_items = 1):
                self.slot = []
                self.max_items = max_items
                
        
        self.equipment = {
            "head": Equipment(),
            "neck": Equipment(),
            "body": Equipment(),
            "weapon_hand": Equipment(),
            "shield_hand": Equipment(),
            "rings": Equipment(max_items=2)}
        

                
    def move(self, level, y, x, map_win):
        ny = self.y + y
        nx = self.x + x
        if level.is_beyond_map(ny,nx) or level.map[ny][nx].solid: return
        elif level.map[ny][nx].occupied:
            monster = level.map[ny][nx].occupied
            # if there is a weapon in equipment slot used its attack
            if self.equipment["weapon_hand"].slot: self.equipment["weapon_hand"].slot[0].attack(level, monster, self, map_win)
            else: self.unarmed.attack(level, monster, self, map_win)
        else: 
            level.map[self.y][self.x].occupied = False
            self.y = ny
            self.x = nx
            level.map[self.y][self.x].occupied = self
            
            
    def bleed(self, map_win):
        curses.curs_set(0)
        map_win.addch(self.y, self.x, self.sign, get_col("red"))
        map_win.refresh()
        time.sleep(0.25)
        self.hit=False
        map_win.addch(self.y, self.x, self.sign)
        curses.curs_set(1)
        
    def regenerate(self):
        if self.hp < self.max_hp:
            self.regen_counter += 1
            if self.regen_counter >= self.regen_interval:
                self.hp += 1
                self.regen_counter -= self.regen_interval
                self.attributes_changed = True
                
    def try_to_identify(self, item):
        if not item.identified:
            if random.randint(1,100) <=2:
                item.identified = True
                item.name = item.full_name
                self.message.append(Message(f" You recognize {item.name}.", get_col("green")))
        
    def calculate_armor(self):
        armor = 0
        for item in self.inventory:
            if item.equipped and hasattr(item, "armor"):
                armor += item.armor
        return armor
        
    def look_move(self, level, status, map_win, message_win, y, x):
        map_win.move(y, x)
        if level.map[y][x].discovered:
            self.message.append(Message(f"{level.map[y][x].name} ", get_col("white")))
            if level.map[y][x].visible and level.map[y][x].occupied:
                self.message.append(Message(f"{level.map[y][x].occupied.name} ", get_col("white")))
            if level.map[y][x].visible and level.map[y][x].loot:
                for item in level.map[y][x].loot:
                    self.message.append(Message(f"{item.name} ", get_col("white")))    
            status.update_message(self, message_win)
        else: 
            self.message.append(Message("Unknown", get_col("white")))
            status.update_message(self, message_win)

        self.look(level, status, map_win, message_win, y, x)
        
    def look(self, level, status, map_win, message_win, y, x):
        key = map_win.getkey()
        if key == "w": self.look_move(level, status, map_win, message_win, y-1, x)
        elif key == "a": self.look_move(level, status, map_win, message_win, y, x-1)
        elif key == "s": self.look_move(level, status, map_win, message_win, y+1, x)
        elif key == "d": self.look_move(level, status, map_win, message_win, y, x+1)
        
    
    # DEPRECIATED        
    def get_loot(self, level): 
        if level.map[self.y][self.x].loot and len(self.inventory) >= self.carry_limit:
            self.message = (self.message or "") + "You carry too much!"
        elif len(level.map[self.y][self.x].loot) == 1:  #if there is only one item take it 
            level.items.remove(level.map[self.y][self.x].loot[0])
            self.inventory.append(level.map[self.y][self.x].loot[0])
            self.message = (self.message or "") + f" You pick up {level.map[self.y][self.x].loot[0].name}."
            del level.map[self.y][self.x].loot[0]

