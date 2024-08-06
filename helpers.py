def check_terminal_size(stdscr):
    MIN_HEIGHT = 40
    MIN_WIDTH = 120
    height, width = stdscr.getmaxyx()
    if height < MIN_HEIGHT or width < MIN_WIDTH:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Terminal too small! Minimum size: {MIN_HEIGHT}x{MIN_WIDTH}.")
        stdscr.addstr(1, 0, "Resize the terminal and/or decrease font size and press any key to retry.")
        stdscr.refresh()
        stdscr.getch()
        return False
