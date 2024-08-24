import random

def d20():
    return random.randint(1,20)


def check_terminal_size(stdscr, min_height, min_width):
    height, width = stdscr.getmaxyx()
    if height < min_height or width < min_width:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Terminal too small! Minimum size: {min_height}x{min_width}.")
        stdscr.addstr(1, 0, "Resize the terminal and/or decrease font size and press any key to retry.")
        stdscr.addstr(2, 0, "Resizing terminal back in game may crash the game.")
        stdscr.refresh()
        stdscr.getch()
        return False

