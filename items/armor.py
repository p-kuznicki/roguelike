from .item import Item

class Armor(Item):
    def __init__(self, name, armor, appropriate_slot):
        super().__init__(name=name, sign="[", category="armor", appropriate_slot=appropriate_slot)
        self.armor = armor

class IronHelmet(Armor):
    def __init__(self):
        super().__init__(name="iron helmet", armor = 1, appropriate_slot= "head")

class LightArmor(Armor):
    def __init__(self):
        super().__init__(name="light armor", armor = 1, appropriate_slot= "body")
        
class IronShield(Armor):
    def __init__(self):
        super().__init__(name="iron shield", armor = 2, appropriate_slot= "shield_hand")
        
