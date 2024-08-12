import curses

class Inventory_view():
    def __init__(self, inventory, width):
        self.inventory = inventory
        #self.height = 10
        self.width = width
        self.letters_to_numbers = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8, "j":9}
        self.numbers_to_letters = list(self.letters_to_numbers.keys()) 
        
    def open(self, map_win, level, player):
        curses.curs_set(0)
        map_win.addstr(0, 0, "Inventory", curses.color_pair(3)) 
        for y, item in enumerate(self.inventory):
            map_win.move(y+1, 0)
            for x in range(self.width):
                map_win.addch(' ', curses.color_pair(3))
            map_win.addstr(y+1, 0, self.numbers_to_letters[y] + ") "+ item.name, curses.color_pair(3))
        key = map_win.getkey()
        if key in self.letters_to_numbers and self.letters_to_numbers[key] < len(self.inventory):
            item = self.inventory[self.letters_to_numbers[key]]
            level.items.append(item)
            level.map[player.y][player.x].loot.append(item)
            self.inventory.remove(item)
        curses.curs_set(1)
        
        

            
        #map_win.refresh()
