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
        self.game.screen.stdscr.refresh()


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

    def draw_enemy_firing(self, ships_on_screen: list) -> None:
        """Draw enemy firing animation and redraw ships"""
        # Show blast animation
        for i in range(3):
            for y in range(24):
                for x in range(79):
                    self.game.screen.stdscr.move(y, x)
                    self.game.screen.stdscr.addstr("*")
            self.game.screen.stdscr.refresh()
            time.sleep(0.2)
            self.game.screen.stdscr.clear()
            self.game.screen.stdscr.refresh()
            time.sleep(0.2)

        # Redraw ships
        x = 10
        y = 6
        for i in range(10):
            if i == 5:
                x = 10
                y = 12

            if ships_on_screen[i] > 0:
                self.draw_lorcha(x, y)

            x += 10

    def message_battle_status(self, status: int) -> None:
        """Display current battle status"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr(f"Current seaworthiness: {status_texts[int(status // 20)]} ({status}%)")
        self.game.screen.stdscr.refresh()

    def message_battle_orders(self) -> int:
        """Display battle orders prompt"""
        self.game.screen.stdscr.timeout(M_PAUSE)
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

    def message_battle_throw_cargo_interface(self, hold_: list[int]) -> None:
        """Display throw cargo interface"""
        self.game.screen.stdscr.move(18, 0)
        self.game.screen.stdscr.clrtobot()
        self.game.screen.stdscr.addstr("You have the following on board, Taipan:")
        self.game.screen.stdscr.move(19, 4)
        self.game.screen.stdscr.addstr(f"Opium: {hold_[0]}")
        self.game.screen.stdscr.move(19, 24)
        self.game.screen.stdscr.addstr(f"Silk: {hold_[1]}")
        self.game.screen.stdscr.move(20, 5)
        self.game.screen.stdscr.addstr(f"Arms: {hold_[2]}")
        self.game.screen.stdscr.move(20, 21)
        self.game.screen.stdscr.addstr(f"General: {hold_[3]}")

        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("What shall I throw overboard, Taipan? ")
        self.game.screen.stdscr.refresh()

    def message_battle_throw_cargo_amount(self) -> None:
        """Display throw cargo amount prompt"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("How much, Taipan? ")
        self.game.screen.stdscr.refresh()

    def message_battle_throw_cargo_success(self) -> None:
        """Display throw cargo success message"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("Let's hope we lose 'em, Taipan!")
        self.game.screen.stdscr.move(18, 0)
        self.game.screen.stdscr.clrtobot()
        self.game.screen.stdscr.refresh()

    def message_battle_throw_cargo_empty(self) -> None:
        """Display throw cargo empty message"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("There's nothing there, Taipan!")
        self.game.screen.stdscr.move(18, 0)
        self.game.screen.stdscr.clrtobot()
        self.game.screen.stdscr.refresh()

    def message_battle_ships_escaped(self, lost: int) -> None:
        """Display message about ships that escaped"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr(f"But we escaped from {lost} of 'em!")
        self.game.screen.stdscr.refresh()

    def message_battle_gun_hit(self) -> None:
        """Display message when a gun is hit"""
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("The buggers hit a gun, Taipan!!")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(M_PAUSE)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)
        
    def message_player_hits(self, sk: int) -> None:
        if sk > 0:
            self.game.screen.stdscr.addstr(f"Sunk {sk} of the buggers, Taipan!")
        else:
            self.game.screen.stdscr.addstr("Hit 'em, but didn't sink 'em, Taipan!")
        

    def fight_stats(self, ships: int, orders: int, guns: int) -> None:
        """Display battle statistics during sea battle"""
        # Determine order text based on current orders
        if orders == 0:
            ch_orders = ""
        elif orders == 1:
            ch_orders = "Fight      "
        elif orders == 2:
            ch_orders = "Run        "
        else:
            ch_orders = "Throw Cargo"

        # Display number of attacking ships
        self.game.screen.stdscr.move(0, 0)
        if ships >= 1000:
            self.game.screen.stdscr.addstr(str(ships))
        elif ships >= 100:
            self.game.screen.stdscr.addstr(f" {ships}")
        elif ships >= 10:
            self.game.screen.stdscr.addstr(f"  {ships}")
        else:
            self.game.screen.stdscr.addstr(f"   {ships}")

        # Display ship/ships text
        self.game.screen.stdscr.move(0, 5)
        if ships == 1:
            self.game.screen.stdscr.addstr("ship attacking, Taipan! \n")
        else:
            self.game.screen.stdscr.addstr("ships attacking, Taipan!\n")

        # Display current orders
        self.game.screen.stdscr.addstr(f"Your orders are to: {ch_orders}")

        # Display guns information
        self.game.screen.stdscr.move(0, 50)
        self.game.screen.stdscr.addstr("|  We have")
        self.game.screen.stdscr.move(1, 50)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr(f"|  {guns} {'gun' if guns == 1 else 'guns'}")
        self.game.screen.stdscr.move(2, 50)
        self.game.screen.stdscr.addstr("+---------")
        self.game.screen.stdscr.move(16, 0)
        
    def message_well_run(self) -> None:
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("Aye, we'll run, Taipan.")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(3000)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)

    def message_got_away(self) -> None:
        curses.flushinp()
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("We got away from 'em, Taipan!")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(3000)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)
        
    def message_couldnt_lose(self) -> None:
        self.game.screen.stdscr.move(3, 0)
        self.game.screen.stdscr.clrtoeol()
        self.game.screen.stdscr.addstr("Couldn't lose 'em.")
        self.game.screen.stdscr.refresh()
        self.game.screen.stdscr.timeout(3000)
        self.game.screen.stdscr.getch()
        self.game.screen.stdscr.timeout(-1)
