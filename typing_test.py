# PASSWORD VALIDATOR BY ARYAN ROSHAN

import curses,time, random
from curses import wrapper

def intro(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to my speed typing test! Created by Aryan Roshan.")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm = 0):
        stdscr.clear()
        stdscr.addstr(target)
        stdscr.addstr(1,0, f"WPM: {wpm}")

        for i, char in enumerate(current):
            correct_c = target[i]
            color = curses.color_pair(1)
            if char != correct_c:
                color = curses.color_pair(2)
            stdscr.addstr(0 , i, char, color)

def load_text():
    with open("generated_phrases.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_t = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_t, 1)
        wpm = round((len(current_text) * (60 / time_elapsed)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text,current_text, wpm)
        stdscr.refresh()
        
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break


        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    intro(stdscr)

    while(True):
        wpm_test(stdscr)

        stdscr.addstr(2, 0, "You completed the text! Press ESC to close or any key to play again!")
        key = stdscr.getkey()

        if ord(key) == 27:
            break



wrapper(main)

