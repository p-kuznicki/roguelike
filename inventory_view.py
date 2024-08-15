import curses

class Inventory_view():
    def __init__(self):
        self.width = 40
        self.key_to_index = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8, "j":9}
        self.index_to_key = list(self.key_to_index.keys()) 
    
    def display_items(self, item_list, map_win, start_column):
        for y, item in enumerate(item_list):
            map_win.move(y+start_column, 0)
            for x in range(self.width): map_win.addch(' ', curses.color_pair(3))
            map_win.addstr(y+start_column, 0, self.index_to_key[y] + ") "+ item.name, curses.color_pair(3))
        curses.curs_set(0)
    
    def get_item(self, item, level, loot, player):
        level.items.remove(item)
        player.inventory.append(item)
        player.message = (player.message or "") + f" You pick up {item.name}."
        loot.remove(item)
    
        
    def try_to_get_item(self, map_win, player, level):
        loot = level.map[player.y][player.x].loot
        if loot and len(player.inventory) >= player.carry_limit:
            player.message = (player.message or "") + "You carry too much!"
        elif len(loot) == 1:                            
            self.get_item(loot[0], level, loot, player)
        elif len(loot) > 1:
            map_win.addstr(0, 0, "Choose item to pick up:", curses.color_pair(3)) 
            self.display_items(loot, map_win, start_column=1)
            key = map_win.getkey()
            if key in self.key_to_index and self.key_to_index[key] < len(loot):
                self.get_item(loot[self.key_to_index[key]], level, loot, player)               
            level.draw_rectangle_area(map_win, len(loot)+2, self.width)  # redraw map
            curses.curs_set(1)
        else: player.message = (player.message or "") + "There is nothing here."

    def equip_or_remove(self, item, player):

        equipment =  player.equipment[item.appropriate_slot]
        if item.equipped:
            equipment.slot.remove(item)
            if item.appropriate_slot=="weapon_hand" and item.two_handed: player.equipment["shield_hand"].slot.remove(item)
            item.equipped = False
            if item.category == "armor": player.defense = player.defense - item.defense
            if item.special: item.special(player, "off")
            player.attributes_changed = True
            item.name = item.name[0:-11]  		# remove " (equipped)" from item name
            instruction = f"You put away {item.name}."
        elif len(equipment.slot) < equipment.max_items:
            if item.appropriate_slot=="weapon_hand" and item.two_handed: 
                if player.equipment["shield_hand"].slot: return "unequip a shield first."
                else: player.equipment["shield_hand"].slot.append(item)
            equipment.slot.append(item)
            item.equipped = True
            if item.category == "armor": player.defense = player.defense + item.defense
            if item.special: item.special(player, "on")
            player.attributes_changed = True
            instruction = f"You equipped {item.name}."
            item.name = item.name + " (equipped)"
        else:
            instruction = "unequip an item first."
        return instruction
            
        
    def open(self, map_win, player, level, instruction):
        map_win.addstr(0, 0, instruction, curses.color_pair(3))
        map_win.addstr(1, 0, "press a-j to (un)equip", curses.color_pair(3))
        map_win.addstr(2, 0, "press A-J to drop", curses.color_pair(3))
        self.display_items(player.inventory, map_win, start_column=3)
        key = map_win.getkey()
        if key in self.key_to_index and self.key_to_index[key] < len(player.inventory):
            item = player.inventory[self.key_to_index[key]]
            if item.appropriate_slot:
                instruction = self.equip_or_remove(item, player) #equip or unequip item, then return instruction
                self.open(map_win, player, level, instruction)
            elif item.usable:
                item.special(player)
                player.inventory.remove(item)
            else: self.open(map_win, player, level, "You don't know how to use that.")
            
        if key == key.upper() and key.lower() in self.key_to_index and self.key_to_index[key.lower()] < len(player.inventory):
            item = player.inventory[self.key_to_index[key.lower()]]
            if item.equipped: self.open(map_win, player, level, "Unequip this item first!!")
            else:
                level.items.append(item)
                level.map[player.y][player.x].loot.append(item)
                player.inventory.remove(item)
                player.message = (player.message or "") + f"You dropped {item.name}"
        level.draw_rectangle_area(map_win, len(player.inventory)+4, self.width) # redraw map
        curses.curs_set(1)
        
        
      
