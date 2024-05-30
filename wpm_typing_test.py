# WPM TYPING TEST BY ARYAN ROSHAN

import curses,time, random
from curses import wrapper

def intro(stdscr):
    # Displays welcome message and instructions.
    stdscr.clear()
    stdscr.addstr("Welcome to my WPM typing test! Created by Aryan Roshan.")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, given, user_in, wpm = 0):
        # Updates the displayed text and WPM on screen.
        stdscr.clear()
        stdscr.addstr(given)
        stdscr.addstr(1,0, f"WPM: {wpm}")

        for i, char in enumerate(user_in):
            correct_c = given[i]
            color = curses.color_pair(1) # Highlights correct input in green.
            if char != correct_c:
                color = curses.color_pair(2) # Highlights incorrect input in red.
            stdscr.addstr(0 , i, char, color)

def load_text():
    # Loads a random phrase from a file.
    with open("generated_phrases.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    given_phrase = load_text()
    user_input = []
    wpm = 0
    start_t = time.time()
    stdscr.nodelay(True) # Allows for real-time key input without blocking.

    while True:
        # Calculates the WPM based on elapsed time and correct inputs.
        time_elapsed = max(time.time() - start_t, 1)
        wpm = round((len(user_input) * (60 / time_elapsed)) / 5)

        stdscr.clear()
        display_text(stdscr, given_phrase, user_input, wpm)
        stdscr.refresh()
        
        if "".join(user_input) == given_phrase:
            stdscr.nodelay(False) # Pause for result display.
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27: # Exit on ESC.
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(user_input) > 0:
                user_input.pop() # Removes last char on backspace.
        elif len(user_input) < len(given_phrase):
            user_input.append(key) # Adds char to input.

def main(stdscr):
    # Initializes color pairs for display.
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    intro(stdscr)

    while(True):
        wpm_test(stdscr)
         # Prompts for replay or exit after completing the test.
        stdscr.addstr(2, 0, "You completed the text! Press any key to play again or press ESC to close.")
        stdscr.addstr(3, 0, "Hope you enjoyed!")
        key = stdscr.getkey() 

        if ord(key) == 27:
            break

wrapper(main)  # Starts the application with curses wrapper for proper terminal handling.
