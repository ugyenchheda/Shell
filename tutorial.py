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

def display_text(stdscr, target, current, wpm=0, accuracy=0):
    stdscr.addstr(target)
    accuracy_str = f"Accuracy: {accuracy:.2f}%"
    stdscr.addstr(2, 0, accuracy_str)

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

def typing_accuracy(current_text, target_text):
    total_characters = min(len(current_text), len(target_text))
    
    if total_characters == 0:
        return 0.0  # If there are no characters, consider accuracy as 100%

    matching_characters = 0

    for current_char, target_char in zip(current_text, target_text):
        if current_char == target_char:
            matching_characters += 1
    
    matching_percentage = (matching_characters / total_characters) * 100
    return matching_percentage

def wpm_test(stdscr):
    target_text = "this is just a test"
    current_text = []
    wpm =0
    accuracy= 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:        
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        accuracy = typing_accuracy(current_text, target_text)
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm, accuracy)
        stdscr.refresh()

        #combines all the characters from list
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            stdscr.refresh()
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
        elif len(current_text) < len(target_text) :
            current_text.append(key)     

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(3, 0, "You completed the texts! Press any key to continue and Esc to leave.")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)