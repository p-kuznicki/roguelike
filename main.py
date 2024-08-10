import curses
from curses import wrapper
from level import Level
from player import Player
from sight import Sight
from status import Status
from helpers import check_terminal_size

min_height = 20
min_width = 80

def main(stdscr):

    check_terminal_size(stdscr, min_height, min_width)
    message_win = curses.newwin(1, min_width, 0, 0)
    map_win = curses.newwin(min_height-2, min_width, 1 , 0)
    attributes_win = curses.newwin(1, min_width, min_height-1, 0)
        

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    level = Level('random level', height=min_height-2, width=min_width)
    
    player = Player('Johnny', 80, 8, 20, 25)
    level.random_place(player)
    status = Status(min_width)
    
    sight = Sight(rays_density=12, sight_range=7)
    
    level_loop = True
    
    while level_loop:
    
        level.draw_visible(sight.rays, player, map_win)
        if player.attributes_changed: status.update_attributes(player, attributes_win)
        if player.message or status.displaying_message: status.update_message(player, message_win)      
              
        map_win.move(player.y,player.x) # move cursor to player position

        key = map_win.getkey()
        if key == 'q':
            level_loop = False
            break
        elif key == 'w': player.move(level, -1, 0)
        elif key == 'a': player.move(level, 0, -1)
        elif key == 's': player.move(level, 1, 0)
        elif key == 'd': player.move(level, 0, 1)
        elif key == 'e': player.get_loot(level)
        
        for item in level.items: level.hide_this(item, map_win)
              
        for monster in level.monsters:
            level.hide_this(monster, map_win)
            monster.action(level, player) 
                
wrapper(main)
