class Item():
    def __init__(self, name, sign, category=None,  appropriate_slot=False, y=None, x=None):
        self.name=name
        self.sign=sign
        self.category=category
        self.appropriate_slot = appropriate_slot
        self.equipped = False
        self.y = y
        self.x = x
        

class Weapon(Item):
    def __init__(self, name, damage):
        super().__init__(name=name, sign=")", category="weapon", appropriate_slot="weapon_hand")
        self.damage = damage

class Armor(Item):
    def __init__(self, name, defense, appropriate_slot):
        super().__init__(name=name, sign="[", category="armor", appropriate_slot=appropriate_slot)
        self.defense = defense
            
class Short_Sword(Weapon):
    def __init__(self):
        super().__init__(name="short sword", damage = 6)       

class Iron_Helmet(Armor):
    def __init__(self):
        super().__init__(name="iron helmet", defense = 10, appropriate_slot= "head")

class Light_Armor(Armor):
    def __init__(self):
        super().__init__(name="light armor", defense = 10, appropriate_slot= "body") 
