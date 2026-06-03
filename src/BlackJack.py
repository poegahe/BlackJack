from colorama import Fore, Back, Style, init
import random
import time
import os
import curses
import sys
from pynput.keyboard import Key, Listener

# Initialize colorama (needed for Windows)
init(autoreset=True)

#♠♥♦♣
#print(Fore.RED + "This is red text")
#sys.stdout.write(f"\rkaas")
class Table():
    def __init__(self):
        self.dealer_cards = []
        self.player_cards = []

    def DealDealerCard(self, card):
        self.dealer_cards.append(card)

    def DealPlayerCard(self, card):
        self.player_ccards.append(card)

    #def GetTable(self):
        


class Deck():
    deck_of_cards = [
        '1♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠',
        '1♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',
        '1♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',
        '1♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣'
    ]

    def __init__(self):
        self.cards = Deck.deck_of_cards
        self.dealt_cards = []
        random.shuffle(self.cards)

    def Shuffle(self):
        random.shuffle(self.cards)

    def DealCard(self):
        self.dealt_cards.append(self.cards[0])
        return self.cards.pop(0)

class Player():
    def __init__(self, starting_chips = 100):
        self.chips = starting_chips
        self.hands_played = 0
        self.hands_won = 0
        self.hands_lost = 0

table = Table()
deck = Deck()
deck.Shuffle()
player = Player()

def Clear():
    os.system("cls" if os.name == "nt" else "clear")

def Card(value):
    border = Back.RED
    face = Back.WHITE
    reset = Style.RESET_ALL

    if value == "back":
        return [
            f"{border},------,{reset}",
            f"{border}|* |  *|{reset}",
            f"{border}|*  | *|{reset}",
            f"{border}|*(][)*|{reset}",
            f"{border}|* |  *|{reset}",
            f"{border}|*  | *|{reset}",
            f"{border}'------'{reset}"
        ]
    if value == "blank":
        return[
            "        ",
            "        ",
            "        ",
            "        ",
            "        ",
            "        ",
            "        "
        ]

    color = Fore.RED if value[-1] in "♥♦" else Fore.BLACK
    if value[:-1] == "10":
        return [
            f"{border},------,{reset}",
            f"{border}|{face}{Fore.BLACK}{value[:-1]:>5}{color}{value[-1:]}{border}{Fore.WHITE}|{reset}",
            f"{border}|{face}      {border}|{reset}",
            f"{border}|{face}      {border}|{reset}",
            f"{border}|{face}      {border}|{reset}",
            f"{border}|{face}{Fore.BLACK}{value[:-1]}{color}{value[-1:]:<4}{border}{Fore.WHITE}|{reset}",
            f"{border}'------'{reset}"
        ]

    return [
        f"{border},------,{reset}",
        f"{border}|{face}{Fore.BLACK}{value[:-1]:>5}{color}{value[-1:]}{border}{Fore.WHITE}|{reset}",
        f"{border}|{face}      {border}|{reset}",
        f"{border}|{face}      {border}|{reset}",
        f"{border}|{face}      {border}|{reset}",
        f"{border}|{face}{Fore.BLACK}{value[:-1]}{color}{value[-1:]:<5}{border}{Fore.WHITE}|{reset}",
        f"{border}'------'{reset}"
    ]

def PrintCards(cards):
    Clear()
    card_lists = [Card(card) for card in cards]

    for i in range(len(card_lists[0])):       
        print("  ".join(card[i] for card in card_lists))

def CardsToLines(cards):
    card_lists = [Card(card) for card in cards]

    lines = []

    for i in range(len(card_lists[0])):
        lines.append("  ".join(card[i] for card in card_lists))

    return lines

def menu(title, classes, cards=None, color='white'):

    def character(stdscr):

        curses.curs_set(0)
        curses.start_color()
        stdscr.keypad(True)

        attributes = {}

        icol = {
            1: 'red',
            2: 'green',
            3: 'yellow',
            4: 'blue',
            5: 'magenta',
            6: 'cyan',
            7: 'white'
        }

        col = {v: k for k, v in icol.items()}

        bc = curses.COLOR_BLACK

        curses.init_pair(1, curses.COLOR_WHITE, bc)
        attributes['normal'] = curses.color_pair(1)

        curses.init_pair(2, col[color], bc)
        attributes['highlighted'] = curses.color_pair(2)

        option = 0

        while True:

            stdscr.erase()

            row = 0

            # Kaarten tekenen
            if cards:
                for line in CardsToLines(cards):
                    stdscr.addstr(row, 0, line)
                    row += 1

                row += 2

            # Titel
            stdscr.addstr(row, 0, title, attributes['normal'])
            row += 2

            # Opties
            for i, item in enumerate(classes):

                attr = (
                    attributes['highlighted']
                    if i == option
                    else attributes['normal']
                )

                prefix = "> " if i == option else "  "

                stdscr.addstr(row, 0, prefix + item, attr)
                row += 1

            stdscr.refresh()

            c = stdscr.getch()

            if c == curses.KEY_UP and option > 0:
                option -= 1

            elif c == curses.KEY_DOWN and option < len(classes) - 1:
                option += 1

            elif c in (10, 13):
                return option

    return curses.wrapper(character)

#PrintCards(["blank", "K♥", "back", "blank"])

#(f"output:", menu('TEST', ['this will return 0','this will return 1', 'this is just to show that you can do more options then just two'], 'blue'))

keuze = menu(
    "Blackjack",
    ["Hit", "Stand", "Double Down"],
    cards=["blank", "K♥", "back", "blank"],
    color="green"
)

def on_press(key):
    if hasattr(key, "char") and key.char == "l":
        PrintCards(["back", "K♥", "back", "blank"])
    if hasattr(key, "char") and key.char == "q":
        print(f"ended black jack with {player.chips or 0} chips")
        sys.exit()

with Listener(on_press=on_press) as listener:
    listener.join()


def DealCards(card, is_player = False, is_dealer = False):
    deck.DealCard(card)
    if is_player:
        table.DealPlayerCard(card)

    if is_dealer:
        table.DealDealerCard(card)