import random
from typing import Optional
import curses

from constants import M_PAUSE, L_PAUSE
from python.keyboard import Keyboard

class McHenry:
    def __init__(self, game):
        self.game = game
        self.keyboard = Keyboard(game.stdscr)

    def offer_repairs(self) -> None:
        """Handle McHenry's ship repair offer"""
        self.game.stdscr.move(16, 0)
        self.game.stdscr.clrtobot()
        self.game.stdscr.addstr("Comprador's Report\n\n")
        self.game.stdscr.addstr("Taipan, Mc Henry from the Hong Kong\n")
        self.game.stdscr.addstr("Shipyards has arrived!!  He says, \"I see\n")
        self.game.stdscr.addstr("ye've a wee bit of damage to yer ship.\n")
        self.game.stdscr.addstr("Will ye be wanting repairs? ")
        self.game.stdscr.refresh()

        if self.keyboard.choice_yes_no():
            self._handle_repairs()

    def _handle_repairs(self) -> None:
        """Handle the actual repair process"""
        percent = int((self.game.damage / self.game.capacity) * 100)
        time = ((self.game.year - 1860) * 12) + self.game.month

        br = int((((60 * (time + 3) / 4) * random.random() +
                 25 * (time + 3) / 4) * self.game.capacity / 50))
        repair_price = (br * self.game.damage) + 1
        amount = 0

        self.game.stdscr.move(18, 0)
        self.game.stdscr.clrtobot()
        self.game.stdscr.addstr(f"Och, 'tis a pity to be {percent}% damaged.\n")
        self.game.stdscr.addstr(f"We can fix yer whole ship for {repair_price},\n")
        self.game.stdscr.addstr("or make partial repairs if you wish.\n")
        self.game.stdscr.addstr("How much will ye spend? ")
        self.game.stdscr.refresh()

        while True:
            amount = self.keyboard.get_num(9)
            # If player cancels, set amount to repair price
            if amount == -1:
                amount = repair_price

            if amount > self.game.cash:
                amount -= self._handle_insufficient_funds(amount)
                
            if amount <= self.game.cash:
                self.game.cash -= amount
                assert br > 0  # Don't divide by zero
                self.game.damage -= int((amount / br) + 0.5)
                self.game.damage = max(0, self.game.damage)
                self.game.port_stats()
                self.game.stdscr.refresh()
                break
            else:
                self.game.stdscr.move(18, 0)
                self.game.stdscr.clrtobot()
                self.game.stdscr.addstr("McHenry does not work for free, Taipan!\n")

    def _handle_insufficient_funds(self, amount: int) -> None:
        """Handle case where player doesn't have enough cash"""
        self.game.stdscr.move(18, 0)
        self.game.stdscr.clrtobot()
        self.game.stdscr.addstr("Taipan, you do not have enough cash!!\n\n")
        self.game.stdscr.refresh()

        self.game.stdscr.timeout(M_PAUSE)
        self.game.stdscr.getch()
        self.game.stdscr.timeout(-1)

        self.game.stdscr.addstr("Do you want Elder Brother Wu to make up\n")
        self.game.stdscr.addstr("the difference for you? ")
        
        if self.keyboard.choice_yes_no():
            self.game.stdscr.move(18, 0)
            self.game.stdscr.clrtobot()
            self.game.stdscr.addstr("Elder Brother has given McHenry the\n")
            self.game.stdscr.addstr("difference between what he wanted and\n")
            self.game.stdscr.addstr("your cash on hand and added the same\n")
            self.game.stdscr.addstr("amount to your debt.\n")

            self.game.stdscr.refresh()
            self.game.stdscr.timeout(L_PAUSE)
            self.game.stdscr.getch()
            self.game.stdscr.timeout(-1)
            loan = amount - self.game.cash
            self.game.debt += loan
            return loan
        else:
            self.game.stdscr.addstr("Very well. Elder Brother Wu will not pay\n")
            self.game.stdscr.addstr("McHenry the difference.  I would be very\n")
            self.game.stdscr.addstr("wary of pirates if I were you, Taipan.\n")

            self.game.stdscr.refresh()
            self.game.stdscr.timeout(L_PAUSE)
            self.game.stdscr.getch()
            self.game.stdscr.timeout(-1)
            return 0

    def visit(self) -> None:
        self.game.stdscr.clear()
        self.game.stdscr.move(0, 0)
        self.game.stdscr.addstr("McHenry is here, Taipan.")
        self.game.stdscr.move(1, 0)
        self.game.stdscr.addstr("He offers to sell you a new ship.")
        self.game.stdscr.move(2, 0)
        self.game.stdscr.addstr("Do you wish to buy? (Y/N)")
        self.game.stdscr.refresh()
        if self.keyboard.choice_yes_no():
            self.game.stdscr.move(3, 0)
            self.game.stdscr.addstr("How much do you wish to spend?")
            self.game.stdscr.refresh()
            amount = self.keyboard.get_num(9)
            if amount > 0:
                self.game.cash -= amount
                self.game.capacity += amount // 10
                self.game.stdscr.move(4, 0)
                self.game.stdscr.addstr(f"Your new capacity is {self.game.capacity}.")
                self.game.stdscr.refresh()
                self.game.stdscr.timeout(M_PAUSE)
                self.game.stdscr.getch()
                self.game.stdscr.timeout(-1)
        self.game.stdscr.clear()
        self.game.stdscr.refresh()
         