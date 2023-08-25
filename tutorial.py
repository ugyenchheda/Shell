import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr( "Welcome to Speed Typing Test!")
    stdscr.addstr( "\n Press any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)

    stdscr.addstr(1, 0, f"WPM: {wpm}")

    #enumerate will give current element along index from the list
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)

        #change color if character is not correct as target
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)

def load_text():
    with open("typingtext.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm =0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:        
        
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        #combines all the characters from list
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue
        
        #if Esc key press, exit
        if ord(key) == 27:
            break

        #backspace to remove character if there is any
        if key in (chr(curses.KEY_BACKSPACE), '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()

        #limiting typing as per the given text
        elif len(current_text)< len(target_text) :
            current_text.append(key)     

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the texts! Press any key to continue and Esc to leave.")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)