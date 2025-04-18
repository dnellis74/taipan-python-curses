import curses

from constants import *
from fancy_numbers import fancy_numbers
from keyboard import Keyboard

class Messages:
    def __init__(self):
        self.init_curses()
        self.keyboard = Keyboard(self.stdscr)  # Initialize keyboard here    

        
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
            
    def port_stats(self, status: int,
                   firm: str, hkw_: list[int], hold: int, hold_: list[int],
                   cash: int, bank: int, guns: int, debt: int, month: int, year: int, port: str) -> None:
        """Display port statistics screen."""        
        # Clear screen and prepare display
        self.stdscr.clear()
        
        # Center firm name
        spacer = 12 - (len(firm) // 2)
        self.stdscr.addstr(0, spacer, f"Firm: {firm}, Hong Kong")
        
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
        self.stdscr.addstr(3, 12, str(hkw_[0]))
        self.stdscr.addstr(4, 12, str(hkw_[1]))
        self.stdscr.addstr(5, 12, str(hkw_[2]))
        self.stdscr.addstr(6, 12, str(hkw_[3]))

        # Display hold status
        self.stdscr.move(8, 6)
        if hold >= 0:
            self.stdscr.addstr(str(hold))
        else:
            self.stdscr.attron(curses.A_REVERSE)
            self.stdscr.addstr("Overload")
            self.stdscr.attroff(curses.A_REVERSE)

        # Display current cargo
        self.stdscr.addstr(9, 12, str(hold_[0]))
        self.stdscr.addstr(10, 12, str(hold_[1]))
        self.stdscr.addstr(11, 12, str(hold_[2]))
        self.stdscr.addstr(12, 12, str(hold_[3]))

        # Display cash
        self.stdscr.move(14, 5)
        self.stdscr.addstr(fancy_numbers(cash))

        # Calculate and display warehouse usage
        in_use = sum(hkw_)
        self.stdscr.addstr(4, 21, str(in_use))
        self.stdscr.addstr(6, 21, str(10000 - in_use))

        # Display guns
        self.stdscr.addstr(8, 25, str(guns))

        # Display bank balance
        self.stdscr.move(14, 25)
        self.stdscr.addstr(fancy_numbers(bank))

        # Display date
        self.stdscr.move(3, 42)
        self.stdscr.addstr("15 ")
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(months[month - 1])
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr(f" {year}")

        # Display location
        self.stdscr.move(6, 43)
        spacer = (9 - len(port)) // 2
        self.stdscr.addstr(" " * spacer)
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(port)
        self.stdscr.attroff(curses.A_REVERSE)

        # Display debt
        self.stdscr.move(9, 41)
        debt_str = fancy_numbers(debt)
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
        self.stdscr.addstr(f"{status_texts[status_index]}:{int(status)}")
        self.stdscr.attroff(curses.A_REVERSE)

        self.stdscr.refresh()
        
    def name_firm(self) -> str:
        """Set the firm name. In debug mode, sets to 'debug'."""
        if DEBUG:
            return "debug"
        else:
            self.message_name_firm()

            character = 0
            firm = ""

            while character < 22:
                input_char = self.stdscr.getch()
                if input_char == ord('\n'):
                    return firm
                elif ((input_char == 8 or input_char == 127) and character == 0):
                    self.stdscr.refresh()
                elif input_char == 8 or input_char == 127:
                    self.stdscr.addch(8)
                    self.stdscr.addch(' ')
                    self.stdscr.addch(8)
                    firm = firm[:-1]
                    character -= 1
                    self.stdscr.refresh()
                elif input_char == 27:  # Escape key
                    curses.flushinp()
                    self.stdscr.refresh()
                else:
                    self.stdscr.addch(input_char)
                    firm += chr(input_char)
                    character += 1
                    self.stdscr.refresh()

    def message_wu_li_deny(self) -> None:
        self.stdscr.addstr("Very well. Elder Brother Wu will not pay\n")
        self.stdscr.addstr("Li Yuen the difference.  I would be very\n")
        self.stdscr.addstr("wary of pirates if I were you, Taipan.\n")

        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_wu_li_accept(self) -> None:
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

    def message_mugged(self, num: int) -> None:
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

    def message_wu_business(self) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Do you have business with Elder Brother\n")
        self.stdscr.addstr("Wu, the moneylender? ")
        self.stdscr.move(19, 21)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

    def message_wu_warning(self, braves: int) -> None:
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
        self.stdscr.addstr("and the importance of paying one's debts.\n")
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

    def message_splash(self) -> None:
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

    def message_name_firm(self) -> None:
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

    def message_cash_or_guns(self) -> None:
        self.stdscr.clear()
        self.stdscr.move(5, 0)
        self.stdscr.addstr("Do you want to start . . .\n\n")
        self.stdscr.addstr("  1) With cash (and a debt)\n\n")
        self.stdscr.addstr("                >> or <<\n\n")
        self.stdscr.addstr("  2) With five guns and no cash\n")
        self.stdscr.addstr("                (But no debt!)\n")
        self.stdscr.move(15, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("          ?")
        self.stdscr.refresh()

    def message_new_ship(self, damage: int, amount: int) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Do you wish to trade in your ")
        if damage > 0:
            self.stdscr.attron(curses.A_REVERSE)
            self.stdscr.addstr("damaged")
            self.stdscr.attroff(curses.A_REVERSE)
        else:
            self.stdscr.addstr("fine")
        self.stdscr.addstr("\nship for one with 50 more capacity by\n")
        self.stdscr.addstr(f"paying an additional {fancy_numbers(amount)}, Taipan? ")
        self.stdscr.refresh()

    def message_new_gun(self, amount: int) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Do you wish to buy a ship's gun\n")
        self.stdscr.addstr(f"for {fancy_numbers(amount)}, Taipan? ")
        self.stdscr.refresh()

    def message_retire(self) -> None:
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
    
    def message_li_yuen(self) -> None:
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
    
    def message_robbed(self, robbed: int) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Bad Joss!!\n")
        self.stdscr.addstr("You've been beaten up and\n")
        self.stdscr.addstr(f"robbed of {fancy_numbers(robbed)} in cash, Taipan!!\n")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)
    
    def message_warehouse_robbery(self) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Messenger reports large theft\n")
        self.stdscr.addstr("from warehouse, Taipan.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)
    
    def message_opium_seized(self, fine: int) -> None:
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

    def message_no_cargo(self) -> None:
        """Display message when player has no cargo"""
        self.stdscr.move(22, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("You have no cargo, Taipan.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_destinations(self) -> None:
        """Display available destinations"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Taipan, do you wish me to go to:\n")
        self.stdscr.addstr("1) Hong Kong, 2) Shanghai, 3) Nagasaki,\n")
        self.stdscr.addstr("4) Saigon, 5) Manila, 6) Singapore, or\n")
        self.stdscr.addstr("7) Batavia ? ")
        self.stdscr.refresh()

    def message_storm_sighted(self) -> None:
        """Display storm sighted message"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Storm, Taipan!!\n\n")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_going_down(self) -> None:
        """Display going down message"""
        self.stdscr.addstr("   I think we're going down!!\n\n")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_sinking(self) -> None:
        """Display sinking message"""
        self.stdscr.addstr("We're going down, Taipan!!\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_made_it(self) -> None:
        """Display made it through storm message"""
        self.stdscr.addstr("    We made it!!\n\n")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_li_donation(self, amount: int) -> None:
        """Display Li Yuen's donation request"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr(f"Li Yuen asks {fancy_numbers(amount)} in donation\n")
        self.stdscr.addstr("to the temple of Tin Hau, the Sea\n")
        self.stdscr.move(20, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Goddess.  Will you pay? ")
        self.stdscr.refresh()

    def message_off_course(self, location: str) -> None:
        """Display off course message"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("We've been blown off course\n")
        self.stdscr.addstr(f"to {location}")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_arriving(self, location: str) -> None:
        """Display arriving message"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr(f"Arriving at {location}...")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_final_stats(self, cash: int, capacity: int, guns: int, years: int, month: int, time: int) -> None:
        """Display final game statistics and rating"""
        self.stdscr.clear()
        self.stdscr.addstr("Your final status:\n\n")
        self.stdscr.addstr(f"Net cash:  {fancy_numbers(cash)}\n\n")
        self.stdscr.addstr(f"Ship size: {capacity} units with {guns} guns\n\n")
        self.stdscr.addstr(f"You traded for {years} year")
        if years != 1:
            self.stdscr.addstr("s")
        self.stdscr.addstr(f" and {month} month")
        if month > 1:
            self.stdscr.addstr("s")
        self.stdscr.addstr("\n\n")
        cash = cash / 100 / time
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(f"Your score is {int(cash)}.\n")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("\n")
        if (cash < 100) and (cash >= 0):
            self.stdscr.addstr("Have you considered a land based job?\n\n\n")
        elif cash < 0:
            self.stdscr.addstr("The crew has requested that you stay on\n")
            self.stdscr.addstr("shore for their safety!!\n\n")
        else:
            self.stdscr.addstr("\n\n\n")
        self.stdscr.addstr("Your Rating:\n")
        self.stdscr.addstr(" _______________________________\n")
        self.stdscr.addstr("|")
        if cash > 49999:
            self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("Ma Tsu")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("         50,000 and over |\n")
        self.stdscr.addstr("|")
        if (cash < 50000) and (cash > 7999):
            self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("Master Taipan")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("   8,000 to 49,999|\n")
        self.stdscr.addstr("|")
        if (cash < 8000) and (cash > 999):
            self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("Taipan")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("          1,000 to  7,999|\n")
        self.stdscr.addstr("|")
        if (cash < 1000) and (cash > 499):
            self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("Compradore")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("        500 to    999|\n")
        self.stdscr.addstr("|")
        if cash < 500:
            self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("Galley Hand")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("       less than 500|\n")
        self.stdscr.addstr("|_______________________________|\n\n")
        self.stdscr.move(22, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Play again? ")
        self.stdscr.refresh()

    def message_warehouse_full(self) -> None:
        """Display message when warehouse is full"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Taipan, the warehouse is full!\n")
        self.stdscr.refresh()

    def message_not_enough(self) -> None:
        """Display message when player doesn't have enough of something"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Taipan, you don't have that much!\n")
        self.stdscr.refresh()

    def message_to_hold(self, item: str) -> None:
        """Display comprador's report for transferring cargo"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr(f"How much {item} shall I move\n")
        self.stdscr.addstr("to the hold, Taipan? ")
        self.stdscr.refresh()

    def message_hold_full(self) -> None:
        """Display message when ship's hold is full"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Taipan, the hold is full!\n")
        self.stdscr.refresh()

    def message_captains_report(self) -> None:
        """Display captain's report header"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("  Captain's Report\n\n")
        self.stdscr.refresh()

    def message_hostile_ships(self, num_ships: int) -> None:
        """Display message about approaching hostile ships"""
        self.stdscr.addstr(f"{num_ships} hostile ships approaching, Taipan!\n")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_li_yuen_pirates(self) -> None:
        """Display message about Li Yuen's pirates"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Li Yuen's pirates, Taipan!!\n\n")
        self.stdscr.refresh()

        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_good_joss(self) -> None:
        """Display message when pirates let you be"""
        self.stdscr.addstr("Good joss!! They let us be!!\n")
        self.stdscr.refresh()

    def message_li_yuen_fleet(self, num_ships: int) -> None:
        """Display message about Li Yuen's pirate fleet"""
        self.stdscr.addstr(f"{num_ships} ships of Li Yuen's pirate\n")
        self.stdscr.addstr("fleet, Taipan!!\n")
        self.stdscr.refresh()

    def message_battle_results(self, result: int, booty: int) -> None:
        """Display battle results"""
        if result == 1:  # Victory!
            self.stdscr.addstr("We captured some booty.\n")
            self.stdscr.addstr(f"It's worth {fancy_numbers(booty)}!")
        elif result == 3:  # Ran and got away.
            self.stdscr.addstr("We made it!")
        else:  # Ship lost!
            self.stdscr.addstr("The buggers got us, Taipan!!!\n")
            self.stdscr.addstr("It's all over, now!!!")
        self.stdscr.refresh()
    
    def message_pirates_help(self, location: str):
        self.stdscr.move(6, 43)
        self.stdscr.addstr(" ")
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(location)
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("  ")

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("  Captain's Report\n\n")
        self.stdscr.addstr("Li Yuen's fleet drove them off!")
        self.stdscr.refresh()

        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_wu_pity(self, i: int, j: int) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Elder Brother is aware of your plight,\n")
        self.stdscr.addstr("Taipan.  He is willing to loan you an\n")
        self.stdscr.addstr(f"additional {i} if you will pay back\n")
        self.stdscr.addstr(f"{j}. Are you willing, Taipan? ")
        self.stdscr.refresh()

    def message_wu_game_over(self) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Very well, Taipan, the game is over!\n")
        self.stdscr.refresh()

    def message_wu_good_joss(self) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Very well, Taipan.  Good joss!!\n")
        self.stdscr.refresh()

    def message_wu_repay(self) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("How much do you wish to repay\n")
        self.stdscr.addstr("him? ")
        self.stdscr.refresh()

    def message_wu_borrow(self) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("How much do you wish to\n")
        self.stdscr.addstr("borrow? ")
        self.stdscr.refresh()

    def message_wu_too_much(self) -> None:
        self.stdscr.addstr("\n\nHe won't loan you so much, Taipan!")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_price_change(self, item: str, price: int, is_drop: bool) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr(f"Taipan!!  The price of {item}\n")
        if is_drop:
            self.stdscr.addstr(f"has dropped to {price}!!\n")
        else:
            self.stdscr.addstr(f"has risen to {price}!!\n")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_buy_prompt(self) -> None:
        self.stdscr.move(22, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("What do you wish me to buy, Taipan? ")
        self.stdscr.refresh()

    def message_sell_prompt(self) -> None:
        self.stdscr.move(22, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("What do you wish me to sell, Taipan? ")
        self.stdscr.refresh()

    def message_bank_deposit(self) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("How much will you deposit? ")
        self.stdscr.refresh()

    def message_bank_withdraw(self) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("How much will you withdraw? ")
        self.stdscr.refresh()

    def message_to_warehouse(self, item: str) -> None:
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr(f"How much {item} shall I move\n")
        self.stdscr.addstr("to the warehouse, Taipan? ")
        self.stdscr.refresh()

    def message_insufficient_cash(self, cash: int) -> None:
        """Display message when player has insufficient cash"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr(f"Taipan, you only have {fancy_numbers(cash)}\n")
        self.stdscr.addstr("in cash.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_insufficient_bank(self, bank: int) -> None:
        """Display message when player has insufficient bank balance"""
        self.stdscr.addstr(f"Taipan, you only have {fancy_numbers(bank)}\n")
        self.stdscr.addstr("in the bank.")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_already_here(self) -> None:
        """Display message when player tries to travel to current location"""
        self.stdscr.addstr("\n\nYou're already here, Taipan.")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_afford_amount(self, amount: int) -> None:
        """Display how much the player can afford"""
        self.stdscr.move(21, 42)
        self.stdscr.clrtobot()
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(" You can ")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.move(22, 0)
        self.stdscr.addstr("How much shall")
        self.stdscr.move(22, 42)
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr("  afford ")
        self.stdscr.move(23, 42)
        self.stdscr.addstr("         ")
        self.stdscr.move(23, 42)
        self.stdscr.move(23, 0)
        self.stdscr.addstr("I buy, Taipan: ")
        self.stdscr.refresh()
        
        # Add appropriate spacing based on number size
        if amount < 100:
            space = "    "
        elif amount < 10000:
            space = "   "
        elif amount < 1000000:
            space = "  "
        elif amount < 100000000:
            space = " "
        else:
            space = ""
            
        self.stdscr.addstr(f"{space}{amount}")
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.refresh()

    def message_comprador_prices(self, prices: list[int]) -> None:
        """Display current prices in the port"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Taipan, present prices per unit here are\n")
        self.stdscr.addstr("   Opium:          Silk:\n")
        self.stdscr.addstr("   Arms:           General:\n")
        self.stdscr.move(19, 11)
        self.stdscr.addstr(str(prices[0]))
        self.stdscr.move(19, 29)
        self.stdscr.addstr(str(prices[1]))
        self.stdscr.move(20, 11)
        self.stdscr.addstr(str(prices[2]))
        self.stdscr.move(20, 29)
        self.stdscr.addstr(str(prices[3]))
        self.stdscr.refresh()

    def message_port_menu(self, can_retire: bool) -> None:
        """Display port menu options"""
        self.stdscr.move(22, 0)
        self.stdscr.clrtobot()
        if can_retire:
            self.stdscr.addstr("Shall I Buy, Sell, Visit bank, Transfer\n")
            self.stdscr.addstr("cargo, Wheedle Wu, Quit trading, or Retire? ")
        else:
            self.stdscr.addstr("Shall I Buy, Sell, Visit bank, Transfer\n")
            self.stdscr.addstr("cargo, Wheedle Wu, or Quit trading? ")
        self.stdscr.refresh()

    def message_buy_amount(self, item: str) -> None:
        """Display buy amount prompt"""
        self.stdscr.move(23, 0)
        self.stdscr.addstr(f"How much {item} shall I buy, Taipan: ")
        self.stdscr.refresh()

    def message_sell_amount(self, item: str) -> None:
        """Display sell amount prompt"""
        self.stdscr.move(22, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr(f"How much {item} shall I sell, Taipan: ")
        self.stdscr.refresh()

    def message_destination_choice(self) -> None:
        """Display destination choice prompt"""
        self.stdscr.move(21, 13)
        self.stdscr.clrtobot()
        self.stdscr.refresh()

    def message_location_update(self, location: str) -> None:
        """Update location display"""
        self.stdscr.move(6, 43)
        self.stdscr.addstr(" ")
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(location)
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("  ")
        self.stdscr.refresh()

    def message_captains_report_header(self) -> None:
        """Display captain's report header"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("  Captain's Report\n\n")
        self.stdscr.refresh()

    def message_wu_difference(self) -> None:
        """Display message asking if Elder Brother Wu should make up the difference"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Do you want Elder Brother Wu to make up\n")
        self.stdscr.addstr("the difference for you? ")
        self.stdscr.refresh()

    def message_paid_in_full(self) -> None:
        """Display message indicating debt has been paid in full"""
        self.stdscr.addstr(f"Taipan, you owe only {fancy_numbers(self.debt)}.\n")
        self.stdscr.addstr("Paid in full.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)

    def message_booty(self) -> None:
        """Display message about captured booty"""
        self.stdscr.addstr("We captured some booty.\n")
        self.stdscr.refresh()

    def message_escaped(self) -> None:
        """Display message about escaping"""
        self.stdscr.addstr("We made it!")
        self.stdscr.refresh()

    def message_pause(self) -> None:
        """Pause for user input"""
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_all_over_now(self) -> None:
        """Display game over message"""
        self.stdscr.addstr("The buggers got us, Taipan!!!\n")
        self.stdscr.addstr("It's all over, now!!!")
        self.stdscr.refresh()

        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_after_battle_header(self, location: str) -> None:
        """Display header after battle"""
        self.stdscr.move(6, 43)
        self.stdscr.addstr(" ")
        self.stdscr.attron(curses.A_REVERSE)
        self.stdscr.addstr(location)
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.addstr("  ")

        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("  Captain's Report\n\n")
        self.stdscr.refresh()

    def message_quit_input(self) -> None:
        """Clear the quit input area"""
        self.stdscr.move(21, 13)
        self.stdscr.clrtobot()
        self.stdscr.refresh()

    def message_clear_refresh(self) -> None:
        """Clear the screen and refresh"""
        self.stdscr.clear()
        self.stdscr.refresh()
        curses.nocbreak()
        curses.endwin()

    def message_mchenry_repairs(self) -> None:
        """Display McHenry's repair offer message"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Taipan, Mc Henry from the Hong Kong\n")
        self.stdscr.addstr("Shipyards has arrived!!  He says, \"I see\n")
        self.stdscr.addstr("ye've a wee bit of damage to yer ship.\n")
        self.stdscr.addstr("Will ye be wanting repairs? ")
        self.stdscr.refresh()

    def message_mchenry_cost(self, amount: int) -> None:
        """Display McHenry's repair cost message"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Taipan, Mc Henry says it will cost\n")
        self.stdscr.addstr(f"{fancy_numbers(amount)} to repair your ship.\n")
        self.stdscr.addstr("Will you pay? ")
        self.stdscr.refresh()

    def message_repairs_complete(self) -> None:
        """Display repair completion message"""
        self.stdscr.move(16, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Comprador's Report\n\n")
        self.stdscr.addstr("Taipan, Mc Henry has repaired your\n")
        self.stdscr.addstr("ship.  It is now in perfect condition.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_mchenry_visit(self) -> None:
        """Display McHenry's visit message"""
        self.stdscr.clear()
        self.stdscr.move(0, 0)
        self.stdscr.addstr("McHenry is here, Taipan.")
        self.stdscr.move(1, 0)
        self.stdscr.addstr("He offers to sell you a new ship.")
        self.stdscr.move(2, 0)
        self.stdscr.addstr("Do you wish to buy? (Y/N)")
        self.stdscr.refresh()

    def message_mchenry_spend(self) -> None:
        """Display McHenry's spend prompt"""
        self.stdscr.move(3, 0)
        self.stdscr.addstr("How much do you wish to spend?")
        self.stdscr.refresh()

    def message_mchenry_new_capacity(self, capacity: int) -> None:
        """Display new ship capacity message"""
        self.stdscr.move(4, 0)
        self.stdscr.addstr(f"Your new capacity is {capacity}.")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)
        self.stdscr.clear()
        self.stdscr.refresh()

    def message_mchenry_damage(self, percent: int, repair_price: int) -> None:
        """Display ship damage and repair cost message"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr(f"Och, 'tis a pity to be {percent}% damaged.\n")
        self.stdscr.addstr(f"We can fix yer whole ship for {repair_price},\n")
        self.stdscr.addstr("or make partial repairs if you wish.\n")
        self.stdscr.addstr("How much will ye spend? ")
        self.stdscr.refresh()

    def message_mchenry_no_free_work(self) -> None:
        """Display message when player can't afford repairs"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("McHenry does not work for free, Taipan!\n")
        self.stdscr.refresh()

    def message_insufficient_funds(self) -> None:
        """Display message when player has insufficient funds"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Taipan, you do not have enough cash!!\n\n")
        self.stdscr.refresh()
        self.stdscr.timeout(M_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_wu_difference_offer(self) -> None:
        """Display Elder Brother Wu's offer to make up the difference"""
        self.stdscr.addstr("Do you want Elder Brother Wu to make up\n")
        self.stdscr.addstr("the difference for you? ")
        self.stdscr.refresh()

    def message_wu_loan_terms(self) -> None:
        """Display Elder Brother Wu's loan terms"""
        self.stdscr.move(18, 0)
        self.stdscr.clrtobot()
        self.stdscr.addstr("Elder Brother has given McHenry the\n")
        self.stdscr.addstr("difference between what he wanted and\n")
        self.stdscr.addstr("your cash on hand and added the same\n")
        self.stdscr.addstr("amount to your debt.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1)

    def message_wu_deny_help(self) -> None:
        """Display message when Elder Brother Wu denies help"""
        self.stdscr.addstr("Very well. Elder Brother Wu will not pay\n")
        self.stdscr.addstr("McHenry the difference.  I would be very\n")
        self.stdscr.addstr("wary of pirates if I were you, Taipan.\n")
        self.stdscr.refresh()
        self.stdscr.timeout(L_PAUSE)
        self.stdscr.getch()
        self.stdscr.timeout(-1) 