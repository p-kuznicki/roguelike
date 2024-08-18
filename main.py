import curses
from curses import wrapper
from level import Level
from player import Player
from sight import Sight
from status import Status
from inventory_view import Inventory_view
from helpers import check_terminal_size

min_height = 25
min_width = 50

def main(stdscr):

    check_terminal_size(stdscr, min_height, min_width)
    message_win = curses.newwin(1, min_width, 0, 0)
    map_win = curses.newwin(min_height-2, min_width, 1 , 0)
    attributes_win = curses.newwin(1, min_width, min_height-1, 0)
        

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_RED)
    
    
    level = Level(height=min_height-2, width=min_width)
    #level.generate_random_rock_map()
    #level = Level(height=min_height-2, width=min_width)
    #level.generate_random_room()
    level.generate_two_random_rooms()
    
    player = Player('Johnny', to_hit=70, base_damage=1, defense=20, hp=25)
    level.random_place_agent(player)
    status = Status(min_width)

    inventory_view = Inventory_view()
    sight = Sight(rays_density=20, sight_range=7)
    
    level_loop = True
    
    while level_loop:
    
        level.draw_visible(sight.rays, player, map_win)
        if player.attributes_changed: status.update_attributes(player, attributes_win)
        if player.message or status.displaying_message: status.update_message(player, message_win)      
        if player.hit: player.bleed(map_win) 
        map_win.move(player.y,player.x) # move cursor to player position

        key = map_win.getkey()
        if key == 'q':
            level_loop = False
            break
        elif key == 'w': player.move(level, -1, 0, map_win)
        elif key == 'a': player.move(level, 0, -1, map_win)
        elif key == 's': player.move(level, 1, 0, map_win)
        elif key == 'd': player.move(level, 0, 1, map_win)
        elif key == 'e': inventory_view.try_to_get_item(map_win, player, level)
        elif key == 'i':
            inventory_view.open(map_win, player, level, "Inventory")
            continue
        
        for item in level.items: level.hide_this(item, map_win)
              
        for monster in level.monsters:
            level.hide_this(monster, map_win)
            monster.action(level, player) 
                
wrapper(main)
