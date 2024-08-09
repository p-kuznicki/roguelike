import curses
from curses import wrapper
from level import Level
from player import Player
from sight import Sight
from helpers import check_terminal_size, draw_info

min_height = 30
min_width = 80

def main(stdscr):

    check_terminal_size(stdscr, min_height, min_width)
    map_win = curses.newwin(min_height-5, min_width, 0 , 0)
    text_win = curses.newwin(2, min_width, min_height-5, 0)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    level = Level('random level', height=min_height-6, width=min_width-1)
    level.generate_monsters()
    
    player = Player('Johnny', 80, 8, 20, 25)
    level.random_place(player)
    
    sight = Sight(rays_density=12, sight_range=8)
    
    game = True
    
    while game:
        
        level.check_visibility(sight.rays, player)
        level.draw(map_win)
        draw_info(text_win, player)        
        map_win.move(player.y,player.x) # move cursor to player position

        #stdscr.refresh()
        
        key = map_win.getkey()
        if key == 'q':
            game = False
            break
        elif key == 'w': player.move(level, -1, 0)
        elif key == 'a': player.move(level, 0, -1)
        elif key == 's': player.move(level, 1, 0)
        elif key == 'd': player.move(level, 0, 1)
        elif key == 'e': player.get_loot(level)
        
        for monster in level.monsters:
            monster.choose_action(level, player)
        
        
                    
wrapper(main)
