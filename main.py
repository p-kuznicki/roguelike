import curses
from curses import wrapper
from level import Level
from player import Player
from sight import Sight
from helpers import check_terminal_size

def main(stdscr):

    check_terminal_size(stdscr)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    level = Level('random level', height=30, width=120)
    level.generate_monsters()
    
    player = Player('Johnny')
    level.random_place(player)
    
    sight = Sight(rays_density=12, sight_range=8)
    
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
            monster.choose_action(level, player)
                    
wrapper(main)
