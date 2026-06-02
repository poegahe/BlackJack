from colorama import Fore, Back, Style, init
import random
import time
import os
import sys
from pynput.keyboard import Key, Listener

# Initialize colorama (needed for Windows)
init(autoreset=True)

#♠♥♦♣
#print(Fore.RED + "This is red text")
#sys.stdout.write(f"\rkaas")

class Deck():
    deck_of_cards = ['1♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠',
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

deck = Deck()
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

def PrintCards(*cards):
    Clear()
    card_lists = [Card(card) for card in cards]

    for i in range(len(card_lists[0])):
        print("  ".join(card[i] for card in card_lists))

PrintCards("blank", "K♥", "10♦", "back")

def on_press(key):
    if hasattr(key, "char") and key.char == "l":
        PrintCards("blank", "K♥", "back", "blank")
    if hasattr(key, "char") and key.char == "q":
        print(f"ended black jack with {player.chips or 0} chips")
        sys.exit()

with Listener(on_press=on_press) as listener:
    listener.join()