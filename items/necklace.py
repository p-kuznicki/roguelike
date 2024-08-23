from .item import Item


class Necklace(Item):
    def __init__(self, name, special):
        super().__init__(name=name, full_name=None, sign="&", category="necklace", appropriate_slot="neck", special=special)
            

        
class Life_Necklace(Necklace):
    def __init__(self):
        super().__init__(name = "ruby necklace", full_name="life necklace", special=self.extra_hp)
