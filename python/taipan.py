#!/usr/bin/env python3
"""
Taipan - A Python port of the classic trading game
Original C version by Jay Link <jlink@ilbbs.com>
Based on Apple ][ program by Ronald J. Berg
"""

import curses
import random
import time
import os
from typing import List, Dict, Tuple, Optional
from sea_battle import SeaBattle
from constants import (
    DEBUG, GENERIC, LI_YUEN, BATTLE_NOT_FINISHED, BATTLE_WON, BATTLE_INTERRUPTED,
    BATTLE_FLED, BATTLE_LOST, BACKSPACE, DELETE, ESCAPE, NEWLINE, ANIMATION_PAUSE,
    M_PAUSE, L_PAUSE, STARTING_YEAR, STARTING_MONTH, STARTING_PORT, STARTING_CAPACITY,
    STARTING_HOLD, STARTING_GUNS, STARTING_DAMAGE, STARTING_CASH, STARTING_BANK,
    STARTING_DEBT, STARTING_BOOTY, BASE_ENEMY_HEALTH, BASE_ENEMY_DAMAGE,
    MAX_WAREHOUSE_CAPACITY, OPIUM, SILK, ARMS, GENERAL, AT_SEA, HONG_KONG,
    SHANGHAI, NAGASAKI, SAIGON, MANILA, SINGAPORE, BATAVIA, CRITICAL, POOR,
    FAIR, GOOD, PRIME, PERFECT
)
from mchenry import McHenry
from shared import fancy_numbers, get_one, get_num

