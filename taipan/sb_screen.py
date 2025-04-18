import curses
import random
import time
from constants import *

class BattleScreen:
    def __init__(self, game):
        self.game = game

    def draw_lorcha(self, x: int, y: int) -> None:
        """Draw a lorcha (ship) at given coordinates"""
        self.game.screen.stdscr.move(y, x)
        self.game.screen.stdscr.addstr("-|-_|_  ")
        self.game.screen.stdscr.move(y + 1, x)
        self.game.screen.stdscr.addstr("-|-_|_  ")
        self.game.screen.stdscr.move(y + 2, x)
        self.game.screen.stdscr.addstr("_|__|__/")
        self.game.screen.stdscr.move(y + 3, x)
        self.game.screen.stdscr.addstr("\\_____/ ")

    def clear_lorcha(self, x: int, y: int) -> None:
        """Clear a lorcha from given coordinates"""
        self.game.screen.stdscr.move(y, x)
        self.game.screen.stdscr.addstr("        ")
        self.game.screen.stdscr.move(y + 1, x)
        self.game.screen.stdscr.addstr("        ")
        self.game.screen.stdscr.move(y + 2, x)
        self.game.screen.stdscr.addstr("        ")
        self.game.screen.stdscr.move(y + 3, x)
        self.game.screen.stdscr.addstr("        ")

    def draw_blast(self, x: int, y: int) -> None:
        """Draw a blast effect at given coordinates"""
        self.game.screen.stdscr.move(y, x)
        self.game.screen.stdscr.addstr("********")
        self.game.screen.stdscr.move(y + 1, x)
        self.game.screen.stdscr.addstr("********")
        self.game.screen.stdscr.move(y + 2, x)
        self.game.screen.stdscr.addstr("********")
        self.game.screen.stdscr.move(y + 3, x)
        self.game.screen.stdscr.addstr("********")

    def sink_lorcha(self, x: int, y: int) -> None:
        """Animate a lorcha sinking at given coordinates"""
        delay = random.randint(0, 19)

        self.game.screen.stdscr.move(y, x)
        self.game.screen.stdscr.addstr("        ")
        self.game.screen.stdscr.move(y + 1, x)
        self.game.screen.stdscr.addstr("-|-_|_  ")
        self.game.screen.stdscr.move(y + 2, x)
        self.game.screen.stdscr.addstr("-|-_|_  ")
        self.game.screen.stdscr.move(y + 3, x)
        self.game.screen.stdscr.addstr("_|__|__/")
        self.game.screen.stdscr.refresh()
        time.sleep(ANIMATION_PAUSE)
        if delay == 0:
            time.sleep(ANIMATION_PAUSE)

        self.game.screen.stdscr.move(y + 1, x)
        self.game.screen.stdscr.addstr("        ")
        self.game.screen.stdscr.move(y + 2, x)
        self.game.screen.stdscr.addstr("-|-_|_  ")
        self.game.screen.stdscr.move(y + 3, x)
        self.game.screen.stdscr.addstr("-|-_|_  ")
        self.game.screen.stdscr.refresh()
        time.sleep(ANIMATION_PAUSE)
        if delay == 0:
            time.sleep(ANIMATION_PAUSE)

        self.game.screen.stdscr.move(y + 2, x)
        self.game.screen.stdscr.addstr("        ")
        self.game.screen.stdscr.move(y + 3, x)
        self.game.screen.stdscr.addstr("-|-_|_  ")
        self.game.screen.stdscr.refresh()
        time.sleep(ANIMATION_PAUSE)
        if delay == 0:
            time.sleep(ANIMATION_PAUSE)

        self.game.screen.stdscr.move(y + 3, x)
        self.game.screen.stdscr.addstr("        ")
        self.game.screen.stdscr.refresh()
        time.sleep(ANIMATION_PAUSE)
        if delay == 0:
            time.sleep(ANIMATION_PAUSE)

    def message_battle_status(self, status: int) -> None:
        """Display current battle status"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr(f"Current seaworthiness: {status_texts[int(status // 20)]} ({status}%)")
        self.game.screen.stdscr.refresh()

    def message_battle_orders(self) -> int:
        """Display battle orders prompt"""
        self.game.screen.stdscr.move(16, 0)
        self.game.screen.stdscr.addstr("\n")
        self.game.screen.stdscr.refresh()
        # This pause is used to allow the player to read the message
        self.game.screen.stdscr.timeout(3000)
        input_char = self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)
        return input_char

    def message_battle_fight(self) -> None:
        """Display fighting messages"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("Aye, we'll fight 'em, Taipan.")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(M_PAUSE)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)

        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("We're firing on 'em, Taipan!")
        self.game.screen.stdscr.timeout(1000)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)
        self.game.screen.stdscr.refresh()

    def message_battle_shots_remaining(self, shots: int) -> None:
        """Display remaining shots"""
        self.game.screen.stdscr.move(3, 30)
        self.game.screen.stdscr.clrtoeol()
        if shots == 1:
            self.game.screen.stdscr.addstr("(1 shot remaining.)")
        else:
            self.game.screen.stdscr.addstr(f"({shots} shots remaining.)")
        self.game.screen.stdscr.refresh()
        time.sleep(0.1)

    def message_battle_enemy_firing(self) -> None:
        """Display enemy firing message"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("They're firing on us, Taipan!")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(M_PAUSE)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)

    def message_battle_hit(self) -> None:
        """Display hit message"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("We've been hit, Taipan!!")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(M_PAUSE)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)

    def message_battle_victory(self) -> None:
        """Display victory message"""
        self.game.screen.stdscr.clear()
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("We got 'em all, Taipan!")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(M_PAUSE)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)

    def message_battle_no_guns(self) -> int:
        """Display no guns message"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("We have no guns, Taipan!!")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(3000)
        input_char = self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)
        return input_char

    def message_battle_throw_cargo(self) -> None:
        """Display throw cargo interface"""
        self.game.screen.stdscr.move(18, 0)
        self.game.screen.stdscr.clrtobot()
        self.game.screen.stdscr.addstr("You have the following on board, Taipan:")
        self.game.screen.stdscr.move(19, 4)
        self.game.screen.stdscr.addstr(f"Opium: {self.game.hold_[0]}")
        self.game.screen.stdscr.move(19, 24)
        self.game.screen.stdscr.addstr(f"Silk: {self.game.hold_[1]}")
        self.game.screen.stdscr.move(20, 5)
        self.game.screen.stdscr.addstr(f"Arms: {self.game.hold_[2]}")
        self.game.screen.stdscr.move(20, 21)
        self.game.screen.stdscr.addstr(f"General: {self.game.hold_[3]}")

        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("What shall I throw overboard, Taipan? ")
        self.game.screen.stdscr.refresh()

    def message_battle_run(self) -> None:
        """Display run message"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("Aye, we'll run, Taipan.")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(M_PAUSE)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)

    def message_battle_escape(self, success: bool) -> None:
        """Display escape result message"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        if success:
            self.game.screen.stdscr.addstr("We got away from 'em, Taipan!")
        else:
            self.game.screen.stdscr.addstr("Couldn't lose 'em.")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(M_PAUSE)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)

    def message_battle_ships_escaped(self, lost: int) -> None:
        """Display message about ships that escaped"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr(f"But we escaped from {lost} of 'em!")
        self.game.screen.stdscr.refresh()

    def message_battle_gun_hit(self, num_ships: int) -> None:
        """Display message when a gun is hit"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("The buggers hit a gun, Taipan!!")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(M_PAUSE)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)
