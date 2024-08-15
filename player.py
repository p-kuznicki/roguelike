import random
from items import *

class Player():

    def __init__(self, name, to_hit, base_damage, defense, hp):
        self.name = name
        self.sign = '@'
        self.kills = 0
        self.inventory= [ShortSword(), MurderMace(), HellfireStaff()]
        self.carry_limit = 10
        self.to_hit = to_hit
        self.base_damage = base_damage
        self.damage = base_damage
        self.defense = defense
        self.hp = hp
        self.weapon_arm = None
        self.message = None
        self.attributes_changed = True
        self.attack = self.default_attack
        self.y = None
        self.x = None
        
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
                
    def move(self, level, y, x):
        ny = self.y + y
        nx = self.x + x
        if level.is_beyond_map(ny,nx) or level.map[ny][nx].solid: return
        elif level.map[ny][nx].occupied:
            self.attack(level.map[ny][nx].occupied, level, self)
            #level.map[ny][nx].occupied.die(level)
            #level.remove_monster(level.map[ny][nx].occupied)
            #self.kills += 1
        else: 
            level.map[self.y][self.x].occupied = False
            self.y = ny
            self.x = nx
            level.map[self.y][self.x].occupied = self
            
    def get_loot(self, level):  # CURRENTLY UNUSED
        if level.map[self.y][self.x].loot and len(self.inventory) >= self.carry_limit:
            self.message = (self.message or "") + "You carry too much!"
        elif len(level.map[self.y][self.x].loot) == 1:  #if there is only one item take it 
            level.items.remove(level.map[self.y][self.x].loot[0])
            self.inventory.append(level.map[self.y][self.x].loot[0])
            self.message = (self.message or "") + f" You pick up {level.map[self.y][self.x].loot[0].name}."
            del level.map[self.y][self.x].loot[0]

