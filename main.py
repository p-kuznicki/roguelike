import curses
from curses import wrapper
from level import Level
from player import Player
from sight import Sight
from status import Status
from color import initialize_colors
from inventory_view import Inventory_view
from helpers import check_terminal_size

min_height = 25
min_width = 80

def main(stdscr):

    initialize_colors()

    check_terminal_size(stdscr, min_height, min_width)
    message_win = curses.newwin(2, min_width, 0, 0)
    map_win = curses.newwin(min_height-3, min_width, 2 , 0)
    attributes_win = curses.newwin(1, min_width, min_height-1, 0)
    
    level = Level(height=min_height-3, width=min_width)
    level.generate_random_rock_map()
    #level.generate_yx_rooms(3,3)
    levels = [level]

    
    player = Player('Johnny', to_hit=3, base_damage=1, defense=3, hp=25)
    level.random_place_agent(player)
    status = Status(min_width)

    inventory_view = Inventory_view()
    sight = Sight(rays_density=20, sight_range=20)
    
    level_loop = True
    
    while level_loop:
        
        if player.depth <= -1:
            level_loop = False
            break
        if player.changed_levels :
            levels[player.depth].draw_all(sight.rays, player, map_win)
            player.changed_levels = False
        else:
            levels[player.depth].draw_visible(sight.rays, player, map_win)
        
        
        if player.attributes_changed: status.update_attributes(player, attributes_win)
        if player.message or status.displaying_message: status.update_message(player, message_win)      
        if player.hit: player.bleed(map_win) 
        map_win.move(player.y,player.x) # move cursor to player position

        key = map_win.getkey()
        if key == 'q':
            level_loop = False
            break
        elif key == "w": player.move(levels[player.depth], -1, 0, map_win)
        elif key == "a": player.move(levels[player.depth], 0, -1, map_win)
        elif key == "s": player.move(levels[player.depth], 1, 0, map_win)
        elif key == "d": player.move(levels[player.depth], 0, 1, map_win)
        elif key == "e": inventory_view.try_to_get_item(map_win, player, levels[player.depth])
        elif key == "\n":
            if hasattr(levels[player.depth].map[player.y][player.x], "activate"):
                levels[player.depth].map[player.y][player.x].activate(player, levels)
            continue
        elif key == "i":
            inventory_view.open(map_win, player, levels[player.depth], "Inventory")
            continue
        
        for item in levels[player.depth].items: levels[player.depth].hide_this(item, map_win)
              
        for monster in level.monsters:
            levels[player.depth].hide_this(monster, map_win)
            monster.action(level, player)
            
        for item in player.inventory:
             player.try_to_identify(item)
            
        player.regenerate()
                
wrapper(main)
