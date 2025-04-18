#!/usr/bin/env python3
"""
Taipan - A Python port of the classic trading game
Original C version by Jay Link <jlink@ilbbs.com>
Based on Apple ][ program by Ronald J. Berg
"""

import curses
import random
import os
from fancy_numbers import fancy_numbers
from sea_battle import SeaBattle
from constants import *
from mchenry import McHenry
from keyboard import choice_yes_no, get_one, get_num
from messages import Messages

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
        self.screen = Messages(self.stdscr)

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
        self.screen.message_splash()
        curses.curs_set(0)
        self.stdscr.refresh()

        self.stdscr.getch()
        curses.curs_set(1)

    def name_firm(self) -> None:
        """Set the firm name. In debug mode, sets to 'debug'."""
        if DEBUG:
            self.firm = "debug"
        else:
            self.screen.message_name_firm()

            character = 0
            self.firm = ""

            while character < 22:
                input_char = self.stdscr.getch()
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
            self.cash = 1000000
            self.debt = 1000
            self.guns = 5
            self.bp = 1  # Set battle probability to 1 for debug mode
            self.hold = 50
        else:
            self.screen.message_cash_or_guns()
            self.stdscr.move(15, 0)
            self.stdscr.clrtobot()
            self.stdscr.addstr("          ?")
            self.stdscr.refresh()
            choice = 0
            while choice not in [ord('1'), ord('2')]:
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

        self.screen.message_comprador_prices(self.price)

        while True:
            can_retire = (self.cash + self.bank) >= 1000000
            self.screen.message_port_menu(can_retire)

            choice = get_one(self.stdscr)
            if self.port == 1:
                if can_retire:
                    if choice in [ord('B'), ord('b'), ord('S'), ord('s'), 
                                ord('V'), ord('v'), ord('T'), ord('t'),
                                ord('W'), ord('w'), ord('Q'), ord('q'),
                                ord('R'), ord('r')]:
                        break
                else:
                    if choice in [ord('B'), ord('b'), ord('S'), ord('s'),
                                ord('V'), ord('v'), ord('T'), ord('t'),
                                ord('W'), ord('w'), ord('Q'), ord('q')]:
                        break
            else:
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

        self.screen.message_new_ship(self.damage, amount)

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
        self.screen.message_new_gun(amount)
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
        i = 1.8
        j = 0
        amount = 0
        if time > 12:
            j = random.randint(0, 1000 * time) + (1000 * time)
            i = 1
        amount = ((self.cash / i) * random.random()) + j
        self.screen.message_li_donation(amount)

        if choice_yes_no(self.stdscr):
            if amount <= self.cash:
                self.cash -= amount
                self.li = 1
            else:
                self.screen.message_not_enough()
                self.stdscr.move(18, 0)
                self.stdscr.clrtobot()
                self.stdscr.addstr("Do you want Elder Brother Wu to make up\n")
                self.stdscr.addstr("the difference for you? ")

                if choice_yes_no(self.stdscr):
                    amount -= self.cash
                    self.debt += amount
                    self.cash = 0
                    self.li = 1
                    self.screen.message_wu_li_accept()
                else:
                    self.cash = 0
                    self.screen.message_wu_li_deny()
        self.port_stats()

    def elder_brother_wu(self) -> None:
        """Handle Elder Brother Wu's interactions"""
        choice = 0
        wu = 0
        self.screen.message_wu_business()
        self.stdscr.move(19, 21)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

        if choice_yes_no(self.stdscr):
            # You're out of cash, bank, guns, and hold.   Li Yeun bails you out.
            if (self.cash == 0 and self.bank == 0 and self.guns == 0 and
                self.hold_[0] == 0 and self.hkw_[0] == 0 and
                self.hold_[1] == 0 and self.hkw_[1] == 0 and
                self.hold_[2] == 0 and self.hkw_[2] == 0 and
                self.hold_[3] == 0 and self.hkw_[3] == 0):
                
                i = random.randint(500, 1999)
                j = random.randint(0, 1999) * self.wu_bailout + 1500
                self.wu_bailout += 1

                while True:
                    self.screen.message_wu_pity(i, j)

                    choice = get_one(self.stdscr)
                    if choice in [ord('N'), ord('n')]:
                        self.screen.message_wu_game_over()
                        self.final_stats()
                    elif choice in [ord('Y'), ord('y')]:
                        self.cash += i
                        self.debt += j
                        self.port_stats()
                        self.screen.message_wu_good_joss()
                        return

            self.screen.message_wu_repay()

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
            else:
                self.screen.message_insufficient_cash(self.cash)

            self.port_stats()

            self.screen.message_wu_borrow()

            wu = get_num(self.stdscr, 9)
            if wu == -1:
                wu = self.cash * 2
            if wu <= (self.cash * 2):
                self.cash += wu
                self.debt += wu
            else:
                self.screen.message_wu_too_much()
                self.stdscr.refresh()
                self.stdscr.timeout(L_PAUSE)
                self.stdscr.getch()
                self.stdscr.timeout(-1)

        self.port_stats()

        if self.debt > 20000 and self.cash > 0 and random.randint(0, 4) == 0:
            num = random.randint(1, 3)
            self.cash = 0
            self.port_stats()
            self.screen.message_mugged(num)

    def good_prices(self) -> None:
        """Handle random price changes for items"""
        i = random.randint(0, 3)
        j = random.randint(0, 1)

        item = self.items[i]
        if j == 0:
            self.price[i] = self.price[i] // 5
        else:
            self.price[i] = self.price[i] * (random.randint(0, 4) + 5)
        self.screen.message_price_change(item, self.price[i], j == 0)

    def buy(self) -> None:
        """Handle buying merchandise"""
        choice = 0
        amount = 0

        # Get item choice
        while True:
            self.screen.message_buy_prompt()
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
            self.screen.message_afford_amount(afford)

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
            self.screen.message_sell_prompt()
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
            self.screen.message_sell_amount(self.items[choice])

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
            self.screen.message_bank_deposit()
            amount = get_num(self.stdscr, 9)
            if amount == -1:
                amount = self.cash
            if amount <= self.cash:
                self.cash -= amount
                self.bank += amount
                break
            else:
                self.screen.message_insufficient_cash(self.cash)

        self.port_stats()

        # Handle withdrawal
        while True:
            self.screen.message_bank_withdraw()
            amount = get_num(self.stdscr, 9)
            if amount == -1:
                amount = self.bank
            if amount <= self.bank:
                self.cash += amount
                self.bank -= amount
                break
            else:
                self.screen.message_insufficient_bank(self.bank)

        self.port_stats()

    def transfer(self) -> None:
        """Handle cargo transfers between ship's hold and warehouse"""
        if (self.hkw_[0] == 0 and self.hold_[0] == 0 and
            self.hkw_[1] == 0 and self.hold_[1] == 0 and
            self.hkw_[2] == 0 and self.hold_[2] == 0 and
            self.hkw_[3] == 0 and self.hold_[3] == 0):
            self.screen.message_no_cargo()
            return

        # Calculate warehouse usage
        in_use = sum(self.hkw_)

        # Transfer cargo from hold to warehouse
        for i in range(4):
            if self.hold_[i] > 0:
                while True:
                    self.screen.message_transfer_prompt(self.items[i])
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
                            self.screen.message_warehouse_full()
                    else:
                        self.screen.message_not_enough()

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
                            self.screen.message_hold_full()
                    else:
                        self.screen.message_not_enough()

        self.port_stats()

    def quit(self) -> None:
        """Handle quitting current port and moving to new location"""
        choice = 0
        result = BATTLE_NOT_FINISHED

        self.screen.message_destinations()

        while True:
            self.stdscr.move(21, 13)
            self.stdscr.clrtobot()

            choice = get_num(self.stdscr, 1)

            if choice == self.port:
                self.screen.message_already_here()
            elif 1 <= choice <= 7:
                self.port = choice
                break

        self.screen.message_location_update(self.locations[0])
        self.screen.message_captains_report_header()

        if random.randint(0, self.bp - 1) == 0:
            num_ships = random.randint(1, (self.capacity // 10) + self.guns)
            if num_ships > 9999:
                num_ships = 9999
            self.screen.message_hostile_ships(num_ships)
            result = self.sea_battle(GENERIC, num_ships)
            
        if result == BATTLE_INTERRUPTED:
            self.port_stats()
            self.screen.message_pirates_help(self.locations[0])

        # Handle Li Yuen's pirates encounter
        if ((result == BATTLE_NOT_FINISHED and random.randint(0, 3 + (8 * self.li)) == 0) or 
            result == BATTLE_INTERRUPTED):
            self.screen.message_li_yuen_pirates()
            if self.li > 0:
                self.screen.message_good_joss()
                return
            else:
                num_ships = random.randint(0, (self.capacity // 5) + self.guns) + 5
                self.screen.message_li_yuen_fleet(num_ships)
                result = self.sea_battle(LI_YUEN, num_ships)

        # Handle battle results
        if result > BATTLE_NOT_FINISHED:
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
            if result == BATTLE_WON:  # Victory!
                self.stdscr.addstr("We captured some booty.\n")
            elif result == BATTLE_FLED:  # Ran and got away.
                self.stdscr.addstr("We made it!")
            else:  # result == BATTLE_LOST - Ship lost!
                assert result != BATTLE_INTERRUPTED  # Shouldn't get interrupted when fighting Li Yuen
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
            self.screen.message_storm_sighted()

            if random.randint(0, 29) == 0:
                self.screen.message_going_down()

                if ((self.damage / self.capacity * 3) * random.random()) >= 1:
                    self.screen.message_sinking()
                    self.final_stats()

            self.screen.message_made_it()

            if random.randint(0, 2) == 0:
                orig = self.port
                while self.port == orig:
                    self.port = random.randint(1, 7)
                self.screen.message_off_course(self.locations[self.port])

        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
            self.ec += 10
            self.ed += 0.5

        self.debt = int(self.debt + (self.debt * 0.1))
        self.bank = int(self.bank + (self.bank * 0.005))
        self.set_prices()

        self.screen.message_arriving(self.locations[self.port])

    def final_stats(self) -> None:
        """Display final game statistics"""
        years = self.year - 1860
        time = ((self.year - 1860) * 12) + self.month
        self.screen.message_final_stats(self.cash + self.bank - self.debt, self.capacity, self.guns, years, self.month, time)

        if choice_yes_no(self.stdscr):
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
        else:
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
                    self.screen.message_li_yuen()

                # Good prices
                if random.randint(0, 8) == 0:
                    self.good_prices()

                # Robbery
                if self.cash > 25000 and random.randint(0, 19) == 0:
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
        braves = random.randint(1, 10)
        self.screen.message_wu_warning(braves)
        self.wu_warn = 1

    def handle_opium_seizure(self) -> None:
        """Handle opium seizure by authorities"""
        fine = (self.cash / 1.8) * random.random() + 1
        if self.cash == 0:
            fine = 0
        self.hold += self.hold_[0]
        self.hold_[0] = 0
        self.cash -= fine
        self.port_stats()
        self.screen.message_opium_seized(fine)

    def handle_warehouse_theft(self) -> None:
        """Handle warehouse theft event"""
        for i in range(4):
            self.hkw_[i] = int((self.hkw_[i] / 1.8) * random.random())
        self.port_stats()
        self.screen.message_warehouse_robbery()

    def handle_robbery(self) -> None:
        """Handle robbery event"""
        robbed = int((self.cash / 1.4) * random.random())
        self.cash -= robbed
        self.port_stats()
        self.screen.message_robbed(robbed)

    def sea_battle(self, battle_type: int, num_ships: int) -> int:
        """Handle a sea battle with pirates"""
        battle = SeaBattle(self)
        # Calculate booty
        time = ((self.year - 1860) * 12) + self.month
        booty = (time // 4 * 1000 * num_ships) + random.randint(0, 999) + 250
        result = battle.battle(battle_type, num_ships)
        if result == BATTLE_WON:  # Victory!
            self.cash += booty
        elif result == BATTLE_LOST:  # Ship lost!
            self.game_over = True
        self.screen.message_battle_results(result, booty)
        get_one(self.stdscr)
        return result

    def retire(self) -> None:
        """Handle retirement sequence"""
        self.screen.message_retire()
        self.final_stats()

    def warehouse_to_hold(self, item: str) -> None:
        """Move cargo from warehouse to ship's hold"""
        if self.hkw_[self.items.index(item)] == 0:
            self.screen.message_not_enough()
            return
        if self.hold == self.capacity:
            self.screen.message_hold_full()
            return
        self.screen.message_comprador_report(item)
        amount = get_num(self.stdscr, 4)
        if amount == -1:
            return
        if amount > self.hkw_[self.items.index(item)]:
            self.screen.message_not_enough()
            return
        if amount > self.capacity - self.hold:
            self.screen.message_hold_full()
            return
        self.hkw_[self.items.index(item)] -= amount
        self.hold += amount
        self.hold_[self.items.index(item)] += amount

    def hold_to_warehouse(self, item: str) -> None:
        """Move cargo from ship's hold to warehouse"""
        if self.hold_[self.items.index(item)] == 0:
            self.screen.message_not_enough()
            return
        if self.hkw_[self.items.index(item)] == 10000:
            self.screen.message_warehouse_full()
            return
        self.screen.message_comprador_report(item)
        amount = get_num(self.stdscr, 4)
        if amount == -1:
            return
        if amount > self.hold_[self.items.index(item)]:
            self.screen.message_not_enough()
            return
        if amount > 10000 - self.hkw_[self.items.index(item)]:
            self.screen.message_warehouse_full()
            return
        self.hold_[self.items.index(item)] -= amount
        self.hold -= amount
        self.hkw_[self.items.index(item)] += amount

if __name__ == "__main__":
    game = TaipanGame()
    game.main()
