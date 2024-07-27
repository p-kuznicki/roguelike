import curses
import time

def main(stdscr):
    # Clear the screen
    stdscr.clear()

    # Print a message in the middle of the screen
    height, width = stdscr.getmaxyx()
    message = "Hello, Curses!"
    x = width // 2 - len(message) // 2
    y = height // 2
    stdscr.addstr(y, x, message)
    stdscr.refresh()

    # Wait for a moment
    time.sleep(1)

    # Simulate flash by turning screen off and on
    for _ in range(3):
        stdscr.clear()
        stdscr.refresh()
        time.sleep(0.1)
        stdscr.addstr(y, x, message)
        stdscr.refresh()
        time.sleep(0.1)

    # Wait again to see the effect
    time.sleep(1)

# Run the curses application
curses.wrapper(main)

