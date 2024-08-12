import curses

class Inventory_view():
    def __init__(self, inventory, width):
        self.width = width
        self.key_to_index = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8, "j":9}
        self.index_to_key = list(self.key_to_index.keys()) 
    
    def display_items(self, item_list, map_win):
        for y, item in enumerate(item_list):
            map_win.move(y+1, 0)
            for x in range(self.width): map_win.addch(' ', curses.color_pair(3))
            map_win.addstr(y+1, 0, self.index_to_key[y] + ") "+ item.name, curses.color_pair(3))
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
            self.display_items(loot, map_win)
            key = map_win.getkey()
            if key in self.key_to_index and self.key_to_index[key] < len(loot):
                self.get_item(loot[self.key_to_index[key]], level, loot, player)               
            level.draw_rectangle_area(map_win, len(loot)+2, self.width)  # redraw map
            curses.curs_set(1)
        else: player.message = (player.message or "") + "There is nothing here."
        
        
    def open(self, map_win, player, level):
        map_win.addstr(0, 0, "Inventory", curses.color_pair(3))
        self.display_items(player.inventory, map_win)
        key = map_win.getkey()
        if key in self.key_to_index and self.key_to_index[key] < len(player.inventory):
            item = player.inventory[self.key_to_index[key]]
            level.items.append(item)
            level.map[player.y][player.x].loot.append(item)
            player.inventory.remove(item)
        level.draw_rectangle_area(map_win, len(player.inventory)+2, self.width) # redraw map
        curses.curs_set(1)
