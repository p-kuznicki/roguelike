from .item import Item


class Weapon(Item):
    def __init__(self, name, damage, two_handed=False, special=None):
        super().__init__(name=name, sign=")", category="weapon", appropriate_slot="weapon_hand", special=special)
        self.damage = damage
        self.two_handed = two_handed



class Short_Sword(Weapon):
    def __init__(self):
        super().__init__(name="short sword", damage = 6)

class Zweihander(Weapon):
    def __init__(self):
        super().__init__(name="zweihander!", damage = 10, two_handed = True)
        
class Murder_Mace(Weapon):
    def __init__(self):
        super().__init__(name="murder mace", damage=10, special=self.fewer_hp)

