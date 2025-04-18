import curses
import random
import time
from constants import *
from sb_screen import BattleScreen

class SeaBattle:
    def __init__(self, game):
        self.game = game
        self.ships_on_screen = [0] * 10
        self.num_on_screen = 0
        self.orders = 0
        self.ok = 0
        self.ik = 1
        self.battle_screen = BattleScreen(game)

    def battle(self, battle_type: int, num_ships: int) -> int:
        """Handle sea battle with pirates"""
        # Initialize battle variables
        self.orders = 0
        self.num_on_screen = 0
        self.ships_on_screen = [0] * 10
        game_time = ((self.game.year - 1860) * 12) + self.game.month
        s0 = num_ships  # Original number of ships
        self.ok = 0  # Escape chance
        self.ik = 1  # Escape increment
        x = 0
        y = 0
        i = 0
        input_char = 0
        status = 0

        # Clear screen and prepare for battle
        self.game.screen.stdscr.clear()
        curses.flushinp()
        self.battle_screen.fight_stats(num_ships, self.orders, self.game.guns)

        # Main battle loop
        while num_ships > 0:
            # Check ship status
            status = 100 - ((self.game.damage / self.game.capacity) * 100)
            if status <= 0:
                return BATTLE_LOST  # Ship lost!

            # Display current seaworthiness
            self.battle_screen.message_battle_status(status)

            # Draw ships
            x = 10
            y = 6
            for i in range(10):
                if i == 5:
                    x = 10
                    y = 12

                if num_ships > self.num_on_screen:
                    if self.ships_on_screen[i] == 0:
                        time.sleep(0.1)  # Small delay for animation
                        self.ships_on_screen[i] = int(self.game.ec * random.random() + 20)
                        self.battle_screen.draw_lorcha(x, y)
                        self.num_on_screen += 1
                        self.game.screen.stdscr.refresh()

                    x += 10

            # Show more ships indicator
            self.game.screen.stdscr.move(11, 62)
            if num_ships > self.num_on_screen:
                self.game.screen.stdscr.addstr("+")
            else:
                self.game.screen.stdscr.addstr(" ")

            # Get player orders
            input_char = self.battle_screen.message_battle_orders()

            # Process orders
            if input_char in [ord('F'), ord('f')]:
                self.orders = 1
            elif input_char in [ord('R'), ord('r')]:
                self.orders = 2
            elif input_char in [ord('T'), ord('t')]:
                self.orders = 3

            if self.orders == 0:
                self.game.screen.stdscr.timeout(M_PAUSE)
                input_char = self.battle_screen.message_battle_orders()
                self.game.screen.stdscr.timeout(-1)

                if input_char in [ord('F'), ord('f')]:
                    self.orders = 1
                elif input_char in [ord('R'), ord('r')]:
                    self.orders = 2
                elif input_char in [ord('T'), ord('t')]:
                    self.orders = 3
                else:
                    self.battle_screen.message_battle_no_guns()
                    self.game.screen.stdscr.timeout(-1)
                    while input_char not in [ord('F'), ord('f'), ord('R'), ord('r'), ord('T'), ord('t')]:
                        input_char = self.game.screen.stdscr.getch()
                    if input_char in [ord('F'), ord('f')]:
                        self.orders = 1
                    elif input_char in [ord('R'), ord('r')]:
                        self.orders = 2
                    else:
                        self.orders = 3

            # Update battle stats
            self.battle_screen.fight_stats(num_ships, self.orders, self.game.guns)
            # Handle fighting
            if self.orders == 1 and self.game.guns > 0:
                self.ok = 3
                self.ik = 1
                self.battle_screen.message_battle_fight()

                sk = 0  # Ships sunk counter
                for i in range(1, self.game.guns + 1):
                    # Check if all ships are sunk
                    if all(ship == 0 for ship in self.ships_on_screen):
                        x = 10
                        y = 6
                        for j in range(10):
                            if j == 5:
                                x = 10
                                y = 12

                            if num_ships > self.num_on_screen:
                                if self.ships_on_screen[j] == 0:
                                    time.sleep(0.1)
                                    self.ships_on_screen[j] = int(self.game.ec * random.random() + 20)
                                    self.battle_screen.draw_lorcha(x, y)
                                    self.num_on_screen += 1

                            x += 10

                    # Update more ships indicator
                    self.game.screen.stdscr.move(11, 62)
                    if num_ships > self.num_on_screen:
                        self.game.screen.stdscr.addstr("+")
                    else:
                        self.game.screen.stdscr.addstr(" ")

                    self.game.screen.stdscr.move(16, 0)
                    self.game.screen.stdscr.addstr("\n")
                    self.game.screen.stdscr.refresh()

                    # Select target
                    targeted = random.randint(0, 9)
                    while self.ships_on_screen[targeted] == 0:
                        targeted = random.randint(0, 9)

                    # Calculate target position
                    x = ((targeted + 1) * 10) if targeted < 5 else ((targeted - 4) * 10)
                    y = 6 if targeted < 5 else 12

                    # Show blast animation
                    self.battle_screen.draw_blast(x, y)
                    self.game.screen.stdscr.refresh()
                    time.sleep(0.1)

                    self.battle_screen.draw_lorcha(x, y)
                    self.game.screen.stdscr.refresh()
                    time.sleep(0.1)

                    self.battle_screen.draw_blast(x, y)
                    self.game.screen.stdscr.refresh()
                    time.sleep(0.1)

                    self.battle_screen.draw_lorcha(x, y)
                    self.game.screen.stdscr.refresh()
                    time.sleep(0.05)

                    # Show remaining shots
                    self.battle_screen.message_battle_shots_remaining(self.game.guns - i)

                    # Apply damage with more sophisticated calculation
                    self.ships_on_screen[targeted] -= random.randint(10, 40)

                    # Check if ship sunk
                    if self.ships_on_screen[targeted] <= 0:
                        self.num_on_screen -= 1
                        num_ships -= 1
                        sk += 1
                        self.ships_on_screen[targeted] = 0

                        delay = random.randint(0, 19)
                        time.sleep(0.1)
                        self.battle_screen.sink_lorcha(x, y)
                        if delay == 0:
                            time.sleep(ANIMATION_PAUSE)

                        if num_ships == self.num_on_screen:
                            self.game.screen.stdscr.move(11, 62)
                            self.game.screen.stdscr.addstr(" ")

                        self.battle_screen.fight_stats(num_ships, self.orders, self.game.guns)
                        self.game.screen.stdscr.refresh()

                    if num_ships == 0:
                        break
                    else:
                        time.sleep(ANIMATION_PAUSE)

                # Show battle results
                self.battle_screen.message_battle_escape(sk > 0)

                # Check if some ships ran away
                if random.randint(0, s0 - 1) > int(num_ships * 0.6 / battle_type) and num_ships > 2:
                    divisor = num_ships // 3 // battle_type
                    if divisor == 0:
                        divisor = 1
                    ran = random.randint(0, divisor - 1)
                    if ran == 0:
                        ran = 1

                    num_ships -= ran
                    self.battle_screen.fight_stats(num_ships, self.orders, self.game.guns)
                    self.battle_screen.message_battle_ships_escaped(ran)

                    # Check for Li Yuen's intervention when ships run away
                    if battle_type == GENERIC and random.randint(0, 19) == 0:
                        return BATTLE_INTERRUPTED

                    if num_ships <= 10:
                        for i in range(9, -1, -1):
                            if self.num_on_screen > num_ships and self.ships_on_screen[i] > 0:
                                self.ships_on_screen[i] = 0
                                self.num_on_screen -= 1

                                x = ((i + 1) * 10) if i < 5 else ((i - 4) * 10)
                                y = 6 if i < 5 else 12
                                self.battle_screen.clear_lorcha(x, y)
                                self.game.screen.stdscr.refresh()
                                time.sleep(0.1)

                        if num_ships == self.num_on_screen:
                            self.game.screen.stdscr.move(11, 62)
                            self.game.screen.stdscr.addstr(" ")
                            self.game.screen.stdscr.refresh()

                    self.game.screen.stdscr.move(16, 0)
                    self.game.screen.stdscr.refresh()
                    self.game.screen.stdscr.timeout(M_PAUSE)
                    input_char = self.game.screen.stdscr.getch()
                    self.game.screen.stdscr.timeout(-1)

                    if input_char in [ord('F'), ord('f')]:
                        self.orders = 1
                    elif input_char in [ord('R'), ord('r')]:
                        self.orders = 2
                    elif input_char in [ord('T'), ord('t')]:
                        self.orders = 3
            elif self.orders == 1 and self.game.guns == 0:
                self.battle_screen.message_battle_no_guns()
                self.game.screen.stdscr.timeout(-1)
            # Handle throwing cargo
            elif self.orders == 3:
                choice = 0
                amount = 0
                total = 0

                self.battle_screen.message_battle_throw_cargo()

                while choice not in [ord('O'), ord('o'), ord('S'), ord('s'), 
                                   ord('A'), ord('a'), ord('G'), ord('g'), ord('*')]:
                    choice = self.game.screen.keyboard.get_one()

                if choice in [ord('O'), ord('o')]:
                    choice = 0
                elif choice in [ord('S'), ord('s')]:
                    choice = 1
                elif choice in [ord('A'), ord('a')]:
                    choice = 2
                elif choice in [ord('G'), ord('g')]:
                    choice = 3
                else:
                    choice = 4

                if choice < 4:
                    self.game.screen.stdscr.move(3, 0)
                    self.game.screen.stdscr.clrtoeol()
                    self.game.screen.stdscr.addstr("How much, Taipan? ")
                    self.game.screen.stdscr.refresh()

                    amount = self.game.screen.keyboard.get_num(9)
                    if self.game.hold_[choice] > 0 and (amount == -1 or amount > self.game.hold_[choice]):
                        amount = self.game.hold_[choice]
                    total = self.game.hold_[choice]
                else:
                    total = sum(self.game.hold_)

                if total > 0:
                    self.game.screen.stdscr.move(3, 0)
                    self.game.screen.stdscr.clrtoeol()
                    self.game.screen.stdscr.addstr("Let's hope we lose 'em, Taipan!")
                    if choice < 4:
                        self.game.hold_[choice] -= amount
                        self.game.hold += amount
                        self.ok += (amount // 10)
                    else:
                        self.game.hold_[0] = 0
                        self.game.hold_[1] = 0
                        self.game.hold_[2] = 0
                        self.game.hold_[3] = 0
                        self.game.hold += total
                        self.ok += (total // 10)
                    self.game.screen.stdscr.move(18, 0)
                    self.game.screen.stdscr.clrtobot()
                    self.game.screen.stdscr.refresh()

                    self.game.screen.stdscr.timeout(M_PAUSE)
                    self.game.screen.stdscr.getch()
                    self.game.screen.stdscr.timeout(-1)
                else:
                    self.game.screen.stdscr.move(3, 0)
                    self.game.screen.stdscr.clrtoeol()
                    self.game.screen.stdscr.addstr("There's nothing there, Taipan!")
                    self.game.screen.stdscr.move(18, 0)
                    self.game.screen.stdscr.clrtobot()
                    self.game.screen.stdscr.refresh()

                    self.game.screen.stdscr.timeout(M_PAUSE)
                    self.game.screen.stdscr.getch()
                    self.game.screen.stdscr.timeout(-1)

            # Handle running or throwing cargo
            if self.orders == 2 or self.orders == 3:
                if self.orders == 2:
                    self.battle_screen.message_battle_run()

                self.ok += self.ik
                self.ik += 1
                assert self.ok > 0  # Prevent division by zero
                assert self.ik > 0  # Prevent division by zero

                if random.randint(0, self.ok - 1) > random.randint(0, num_ships - 1):
                    curses.flushinp()
                    self.battle_screen.message_battle_escape(True)
                    self.game.screen.stdscr.timeout(M_PAUSE)
                    self.game.screen.stdscr.getch()
                    self.game.screen.stdscr.timeout(-1)
                    num_ships = 0
                else:
                    self.battle_screen.message_battle_escape(False)
                    self.game.screen.stdscr.timeout(M_PAUSE)
                    self.game.screen.stdscr.getch()
                    self.game.screen.stdscr.timeout(-1)

                    if num_ships > 2 and random.randint(0, 4) == 0:
                        lost = (random.randint(0, num_ships - 1) // 2) + 1

                        num_ships -= lost
                        self.battle_screen.fight_stats(num_ships, self.orders, self.game.guns)
                        self.battle_screen.message_battle_ships_escaped(lost)

                        if num_ships <= 10:
                            for i in range(9, -1, -1):
                                if self.num_on_screen > num_ships and self.ships_on_screen[i] > 0:
                                    self.ships_on_screen[i] = 0
                                    self.num_on_screen -= 1

                                    x = ((i + 1) * 10) if i < 5 else ((i - 4) * 10)
                                    y = 6 if i < 5 else 12
                                    self.battle_screen.clear_lorcha(x, y)
                                    self.game.screen.stdscr.refresh()
                                    time.sleep(0.1)

                            if num_ships == self.num_on_screen:
                                self.game.screen.stdscr.move(11, 62)
                                self.game.screen.stdscr.addstr(" ")
                                self.game.screen.stdscr.refresh()

                        self.game.screen.stdscr.move(16, 0)
                        self.game.screen.stdscr.refresh()
                        self.game.screen.stdscr.timeout(M_PAUSE)
                        input_char = self.game.screen.stdscr.getch()
                        self.game.screen.stdscr.timeout(-1)

                        if input_char in [ord('F'), ord('f')]:
                            self.orders = 1
                        elif input_char in [ord('R'), ord('r')]:
                            self.orders = 2
                        elif input_char in [ord('T'), ord('t')]:
                            self.orders = 3

            # Handle enemy firing
            if num_ships > 0:
                self.battle_screen.message_battle_enemy_firing()
                curses.flushinp()

                self.battle_screen.draw_enemy_firing(self.ships_on_screen)

                # Update more ships indicator
                self.game.screen.stdscr.move(11, 62)
                if num_ships > self.num_on_screen:
                    self.game.screen.stdscr.addstr("+")
                else:
                    self.game.screen.stdscr.addstr(" ")

                self.battle_screen.message_battle_hit()

                # Calculate damage
                i = min(num_ships, 15)
                if (self.game.guns > 0 and 
                    (random.randint(0, 99) < int((self.game.damage / self.game.capacity) * 100) or
                     int((self.game.damage / self.game.capacity) * 100) > 80)):
                    i = 1
                    if not DEBUG:  # Only prevent gun loss in debug mode
                        self.game.guns -= 1
                        self.game.hold += 10
                    self.battle_screen.fight_stats(num_ships, self.orders, self.game.guns)
                    self.battle_screen.message_battle_gun_hit(num_ships)

                # Apply damage regardless of debug mode
                self.game.damage += int((self.game.ed * i * battle_type) * random.random() + (i / 2))

                # Check for Li Yuen's intervention
                if battle_type == GENERIC and random.randint(0, 19) == 0:
                    return BATTLE_INTERRUPTED  # Battle interrupted by Li Yuen's pirates

        if num_ships == 0:
            if self.orders == 1:
                self.battle_screen.message_battle_victory()
                self.battle_screen.fight_stats(0, self.orders, self.game.guns)
                return BATTLE_WON  # Victory!
            else:
                return BATTLE_FLED  # Ran and got away. 