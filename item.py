class Item():
    def __init__(self, name, sign, equipment=False, y=None, x=None):
        self.name=name
        self.sign=sign
        self.equipment = equipment
        self.equipped = False
        self.y = y
        self.x = x
        

class Weapon(Item):
    def __init__(self, name, damage):
        super().__init__(name=name, sign=")", equipment="weapon_arm")
        self.damage = damage
            
class Short_Sword(Weapon):
    def __init__(self):
        super().__init__(name="short sword", damage = 6)       
   
