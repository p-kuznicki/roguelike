import curses


COLOR_PAIRS = {
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
        "black_on_white": 8,
        "red_on_white": 9,
        "green_on_white": 10,
        "yellow_on_white": 11,
        "blue_on_white": 12,
        "magenta_on_white": 13,
        "cyan_on_white": 14,
    }

def get_col(alias):
    return curses.color_pair(COLOR_PAIRS[alias])

def initialize_colors():

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(11, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(13, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(14, curses.COLOR_CYAN, curses.COLOR_WHITE)
    
#color = {"green": curses.color_pair(2)}
