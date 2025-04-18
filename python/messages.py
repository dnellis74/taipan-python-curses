import curses

from constants import *
from shared import fancy_numbers

def message_wu_li_deny(stdscr: curses.window) -> None:
    stdscr.addstr("Very well. Elder Brother Wu will not pay\n")
    stdscr.addstr("Li Yuen the difference.  I would be very\n")
    stdscr.addstr("wary of pirates if I were you, Taipan.\n")

    stdscr.refresh()
    stdscr.timeout(L_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_wu_li_accept(stdscr: curses.window) -> None:
    stdscr.move(18, 0)
    stdscr.clrtobot()
    stdscr.addstr("Elder Brother has given Li Yuen the\n")
    stdscr.addstr("difference between what he wanted and\n")
    stdscr.addstr("your cash on hand and added the same\n")
    stdscr.addstr("amount to your debt.\n")

    stdscr.refresh()
    stdscr.timeout(L_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_mugged(stdscr: curses.window, num: int) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Bad joss!!\n")
    stdscr.addstr(f"{num} of your bodyguards have been killed\n")
    stdscr.addstr("by cutthroats and you have been robbed\n")
    stdscr.addstr("of all of your cash, Taipan!!\n")

    stdscr.refresh()
    stdscr.timeout(L_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_wu_business(stdscr: curses.window) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Do you have business with Elder Brother\n")
    stdscr.addstr("Wu, the moneylender? ")

def message_wu_warning(stdscr: curses.window, braves: int) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr(f"Elder Brother Wu has sent {braves} braves\n")
    stdscr.addstr("to escort you to the Wu mansion, Taipan.\n")
    stdscr.refresh()
    stdscr.timeout(M_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

    stdscr.move(18, 0)
    stdscr.clrtobot()
    stdscr.addstr("Elder Brother Wu reminds you of the\n")
    stdscr.addstr("Confucian ideal of personal worthiness,\n")
    stdscr.addstr("and the importance of paying one's debts.\n")
    stdscr.refresh()
    stdscr.timeout(M_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)
    
    stdscr.move(18, 0)
    stdscr.clrtobot()
    stdscr.addstr("He is reminded of a fabled barbarian\n")
    stdscr.addstr("who came to a bad end, after not caring\n")
    stdscr.addstr("for his obligations.\n\n")
    stdscr.addstr("He hopes no such fate awaits you, his\n")
    stdscr.addstr("friend, Taipan.\n")

    stdscr.refresh()
    stdscr.timeout(5000)
    stdscr.getch()
    stdscr.timeout(-1)

def message_splash(stdscr: curses.window) -> None:
    stdscr.clear()
    stdscr.addstr("\n")
    stdscr.addstr("         _____  _    ___ ____   _    _   _               ===============\n")
    stdscr.addstr("        |_   _|/ \\  |_ _|  _ \\ / \\  | \\ | |              Created by:\n")
    stdscr.addstr("          | | / _ \\  | || |_) / _ \\ |  \\| |                 Art Canfil\n")
    stdscr.addstr("          | |/ ___ \\ | ||  __/ ___ \\| |\\  |\n")
    stdscr.addstr("          |_/_/   \\_\\___|_| /_/   \\_\\_| \\_|              ===============\n")
    stdscr.addstr("                                                         Programmed by:\n")
    stdscr.addstr("   A game based on the China trade of the 1800's            Jay Link\n")
    stdscr.addstr("\n")
    stdscr.addstr("                      ~~|     ,                          jlink@ilbbs.com\n")
    stdscr.addstr("                       ,|`-._/|\n")
    stdscr.addstr("                     .' |   /||\\                         ===============\n")
    stdscr.addstr("                   .'   | ./ ||`\\                         Copyright (c)\n")
    stdscr.addstr("                  / `-. |/._ ||  \\                         1978 - 2002\n")
    stdscr.addstr("                 /     `||  `|;-._\\                         Art Canfil\n")
    stdscr.addstr("                 |      ||   ||   \\\n")
    stdscr.addstr("~^~_-~^~=~^~~^= /       ||   ||__  \\~^=~^~-~^~_~^~=      ===============\n")
    stdscr.addstr(" ~=~^~ _~^~ =~ `--------|`---||  `\"-`___~~^~ =_~^=        Press ")
    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr("ANY")
    stdscr.attroff(curses.A_REVERSE)
    stdscr.addstr(" key\n")
    stdscr.addstr("~ ~^~=~^_~^~ =~ \\~~~~~~~'~~~~'~~~~/~~`` ~=~^~ ~^=           to start.\n")
    stdscr.addstr(" ~^=~^~_~-=~^~ ^ `--------------'~^~=~^~_~^=~^~=~\n")

def message_name_firm(stdscr: curses.window) -> None:
    stdscr.clear()
    stdscr.move(7, 0)
    stdscr.addstr(" _______________________________________\n")
    stdscr.addstr("|     Taipan,                           |\n")
    stdscr.addstr("|                                       |\n")
    stdscr.addstr("| What will you name your               |\n")
    stdscr.addstr("|                                       |\n")
    stdscr.addstr("|     Firm:                             |\n")
    stdscr.addstr("|           ----------------------      |\n")
    stdscr.addstr("|_______________________________________|\n")        
    stdscr.move(12, 12)
    stdscr.refresh()

def message_cash_or_guns(stdscr: curses.window) -> None:
    stdscr.clear()
    stdscr.move(5, 0)
    stdscr.addstr("Do you want to start . . .\n\n")
    stdscr.addstr("  1) With cash (and a debt)\n\n")
    stdscr.addstr("                >> or <<\n\n")
    stdscr.addstr("  2) With five guns and no cash\n")
    stdscr.addstr("                (But no debt!)\n")

def message_new_ship(stdscr: curses.window, damage: int, amount: int) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Do you wish to trade in your ")
    if damage > 0:
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr("damaged")
        stdscr.attroff(curses.A_REVERSE)
    else:
        stdscr.addstr("fine")
    stdscr.addstr("\nship for one with 50 more capacity by\n")
    stdscr.addstr(f"paying an additional {fancy_numbers(amount)}, Taipan? ")
    stdscr.refresh()

def message_new_gun(stdscr: curses.window, amount: int) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Do you wish to buy a ship's gun\n")
    stdscr.addstr(f"for {fancy_numbers(amount)}, Taipan? ")
    stdscr.refresh()

def message_retire(stdscr: curses.window) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr("                         \n")
    stdscr.addstr(" Y o u ' r e    a        \n")
    stdscr.addstr("                         \n")
    stdscr.addstr(" M I L L I O N A I R E ! \n")
    stdscr.addstr("                         \n")
    stdscr.attroff(curses.A_REVERSE)
    stdscr.refresh()
    stdscr.timeout(L_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)
    
def message_li_yuen(stdscr: curses.window) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Li Yuen has sent a Lieutenant,\n")
    stdscr.addstr("Taipan.  He says his admiral wishes\n")
    stdscr.addstr("to see you in Hong Kong, posthaste!\n")
    stdscr.refresh()
    stdscr.timeout(M_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)
    
def message_robbed(stdscr: curses.window, robbed: int) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Bad Joss!!\n")
    stdscr.addstr("You've been beaten up and\n")
    stdscr.addstr(f"robbed of {fancy_numbers(robbed)} in cash, Taipan!!\n")
    stdscr.refresh()
    stdscr.timeout(M_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)
    
def message_warehouse_robbery(stdscr: curses.window) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Messenger reports large theft\n")
    stdscr.addstr("from warehouse, Taipan.\n")
    stdscr.refresh()
    stdscr.timeout(L_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)
    
def message_opium_seized(stdscr: curses.window, fine: int) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Bad Joss!!\n")
    stdscr.addstr("The local authorities have seized your\n")
    if fine <= 0:
        stdscr.addstr("Opium cargo, Taipan!")
    else:
        stdscr.addstr("Opium cargo and have also fined you\n")
        stdscr.addstr(f"{fancy_numbers(fine)}, Taipan!\n")
    stdscr.refresh()
    stdscr.timeout(L_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_no_cargo(stdscr: curses.window) -> None:
    """Display message when player has no cargo"""
    stdscr.move(22, 0)
    stdscr.clrtobot()
    stdscr.addstr("You have no cargo, Taipan.\n")
    stdscr.refresh()
    stdscr.timeout(L_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_destinations(stdscr: curses.window) -> None:
    """Display available destinations"""
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Taipan, do you wish me to go to:\n")
    stdscr.addstr("1) Hong Kong, 2) Shanghai, 3) Nagasaki,\n")
    stdscr.addstr("4) Saigon, 5) Manila, 6) Singapore, or\n")
    stdscr.addstr("7) Batavia ? ")
    stdscr.refresh()

def message_storm_sighted(stdscr: curses.window) -> None:
    """Display storm sighted message"""
    stdscr.move(18, 0)
    stdscr.clrtobot()
    stdscr.addstr("Storm, Taipan!!\n\n")
    stdscr.refresh()
    stdscr.timeout(M_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_going_down(stdscr: curses.window) -> None:
    """Display going down message"""
    stdscr.addstr("   I think we're going down!!\n\n")
    stdscr.refresh()
    stdscr.timeout(M_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_sinking(stdscr: curses.window) -> None:
    """Display sinking message"""
    stdscr.addstr("We're going down, Taipan!!\n")
    stdscr.refresh()
    stdscr.timeout(L_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_made_it(stdscr: curses.window) -> None:
    """Display made it through storm message"""
    stdscr.addstr("    We made it!!\n\n")
    stdscr.refresh()
    stdscr.timeout(M_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_li_donation(stdscr: curses.window, amount: int) -> None:
    """Display Li Yuen's donation request"""
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr(f"Li Yuen asks {fancy_numbers(amount)} in donation\n")
    stdscr.addstr("to the temple of Tin Hau, the Sea\n")
    stdscr.move(20, 0)
    stdscr.clrtobot()
    stdscr.addstr("Goddess.  Will you pay? ")
    stdscr.refresh()

def message_off_course(stdscr: curses.window, location: str) -> None:
    """Display off course message"""
    stdscr.move(18, 0)
    stdscr.clrtobot()
    stdscr.addstr("We've been blown off course\n")
    stdscr.addstr(f"to {location}")
    stdscr.refresh()
    stdscr.timeout(M_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_arriving(stdscr: curses.window, location: str) -> None:
    """Display arriving message"""
    stdscr.move(18, 0)
    stdscr.clrtobot()
    stdscr.addstr(f"Arriving at {location}...")
    stdscr.refresh()
    stdscr.timeout(M_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_final_stats(stdscr, cash: int, capacity: int, guns: int, years: int, month: int, time: int) -> None:
    """Display final game statistics and rating"""
    stdscr.clear()
    stdscr.addstr("Your final status:\n\n")
    stdscr.addstr(f"Net cash:  {fancy_numbers(cash)}\n\n")
    stdscr.addstr(f"Ship size: {capacity} units with {guns} guns\n\n")
    stdscr.addstr(f"You traded for {years} year")
    if years != 1:
        stdscr.addstr("s")
    stdscr.addstr(f" and {month} month")
    if month > 1:
        stdscr.addstr("s")
    stdscr.addstr("\n\n")
    cash = cash / 100 / time
    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr(f"Your score is {int(cash)}.\n")
    stdscr.attroff(curses.A_REVERSE)
    stdscr.addstr("\n")
    if (cash < 100) and (cash >= 0):
        stdscr.addstr("Have you considered a land based job?\n\n\n")
    elif cash < 0:
        stdscr.addstr("The crew has requested that you stay on\n")
        stdscr.addstr("shore for their safety!!\n\n")
    else:
        stdscr.addstr("\n\n\n")
    stdscr.addstr("Your Rating:\n")
    stdscr.addstr(" _______________________________\n")
    stdscr.addstr("|")
    if cash > 49999:
        stdscr.attron(curses.A_REVERSE)
    stdscr.addstr("Ma Tsu")
    stdscr.attroff(curses.A_REVERSE)
    stdscr.addstr("         50,000 and over |\n")
    stdscr.addstr("|")
    if (cash < 50000) and (cash > 7999):
        stdscr.attron(curses.A_REVERSE)
    stdscr.addstr("Master Taipan")
    stdscr.attroff(curses.A_REVERSE)
    stdscr.addstr("   8,000 to 49,999|\n")
    stdscr.addstr("|")
    if (cash < 8000) and (cash > 999):
        stdscr.attron(curses.A_REVERSE)
    stdscr.addstr("Taipan")
    stdscr.attroff(curses.A_REVERSE)
    stdscr.addstr("          1,000 to  7,999|\n")
    stdscr.addstr("|")
    if (cash < 1000) and (cash > 499):
        stdscr.attron(curses.A_REVERSE)
    stdscr.addstr("Compradore")
    stdscr.attroff(curses.A_REVERSE)
    stdscr.addstr("        500 to    999|\n")
    stdscr.addstr("|")
    if cash < 500:
        stdscr.attron(curses.A_REVERSE)
    stdscr.addstr("Galley Hand")
    stdscr.attroff(curses.A_REVERSE)
    stdscr.addstr("       less than 500|\n")
    stdscr.addstr("|_______________________________|\n\n")
    stdscr.move(22, 0)
    stdscr.clrtobot()
    stdscr.addstr("Play again? ")
    stdscr.refresh()

def message_warehouse_full(stdscr) -> None:
    """Display message when warehouse is full"""
    stdscr.move(18, 0)
    stdscr.clrtobot()
    stdscr.addstr("Taipan, the warehouse is full!\n")
    stdscr.refresh()

def message_not_enough(stdscr) -> None:
    """Display message when player doesn't have enough of something"""
    stdscr.move(18, 0)
    stdscr.clrtobot()
    stdscr.addstr("Taipan, you don't have that much!\n")
    stdscr.refresh()

def message_comprador_report(stdscr, item: str) -> None:
    """Display comprador's report for transferring cargo"""
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr(f"How much {item} shall I move\n")
    stdscr.addstr("to the hold, Taipan? ")
    stdscr.refresh()

def message_hold_full(stdscr) -> None:
    """Display message when ship's hold is full"""
    stdscr.move(18, 0)
    stdscr.clrtobot()
    stdscr.addstr("Taipan, the hold is full!\n")
    stdscr.refresh()

def message_captains_report(stdscr) -> None:
    """Display captain's report header"""
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("  Captain's Report\n\n")
    stdscr.refresh()

def message_hostile_ships(stdscr, num_ships: int) -> None:
    """Display message about approaching hostile ships"""
    stdscr.addstr(f"{num_ships} hostile ships approaching, Taipan!\n")
    stdscr.refresh()

def message_li_yuen_pirates(stdscr) -> None:
    """Display message about Li Yuen's pirates"""
    stdscr.move(18, 0)
    stdscr.clrtobot()
    stdscr.addstr("Li Yuen's pirates, Taipan!!\n\n")
    stdscr.refresh()

def message_good_joss(stdscr) -> None:
    """Display message when pirates let you be"""
    stdscr.addstr("Good joss!! They let us be!!\n")
    stdscr.refresh()

def message_li_yuen_fleet(stdscr, num_ships: int) -> None:
    """Display message about Li Yuen's pirate fleet"""
    stdscr.addstr(f"{num_ships} ships of Li Yuen's pirate\n")
    stdscr.addstr("fleet, Taipan!!\n")
    stdscr.refresh()

def message_battle_results(stdscr, result: int, booty: int) -> None:
    """Display battle results"""
    if result == 1:  # Victory!
        stdscr.addstr("We captured some booty.\n")
        stdscr.addstr(f"It's worth {fancy_numbers(booty)}!")
    elif result == 3:  # Ran and got away.
        stdscr.addstr("We made it!")
    else:  # Ship lost!
        stdscr.addstr("The buggers got us, Taipan!!!\n")
        stdscr.addstr("It's all over, now!!!")
    stdscr.refresh()
    
def message_pirates_help(stdscr: curses.window, location: str):
    stdscr.move(6, 43)
    stdscr.addstr(" ")
    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr(location)
    stdscr.attroff(curses.A_REVERSE)
    stdscr.addstr("  ")

    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("  Captain's Report\n\n")
    stdscr.addstr("Li Yuen's fleet drove them off!")
    stdscr.refresh()

    stdscr.timeout(M_PAUSE)
    stdscr.getch()
    stdscr.timeout(-1)

def message_wu_pity(stdscr: curses.window, i: int, j: int) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Elder Brother is aware of your plight,\n")
    stdscr.addstr("Taipan.  He is willing to loan you an\n")
    stdscr.addstr(f"additional {i} if you will pay back\n")
    stdscr.addstr(f"{j}. Are you willing, Taipan? ")
    stdscr.refresh()

def message_wu_game_over(stdscr: curses.window) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Very well, Taipan, the game is over!\n")
    stdscr.refresh()

def message_wu_good_joss(stdscr: curses.window) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("Very well, Taipan.  Good joss!!\n")
    stdscr.refresh()

def message_wu_repay(stdscr: curses.window) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("How much do you wish to repay\n")
    stdscr.addstr("him? ")
    stdscr.refresh()

def message_wu_borrow(stdscr: curses.window) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("How much do you wish to\n")
    stdscr.addstr("borrow? ")
    stdscr.refresh()

def message_wu_too_much(stdscr: curses.window) -> None:
    stdscr.addstr("\n\nHe won't loan you so much, Taipan!")
    stdscr.refresh()

def message_price_change(stdscr: curses.window, item: str, price: int, is_drop: bool) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr(f"Taipan!!  The price of {item}\n")
    if is_drop:
        stdscr.addstr(f"has dropped to {price}!!\n")
    else:
        stdscr.addstr(f"has risen to {price}!!\n")
    stdscr.refresh()

def message_buy_prompt(stdscr: curses.window) -> None:
    stdscr.move(22, 0)
    stdscr.clrtobot()
    stdscr.addstr("What do you wish me to buy, Taipan? ")
    stdscr.refresh()

def message_sell_prompt(stdscr: curses.window) -> None:
    stdscr.move(22, 0)
    stdscr.clrtobot()
    stdscr.addstr("What do you wish me to sell, Taipan? ")
    stdscr.refresh()

def message_bank_deposit(stdscr: curses.window) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("How much will you deposit? ")
    stdscr.refresh()

def message_bank_withdraw(stdscr: curses.window) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr("How much will you withdraw? ")
    stdscr.refresh()

def message_transfer_prompt(stdscr: curses.window, item: str) -> None:
    stdscr.move(16, 0)
    stdscr.clrtobot()
    stdscr.addstr("Comprador's Report\n\n")
    stdscr.addstr(f"How much {item} shall I move\n")
    stdscr.addstr("to the warehouse, Taipan? ")
    stdscr.refresh()