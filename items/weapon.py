from .item import Item
import random


class Weapon(Item):
    def __init__(self, name, damage, two_handed=False, attack=None, special=None):
        super().__init__(name=name, sign=")", category="weapon", appropriate_slot="weapon_hand", special=special)
        self.damage = damage
        self.two_handed = two_handed
        if attack == None: self.attack = self.standard_attack
        else: self.attack = attack
        
        
    def hit_and_damage(self, monster, player):
        if random.randint(1,100) <= player.to_hit - monster.defense:
            player.message = (player.message or "") + f" You hit {monster.name}."
            monster.hp -= random.randint(1, self.damage)
    
    def death_check(self, level, monster, player):
        if monster.hp <= 0:
            player.message = (player.message or "") + f" You kill {monster.name}."
            player.kills += 1
            player.attributes_changed = True
            monster.die(level)
            return True
    
    def standard_attack(self, level, monster, player):
        self.hit_and_damage(monster, player)
        self.death_check(level, monster, player)
        
    def double_strike(self, level, monster, player):
        self.hit_and_damage(monster, player)
        if not self.death_check(level, monster, player):
            self.hit_and_damage(monster, player)
            self.death_check(level, monster, player)
        
class Fists(Weapon):
    def __init__(self):
        super().__init__(name="fists", damage = 2)        

class ShortSword(Weapon):
    def __init__(self):
        super().__init__(name="short sword", damage = 6)

class HellfireStaff(Weapon):
    def __init__(self):
        super().__init__(name="hellfire staff", damage = 10, two_handed = True)
        
class MurderMace(Weapon):
    def __init__(self):
        super().__init__(name="murder mace", damage=10, attack=self.double_strike)

