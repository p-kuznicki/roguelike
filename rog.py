from curses import wrapper




def main(stdscr):
    stdscr.clear()

    y = 10
    x = 30
    stdscr.move(y,x)
#    stdscr.addstr("@")
    game = True
    while game:
        key = stdscr.getkey()
        if key == 'w':
            y -= 1
            stdscr.move(y,x)
        if key == 'a':
            x -= 1
            stdscr.move(y,x)
        if key == 's':
            y += 1
            stdscr.move(y,x)
        if key == 'd':
            x += 1
            stdscr.move(y,x)
        elif key == 'q':
            game = False

wrapper(main)

#import curses
#stdscr = curses.initscr()
#    stdscr.refresh()
#curses.has_colors()
#curses.start_color()
#curses.flash()
#curses.beep()
#curses.endwin()
