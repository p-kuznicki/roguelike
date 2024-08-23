from .item import Item


        
class Dummy_Ring(Item):
    def __init__(self):
        super().__init__(name="dummy ring", sign = "=", category="ring",  appropriate_slot="rings")
