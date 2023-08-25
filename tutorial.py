import curses
from curses import wrapper

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr( "Welcome to Speed Typing Test!")
    stdscr.addstr( "\n Press any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def wpm_test(stdscr):
    target_text = "Hello world this is some test text for this app!"
    current_text = []

    while True:
        key = stdscr.getkey()

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
            else:
                current_text.append(key)

        current_text.append(key)
        
        stdscr.clear()
        stdscr.addstr( target_text)
        stdscr.refresh()

        for char in current_text:
            stdscr.addstr(char, curses.color_pair(1))

        
        stdscr.refresh()

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    
    start_screen(stdscr)
    wpm_test(stdscr)

wrapper(main)