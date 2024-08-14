class Item():
    def __init__(self, name, sign, category=None,  appropriate_slot=None, special=None, y=None, x=None):
        self.name=name
        self.sign=sign
        self.category=category
        self.appropriate_slot = appropriate_slot
        self.special = special
        self.equipped = False
        self.y = y
        self.x = x
        
    def extra_hp(self, mode, player):
        if mode == "on":
            player.hp +=10
        else: player.hp -=10
        
    def fewer_hp(self, mode, player):
        if mode == "on":
            player.hp -=5
        else: player.hp +=5
        

class Weapon(Item):
    def __init__(self, name, damage, two_handed=False, special=None):
        super().__init__(name=name, sign=")", category="weapon", appropriate_slot="weapon_hand", special=special)
        self.damage = damage
        self.two_handed = two_handed

class Armor(Item):
    def __init__(self, name, defense, appropriate_slot):
        super().__init__(name=name, sign="[", category="armor", appropriate_slot=appropriate_slot)
        self.defense = defense
        
class Necklace(Item):
    def __init__(self, name, special):
        super().__init__(name=name, sign="&", category="necklace", appropriate_slot="neck", special=special)
            
class Short_Sword(Weapon):
    def __init__(self):
        super().__init__(name="short sword", damage = 6)

class Zweihander(Weapon):
    def __init__(self):
        super().__init__(name="zweihander!", damage = 10, two_handed = True)
        
class Murder_Mace(Weapon):
    def __init__(self):
        super().__init__(name="murder mace", damage=10, special=self.fewer_hp)


class Iron_Helmet(Armor):
    def __init__(self):
        super().__init__(name="iron helmet", defense = 10, appropriate_slot= "head")

class Light_Armor(Armor):
    def __init__(self):
        super().__init__(name="light armor", defense = 10, appropriate_slot= "body")
        
class Iron_Shield(Armor):
    def __init__(self):
        super().__init__(name="iron shield", defense = 10, appropriate_slot= "shield_hand")
        
        
class Life_Necklace(Necklace):
    def __init__(self):
        super().__init__(name="life necklace", special=self.extra_hp)
        
class Dummy_Ring(Item):
    def __init__(self):
        super().__init__(name="dummy_ring", sign = "=", category="ring",  appropriate_slot="rings")
