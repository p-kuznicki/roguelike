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
        
def draw_info(text_win, player):
    text_win.addstr(0,1, player.name)
    text_win.addstr(0,10, f"ToHit:{player.to_hit}  DMG:1-{player.damage}  DFNS:{player.defense}  HP:{player.hp}  kills:{player.kills}")
    text_win.refresh()
