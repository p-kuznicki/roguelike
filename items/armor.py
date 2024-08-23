from .item import Item

class Armor(Item):
    def __init__(self, name, defense, appropriate_slot):
        super().__init__(name=name, sign="[", category="armor", appropriate_slot=appropriate_slot)
        self.defense = defense

class IronHelmet(Armor):
    def __init__(self):
        super().__init__(name="iron helmet", defense = 10, appropriate_slot= "head")

class LightArmor(Armor):
    def __init__(self):
        super().__init__(name="light armor", defense = 10, appropriate_slot= "body")
        
class IronShield(Armor):
    def __init__(self):
        super().__init__(name="iron shield", defense = 10, appropriate_slot= "shield_hand")
        
