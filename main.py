import curses
#import random
#import math
from curses import wrapper
from level import Level
from player import Player
from sight import Sight


def main(stdscr):

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    level = Level('random level')
    level.generate_monsters()
    
    player = Player('Johnny')
    level.random_place(player)
    
    sight = Sight(N=12, R=6)
    
    game = True
    
    while game:
        
        level.check_visibility(sight.rays, player)
        level.draw(stdscr)
        
        stdscr.move(player.y,player.x) # move cursor to player position
        
        key = stdscr.getkey()
        if key == 'q':
            game = False
            break
        elif key == 'w': player.move(level, -1, 0)
        elif key == 'a': player.move(level, 0, -1)
        elif key == 's': player.move(level, 1, 0)
        elif key == 'd': player.move(level, 0, 1)
        elif key == 'e': player.get_loot(level)
        
        for monster in level.monsters:
            monster.do_something(level, player)
            
        
        
wrapper(main)
