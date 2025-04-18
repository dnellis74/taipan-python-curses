#!/usr/bin/env python3
"""
Taipan - A Python port of the classic trading game
Original C version by Jay Link <jlink@ilbbs.com>
Based on Apple ][ program by Ronald J. Berg
"""

import random
import os
from sea_battle import SeaBattle
from constants import *
from messages import Messages

class TaipanGame:
    def __init__(self):
        self.screen = Messages();
        # Game state
        self.firm = ""  # Firm name (was char[23])

        # Item and location names
        self.items = ["Opium", "Silk", "Arms", "General Cargo"]

        # Financial state
        self.cash = STARTING_CASH
        self.bank = STARTING_BANK
        self.debt = STARTING_DEBT

        # Combat stats
        self.ec = BASE_ENEMY_HEALTH
        self.ed = BASE_ENEMY_DAMAGE
        
        self.locations = [
            "At sea", "Hong Kong", "Shanghai", "Nagasaki",
            "Saigon", "Manila", "Singapore", "Batavia"
        ]

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

    def splash_intro(self) -> None:
        """Display the game's splash screen and wait for user input."""
        self.screen.message_splash()

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

            choice = 0
            while choice not in [ord('1'), ord('2')]:
                choice = self.screen.keyboard.get_one()

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
        self.screen.port_stats(status, self.firm, self.hkw_, self.hold, self.hold_,
                               self.cash, self.bank, self.guns, self.debt,
                               self.month, self.year, self.locations[self.port])

    def port_choices(self) -> int:
        """Display port menu choices and get user selection"""
        choice = 0

        self.screen.message_comprador_prices(self.price)

        while True:
            can_retire = (self.cash + self.bank) >= 1000000
            self.screen.message_port_menu(can_retire)

            choice = self.screen.keyboard.get_one()
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
            choice = self.screen.keyboard.get_one()

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
            choice = self.screen.keyboard.get_one()
        if choice in [ord('Y'), ord('y')]:
            self.cash -= amount
            self.hold -= 10
            self.guns += 1
        self.port_stats()

    def elder_brother_wu(self) -> None:
        """Handle Elder Brother Wu's interactions"""
        choice = 0
        wu = 0
        self.screen.message_wu_business()
        if self.screen.keyboard.choice_yes_no():
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

                    choice = self.screen.keyboard.get_one()
                    if choice in [ord('N'), ord('n')]:
                        self.screen.message_wu_game_over()
                        self.final_stats()
                    elif choice in [ord('Y'), ord('y')]:
                        self.cash += i
                        self.debt += j
                        self.port_stats()
                        self.screen.message_wu_good_joss()
                        return
            else:
                self.screen.message_wu_repay()

                wu = self.screen.keyboard.get_num(9)
                if wu == -1:
                        wu = min(self.cash, self.debt)
                if wu <= self.cash:
                    if wu > self.debt:
                        self.screen.message_paid_in_full()
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

                wu = self.screen.keyboard.get_num(9)
                if wu == -1:
                        wu = self.cash * 2
                if wu <= (self.cash * 2):
                        self.cash += wu
                        self.debt += wu
                else:
                    self.screen.message_wu_too_much()

                self.port_stats()

        if self.debt > 20000 and self.cash > 0 and random.randint(0, 4) == 0:
            num = random.randint(1, 3)
            self.cash = 0
            self.port_stats()
            self.screen.message_mugged(num)

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

        if self.screen.keyboard.choice_yes_no():
            if amount <= self.cash:
                self.cash -= amount
                self.li = 1
            else:
                self.screen.message_not_enough()

                if self.screen.keyboard.choice_yes_no():
                    amount -= self.cash
                    self.debt += amount
                    self.cash = 0
                    self.li = 1
                    self.screen.message_wu_li_accept()
                else:
                    self.cash = 0
                    self.screen.message_wu_li_deny()
        self.port_stats()

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
        self.screen.message_buy_prompt()
        choice_char = self.screen.keyboard.get_one()
        choice = 0
        amount = 0

        # Get item choice
        while True:
            choice_char = self.screen.keyboard.get_one()
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
            # Calculate how much player can afford
            afford = self.cash // self.price[choice]
            self.screen.message_afford_amount(afford)
            amount = self.screen.keyboard.get_num(9)
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
        self.screen.message_sell_prompt()
        choice_char = self.screen.keyboard.get_one()
        choice = 0
        if choice_char in [ord('O'), ord('o')]:
            choice = 0
        elif choice_char in [ord('S'), ord('s')]:
            choice = 1
        elif choice_char in [ord('A'), ord('a')]:
            choice = 2
        elif choice_char in [ord('G'), ord('g')]:
            choice = 3

        # Get amount to sell
        while True:
            self.screen.message_sell_amount(self.items[choice])

            amount = self.screen.keyboard.get_num(9)
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
            amount = self.screen.keyboard.get_num(9)
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
            amount = self.screen.keyboard.get_num(9)
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
                    self.screen.message_to_warehouse(self.items[i])
                    amount = self.screen.keyboard.get_num(9)
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
                    self.screen.message_to_hold(self.items[i])
                    amount = self.screen.keyboard.get_num(9)
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
        
    def offer_repairs(self) -> None:
        """Offer to repair the ship"""
        self.screen.message_mchenry_repairs()

        choice = self.screen.keyboard.get_one()
        if choice in [ord('Y'), ord('y')]:
            self.repair_ship()
        self.port_stats()

    def _handle_repairs(self) -> None:
        """Handle the actual repair process"""
        percent = int((self.damage / self.capacity) * 100)
        time = ((self.year - 1860) * 12) + self.month

        br = int((((60 * (time + 3) / 4) * random.random() +
                 25 * (time + 3) / 4) * self.capacity / 50))
        repair_price = (br * self.damage) + 1
        amount = 0

        self.screen.message_mchenry_damage(percent, repair_price)

        while True:
            amount = self.skeyboard.get_num(9)
            # If player cancels, set amount to repair price
            if amount == -1:
                amount = repair_price

            if amount > self.cash:
                amount -= self._handle_insufficient_funds(amount)
                
            if amount <= self.cash:
                self.cash -= amount
                assert br > 0  # Don't divide by zero
                self.damage -= int((amount / br) + 0.5)
                self.damage = max(0, self.damage)
                self.port_stats()
                break
            else:
                self.screen.message_mchenry_no_free_work()

    def _handle_insufficient_funds(self, amount: int) -> None:
        """Handle case where player doesn't have enough cash"""
        self.screen.message_insufficient_funds()
        self.screen.message_wu_difference_offer()
        
        if self.screen.keyboard.choice_yes_no():
            self.screen.message_wu_loan_terms()
            loan = amount - self.cash
            self.debt += loan
            return loan
        else:
            self.screen.message_wu_deny_help()
            return 0

    def visit(self) -> None:
        self.screen.message_mchenry_visit()
        if self.screen.keyboard.choice_yes_no():
            self.screen.message_mchenry_spend()
            amount = self.screen.keyboard.get_num(9)
            if amount > 0:
                self.cash -= amount
                self.capacity += amount // 10
                self.screen.message_mchenry_new_capacity(self.capacity)

    def repair_ship(self) -> None:
        """Handle ship repairs"""
        amount = random.randint(0, 1000 * self.capacity) + 1000
        if amount > self.cash:
            self.screen.message_insufficient_cash(self.cash)
            return

        self.screen.message_mchenry_cost(amount)

        choice = self.screen.keyboard.get_one()
        if choice in [ord('Y'), ord('y')]:
            self.cash -= amount
            self.damage = 0
            self.screen.message_repairs_complete()
            self.port_stats()

    def quit(self) -> None:
        """Handle quitting current port and moving to new location"""
        choice = 0
        result = BATTLE_NOT_FINISHED

        self.screen.message_destinations()

        while True:
            self.screen.message_quit_input()

            choice = self.screen.keyboard.get_num(1)

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
            self.screen.message_after_battle_header(self.locations[0])
            if result == BATTLE_WON:  # Victory!
                self.screen.message_booty()
            elif result == BATTLE_FLED:  # Ran and got away.
                self.screen.message_escaped()
            else:  # result == BATTLE_LOST - Ship lost!
                assert result != BATTLE_INTERRUPTED  # Shouldn't get interrupted when fighting Li Yuen
                self.screen.message_all_over_now()
                self.final_stats()
                return

            self.screen.message_pause()

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

        if self.screen.keyboard.choice_yes_no():
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
            self.firm = self.screen.name_firm()
            self.cash_or_guns()
            self.set_prices()
            return
        else:
            self.screen.message_clear_refresh()
        exit(0)

    def main(self) -> None:
        """Main game loop"""
        try:
            random.seed(os.getpid())
            self.splash_intro()
            self.firm = self.screen.name_firm()
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
                    self.offer_repairs()

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
            self.screen.cleanup_curses()

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
        self.screen.keyboard.get_one()
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
        self.screen.message_to_hold(item)
        amount = self.screen.keyboard.get_num(4)
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
        self.screen.message_to_hold(item)
        amount = self.screen.keyboard.get_num(4)
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
