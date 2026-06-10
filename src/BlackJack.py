from colorama import Fore, Back, Style, init
import random
import time
import os
import curses
import sys
import numbers
import keyboard

# Initialize colorama (needed for Windows)
init(autoreset=True)

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

    def Reset(self):
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
        if self.dealer_total > 21 and any(card[:-1] == "A" for card in self.dealer_cards) and self.dealer_aces < sum(1 for card in self.dealer_cards if "A" in card):
            self.dealer_total -= 10
            self.dealer_aces += 1


    def DealPlayerCard(self, card):
        self.player_cards.append(card)

        non_number = "KJQ"
        if card[:-1] in non_number:
            self.player_total += 10
        elif card[:-1] == "A":
            self.player_total += 11          
        else:
            self.player_total += int(card[:-1])
        if self.player_total > 21 and any(card[:-1] == "A" for card in self.player_cards) and self.player_aces < sum(1 for card in self.player_cards if "A" in card):
            self.player_total -= 10
            self.player_aces += 1

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

    def NewDeck(self):
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

def menu(title, options, top_cards=None, bottom_cards=None, color="white"):
    Clear()
    new_top_cards = [card for card in top_cards]
    new_bottom_cards = [card for card in bottom_cards]
    choice = 0

    if table.dealer_card_hidden:
        new_top_cards[0] = "back"

    if len(options) == 0:
        top_lines = CardsToLines(new_top_cards, [], 0)
        bottom_lines = CardsToLines([], new_bottom_cards, 0)                
        

        #add dealer header
        dealer_cards = [card[:-1] for card in table.dealer_cards]
        dealer_value = ""
        if table.dealer_card_hidden:
            dealer_cards[0] = "?"
            dealer_value = " + ".join(dealer_cards)
        else:
            dealer_value = " + ".join(dealer_cards) + " = " + str(table.dealer_total)

        print(f"Dealer ({dealer_value}):")

        for line in top_lines:
            print(f"{line}")

        #print("\n")


        #add player header
        player_cards = [card[:-1] for card in table.player_cards]
        player_value = " + ".join(player_cards) + " = " + str(table.player_total)

        print(f"Player ({player_value}):")

        for line in bottom_lines:
            print(f"{line}")

        time.sleep(0.75)
        return choice

    else:
        selected = 0
        while True:
            #time.sleep(0.75)
            
            top_lines = CardsToLines(new_top_cards, [], 0)
            bottom_lines = CardsToLines([], new_bottom_cards, 0)                
        

            #calculate dealer total
            dealer_cards = [card[:-1] for card in table.dealer_cards]
            dealer_value = ""
            if table.dealer_card_hidden:
                dealer_cards[0] = "?"
                dealer_value = " + ".join(dealer_cards)
            else:
                dealer_value = " + ".join(dealer_cards) + " = " + str(table.dealer_total)

            #calculate player total
            player_cards = [card[:-1] for card in table.player_cards]
            player_value = " + ".join(player_cards) + " = " + str(table.player_total)

            #print dealer total and cards
            Clear()
            print(f"Dealer ({dealer_value}):")

            for line in top_lines:
                print(f"{line}")

            #print player total and cards
            print(f"Dealer ({player_value}):")

            for line in bottom_lines:
                print(f"{line}")

            
            #print actions options and header
            print(title)

            for i in range(len(options)):
                if i == selected:
                    print(Fore.GREEN + f"   {options[i]}\n")
                else:
                    print(f"   {options[i]}\n")


            #check for option
            while True:
                if keyboard.is_pressed('down'):
                    if selected < len(options) - 1:
                        selected += 1
                        break
                elif keyboard.is_pressed('up'):
                    if selected > 0:
                        selected -= 1
                        break
                elif keyboard.is_pressed('enter'):
                    time.sleep(0.25)
                    return selected
                


def PrintTable(title, options, cards_top, cards_bottom):
    choice = menu(
        title,
        options,
        top_cards=cards_top,
        bottom_cards=cards_bottom,
        color="green"
    )
    return choice

def DealCards(card, choices = None, is_player = False, is_dealer = False, back_card = None):
    if choices == None:
        choices = []

    if is_player:
        table.DealPlayerCard(card)
        if table.player_total > 21:
            Lose()
            return
        elif table.player_total == 21 and len(table.player_cards) == 2:
            Win()
            return

        choice = PrintTable("blackJack", choices, table.dealer_cards, table.player_cards)
        return choice

    if is_dealer:
        if card == "back":
            table.DealDealerCard(back_card)
        else:            
            table.DealDealerCard(card)

        choice = PrintTable("BlackJack", choices, table.dealer_cards, table.player_cards)
        return choice

def Restart(new_deck):
    Clear()
    if new_deck:
        deck.NewDeck()
    
    table.Reset()
    return
    

def Hit():
    choice = DealCards(deck.DealCard(), choices = ["hit", "stand"], is_player = True)
    return choice

def Win():
    table.Continue()

    choice = PrintTable("You won!", ["Another game", "Quit"], table.dealer_cards, table.player_cards)

    if choice == 0:
        Restart(len(deck.cards) <= 26)
        table.keep_going = False
        return "Restart"

    elif choice == 1:
        return "Quit"

def Lose():
    table.Continue()

    choice = PrintTable("You lost", ["Another game", "Quit"], table.dealer_cards, table.player_cards)

    if choice == 0:
        Restart(len(deck.cards) <= 26)
        table.keep_going = False
        return "Restart"

    elif choice == 1:
        return "Quit"

def PlayLoop():
    table.Reset()
    
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
            PrintTable("BlackJack", [], table.dealer_cards, table.player_cards)
            time.sleep(0.75)
            
            while True:
                if table.dealer_total >= 17:
                    break
                DealCards(deck.DealCard(), is_dealer=True)

            if table.dealer_total > 21:
                Win()
            elif table.dealer_total >= table.player_total:
                return Lose()
            else:
                return Win()
    return "Restart"

#with Listener(on_release=on_press) as listener:
    #listener.join()

while True:
    result = PlayLoop()

    if result == "Restart":
        continue
    elif result == "Quit":
        break