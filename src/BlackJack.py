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

Clear()

def Card(value):
    #border = Back.RED
    #face = Back.WHITE
    #reset = Style.RESET_ALL

    if value == "back":
        return [
            "+------+",
            "|# |  #|",
            "|#  | #|",
            "|#(][)#|",
            "|# |  #|",
            "|#  | #|",
            "+------+"
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

    #color = Fore.RED if value[-1] in "♥♦" else Fore.BLACK
    if value[:-1] == "10":
        return [
            "+------+",
            f"|{value:>6}|",
            "|      |",
            "|      |",
            "|      |",
            f"|{value:<6}|",
            "+------+"
        ]

    return [
            "+------+",
            f"|{value:>6}|",
            "|      |",
            "|      |",
            "|      |",
            f"|{value:<6}|",
            "+------+"
    ]

# niet door mij gemaakt
def PrintCards(cards):
    Clear()
    card_lists = [Card(card) for card in cards]

    for i in range(len(card_lists[0])):       
        print("  ".join(card[i] for card in card_lists))

# niet door mij gemaakt
def CardsToLines(top_cards, bottom_cards, width):

    def build_row(cards):
        if not cards:
            return []

        card_lists = [Card(card) for card in cards]

        lines = []
        for i in range(7):
            line = "  ".join(card[i] for card in card_lists)

            # centreren
            padding = max(0, (width - len(line)) // 2)
            lines.append(" " * padding + line)

        return lines

    lines = []

    # boven
    lines += build_row(top_cards)
    lines.append("")

    # onder
    lines += build_row(bottom_cards)

    return lines

#niet door mij gemaakt
def menu(title, classes, top_cards=None, bottom_cards=None, color='white'):

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
            h, w = stdscr.getmaxyx()

            for line in CardsToLines(top_cards or [], bottom_cards or [], w):
                stdscr.addstr(row, 0, line)
                row += 1

            

            # Kaarten tekenen
            #if top_cards or bottom_cards:
                #for line in CardsToLines(top_cards or [], bottom_cards or []):
                    #stdscr.addstr(row, 0, line)
                    #row += 1

                #row += 1

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

def PrintTable(options, cards_top, cards_bottom):
    choise = menu(
        "Blackjack",
        options,
        top_cards=cards_top,
        bottom_cards=cards_bottom,
        color="green"
    )
    return choise


#PrintTable(["Hit", "Stand", "Double Down"], ["blank", "K♥", "back", "blank"], ["blank", "K♥", "A♥", "blank"])


def DealCards(card, is_player = False, is_dealer = False):
    deck.DealCard(card)
    if is_player:
        table.DealPlayerCard(card)
        PrintTable(["Hit", "Stand", "double Down"], table.dealer_cards, table.player_cards)


    if is_dealer:
        table.DealDealerCard(card)
        PrintTable(["Hit", "Stand", "double Down"], table.dealer_cards, table.player_cards)

def on_press(key):
    if hasattr(key, "char") and key.char == "q":
        print(f"ended black jack with {player.chips or 0} chips")
        sys.exit()

with Listener(on_press=on_press) as listener:
    listener.join()