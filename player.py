import curses
import random
import time

from items import *

class Player():

    def __init__(self, name, to_hit, base_damage, defense, hp):
        self.name = name
        self.sign = '@'
        self.kills = 0
        self.inventory= [ShortSword(), MurderMace(), HellfireStaff()]
        self.carry_limit = 10
        self.to_hit = to_hit
        self.unarmed = Fists()
        self.defense = defense
        
        self.hp = hp
        self.max_hp = hp
        self.regen_interval = 200/self.max_hp
        self.regen_counter = 0
 
        self.hit = False
        self.message = None
        self.attributes_changed = True
        self.changed_levels = False
        self.attack = self.default_attack
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
        
        
        
    # CURRENTLY UNUSED
    def default_attack(self, monster, level, player=None):   
        if random.randint(1,100) <= self.to_hit - monster.defense:
            self.message = (self.message or "") + f" You hit {monster.name}."
            monster.hp -= random.randint(1, self.damage)
            if monster.hp <= 0:
                self.message = (self.message or "") + f" You kill {monster.name}."
                self.kills += 1
                self.attributes_changed = True
                monster.die(level)
        else: self.message = (self.message or "") + f" You miss {monster.name}."
                
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
        map_win.addch(self.y, self.x, self.sign, curses.color_pair(4))
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
        
    
    # DEPRECIATED        
    def get_loot(self, level): 
        if level.map[self.y][self.x].loot and len(self.inventory) >= self.carry_limit:
            self.message = (self.message or "") + "You carry too much!"
        elif len(level.map[self.y][self.x].loot) == 1:  #if there is only one item take it 
            level.items.remove(level.map[self.y][self.x].loot[0])
            self.inventory.append(level.map[self.y][self.x].loot[0])
            self.message = (self.message or "") + f" You pick up {level.map[self.y][self.x].loot[0].name}."
            del level.map[self.y][self.x].loot[0]

