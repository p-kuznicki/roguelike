import random


class Item():
    def __init__(self, name, sign, category=None,  appropriate_slot=None, special=None, usable=False, y=None, x=None):
        self.name=name
        self.sign=sign
        self.category=category
        self.appropriate_slot = appropriate_slot
        self.special = special
        self.usable = usable
        self.equipped = False
        self.y = y
        self.x = x
        
    def extra_hp(self, player, mode):
        if mode == "on":
            player.hp +=10
        else: player.hp -=10
        
    def fewer_hp(self, player, mode):
        if mode == "on":
            player.hp -=5
        else: player.hp +=5
        
    def food(self, player):
        gain = random.randint(1,3)
        player.hp += gain
        player.message = (player.message or "") + f"You eat and recover {gain} hp. "
        player.attributes_changed = True
        

class Corpse(Item):
    def __init__(self, name, y, x):
        super().__init__(name=name, sign="%", special=self.food, usable=True, y=y, x=x)