class TaipanGame:
    def __init__(self):
        # Curses screen
        self.stdscr = None

        # Game state
        self.firm = ""  # Firm name (was char[23])

        # Item and location names
        self.items = ["Opium", "Silk", "Arms", "General Cargo"]
        self.locations = [
            "At sea", "Hong Kong", "Shanghai", "Nagasaki",
            "Saigon", "Manila", "Singapore", "Batavia"
        ]
        self.months = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]
        self.status_texts = [
            "Critical", "  Poor", "  Fair",
            "  Good", " Prime", "Perfect"
        ]

        # Financial state
        self.cash = STARTING_CASH
        self.bank = STARTING_BANK
        self.debt = STARTING_DEBT
        self.booty = STARTING_BOOTY

        # Combat stats
        self.ec = BASE_ENEMY_HEALTH
        self.ed = BASE_ENEMY_DAMAGE

        # Prices and inventory
        self.price = [0] * 4  # Current prices
        self.base_price = [
            [1000, 11, 16, 15, 14, 12, 10, 13],
            [100,  11, 14, 15, 16, 10, 13, 12],
            [10,   12, 16, 10, 11, 13, 14, 15],
            [1,    10, 11, 12, 13, 14, 15, 16]
        ]
        self.hkw_ = [0] * 4  # Hong Kong warehouse
        self.hold_ = [0] * 4  # Current cargo hold

        # Ship stats
        self.hold = STARTING_HOLD
        self.capacity = STARTING_CAPACITY
        self.guns = STARTING_GUNS
        self.bp = 0
        self.damage = STARTING_DAMAGE

        # Time and location
        self.month = STARTING_MONTH
        self.year = STARTING_YEAR
        self.li = 0
        self.port = STARTING_PORT
        self.wu_warn = 0
        self.wu_bailout = 0

        # Battle constants
        self.GENERIC = GENERIC
        self.LI_YUEN = LI_YUEN

        self.BATTLE_NOT_FINISHED = BATTLE_NOT_FINISHED
        self.BATTLE_WON = BATTLE_WON
        self.BATTLE_INTERRUPTED = BATTLE_INTERRUPTED
        self.BATTLE_FLED = BATTLE_FLED
        self.BATTLE_LOST = BATTLE_LOST

    def init_curses(self):
        """Initialize curses and set up the screen"""
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.curs_set(0)  # Hide cursor

    def cleanup_curses(self):
        """Clean up curses before exiting"""
        if self.stdscr:
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()
            curses.endwin()

    def splash_intro(self) -> None:
        """Display the game's splash screen and wait for user input."""
        curses.flushinp()
        self.stdscr.clear()
        self.stdscr.addstr("\n")
        self.stdscr.addstr("         _____  _    ___ ____   _    _   _               ===============\n")
        self.stdscr.addstr("        |_   _|/ \\  |_ _|  _ \\ / \\  | \\ | |              Created by:\n")
        self.stdscr.addstr("          | | / _ \\  | || |_) / _ \\ |  \\| |                 Art Canfil\n")
        self.stdscr.addstr("          | |/ ___ \\ | ||  __/ ___ \\| |\\  |\n")
        self.stdscr.addstr("          |_/_/   \\_\\___|_| /_/   \\_\\_| \\_|              ===============\n")
        self.stdscr.addstr("                                                         Programmed by:\n")
        self.stdscr.addstr("   A game based on the China trade of the 1800's            Jay Link\n")
        self.stdscr.addstr("\n")
        self.stdscr.addstr("                      ~~|     ,                          jlink@ilbbs.com\n")
        self.stdscr.addstr("                       ,|`-._/|\n")
        self.stdscr.addstr("                     .' |   /||\\                         ===============\n")
        self.stdscr.addstr("                   .'   | ./ ||`\\                         Copyright (c)\n")
        self.stdscr.addstr("                  / `-. |/._ ||  \\                         1978 - 2002\n")
        self.stdscr.addstr("                 /     `||  `|;-._\\                         Art Canfil\n")
        self.stdscr.addstr("                 |      ||   ||   \\\n")
        self.stdscr.addstr("~^~_-~^~=~^~~^= /       ||   ||__  \\~^=~^~-~^~_~^~=      ===============\n")
        self.stdscr.addstr(" ~=~^~ _~^~ =~ `--------|`---||  `\"-`___~~^~ =_~^=        Press ")
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("ANY")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr(" key\n")
        self.stdscr.addstr("~ ~^~=~^_~^~ =~ \\~~~~~~~'~~~~'~~~~/~~`` ~=~^~ ~^=           to start.\n")
        self.stdscr.addstr(" ~^=~^~_~-=~^~ ^ `--------------'~^~=~^~_~^=~^~=~\n")
        curses.curs_set(0)
        self.stdscr.refresh()

        self.stdscr.getch()
        curses.curs_set(1)

    def get_one(self) -> int:
        """
        Get a single character input from the user.
        Handles backspace and escape key.
        Returns the character code of the input.
        """
        character = 0
        choice = 0

        while True:
            input_char = self.stdscr.getch()
            
            if input_char == NEWLINE:
                break
            elif (input_char == BACKSPACE or input_char == DELETE) and character == 0:
                self.stdscr.refresh()
            elif input_char == BACKSPACE or input_char == DELETE:
                self.stdscr.addch(curses.KEY_BACKSPACE)
                self.stdscr.addch(' ')
                self.stdscr.addch(curses.KEY_BACKSPACE)
                character -= 1
                self.stdscr.refresh()
            elif character >= 1:
                self.stdscr.refresh()
            elif input_char == ESCAPE:
                curses.flushinp()
                self.stdscr.refresh()
            else:
                self.stdscr.addch(input_char)
                choice = input_char
                character += 1
                self.stdscr.refresh()

        return choice

    def get_num(self, maxlen: int) -> int:
        """
        Get a number input from the user with maximum length.
        Handles backspace, escape, and allows 'A' for -1.
        Returns the number entered or -1 if 'A' was entered.
        """
        number = ""
        character = 0

        while True:
            input_char = self.stdscr.getch()
            
            if input_char == NEWLINE:
                break
            elif (input_char == BACKSPACE or input_char == DELETE) and character == 0:
                self.stdscr.refresh()
            elif input_char == BACKSPACE or input_char == DELETE:
                self.stdscr.addch(curses.KEY_BACKSPACE)
                self.stdscr.addch(' ')
                self.stdscr.addch(curses.KEY_BACKSPACE)
                number = number[:-1]
                character -= 1
                self.stdscr.refresh()
            elif character >= maxlen:
                self.stdscr.refresh()
            elif input_char == ESCAPE:
                curses.flushinp()
                self.stdscr.refresh()
            elif ((input_char == ord('A') or input_char == ord('a')) and 
                  character == 0 and maxlen > 1):
                self.stdscr.addch(input_char)
                number += chr(input_char)
                character += 1
                self.stdscr.refresh()
            elif input_char < 0 or input_char > 255:  # Skip invalid character codes
                continue
            elif not chr(input_char).isdigit():
                self.stdscr.refresh()
            else:
                self.stdscr.addch(input_char)
                number += chr(input_char)
                character += 1
                self.stdscr.refresh()

        if number.upper() == 'A':
            return -1
        return int(number) if number else 0

    def name_firm(self) -> None:
        """Set the firm name. In debug mode, sets to 'debug'."""
        if DEBUG:
            self.firm = "debug"
            self.stdscr.clear()
            self.stdscr.addstr(5, 10, f"Welcome to {self.firm}, Taipan!")
            self.stdscr.refresh()
            # time.sleep(1)  # Brief pause to show the message
        else:
            self.stdscr.clear()
            self.stdscr.move(7, 0)
            self.stdscr.addstr(" _______________________________________\n")
            self.stdscr.addstr("|     Taipan,                           |\n")
            self.stdscr.addstr("|                                       |\n")
            self.stdscr.addstr("| What will you name your               |\n")
            self.stdscr.addstr("|                                       |\n")
            self.stdscr.addstr("|     Firm:                             |\n")
            self.stdscr.addstr("|           ----------------------      |\n")
            self.stdscr.addstr("|_______________________________________|\n")

            self.stdscr.move(12, 12)
            self.stdscr.refresh()

            character = 0
            self.firm = ""

            while character < 22:
                input_char = get_one(self.stdscr)
                if input_char == ord('\n'):
                    break
                elif ((input_char == 8 or input_char == 127) and character == 0):
                    self.stdscr.refresh()
                elif input_char == 8 or input_char == 127:
                    self.stdscr.addch(8)
                    self.stdscr.addch(' ')
                    self.stdscr.addch(8)
                    self.firm = self.firm[:-1]
                    character -= 1
                    self.stdscr.refresh()
                elif input_char == 27:  # Escape key
                    curses.flushinp()
                    self.stdscr.refresh()
                else:
                    self.stdscr.addch(input_char)
                    self.firm += chr(input_char)
                    character += 1
                    self.stdscr.refresh()

    def cash_or_guns(self) -> None:
        """Set initial cash and guns. In debug mode, sets debug values."""
        if DEBUG:
            self.cash = 10000
            self.debt = 1000
            self.guns = 5
            self.bp = 1  # Set battle probability to 1 for debug mode
            self.hold = 50
            
            self.stdscr.clear()
            self.stdscr.addstr(5, 10, "Initial resources set for debug mode:")
            self.stdscr.addstr(7, 10, f"Cash: ${self.cash}")
            self.stdscr.addstr(8, 10, f"Debt: ${self.debt}")
            self.stdscr.addstr(9, 10, f"Guns: {self.guns}")
            self.stdscr.refresh()
            # time.sleep(2)  # Brief pause to show the values
        else:
            self.stdscr.clear()
            self.stdscr.move(5, 0)
            self.stdscr.addstr("Do you want to start . . .\n\n")
            self.stdscr.addstr("  1) With cash (and a debt)\n\n")
            self.stdscr.addstr("                >> or <<\n\n")
            self.stdscr.addstr("  2) With five guns and no cash\n")
            self.stdscr.addstr("                (But no debt!)\n")

            choice = 0
            while choice not in [ord('1'), ord('2')]:
                self.stdscr.move(15, 0)
                self.stdscr.clrtobot()
                self.stdscr.addstr("          ?")
                self.stdscr.refresh()
                choice = get_one(self.stdscr)

            if choice == ord('1'):
                self.cash = 400
                self.debt = 5000
                self.hold = 60
                self.guns = 0
                self.li = 0
                self.bp = 10
            else:
                self.cash = 0
                self.debt = 0
                self.hold = 10
                self.guns = 5
                self.li = 1
                self.bp = 7

    def set_prices(self) -> None:
        """Set prices for merchandise in current port based on base prices and random factors."""
        # Original C logic: price = (base_price[port] / 2) * (random 1-3) * base_price[0]
        for i in range(4):
            self.price[i] = (self.base_price[i][self.port] / 2) * (random.randint(1, 3)) * self.base_price[i][0]

    def port_stats(self) -> None:
        """Display port statistics screen."""
        # Get screen dimensions
        max_y, max_x = self.stdscr.getmaxyx()
        
        # Calculate status percentage
        status = 100 - ((self.damage / self.capacity) * 100)
        
        # Clear screen and prepare display
        self.stdscr.clear()
        
        # Center firm name
        spacer = 12 - (len(self.firm) // 2)
        self.stdscr.addstr(0, spacer, f"Firm: {self.firm}, Hong Kong")
        
        # Draw the main display boxes
        self.stdscr.addstr(1, 0, " ______________________________________")
        self.stdscr.addstr(2, 0, "|Hong Kong Warehouse                   |     Date")
        self.stdscr.addstr(3, 0, "|   Opium           In Use:            |")
        self.stdscr.addstr(4, 0, "|   Silk                               |")
        self.stdscr.addstr(5, 0, "|   Arms            Vacant:            |   Location")
        self.stdscr.addstr(6, 0, "|   General                            |")
        self.stdscr.addstr(7, 0, "|______________________________________|")
        self.stdscr.addstr(8, 0, "|Hold               Guns               |     Debt")
        self.stdscr.addstr(9, 0, "|   Opium                              |")
        self.stdscr.addstr(10, 0, "|   Silk                               |")
        self.stdscr.addstr(11, 0, "|   Arms                               |  Ship Status")
        self.stdscr.addstr(12, 0, "|   General                            |")
        self.stdscr.addstr(13, 0, "|______________________________________|")
        self.stdscr.addstr(14, 0, "Cash:               Bank:")
        self.stdscr.addstr(15, 0, "________________________________________")

        # Display warehouse contents
        self.stdscr.addstr(3, 12, str(self.hkw_[0]))
        self.stdscr.addstr(4, 12, str(self.hkw_[1]))
        self.stdscr.addstr(5, 12, str(self.hkw_[2]))
        self.stdscr.addstr(6, 12, str(self.hkw_[3]))

        # Display hold status
        self.stdscr.move(8, 6)
        if self.hold >= 0:
            self.stdscr.addstr(str(self.hold))
        else:
            self.stdscr.attron(curses.A_REVERSE)
            self.stdscr.addstr("Overload")
            self.stdscr.attroff(curses.A_REVERSE)

        # Display current cargo
        self.stdscr.addstr(9, 12, str(self.hold_[0]))
        self.stdscr.addstr(10, 12, str(self.hold_[1]))
        self.stdscr.addstr(11, 12, str(self.hold_[2]))
        self.stdscr.addstr(12, 12, str(self.hold_[3]))

        # Display cash
        self.stdscr.move(14, 5)
        self.stdscr.addstr(fancy_numbers(self.cash))

        # Calculate and display warehouse usage
        in_use = sum(self.hkw_)
        self.stdscr.addstr(4, 21, str(in_use))
        self.stdscr.addstr(6, 21, str(10000 - in_use))

        # Display guns
        self.stdscr.addstr(8, 25, str(self.guns))

        # Display bank balance
        self.stdscr.move(14, 25)
        self.stdscr.addstr(fancy_numbers(self.bank))

        # Display date
        self.stdscr.move(3, 42)
        self.stdscr.addstr("15 ")
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(self.months[self.month - 1])
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr(f" {self.year}")

        # Display location
        self.stdscr.move(6, 43)
        spacer = (9 - len(self.locations[self.port])) // 2
        self.stdscr.addstr(" " * spacer)
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(self.locations[self.port])
        self.stdscr.attroff(curses.A_REVERSE)

        # Display debt
        self.stdscr.move(9, 41)
        debt_str = fancy_numbers(self.debt)
        spacer = (12 - len(debt_str)) // 2
        self.stdscr.addstr(" " * spacer)
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(debt_str)
        self.stdscr.attroff(curses.A_REVERSE)

        # Display ship status
        status_index = int(status / 20)
        if status_index < 2:
            self.stdscr.attron(curses.A_REVERSE)
            self.stdscr.move(12, 51)
            self.stdscr.addstr("  ")
        self.stdscr.move(12, 42)
        self.stdscr.addstr(f"{self.status_texts[status_index]}:{int(status)}")
        self.stdscr.attroff(curses.A_REVERSE)

        self.stdscr.refresh()

    def port_choices(self) -> int:
        """Display port menu choices and get user selection"""
        choice = 0

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Taipan, present prices per unit here are\n")
        self.stdscr.addstr("   Opium:          Silk:\n")
        self.stdscr.addstr("   Arms:           General:\n")
        self.stdscr.move(19, 11)
        self.stdscr.addstr(str(self.price[0]))
        self.stdscr.move(19, 29)
        self.stdscr.addstr(str(self.price[1]))
        self.stdscr.move(20, 11)
        self.stdscr.addstr(str(self.price[2]))
        self.stdscr.move(20, 29)
        self.stdscr.addstr(str(self.price[3]))

        while True:
            self.stdscr.move(22, 0)
            self.stdscr.clrtobot()

            if self.port == 1:
                if (self.cash + self.bank) >= 1000000:
                    self.stdscr.addstr("Shall I Buy, Sell, Visit bank, Transfer\n")
                    self.stdscr.addstr("cargo, Wheedle Wu, Quit trading, or Retire? ")
                    self.stdscr.refresh()

                    choice = get_one(self.stdscr)
                    if choice in [ord('B'), ord('b'), ord('S'), ord('s'), 
                                ord('V'), ord('v'), ord('T'), ord('t'),
                                ord('W'), ord('w'), ord('Q'), ord('q'),
                                ord('R'), ord('r')]:
                        break
                else:
                    self.stdscr.addstr("Shall I Buy, Sell, Visit bank, Transfer\n")
                    self.stdscr.addstr("cargo, Wheedle Wu, or Quit trading? ")
                    self.stdscr.refresh()

                    choice = get_one(self.stdscr)
                    if choice in [ord('B'), ord('b'), ord('S'), ord('s'),
                                ord('V'), ord('v'), ord('T'), ord('t'),
                                ord('W'), ord('w'), ord('Q'), ord('q')]:
                        break
            else:
                self.stdscr.addstr("Shall I Buy, Sell, or Quit trading? ")
                self.stdscr.refresh()

                choice = get_one(self.stdscr)
                if choice in [ord('B'), ord('b'), ord('S'), ord('s'),
                            ord('Q'), ord('q')]:
                    break

        return choice

    def new_ship(self) -> None:
        """Handle ship upgrades"""
        choice = 0
        time = ((self.year - 1860) * 12) + self.month
        amount = random.randint(0, 1000 * (time + 5) // 6) * (self.capacity // 50) + 1000

        if self.cash < amount:
            return

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Do you wish to trade in your ")
        if self.damage > 0:
            self.stdscr.attron(curses.A_REVERSE)
            self.stdscr.addstr("damaged")
            self.stdscr.attroff(curses.A_REVERSE)
        else:
            self.stdscr.addstr("fine")
        self.stdscr.addstr("\nship for one with 50 more capacity by\n")
        self.stdscr.addstr(f"paying an additional {fancy_numbers(amount)}, Taipan? ")
        self.stdscr.refresh()

        while choice not in [ord('Y'), ord('y'), ord('N'), ord('n')]:
            choice = get_one(self.stdscr)

        if choice in [ord('Y'), ord('y')]:
            self.cash -= amount
            self.hold += 50
            self.capacity += 50
            self.damage = 0

        if random.randint(0, 1) == 0 and self.guns < 1000:
            self.port_stats()
            self.new_gun()

        self.port_stats()

    def new_gun(self) -> None:
        """Handle buying new guns"""
        choice = 0
        time = ((self.year - 1860) * 12) + self.month
        amount = random.randint(0, 1000 * (time + 5) // 6) + 500

        if self.cash < amount or self.hold < 10:
            return


        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Do you wish to buy a ship's gun\n")
        self.stdscr.addstr(f"for {fancy_numbers(amount)}, Taipan? ")
        self.stdscr.refresh()

        while choice not in [ord('Y'), ord('y'), ord('N'), ord('n')]:
            choice = get_one(self.stdscr)

        if choice in [ord('Y'), ord('y')]:
            self.cash -= amount
            self.hold -= 10
            self.guns += 1

        self.port_stats()

    def li_yuen_extortion(self) -> None:
        """Handle Li Yuen's extortion attempt"""
        time = ((self.year - 1860) * 12) + self.month
        choice = 0
        i = 1.8
        j = 0
        amount = 0

        if time > 12:
            j = random.randint(0, 1000 * time) + (1000 * time)
            i = 1

        amount = ((self.cash / i) * random.random()) + j

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr(f"Li Yuen asks {fancy_numbers(amount)} in donation\n")
        self.stdscr.addstr("to the temple of Tin Hau, the Sea\n")

        while choice not in [ord('Y'), ord('y'), ord('N'), ord('n')]:
            self.stdscr.move(20, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("Goddess.  Will you pay? ")
            self.stdscr.refresh()
            choice = get_one(self.stdscr)

        if choice in [ord('Y'), ord('y')]:
            if amount <= self.cash:
                self.cash -= amount
                self.li = 1
            else:
                self.stdscr.move(18, 0)
                self.stdscr.clrtobot()
                self.stdscr.addstr("Taipan, you do not have enough cash!!\n\n")
                self.stdscr.refresh()

                self.stdscr.timeout(M_PAUSE)
                self.stdscr.getch()
                self.stdscr.timeout(-1)

                self.stdscr.addstr("Do you want Elder Brother Wu to make up\n")
                self.stdscr.addstr("the difference for you? ")
                choice = 0
                while choice not in [ord('Y'), ord('y'), ord('N'), ord('n')]:
                    choice = get_one(self.stdscr)

                if choice in [ord('Y'), ord('y')]:
                    amount -= self.cash
                    self.debt += amount
                    self.cash = 0
                    self.li = 1

                    self.stdscr.move(18, 0)
                    self.stdscr.clrtobot()
                    self.stdscr.addstr("Elder Brother has given Li Yuen the\n")
                    self.stdscr.addstr("difference between what he wanted and\n")
                    self.stdscr.addstr("your cash on hand and added the same\n")
                    self.stdscr.addstr("amount to your debt.\n")

                    self.stdscr.refresh()
                    self.stdscr.timeout(L_PAUSE)
                    self.stdscr.getch()
                    self.stdscr.timeout(-1)
                else:
                    self.cash = 0

                    self.stdscr.addstr("Very well. Elder Brother Wu will not pay\n")
                    self.stdscr.addstr("Li Yuen the difference.  I would be very\n")
                    self.stdscr.addstr("wary of pirates if I were you, Taipan.\n")

                    self.stdscr.refresh()
                    self.stdscr.timeout(L_PAUSE)
                    self.stdscr.getch()
                    self.stdscr.timeout(-1)

        self.port_stats()

    def elder_brother_wu(self) -> None:
        """Handle Elder Brother Wu's interactions"""
        choice = 0
        wu = 0

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Do you have business with Elder Brother\n")
        self.stdscr.addstr("Wu, the moneylender? ")

        while True:
            self.stdscr.move(19, 21)
            self.stdscr.clrtoeol()
            self.stdscr.refresh()

            choice = get_one(self.stdscr)
            if choice in [ord('N'), ord('n')]:
                break
            elif choice in [ord('Y'), ord('y')]:
                if (self.cash == 0 and self.bank == 0 and self.guns == 0 and
                    self.hold_[0] == 0 and self.hkw_[0] == 0 and
                    self.hold_[1] == 0 and self.hkw_[1] == 0 and
                    self.hold_[2] == 0 and self.hkw_[2] == 0 and
                    self.hold_[3] == 0 and self.hkw_[3] == 0):
                    
                    i = random.randint(500, 1999)
                    j = random.randint(0, 1999) * self.wu_bailout + 1500
                    self.wu_bailout += 1

                    while True:
                        self.stdscr.move(16, 0)
                        self.stdscr.clrtobot()
                        self.stdscr.addstr("Comprador's Report\n\n")
                        self.stdscr.addstr("Elder Brother is aware of your plight,\n")
                        self.stdscr.addstr("Taipan.  He is willing to loan you an\n")
                        self.stdscr.addstr(f"additional {i} if you will pay back\n")
                        self.stdscr.addstr(f"{j}. Are you willing, Taipan? ")
                        self.stdscr.refresh()

                        choice = get_one(self.stdscr)
                        if choice in [ord('N'), ord('n')]:
                            self.stdscr.move(16, 0)
                            self.stdscr.clrtobot()
                            self.stdscr.addstr("Comprador's Report\n\n")
                            self.stdscr.addstr("Very well, Taipan, the game is over!\n")

                            self.stdscr.refresh()
                            self.stdscr.timeout(L_PAUSE)
                            self.stdscr.getch()
                            self.stdscr.timeout(-1)

                            self.final_stats()
                        elif choice in [ord('Y'), ord('y')]:
                            self.cash += i
                            self.debt += j
                            self.port_stats()

                            self.stdscr.move(16, 0)
                            self.stdscr.clrtobot()
                            self.stdscr.addstr("Comprador's Report\n\n")
                            self.stdscr.addstr("Very well, Taipan.  Good joss!!\n")

                            self.stdscr.refresh()
                            self.stdscr.timeout(L_PAUSE)
                            self.stdscr.getch()
                            self.stdscr.timeout(-1)

                            return

                while True:
                    self.stdscr.move(16, 0)
                    self.stdscr.clrtobot()
                    self.stdscr.addstr("Comprador's Report\n\n")
                    self.stdscr.addstr("How much do you wish to repay\n")
                    self.stdscr.addstr("him? ")
                    self.stdscr.refresh()

                    wu = get_num(self.stdscr, 9)
                    if wu == -1:
                        wu = min(self.cash, self.debt)
                    if wu <= self.cash:
                        if wu > self.debt:
                            self.stdscr.addstr(f"Taipan, you owe only {fancy_numbers(self.debt)}.\n")
                            self.stdscr.addstr("Paid in full.\n")
                            self.stdscr.refresh()
                            self.stdscr.timeout(L_PAUSE)
                            wu = self.debt
                        self.cash -= wu
                        if wu > self.debt and self.debt > 0:
                            self.debt -= (wu + 1)
                        else:
                            self.debt -= wu
                        break
                    else:
                        self.stdscr.move(18, 0)
                        self.stdscr.clrtobot()
                        self.stdscr.addstr(f"Taipan, you only have {fancy_numbers(self.cash)}\n")
                        self.stdscr.addstr("in cash.\n")

                        self.stdscr.refresh()
                        self.stdscr.timeout(L_PAUSE)
                        self.stdscr.getch()
                        self.stdscr.timeout(-1)

                self.port_stats()

                while True:
                    self.stdscr.move(16, 0)
                    self.stdscr.clrtobot()
                    self.stdscr.addstr("Comprador's Report\n\n")
                    self.stdscr.addstr("How much do you wish to\n")
                    self.stdscr.addstr("borrow? ")
                    self.stdscr.refresh()

                    wu = get_num(self.stdscr, 9)
                    if wu == -1:
                        wu = self.cash * 2
                    if wu <= (self.cash * 2):
                        self.cash += wu
                        self.debt += wu
                        break
                    else:
                        self.stdscr.addstr("\n\nHe won't loan you so much, Taipan!")

                        self.stdscr.refresh()
                        self.stdscr.timeout(L_PAUSE)
                        self.stdscr.getch()
                        self.stdscr.timeout(-1)

                self.port_stats()
                break

        if self.debt > 20000 and self.cash > 0 and random.randint(0, 4) == 0:
            num = random.randint(1, 3)

            self.cash = 0
            self.port_stats()

            self.stdscr.move(16, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("Comprador's Report\n\n")
            self.stdscr.addstr("Bad joss!!\n")
            self.stdscr.addstr(f"{num} of your bodyguards have been killed\n")
            self.stdscr.addstr("by cutthroats and you have been robbed\n")
            self.stdscr.addstr("of all of your cash, Taipan!!\n")

            self.stdscr.refresh()
            self.stdscr.timeout(L_PAUSE)
            self.stdscr.getch()
            self.stdscr.timeout(-1)

    def good_prices(self) -> None:
        """Handle random price changes for items"""
        i = random.randint(0, 3)
        j = random.randint(0, 1)

        item = self.items[i]

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr(f"Taipan!!  The price of {item}\n")
        if j == 0:
            self.price[i] = self.price[i] // 5
            self.stdscr.addstr(f"has dropped to {self.price[i]}!!\n")
        else:
            self.price[i] = self.price[i] * (random.randint(0, 4) + 5)
            self.stdscr.addstr(f"has risen to {self.price[i]}!!\n")

        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def buy(self) -> None:
        """Handle buying merchandise"""
        choice = 0
        amount = 0

        # Get item choice
        while True:
            self.stdscr.move(22, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("What do you wish me to buy, Taipan? ")
            self.stdscr.refresh()

            choice_char = get_one(self.stdscr)
            if choice_char in [ord('O'), ord('o')]:
                choice = 0
                break
            elif choice_char in [ord('S'), ord('s')]:
                choice = 1
                break
            elif choice_char in [ord('A'), ord('a')]:
                choice = 2
                break
            elif choice_char in [ord('G'), ord('g')]:
                choice = 3
                break
            
        # Get amount to buy
        while True:
            self.stdscr.move(21, 42)
            self.stdscr.clrtobot()

            # Calculate how much player can afford
            afford = self.cash // self.price[choice]
            self.stdscr.attron(curses.A_REVERSE)
            self.stdscr.addstr(" You can ")
            self.stdscr.attroff(curses.A_REVERSE)
            self.stdscr.move(22, 0)
            self.stdscr.addstr(f"How much {self.items[choice]} shall")
            self.stdscr.move(22, 42)
            self.stdscr.attron(curses.A_REVERSE)
            self.stdscr.addstr("  afford ")
            self.stdscr.move(23, 42)
            self.stdscr.addstr("         ")
            self.stdscr.move(23, 42)
        
            # Add appropriate spacing based on number size
            if afford < 100:
                space = "    "
            elif afford < 10000:
                space = "   "
            elif afford < 1000000:
                space = "  "
            elif afford < 100000000:
                space = " "
            else:
                space = ""
                
            self.stdscr.addstr(f"{space}{afford}")
            self.stdscr.attroff(curses.A_REVERSE)

            self.stdscr.move(23, 0)
            self.stdscr.addstr("I buy, Taipan: ")
            self.stdscr.refresh()

            amount = get_num(self.stdscr, 9)
            if amount == -1:
                amount = self.cash // self.price[choice]
            if amount <= self.cash // self.price[choice]:
                break

        # Update game state
        self.cash -= (amount * self.price[choice])
        self.hold_[choice] += amount
        self.hold -= amount
        return

    def sell(self) -> None:
        """Handle selling merchandise"""
        choice = 0
        amount = 0

        # Get item choice
        while True:
            self.stdscr.move(22, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("What do you wish me to sell, Taipan? ")
            self.stdscr.refresh()

            choice_char = get_one(self.stdscr)
            if choice_char in [ord('O'), ord('o')]:
                choice = 0
                break
            elif choice_char in [ord('S'), ord('s')]:
                choice = 1
                break
            elif choice_char in [ord('A'), ord('a')]:
                choice = 2
                break
            elif choice_char in [ord('G'), ord('g')]:
                choice = 3
                break

        # Get amount to sell
        while True:
            self.stdscr.move(22, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr(f"How much {self.items[choice]} shall\n")
            self.stdscr.addstr("I sell, Taipan: ")
            self.stdscr.refresh()

            amount = get_num(self.stdscr, 9)
            if amount == -1:
                amount = self.hold_[choice]
            if self.hold_[choice] >= amount:
                self.hold_[choice] -= amount
                break

        self.cash += (amount * self.price[choice])
        self.hold += amount

    def visit_bank(self) -> None:
        """Handle bank deposits and withdrawals"""
        amount = 0

        # Handle deposit
        while True:
            self.stdscr.move(16, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("Comprador's Report\n\n")
            self.stdscr.addstr("How much will you deposit? ")
            self.stdscr.refresh()

            amount = get_num(self.stdscr, 9)
            if amount == -1:
                amount = self.cash
            if amount <= self.cash:
                self.cash -= amount
                self.bank += amount
                break
            else:
                self.stdscr.move(18, 0)
                self.stdscr.clrtobot()
                self.stdscr.addstr(f"Taipan, you only have {fancy_numbers(self.cash)}\n")
                self.stdscr.addstr("in cash.\n")
                self.stdscr.refresh()
                self.stdscr.timeout(L_PAUSE)
                self.stdscr.getch()
                self.stdscr.timeout(-1)

        self.port_stats()

        # Handle withdrawal
        while True:
            self.stdscr.move(16, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("Comprador's Report\n\n")
            self.stdscr.addstr("How much will you withdraw? ")
            self.stdscr.refresh()

            amount = get_num(self.stdscr, 9)
            if amount == -1:
                amount = self.bank
            if amount <= self.bank:
                self.cash += amount
                self.bank -= amount
                break
            else:
                self.stdscr.addstr(f"Taipan, you only have {fancy_numbers(self.bank)}\n")
                self.stdscr.addstr("in the bank.")
                self.stdscr.refresh()
                self.stdscr.timeout(L_PAUSE)
                self.stdscr.getch()
                self.stdscr.timeout(-1)

        self.port_stats()

    def transfer(self) -> None:
        """Handle cargo transfers between ship's hold and warehouse"""
        # Check if there's any cargo to transfer
        if (self.hkw_[0] == 0 and self.hold_[0] == 0 and
            self.hkw_[1] == 0 and self.hold_[1] == 0 and
            self.hkw_[2] == 0 and self.hold_[2] == 0 and
            self.hkw_[3] == 0 and self.hold_[3] == 0):
            self.stdscr.move(22, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("You have no cargo, Taipan.\n")
            self.stdscr.refresh()
            self.stdscr.timeout(L_PAUSE)
            self.stdscr.getch()
            self.stdscr.timeout(-1)
            return

        # Calculate warehouse usage
        in_use = sum(self.hkw_)

        # Transfer cargo from hold to warehouse
        for i in range(4):
            if self.hold_[i] > 0:
                while True:
                    self.stdscr.move(16, 0)
                    self.stdscr.clrtobot()
                    self.stdscr.addstr("Comprador's Report\n\n")
                    self.stdscr.addstr(f"How much {self.items[i]} shall I move\n")
                    self.stdscr.addstr("to the warehouse, Taipan? ")
                    self.stdscr.refresh()

                    amount = get_num(self.stdscr, 9)
                    if amount == -1:
                        amount = self.hold_[i]
                    if amount <= self.hold_[i]:
                        if (in_use + amount) <= 10000:
                            self.hold_[i] -= amount
                            self.hkw_[i] += amount
                            self.hold += amount
                            in_use += amount
                            break
                        else:
                            self.stdscr.move(18, 0)
                            self.stdscr.clrtobot()
                            self.stdscr.addstr("Taipan, the warehouse is full!\n")
                            self.stdscr.refresh()
                            self.stdscr.timeout(L_PAUSE)
                            self.stdscr.getch()
                            self.stdscr.timeout(-1)
                    else:
                        self.stdscr.move(18, 0)
                        self.stdscr.clrtobot()
                        self.stdscr.addstr("Taipan, you don't have that much!\n")
                        self.stdscr.refresh()
                        self.stdscr.timeout(L_PAUSE)
                        self.stdscr.getch()
                        self.stdscr.timeout(-1)

        # Transfer cargo from warehouse to hold
        for i in range(4):
            if self.hkw_[i] > 0:
                while True:
                    self.stdscr.move(16, 0)
                    self.stdscr.clrtobot()
                    self.stdscr.addstr("Comprador's Report\n\n")
                    self.stdscr.addstr(f"How much {self.items[i]} shall I move\n")
                    self.stdscr.addstr("to the hold, Taipan? ")
                    self.stdscr.refresh()

                    amount = get_num(self.stdscr, 9)
                    if amount == -1:
                        amount = self.hkw_[i]
                    if amount <= self.hkw_[i]:
                        if (self.hold - amount) >= 0:
                            self.hkw_[i] -= amount
                            self.hold_[i] += amount
                            self.hold -= amount
                            in_use -= amount
                            break
                        else:
                            self.stdscr.move(18, 0)
                            self.stdscr.clrtobot()
                            self.stdscr.addstr("Taipan, the hold is full!\n")
                            self.stdscr.refresh()
                            self.stdscr.timeout(L_PAUSE)
                            self.stdscr.getch()
                            self.stdscr.timeout(-1)
                    else:
                        self.stdscr.move(18, 0)
                        self.stdscr.clrtobot()
                        self.stdscr.addstr("Taipan, you don't have that much!\n")
                        self.stdscr.refresh()
                        self.stdscr.timeout(L_PAUSE)
                        self.stdscr.getch()
                        self.stdscr.timeout(-1)

        self.port_stats()

    def quit(self) -> None:
        """Handle quitting current port and moving to new location"""
        choice = 0
        result = self.BATTLE_NOT_FINISHED

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Taipan, do you wish me to go to:\n")
        self.stdscr.addstr("1) Hong Kong, 2) Shanghai, 3) Nagasaki,\n")
        self.stdscr.addstr("4) Saigon, 5) Manila, 6) Singapore, or\n")
        self.stdscr.addstr("7) Batavia ? ")
        self.stdscr.refresh()

        while True:
            self.stdscr.move(21, 13)
            self.stdscr.clrtobot()

            choice = get_num(self.stdscr, 1)

            if choice == self.port:
                self.stdscr.addstr("\n\nYou're already here, Taipan.")
                self.stdscr.refresh()
                self.stdscr.timeout(L_PAUSE)
                self.stdscr.getch()
                self.stdscr.timeout(-1)
            elif 1 <= choice <= 7:
                self.port = choice
                break

        self.stdscr.move(6, 43)
        self.stdscr.addstr(" ")
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(self.locations[0])
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("  ")

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("  Captain's Report\n\n")

        if random.randint(0, self.bp - 1) == 0:
            num_ships = random.randint(1, (self.capacity // 10) + self.guns)
            if num_ships > 9999:
                num_ships = 9999
            self.stdscr.addstr(f"{num_ships} hostile ships approaching, Taipan!\n")
            self.stdscr.refresh()

            self.stdscr.timeout(M_PAUSE)
            self.stdscr.getch()
            self.stdscr.timeout(-1)

            result = self.sea_battle(self.GENERIC, num_ships)
            
        if result == self.BATTLE_INTERRUPTED:
            self.port_stats()
            self.stdscr.move(6, 43)
            self.stdscr.addstr(" ")
            self.stdscr.attron(curses.A_REVERSE)
            self.stdscr.addstr(self.locations[0])
            self.stdscr.attroff(curses.A_REVERSE)
            self.stdscr.addstr("  ")

            self.stdscr.move(16, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("  Captain's Report\n\n")
            self.stdscr.addstr("Li Yuen's fleet drove them off!")

            self.stdscr.move(16, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("  Captain's Report\n\n")
            self.stdscr.addstr("Li Yuen's fleet drove them off!")
            self.stdscr.refresh()

            self.stdscr.timeout(M_PAUSE)
            self.stdscr.getch()
            self.stdscr.timeout(-1)

        # Handle Li Yuen's pirates encounter
        if ((result == self.BATTLE_NOT_FINISHED and random.randint(0, 3 + (8 * self.li)) == 0) or 
            result == self.BATTLE_INTERRUPTED):
            self.stdscr.move(18, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("Li Yuen's pirates, Taipan!!\n\n")
            self.stdscr.refresh()

            self.stdscr.timeout(M_PAUSE)
            self.stdscr.getch()
            self.stdscr.timeout(-1)

            if self.li > 0:
                self.stdscr.addstr("Good joss!! They let us be!!\n")
                self.stdscr.refresh()

                self.stdscr.timeout(M_PAUSE)
                self.stdscr.getch()
                self.stdscr.timeout(-1)

                return
            else:
                num_ships = random.randint(0, (self.capacity // 5) + self.guns) + 5

                self.stdscr.addstr(f"{num_ships} ships of Li Yuen's pirate\n")
                self.stdscr.addstr("fleet, Taipan!!\n")
                self.stdscr.refresh()

                self.stdscr.timeout(M_PAUSE)
                self.stdscr.getch()
                self.stdscr.timeout(-1)

                result = self.sea_battle(self.LI_YUEN, num_ships)

        # Handle battle results
        if result > self.BATTLE_NOT_FINISHED:
            self.port_stats()
            self.stdscr.move(6, 43)
            self.stdscr.addstr(" ")
            self.stdscr.attron(curses.A_REVERSE)
            self.stdscr.addstr(self.locations[0])
            self.stdscr.attroff(curses.A_REVERSE)
            self.stdscr.addstr("  ")

            self.stdscr.move(16, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("  Captain's Report\n\n")
            if result == self.BATTLE_WON:  # Victory!
                self.stdscr.addstr("We captured some booty.\n")
                self.stdscr.addstr(f"It's worth {fancy_numbers(self.booty)}!")
                self.cash += self.booty
            elif result == self.BATTLE_FLED:  # Ran and got away.
                self.stdscr.addstr("We made it!")
            else:  # result == BATTLE_LOST - Ship lost!
                assert result != self.BATTLE_INTERRUPTED  # Shouldn't get interrupted when fighting Li Yuen
                self.stdscr.addstr("The buggers got us, Taipan!!!\n")
                self.stdscr.addstr("It's all over, now!!!")
                self.stdscr.refresh()

                self.stdscr.timeout(L_PAUSE)
                self.stdscr.getch()
                self.stdscr.timeout(-1)

                self.final_stats()
                return

            self.stdscr.refresh()
            self.stdscr.timeout(M_PAUSE)
            self.stdscr.getch()
            self.stdscr.timeout(-1)

        if random.randint(0, 9) == 0:
            self.stdscr.move(18, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("Storm, Taipan!!\n\n")
            self.stdscr.refresh()
            self.stdscr.timeout(M_PAUSE)
            self.stdscr.getch()
            self.stdscr.timeout(-1)

            if random.randint(0, 29) == 0:
                self.stdscr.addstr("   I think we're going down!!\n\n")
                self.stdscr.refresh()
                self.stdscr.timeout(M_PAUSE)
                self.stdscr.getch()
                self.stdscr.timeout(-1)

                if ((self.damage / self.capacity * 3) * random.random()) >= 1:
                    self.stdscr.addstr("We're going down, Taipan!!\n")
                    self.stdscr.refresh()
                    self.stdscr.timeout(L_PAUSE)
                    self.stdscr.getch()
                    self.stdscr.timeout(-1)

                    self.final_stats()

            self.stdscr.addstr("    We made it!!\n\n")
            self.stdscr.refresh()
            self.stdscr.timeout(M_PAUSE)
            self.stdscr.getch()
            self.stdscr.timeout(-1)

            if random.randint(0, 2) == 0:
                orig = self.port
                while self.port == orig:
                    self.port = random.randint(1, 7)

                self.stdscr.move(18, 0)
                self.stdscr.clrtobot()
                self.stdscr.addstr("We've been blown off course\n")
                self.stdscr.addstr(f"to {self.locations[self.port]}")
                self.stdscr.refresh()
                self.stdscr.timeout(M_PAUSE)
                self.stdscr.getch()
                self.stdscr.timeout(-1)

        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
            self.ec += 10
            self.ed += 0.5

        self.debt = int(self.debt + (self.debt * 0.1))
        self.bank = int(self.bank + (self.bank * 0.005))
        self.set_prices()

        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr(f"Arriving at {self.locations[self.port]}...")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def overload(self) -> None:
        """Handle ship overload situation"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Your ship is overloaded, Taipan!!")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def final_stats(self) -> None:
        """Display final game statistics"""
        years = self.year - 1860
        time = ((self.year - 1860) * 12) + self.month
        choice = 0

        self.stdscr.clear()
        self.stdscr.addstr("Your final status:\n\n")
        self.cash = self.cash + self.bank - self.debt
        self.stdscr.addstr(f"Net cash:  {fancy_numbers(self.cash)}\n\n")
        self.stdscr.addstr(f"Ship size: {self.capacity} units with {self.guns} guns\n\n")
        self.stdscr.addstr(f"You traded for {years} year")
        if years != 1:
            self.stdscr.addstr("s")
        self.stdscr.addstr(f" and {self.month} month")
        if self.month > 1:
            self.stdscr.addstr("s")
        self.stdscr.addstr("\n\n")
        self.cash = self.cash / 100 / time
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(f"Your score is {int(self.cash)}.\n")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("\n")
        if (self.cash < 100) and (self.cash >= 0):
            self.stdscr.addstr("Have you considered a land based job?\n\n\n")
        elif self.cash < 0:
            self.stdscr.addstr("The crew has requested that you stay on\n")
            self.stdscr.addstr("shore for their safety!!\n\n")
        else:
            self.stdscr.addstr("\n\n\n")
        self.stdscr.addstr("Your Rating:\n")
        self.stdscr.addstr(" _______________________________\n")
        self.stdscr.addstr("|")
        if self.cash > 49999:
            self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("Ma Tsu")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("         50,000 and over |\n")
        self.stdscr.addstr("|")
        if (self.cash < L_PAUSE) and (self.cash > 7999):
            self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("Master Taipan")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("   8,000 to 49,999|\n")
        self.stdscr.addstr("|")
        if (self.cash < 8000) and (self.cash > 999):
            self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("Taipan")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("          1,000 to  7,999|\n")
        self.stdscr.addstr("|")
        if (self.cash < 1000) and (self.cash > 499):
            self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("Compradore")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("        500 to    999|\n")
        self.stdscr.addstr("|")
        if self.cash < 500:
            self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("Galley Hand")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("       less than 500|\n")
        self.stdscr.addstr("|_______________________________|\n\n")

        while choice not in [ord('Y'), ord('y'), ord('N'), ord('n')]:
            self.stdscr.move(22, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("Play again? ")
            self.stdscr.refresh()
            choice = get_one(self.stdscr)

        if choice in [ord('Y'), ord('y')]:
            self.bank = 0
            self.hkw_ = [0] * 4
            self.hold_ = [0] * 4
            self.hold = 0
            self.capacity = 60
            self.damage = 0
            self.month = 1
            self.year = 1860
            self.port = 1

            self.splash_intro()
            self.name_firm()
            self.cash_or_guns()
            self.set_prices()
            return

        self.stdscr.clear()
        self.stdscr.refresh()
        curses.nocbreak()
        curses.endwin()
        exit(0)

    def main(self) -> None:
        """Main game loop"""
        try:
            random.seed(os.getpid())
            self.init_curses()
            self.splash_intro()
            self.name_firm()
            self.cash_or_guns()
            self.set_prices()

            while True:
                choice = 0
                self.port_stats()

                # Li Yuen extortion check
                if self.port == 1 and self.li == 0 and self.cash > 0:
                    self.li_yuen_extortion()

                # McHenry check
                if self.port == 1 and self.damage > 0:
                    McHenry(self).offer_repairs()

                # Elder Brother Wu warning
                if self.port == 1 and self.debt >= 10000 and self.wu_warn == 0:
                    self.show_wu_warning()
                    self.wu_warn = 1

                # Elder Brother Wu encounter
                if self.port == 1:
                    self.elder_brother_wu()

                # Random events
                if random.randint(0, 3) == 0:
                    if random.randint(0, 1) == 0:
                        self.new_ship()
                    elif self.guns < 1000:
                        self.new_gun()

                # Opium seizure
                if self.port != 1 and random.randint(0, 17) == 0 and self.hold_[0] > 0:
                    self.handle_opium_seizure()

                # Warehouse theft
                if random.randint(0, 49) == 0 and sum(self.hkw_) > 0:
                    self.handle_warehouse_theft()

                # Li Yuen counter
                if random.randint(0, 19) == 0:
                    if self.li > 0:
                        self.li += 1
                    if self.li == 4:
                        self.li = 0

                # Li Yuen message
                if self.port != 1 and self.li == 0 and random.randint(0, 3) != 0:
                    self.show_li_yuen_message()

                # Good prices
                if random.randint(0, 8) == 0:
                    self.good_prices()

                # Robbery
                if self.cash > L_PAUSE and random.randint(0, 19) == 0:
                    self.handle_robbery()

                # Main game loop
                while True:
                    while choice not in [ord('Q'), ord('q')]:
                        choice = self.port_choices()
                        
                        if choice in [ord('B'), ord('b')]:
                            self.buy()
                        elif choice in [ord('S'), ord('s')]:
                            self.sell()
                        elif choice in [ord('V'), ord('v')]:
                            self.visit_bank()
                        elif choice in [ord('T'), ord('t')]:
                            self.transfer()
                        elif choice in [ord('W'), ord('w')]:
                            self.elder_brother_wu()
                        elif choice in [ord('R'), ord('r')]:
                            self.retire()

                        self.port_stats()

                    choice = 0
                    if self.hold >= 0:
                        self.quit()
                        break
                    else:
                        self.overload()

        finally:
            self.cleanup_curses()

    def show_wu_warning(self) -> None:
        """Show Elder Brother Wu's warning message"""
        braves = random.randint(50, 149)
        
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr(f"Elder Brother Wu has sent {braves} braves\n")
        self.stdscr.addstr("to escort you to the Wu mansion, Taipan.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Elder Brother Wu reminds you of the\n")
        self.stdscr.addstr("Confucian ideal of personal worthiness,\n")
        self.stdscr.addstr("and how this applies to paying one's\n")
        self.stdscr.addstr("debts.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("He is reminded of a fabled barbarian\n")
        self.stdscr.addstr("who came to a bad end, after not caring\n")
        self.stdscr.addstr("for his obligations.\n\n")
        self.stdscr.addstr("He hopes no such fate awaits you, his\n")
        self.stdscr.addstr("friend, Taipan.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def handle_opium_seizure(self) -> None:
        """Handle opium seizure by authorities"""
        fine = (self.cash / 1.8) * random.random() + 1
        if self.cash == 0:
            fine = 0

        self.hold += self.hold_[0]
        self.hold_[0] = 0
        self.cash -= fine

        self.port_stats()

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Bad Joss!!\n")
        self.stdscr.addstr("The local authorities have seized your\n")
        if fine <= 0:
            self.stdscr.addstr("Opium cargo, Taipan!")
        else:
            self.stdscr.addstr("Opium cargo and have also fined you\n")
            self.stdscr.addstr(f"{fancy_numbers(fine)}, Taipan!\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def handle_warehouse_theft(self) -> None:
        """Handle warehouse theft event"""
        for i in range(4):
            self.hkw_[i] = int((self.hkw_[i] / 1.8) * random.random())

        self.port_stats()

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Messenger reports large theft\n")
        self.stdscr.addstr("from warehouse, Taipan.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def show_li_yuen_message(self) -> None:
        """Show Li Yuen's message"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Li Yuen has sent a Lieutenant,\n")
        self.stdscr.addstr("Taipan.  He says his admiral wishes\n")
        self.stdscr.addstr("to see you in Hong Kong, posthaste!\n")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def handle_robbery(self) -> None:
        """Handle robbery event"""
        robbed = (self.cash / 1.4) * random.random()
        self.cash -= robbed
        self.port_stats()

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Bad Joss!!\n")
        self.stdscr.addstr("You've been beaten up and\n")
        self.stdscr.addstr(f"robbed of {fancy_numbers(robbed)} in cash, Taipan!!\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def sea_battle(self, id: int, num_ships: int) -> int:
        """Handle sea battle with pirates"""
        sea_battle = SeaBattle(self)
        return sea_battle.battle(id, num_ships)

    def retire(self) -> None:
        """Handle retirement sequence"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("                         \n")
        self.stdscr.addstr(" Y o u ' r e    a        \n")
        self.stdscr.addstr("                         \n")
        self.stdscr.addstr(" M I L L I O N A I R E ! \n")
        self.stdscr.addstr("                         \n")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

        self.final_stats()

if __name__ == "__main__":
    game = TaipanGame()
    game.main() 