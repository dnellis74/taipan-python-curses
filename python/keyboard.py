import curses

def choice_yes_no(stdscr: curses.window) -> bool:
    choice = 0
    while choice not in [ord('Y'), ord('y'), ord('N'), ord('n')]:
        choice = get_one(stdscr)
    if choice in [ord('Y'), ord('y')]:
        return True
    else:
        return False
    
def get_one(stdscr: curses.window) -> int:
    """
    Get a single character input from the user.
    Handles backspace and escape key.
    Returns the character code of the input.
    """
    character = 0
    choice = 0

    while True:
        input_char = stdscr.getch()
        
        if input_char == ord('\n'):  # NEWLINE
            break
        elif (input_char == 8 or input_char == 127) and character == 0:  # BACKSPACE/DELETE
            stdscr.refresh()
        elif input_char == 8 or input_char == 127:  # BACKSPACE/DELETE
            stdscr.addch(curses.KEY_BACKSPACE)
            stdscr.addch(' ')
            stdscr.addch(curses.KEY_BACKSPACE)
            character -= 1
            stdscr.refresh()
        elif character >= 1:
            stdscr.refresh()
        elif input_char == 27:  # ESCAPE
            curses.flushinp()
            stdscr.refresh()
        else:
            stdscr.addch(input_char)
            choice = input_char
            character += 1
            stdscr.refresh()

    return choice

def get_num(stdscr: curses.window, maxlen: int) -> int:
    """
    Get a number input from the user with maximum length.
    Handles backspace, escape, and allows 'A' for -1.
    Returns the number entered or -1 if 'A' was entered.
    """
    number = ""
    character = 0

    while True:
        input_char = stdscr.getch()
        
        if input_char == ord('\n'):  # NEWLINE
            break
        elif (input_char == 8 or input_char == 127) and character == 0:  # BACKSPACE/DELETE
            stdscr.refresh()
        elif input_char == 8 or input_char == 127:  # BACKSPACE/DELETE
            stdscr.addch(curses.KEY_BACKSPACE)
            stdscr.addch(' ')
            stdscr.addch(curses.KEY_BACKSPACE)
            number = number[:-1]
            character -= 1
            stdscr.refresh()
        elif character >= maxlen:
            stdscr.refresh()
        elif input_char == 27:  # ESCAPE
            curses.flushinp()
            stdscr.refresh()
        elif ((input_char == ord('A') or input_char == ord('a')) and 
              character == 0 and maxlen > 1):
            stdscr.addch(input_char)
            number += chr(input_char)
            character += 1
            stdscr.refresh()
        elif input_char < 0 or input_char > 255:  # Skip invalid character codes
            continue
        elif not chr(input_char).isdigit():
            stdscr.refresh()
        else:
            stdscr.addch(input_char)
            number += chr(input_char)
            character += 1
            stdscr.refresh()

    if number.upper() == 'A':
        return -1
    return int(number) if number else 0 