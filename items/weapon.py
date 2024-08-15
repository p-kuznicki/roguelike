from .item import Item
import random


class Weapon(Item):
    def __init__(self, name, damage, two_handed=False, special=None, alternative_attack=None):
        super().__init__(name=name, sign=")", category="weapon", appropriate_slot="weapon_hand", special=special)
        self.damage = damage
        self.two_handed = two_handed
        self.alternative_attack = alternative_attack
        
    def alternate_attack(self, player, mode):
        if mode == "on":
            player.attack = self.alternative_attack
        else: player.attack = player.default_attack
        
    def double_strike(self, monster, level, player):
        if random.randint(1,100) <= player.to_hit - monster.defense:
            player.message = (player.message or "") + f" You hit {monster.name}."
            monster.hp -= random.randint(1, player.damage)
            if monster.hp <= 0:
                player.message = (player.message or "") + f" You kill {monster.name}."
                player.kills += 1
                player.attributes_changed = True
                monster.die(level)
            else:
                if random.randint(1,100) <= player.to_hit - monster.defense:
                    player.message = (player.message or "") + f" You hit {monster.name}."
                    monster.hp -= random.randint(1, player.damage)
                if monster.hp <= 0:
                    player.message = (player.message or "") + f" You kill {monster.name}."
                    player.kills += 1
                    player.attributes_changed = True
                    monster.die(level)
        else:
            player.message = (player.message or "") + f" You miss {monster.name}."
            if random.randint(1,100) <= player.to_hit - monster.defense:
                player.message = (player.message or "") + f" You hit {monster.name}."
                monster.hp -= random.randint(1, player.damage)
                if monster.hp <= 0:
                   player.message = (player.message or "") + f" You kill {monster.name}."
                   player.kills += 1
                   player.attributes_changed = True
                   monster.die(level)
        
class ShortSword(Weapon):
    def __init__(self):
        super().__init__(name="short sword", damage = 6)

class HellfireStaff(Weapon):
    def __init__(self):
        super().__init__(name="hellfire staff", damage = 10, two_handed = True)
        
class MurderMace(Weapon):
    def __init__(self):
        super().__init__(name="murder mace", damage=10, special=self.alternate_attack, alternative_attack=self.double_strike)

