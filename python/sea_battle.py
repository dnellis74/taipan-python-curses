
import curses
import random
import time
from constants import *
from keyboard import Keyboard

class SeaBattle:
    def __init__(self, game):
        self.game = game
        self.ships_on_screen = [0] * 10
        self.num_on_screen = 0
        self.orders = 0
        self.ok = 0
        self.ik = 1
        self.keyboard = Keyboard(game.stdscr)

    def draw_lorcha(self, x: int, y: int) -> None:
        """Draw a lorcha (ship) at given coordinates"""
        self.game.stdscr.move(y, x)
        self.game.stdscr.addstr("-|-_|_  ")
        self.game.stdscr.move(y + 1, x)
        self.game.stdscr.addstr("-|-_|_  ")
        self.game.stdscr.move(y + 2, x)
        self.game.stdscr.addstr("_|__|__/")
        self.game.stdscr.move(y + 3, x)
        self.game.stdscr.addstr("\\_____/ ")

    def clear_lorcha(self, x: int, y: int) -> None:
        """Clear a lorcha from given coordinates"""
        self.game.stdscr.move(y, x)
        self.game.stdscr.addstr("        ")
        self.game.stdscr.move(y + 1, x)
        self.game.stdscr.addstr("        ")
        self.game.stdscr.move(y + 2, x)
        self.game.stdscr.addstr("        ")
        self.game.stdscr.move(y + 3, x)
        self.game.stdscr.addstr("        ")

    def draw_blast(self, x: int, y: int) -> None:
        """Draw a blast effect at given coordinates"""
        self.game.stdscr.move(y, x)
        self.game.stdscr.addstr("********")
        self.game.stdscr.move(y + 1, x)
        self.game.stdscr.addstr("********")
        self.game.stdscr.move(y + 2, x)
        self.game.stdscr.addstr("********")
        self.game.stdscr.move(y + 3, x)
        self.game.stdscr.addstr("********")

    def sink_lorcha(self, x: int, y: int) -> None:
        """Animate a lorcha sinking at given coordinates"""
        delay = random.randint(0, 19)

        self.game.stdscr.move(y, x)
        self.game.stdscr.addstr("        ")
        self.game.stdscr.move(y + 1, x)
        self.game.stdscr.addstr("-|-_|_  ")
        self.game.stdscr.move(y + 2, x)
        self.game.stdscr.addstr("-|-_|_  ")
        self.game.stdscr.move(y + 3, x)
        self.game.stdscr.addstr("_|__|__/")
        self.game.stdscr.refresh()
        time.sleep(ANIMATION_PAUSE)
        if delay == 0:
            time.sleep(ANIMATION_PAUSE)

        self.game.stdscr.move(y + 1, x)
        self.game.stdscr.addstr("        ")
        self.game.stdscr.move(y + 2, x)
        self.game.stdscr.addstr("-|-_|_  ")
        self.game.stdscr.move(y + 3, x)
        self.game.stdscr.addstr("-|-_|_  ")
        self.game.stdscr.refresh()
        time.sleep(ANIMATION_PAUSE)
        if delay == 0:
            time.sleep(ANIMATION_PAUSE)

        self.game.stdscr.move(y + 2, x)
        self.game.stdscr.addstr("        ")
        self.game.stdscr.move(y + 3, x)
        self.game.stdscr.addstr("-|-_|_  ")
        self.game.stdscr.refresh()
        time.sleep(ANIMATION_PAUSE)
        if delay == 0:
            time.sleep(ANIMATION_PAUSE)

        self.game.stdscr.move(y + 3, x)
        self.game.stdscr.addstr("        ")
        self.game.stdscr.refresh()
        time.sleep(ANIMATION_PAUSE)
        if delay == 0:
            time.sleep(ANIMATION_PAUSE)

    def fight_stats(self, ships: int, orders: int) -> None:
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
        self.game.stdscr.move(0, 0)
        if ships >= 1000:
            self.game.stdscr.addstr(str(ships))
        elif ships >= 100:
            self.game.stdscr.addstr(f" {ships}")
        elif ships >= 10:
            self.game.stdscr.addstr(f"  {ships}")
        else:
            self.game.stdscr.addstr(f"   {ships}")

        # Display ship/ships text
        self.game.stdscr.move(0, 5)
        if ships == 1:
            self.game.stdscr.addstr("ship attacking, Taipan! \n")
        else:
            self.game.stdscr.addstr("ships attacking, Taipan!\n")

        # Display current orders
        self.game.stdscr.addstr(f"Your orders are to: {ch_orders}")

        # Display guns information
        self.game.stdscr.move(0, 50)
        self.game.stdscr.addstr("|  We have")
        self.game.stdscr.move(1, 50)
        self.game.stdscr.clrtoeol()
        self.game.stdscr.addstr(f"|  {self.game.guns} {'gun' if self.game.guns == 1 else 'guns'}")
        self.game.stdscr.move(2, 50)
        self.game.stdscr.addstr("+---------")
        self.game.stdscr.move(16, 0)

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
        self.game.stdscr.clear()
        curses.flushinp()
        self.fight_stats(num_ships, self.orders)

        # Main battle loop
        while num_ships > 0:
            # Check ship status
            status = 100 - ((self.game.damage / self.game.capacity) * 100)
            if status <= 0:
                return BATTLE_LOST  # Ship lost!

            # Display current seaworthiness
            self.game.stdscr.move(3, 0)
            self.game.stdscr.clrtoeol()
            self.game.stdscr.addstr(f"Current seaworthiness: {status_texts[int(status // 20)]} ({status}%)")
            self.game.stdscr.refresh()

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
                        self.draw_lorcha(x, y)
                        self.num_on_screen += 1
                        self.game.stdscr.refresh()

                    x += 10

            # Show more ships indicator
            self.game.stdscr.move(11, 62)
            if num_ships > self.num_on_screen:
                self.game.stdscr.addstr("+")
            else:
                self.game.stdscr.addstr(" ")

            # Get player orders
            self.game.stdscr.move(16, 0)
            self.game.stdscr.addstr("\n")
            self.game.stdscr.refresh()
            # This pause is used to allow the player to read the message
            self.game.stdscr.timeout(3000)
            input_char = self.game.stdscr.getch()
            self.game.stdscr.timeout(-1)

            # Process orders
            if input_char in [ord('F'), ord('f')]:
                self.orders = 1
            elif input_char in [ord('R'), ord('r')]:
                self.orders = 2
            elif input_char in [ord('T'), ord('t')]:
                self.orders = 3

            if self.orders == 0:
                self.game.stdscr.timeout(M_PAUSE)
                input_char = self.game.stdscr.getch()
                self.game.stdscr.timeout(-1)

                if input_char in [ord('F'), ord('f')]:
                    self.orders = 1
                elif input_char in [ord('R'), ord('r')]:
                    self.orders = 2
                elif input_char in [ord('T'), ord('t')]:
                    self.orders = 3
                else:
                    self.game.stdscr.move(3, 0)
                    self.game.stdscr.clrtoeol()
                    self.game.stdscr.addstr("Taipan, what shall we do??    (f=Fight, r=Run, t=Throw cargo)")
                    self.game.stdscr.refresh()
                    self.game.stdscr.timeout(-1)
                    while input_char not in [ord('F'), ord('f'), ord('R'), ord('r'), ord('T'), ord('t')]:
                        input_char = self.game.stdscr.getch()
                    if input_char in [ord('F'), ord('f')]:
                        self.orders = 1
                    elif input_char in [ord('R'), ord('r')]:
                        self.orders = 2
                    else:
                        self.orders = 3

            # Update battle stats
            self.fight_stats(num_ships, self.orders)
            # Handle fighting
            if self.orders == 1 and self.game.guns > 0:
                self.ok = 3
                self.ik = 1
                self.game.stdscr.move(3, 0)
                self.game.stdscr.clrtoeol()
                self.game.stdscr.addstr("Aye, we'll fight 'em, Taipan.")
                self.game.stdscr.refresh()
                self.game.stdscr.timeout(M_PAUSE)
                self.game.stdscr.getch()
                self.game.stdscr.timeout(-1)

                self.game.stdscr.move(3, 0)
                self.game.stdscr.clrtoeol()
                self.game.stdscr.addstr("We're firing on 'em, Taipan!")
                self.game.stdscr.timeout(1000)
                self.game.stdscr.getch()
                self.game.stdscr.timeout(-1)
                self.game.stdscr.refresh()

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
                                    self.draw_lorcha(x, y)
                                    self.num_on_screen += 1

                            x += 10

                    # Update more ships indicator
                    self.game.stdscr.move(11, 62)
                    if num_ships > self.num_on_screen:
                        self.game.stdscr.addstr("+")
                    else:
                        self.game.stdscr.addstr(" ")

                    self.game.stdscr.move(16, 0)
                    self.game.stdscr.addstr("\n")
                    self.game.stdscr.refresh()

                    # Select target
                    targeted = random.randint(0, 9)
                    while self.ships_on_screen[targeted] == 0:
                        targeted = random.randint(0, 9)

                    # Calculate target position
                    x = ((targeted + 1) * 10) if targeted < 5 else ((targeted - 4) * 10)
                    y = 6 if targeted < 5 else 12

                    # Show blast animation
                    self.draw_blast(x, y)
                    self.game.stdscr.refresh()
                    time.sleep(0.1)

                    self.draw_lorcha(x, y)
                    self.game.stdscr.refresh()
                    time.sleep(0.1)

                    self.draw_blast(x, y)
                    self.game.stdscr.refresh()
                    time.sleep(0.1)

                    self.draw_lorcha(x, y)
                    self.game.stdscr.refresh()
                    time.sleep(0.05)

                    # Show remaining shots
                    self.game.stdscr.move(3, 30)
                    self.game.stdscr.clrtoeol()
                    if self.game.guns - i == 1:
                        self.game.stdscr.addstr("(1 shot remaining.)")
                    else:
                        self.game.stdscr.addstr(f"({self.game.guns - i} shots remaining.)")
                    self.game.stdscr.refresh()
                    time.sleep(0.1)

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
                        self.sink_lorcha(x, y)
                        if delay == 0:
                            time.sleep(ANIMATION_PAUSE)

                        if num_ships == self.num_on_screen:
                            self.game.stdscr.move(11, 62)
                            self.game.stdscr.addstr(" ")

                        self.fight_stats(num_ships, self.orders)
                        self.game.stdscr.refresh()

                    if num_ships == 0:
                        break
                    else:
                        time.sleep(ANIMATION_PAUSE)

                # Show battle results
                self.game.stdscr.move(3, 0)
                self.game.stdscr.clrtoeol()
                if sk > 0:
                    self.game.stdscr.addstr(f"Sunk {sk} of the buggers, Taipan!")
                else:
                    self.game.stdscr.addstr("Hit 'em, but didn't sink 'em, Taipan!")
                self.game.stdscr.refresh()
                self.game.stdscr.timeout(M_PAUSE)
                self.game.stdscr.getch()
                self.game.stdscr.timeout(-1)

                # Check if some ships ran away
                if random.randint(0, s0 - 1) > int(num_ships * 0.6 / battle_type) and num_ships > 2:
                    divisor = num_ships // 3 // battle_type
                    if divisor == 0:
                        divisor = 1
                    ran = random.randint(0, divisor - 1)
                    if ran == 0:
                        ran = 1

                    num_ships -= ran
                    self.fight_stats(num_ships, self.orders)
                    self.game.stdscr.move(3, 0)
                    self.game.stdscr.clrtoeol()
                    self.game.stdscr.addstr(f"{ran} ran away, Taipan!")

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
                                self.clear_lorcha(x, y)
                                self.game.stdscr.refresh()
                                time.sleep(0.1)

                        if num_ships == self.num_on_screen:
                            self.game.stdscr.move(11, 62)
                            self.game.stdscr.addstr(" ")
                            self.game.stdscr.refresh()

                    self.game.stdscr.move(16, 0)
                    self.game.stdscr.refresh()
                    self.game.stdscr.timeout(M_PAUSE)
                    input_char = self.game.stdscr.getch()
                    self.game.stdscr.timeout(-1)

                    if input_char in [ord('F'), ord('f')]:
                        self.orders = 1
                    elif input_char in [ord('R'), ord('r')]:
                        self.orders = 2
                    elif input_char in [ord('T'), ord('t')]:
                        self.orders = 3
            elif self.orders == 1 and self.game.guns == 0:
                self.game.stdscr.move(3, 0)
                self.game.stdscr.clrtoeol()
                self.game.stdscr.addstr("We have no guns, Taipan!!")
                self.game.stdscr.refresh()
                self.game.stdscr.timeout(3000)
                input_char = self.game.stdscr.getch()
                self.game.stdscr.timeout(-1)
            # Handle throwing cargo
            elif self.orders == 3:
                choice = 0
                amount = 0
                total = 0

                self.game.stdscr.move(18, 0)
                self.game.stdscr.clrtobot()
                self.game.stdscr.addstr("You have the following on board, Taipan:")
                self.game.stdscr.move(19, 4)
                self.game.stdscr.addstr(f"Opium: {self.game.hold_[0]}")
                self.game.stdscr.move(19, 24)
                self.game.stdscr.addstr(f"Silk: {self.game.hold_[1]}")
                self.game.stdscr.move(20, 5)
                self.game.stdscr.addstr(f"Arms: {self.game.hold_[2]}")
                self.game.stdscr.move(20, 21)
                self.game.stdscr.addstr(f"General: {self.game.hold_[3]}")

                self.game.stdscr.move(3, 0)
                self.game.stdscr.clrtoeol()
                self.game.stdscr.addstr("What shall I throw overboard, Taipan? ")
                self.game.stdscr.refresh()

                while choice not in [ord('O'), ord('o'), ord('S'), ord('s'), 
                                   ord('A'), ord('a'), ord('G'), ord('g'), ord('*')]:
                    choice = self.keyboard.get_one()

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
                    self.game.stdscr.move(3, 0)
                    self.game.stdscr.clrtoeol()
                    self.game.stdscr.addstr("How much, Taipan? ")
                    self.game.stdscr.refresh()

                    amount = self.game.get_num(9)
                    if self.game.hold_[choice] > 0 and (amount == -1 or amount > self.game.hold_[choice]):
                        amount = self.game.hold_[choice]
                    total = self.game.hold_[choice]
                else:
                    total = sum(self.game.hold_)

                if total > 0:
                    self.game.stdscr.move(3, 0)
                    self.game.stdscr.clrtoeol()
                    self.game.stdscr.addstr("Let's hope we lose 'em, Taipan!")
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
                    self.game.stdscr.move(18, 0)
                    self.game.stdscr.clrtobot()
                    self.game.stdscr.refresh()

                    self.game.stdscr.timeout(M_PAUSE)
                    self.game.stdscr.getch()
                    self.game.stdscr.timeout(-1)
                else:
                    self.game.stdscr.move(3, 0)
                    self.game.stdscr.clrtoeol()
                    self.game.stdscr.addstr("There's nothing there, Taipan!")
                    self.game.stdscr.move(18, 0)
                    self.game.stdscr.clrtobot()
                    self.game.stdscr.refresh()

                    self.game.stdscr.timeout(M_PAUSE)
                    self.game.stdscr.getch()
                    self.game.stdscr.timeout(-1)

            # Handle running or throwing cargo
            if self.orders == 2 or self.orders == 3:
                if self.orders == 2:
                    self.game.stdscr.move(3, 0)
                    self.game.stdscr.clrtoeol()
                    self.game.stdscr.addstr("Aye, we'll run, Taipan.")
                    self.game.stdscr.refresh()
                    self.game.stdscr.timeout(M_PAUSE)
                    self.game.stdscr.getch()
                    self.game.stdscr.timeout(-1)

                self.ok += self.ik
                self.ik += 1
                assert self.ok > 0  # Prevent division by zero
                assert self.ik > 0  # Prevent division by zero

                if random.randint(0, self.ok - 1) > random.randint(0, num_ships - 1):
                    curses.flushinp()
                    self.game.stdscr.move(3, 0)
                    self.game.stdscr.clrtoeol()
                    self.game.stdscr.addstr("We got away from 'em, Taipan!")
                    self.game.stdscr.refresh()
                    self.game.stdscr.timeout(M_PAUSE)
                    self.game.stdscr.getch()
                    self.game.stdscr.timeout(-1)
                    num_ships = 0
                else:
                    self.game.stdscr.move(3, 0)
                    self.game.stdscr.clrtoeol()
                    self.game.stdscr.addstr("Couldn't lose 'em.")
                    self.game.stdscr.refresh()
                    self.game.stdscr.timeout(M_PAUSE)
                    self.game.stdscr.getch()
                    self.game.stdscr.timeout(-1)

                    if num_ships > 2 and random.randint(0, 4) == 0:
                        lost = (random.randint(0, num_ships - 1) // 2) + 1

                        num_ships -= lost
                        self.fight_stats(num_ships, self.orders)
                        self.game.stdscr.move(3, 0)
                        self.game.stdscr.clrtoeol()
                        self.game.stdscr.addstr(f"But we escaped from {lost} of 'em!")

                        if num_ships <= 10:
                            for i in range(9, -1, -1):
                                if self.num_on_screen > num_ships and self.ships_on_screen[i] > 0:
                                    self.ships_on_screen[i] = 0
                                    self.num_on_screen -= 1

                                    x = ((i + 1) * 10) if i < 5 else ((i - 4) * 10)
                                    y = 6 if i < 5 else 12
                                    self.clear_lorcha(x, y)
                                    self.game.stdscr.refresh()
                                    time.sleep(0.1)

                            if num_ships == self.num_on_screen:
                                self.game.stdscr.move(11, 62)
                                self.game.stdscr.addstr(" ")
                                self.game.stdscr.refresh()

                        self.game.stdscr.move(16, 0)
                        self.game.stdscr.refresh()
                        self.game.stdscr.timeout(M_PAUSE)
                        input_char = self.game.stdscr.getch()
                        self.game.stdscr.timeout(-1)

                        if input_char in [ord('F'), ord('f')]:
                            self.orders = 1
                        elif input_char in [ord('R'), ord('r')]:
                            self.orders = 2
                        elif input_char in [ord('T'), ord('t')]:
                            self.orders = 3

            # Handle enemy firing
            if num_ships > 0:
                self.game.stdscr.move(3, 0)
                self.game.stdscr.clrtoeol()
                self.game.stdscr.addstr("They're firing on us, Taipan!")
                self.game.stdscr.refresh()
                self.game.stdscr.timeout(M_PAUSE)
                self.game.stdscr.getch()
                self.game.stdscr.timeout(-1)
                curses.flushinp()

                # Show blast animation
                for i in range(3):
                    for y in range(24):
                        for x in range(79):
                            self.game.stdscr.move(y, x)
                            self.game.stdscr.addstr("*")
                    self.game.stdscr.refresh()
                    time.sleep(0.2)
                    self.game.stdscr.clear()
                    self.game.stdscr.refresh()
                    time.sleep(0.2)

                self.fight_stats(num_ships, self.orders)

                # Redraw ships
                x = 10
                y = 6
                for i in range(10):
                    if i == 5:
                        x = 10
                        y = 12

                    if self.ships_on_screen[i] > 0:
                        self.draw_lorcha(x, y)

                    x += 10

                # Update more ships indicator
                self.game.stdscr.move(11, 62)
                if num_ships > self.num_on_screen:
                    self.game.stdscr.addstr("+")
                else:
                    self.game.stdscr.addstr(" ")

                self.game.stdscr.move(3, 0)
                self.game.stdscr.clrtoeol()
                self.game.stdscr.addstr("We've been hit, Taipan!!")
                self.game.stdscr.refresh()
                self.game.stdscr.timeout(M_PAUSE)
                self.game.stdscr.getch()
                self.game.stdscr.timeout(-1)

                # Calculate damage
                i = min(num_ships, 15)
                if (self.game.guns > 0 and 
                    (random.randint(0, 99) < int((self.game.damage / self.game.capacity) * 100) or
                     int((self.game.damage / self.game.capacity) * 100) > 80)):
                    i = 1
                    if not DEBUG:  # Only prevent gun loss in debug mode
                        self.game.guns -= 1
                        self.game.hold += 10
                    self.fight_stats(num_ships, self.orders)
                    self.game.stdscr.move(3, 0)
                    self.game.stdscr.clrtoeol()
                    self.game.stdscr.addstr("The buggers hit a gun, Taipan!!")
                    self.fight_stats(num_ships, self.orders)
                    self.game.stdscr.refresh()
                    self.game.stdscr.timeout(M_PAUSE)
                    self.game.stdscr.getch()
                    self.game.stdscr.timeout(-1)

                # Apply damage regardless of debug mode
                self.game.damage += int((self.game.ed * i * battle_type) * random.random() + (i / 2))

                # Check for Li Yuen's intervention
                if battle_type == GENERIC and random.randint(0, 19) == 0:
                    return BATTLE_INTERRUPTED  # Battle interrupted by Li Yuen's pirates

        if num_ships == 0:
            if self.orders == 1:
                self.game.stdscr.clear()
                self.fight_stats(num_ships, self.orders)
                self.game.stdscr.move(3, 0)
                self.game.stdscr.clrtoeol()
                self.game.stdscr.addstr("We got 'em all, Taipan!")
                self.game.stdscr.refresh()
                self.game.stdscr.timeout(M_PAUSE)
                self.game.stdscr.getch()
                self.game.stdscr.timeout(-1)

                return BATTLE_WON  # Victory!
            else:
                return BATTLE_FLED  # Ran and got away. 