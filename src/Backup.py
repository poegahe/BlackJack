from colorama import Fore, Back, Style, init
import random
import time
import os
import curses
import sys
import numbers
from pynput.keyboard import Key, Listener

# Initialize colorama (needed for Windows)
init(autoreset=True)

#♠♥♦♣
#print(Fore.RED + "This is red text")
#sys.stdout.write(f"\rkaas")
class Table():
    def __init__(self):
        self.dealer_card_hidden = False
        self.dealer_cards = []
        self.player_cards = []
        self.player_total = 0
        self.dealer_total = 0
        self.keep_going = True
        self.player_aces = 0
        self.dealer_aces = 0

    def DealDealerCard(self, card):
        self.dealer_cards.append(card)

        non_number = "KJQ"
        if card[:-1] in non_number:
            self.dealer_total += 10
        elif card[:-1] == "A":
            self.dealer_total += 11
        else:
            self.dealer_total += int(card[:-1])
        if self.dealer_total > 21 and ("A" == card[:-1] for card in self.dealer_cards) and self.dealer_aces < sum(card.count("A") for card in self.dealer_cards):
            self.dealer_total -= 10


    def DealPlayerCard(self, card):
        self.player_cards.append(card)

        non_number = "KJQ"
        if card[:-1] in non_number:
            self.player_total += 10
        elif card[:-1] == "A":
            self.player_total += 11
        else:
            self.player_total += int(card[:-1])
        if self.player_total > 21 and ("A" == card[:-1] for card in self.player_cards) and self.player_aces < sum(card.count("A") for card in self.player_cards):
            self.player_total -= 10

    def ShowOrHide(self, show):
        if show:
            self.dealer_card_hidden = False
        else:
            self.dealer_card_hidden = True

    def Continue(self):
        self.keep_going = False
        


class Deck():
    deck_of_cards = [
        '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠',
        '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',
        '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',
        '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣'
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

def PrintCards(cards):
    Clear()
    card_lists = [Card(card) for card in cards]

    for i in range(len(card_lists[0])):       
        print("  ".join(card[i] for card in card_lists))


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

def Debug(msg):
    with open("debug.txt", "a", encoding="utf-8") as f:
        f.write(str(msg) + "\n")

def menu(title, classes, top_cards=None, bottom_cards=None, color='white'):
    new_top_cards = [card for card in top_cards]
    new_bottom_cards = [card for card in bottom_cards]
    
    
    if len(classes) == 0:
        def character(stdscr):
            while True:
                stdscr.erase()
            
                row = 0
                h, w = stdscr.getmaxyx()

                Debug(table.dealer_card_hidden)
                if table.dealer_card_hidden == True:
                    new_top_cards[0] = "back"


                top_lines = CardsToLines(new_top_cards, [], w)
                bottom_lines = CardsToLines([], new_bottom_cards, w)                
                
                #add dealer header
                dealer_cards = [card[:-1] for card in table.dealer_cards]
                dealer_value = ""
                if table.dealer_card_hidden:
                    dealer_cards[0] = "?"
                    dealer_value = " + ".join(dealer_cards)
                else:
                    dealer_value = " + ".join(dealer_cards) + " = " + str(table.dealer_total)

                stdscr.addstr(row, 0, f"Dealer ({dealer_value}):")
                row += 1


                for line in top_lines:
                    stdscr.addstr(row, 0, line) 
                    row += 1

                #add player header
                player_cards = [card[:-1] for card in table.player_cards]
                player_value = " + ".join(player_cards) + " = " + str(table.player_total)

                stdscr.addstr(row, 0, f"Dealer ({player_value}):")
                row += 1

                for line in bottom_lines:
                    stdscr.addstr(row, 0, line) 
                    row += 1

                stdscr.refresh()
                time.sleep(0.75)

                return 0

        return curses.wrapper(character)
        
    
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

            if table.dealer_card_hidden:
                new_top_cards[0] = "back"
            top_lines = CardsToLines(new_top_cards, [], w)
            bottom_lines = CardsToLines([], new_bottom_cards, w)

            #add dealer header
            dealer_cards = [card[:-1] for card in table.dealer_cards]
            dealer_value = ""
            if table.dealer_card_hidden:
                dealer_cards[0] = "?"
                dealer_value = " + ".join(dealer_cards)
            else:
                dealer_value = " + ".join(dealer_cards) + " = " + str(table.dealer_total)

            stdscr.addstr(row, 0, f"Dealer ({dealer_value}):")
            row += 1


            for line in top_lines:
                stdscr.addstr(row, 0, line) 
                row += 1


            #add player header
            player_cards = [card[:-1] for card in table.player_cards]
            player_value = " + ".join(player_cards) + " = " + str(table.player_total)

            stdscr.addstr(row, 0, f"Dealer ({player_value}):")
            row += 1

            for line in bottom_lines:
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
    time.sleep(0.75)

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


def DealCards(card, choices = None, is_player = False, is_dealer = False, back_card = None):
    if choices == None:
        choices = []

    if is_player:
        table.DealPlayerCard(card)
        if table.player_total > 21:
            Lose()
        elif table.player_total == 21 and len(table.player_cards) == 2:
            Win()

        choise = PrintTable(choices, table.dealer_cards, table.player_cards)
        return choise

    if is_dealer:
        if card == "back":
            table.DealDealerCard(back_card)
        else:            
            table.DealDealerCard(card)

        choise = PrintTable(choices, table.dealer_cards, table.player_cards)
        return choise


def Hit():
    choice = DealCards(deck.DealCard(), choices = ["hit", "stand"], is_player = True)
    return choice

def Win():
    table.Continue()

    curses.endwin()

    print("YOU WON!!!")
    print(f"Dealer: {table.dealer_cards}")
    print(f"Player: {table.player_cards}")

    sys.exit()

def Lose():
    table.Continue()

    curses.endwin()

    print("YOU LOST :(")
    print(f"Dealer: {table.dealer_cards}")
    print(f"Player: {table.player_cards}")

    sys.exit()

def PlayLoop():
    choice = 0
    
    #deal first card for dealer
    dealer_card = deck.DealCard()       
    table.ShowOrHide(False)
    DealCards("back", is_dealer = True, back_card = dealer_card)

    #deal first card for Player
    DealCards(deck.DealCard(), is_player = True)

    #deal second dealer card
    DealCards(deck.DealCard(), is_dealer = True)

    #deal second player Card
    choice = DealCards(deck.DealCard(), choices = ["hit", "stand"], is_player = True)

    while table.keep_going == True:
        if choice == 0:
            choice = Hit()

        elif choice == 1:
            table.ShowOrHide(True)
            
            if table.dealer_total >= 17:
                if table.dealer_total > 21:
                    Win()
                elif table.dealer_total >= table.player_total:
                    Lose()
            else:
                DealCards(deck.DealCard(), is_dealer = True)
            

        

PlayLoop()

#def on_press(key):
    #if hasattr(key, "char") and key.char == "q":
        #print(f"ended black jack with {player.chips or 0} chips")
        #sys.exit()

#with Listener(on_press=on_press) as listener:
    #listener.join()