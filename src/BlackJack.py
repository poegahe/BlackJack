from colorama import Fore, Back, Style, init
import random
import time
import os
import sys
import numbers
import keyboard
import msvcrt

#systeem functies to clear terminal buffer
def clear_buffer():
    while msvcrt.kbhit():
        msvcrt.getch()

def Clear():
    os.system("cls" if os.name == "nt" else "clear")

def Debug(msg):
    with open("debug.txt", "a", encoding="utf-8") as f:
        f.write(str(msg) + "\n")

clear_buffer()

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
        self.cards = [card for card in Deck.deck_of_cards]
        self.dealt_cards = []
        random.shuffle(self.cards)

    def NewDeck(self):
        self.cards = [card for card in Deck.deck_of_cards]
        self.dealt_cards = []
        random.shuffle(self.cards)

    def Shuffle(self):
        random.shuffle(self.cards)

    def DealCard(self):
        self.dealt_cards.append(self.cards[0])
        return self.cards.pop(0)

class Player():
    def __init__(self, starting_chips = 250):
        self.chips = starting_chips
        self.bet_amount = 0
        self.hands_played = 0
        self.hands_won = 0
        self.hands_lost = 0

    def SetBetAmount(self, amount):
        self.bet_amount = amount

    def Lose(self):
        self.chips -= self.bet_amount
        self.bet_amount = 0

    def Win(self):
        self.chips += self.bet_amount
        self.bet_amount = 0

#initalizeer de classes
table = Table()
deck = Deck()
deck.Shuffle()
player = Player()

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

def CardsToLines(top_cards, bottom_cards):

    def build_row(cards):
        if not cards:
            return []

        card_lists = [Card(card) for card in cards]

        lines = []
        for i in range(7):
            line = "  ".join(card[i] for card in card_lists)
            lines.append(line)

        return lines

    lines = []

    # boven
    lines += build_row(top_cards)
    lines.append("")

    # onder
    lines += build_row(bottom_cards)

    return lines

def menu(title=None, options=None, top_cards=None, bottom_cards=None, color="white", strings=[]):
    Clear()
    choice = 0

    if top_cards == None and bottom_cards == None and len(strings) > 0:
        if not options == None:
            selected = 0
            while True:
                Clear()
                for string in strings:
                    print(string)

                print("")

                #print actions options and header
                print(title)

                for i in range(len(options)):
                    if i == selected:
                        print(Fore.GREEN + f"   {options[i]}\n")
                    else:
                        print(f"   {options[i]}\n")

                time.sleep(0.2)
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
        else:
            for string in strings:
                print(string)
            time.sleep(2)
            return 0    
    
    #initialize variables for the cards
    new_top_cards = [card for card in top_cards]
    new_bottom_cards = [card for card in bottom_cards]

    #check if the dealer still has his card upside down
    if table.dealer_card_hidden:
        new_top_cards[0] = "back"

    #if there are no options print the table and return 0
    if len(options) == 0:
        top_lines = CardsToLines(new_top_cards, [])
        bottom_lines = CardsToLines([], new_bottom_cards)                
        
        print("|||||||||||||||||||||||")
        print(f" U have {player.chips} chips")
        print(f" Current amount you bet is {player.bet_amount} chips")
        print("|||||||||||||||||||||||")

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
            top_lines = CardsToLines(new_top_cards, [])
            bottom_lines = CardsToLines([], new_bottom_cards)                

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

            Clear()
            print("|||||||||||||||||||||||")
            print(f" U have {player.chips} chips")
            print(f" Current amount you bet is {player.bet_amount} chips")
            print("|||||||||||||||||||||||")

            #print dealer total and cards          
            print(f"Dealer ({dealer_value}):")

            for line in top_lines:
                print(f"{line}")

            #print player total and cards
            print(f"Player ({player_value}):")

            for line in bottom_lines:
                print(f"{line}")
            
            #print actions options and header
            print(title)

            for i in range(len(options)):
                if i == selected:
                    print(Fore.GREEN + f"   {options[i]}\n")
                else:
                    print(f"   {options[i]}\n")

            time.sleep(0.2)
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
                
def PrintTable(title, options, top_cards, bottom_cards):
    choice = menu(
        title = title,
        options = options,
        top_cards = top_cards,
        bottom_cards = bottom_cards,
        color="green"
    )
    return choice

def PrintChipsBetting():
    amount = 0
    while True:
        Clear()
        choice = menu(
            title = "Choose how much you want to bet",
            options = ["bet 25", "bet 50", "bet 100", "bet 250", "bet custom amount"],
            strings = ["|||||||||||||||||||||||", f" You have {player.chips} chips", "|||||||||||||||||||||||"]
        )   
        print("")
        if choice == 0:
            player.SetBetAmount(25)
            return 25
        elif choice == 1:
            if player.chips < 50:
                print("you dont have enough chips")
                time.sleep(1)
                continue
            player.SetBetAmount(50)
            return 50
        elif choice == 2:
            if player.chips < 100:
                print("you dont have enough chips")
                time.sleep(1)
                continue
            player.SetBetAmount(100)
            return 100
        elif choice == 3:
            if player.chips < 250:
                print("you dont have enough chips")
                time.sleep(1)
                continue
            player.SetBetAmount(250)
            return 250
        else:       
            clear_buffer()
            amount = input("Choose how much you want to bet: ")
            if int(amount) > player.chips:
                print("You dont have that mutch chips, please choose again")
                continue
            elif not int(amount) % 25 == 0:
                print("You must bet a amount in increments of 25, please choose again")
                continue
            else:
                player.SetBetAmount(int(amount))
                return int(amount)

def Restart(new_deck):
    Clear()
    if new_deck:
        deck.NewDeck()
    
    table.Reset()
    return

def Win():
    table.Continue()

    choice = PrintTable(f"You won {player.bet_amount} chips \nYour new balance is {player.chips + player.bet_amount} chips", ["Another game", "Quit"], table.dealer_cards, table.player_cards)
    player.Win()

    if choice == 0:
        Restart(len(deck.cards) <= 26)
        #table.keep_going = False
        return "Restart"

    elif choice == 1:
        return "Quit"

def Lose():
    table.Continue()

    choice = PrintTable(f"You lost {player.bet_amount} chips \nYour new balance is {player.chips - player.bet_amount} chips", ["Another game", "Quit"], table.dealer_cards, table.player_cards)
    player.Lose()

    if choice == 0:
        Restart(len(deck.cards) <= 26)
        #table.keep_going = False
        return "Restart"

    elif choice == 1:
        return "Quit"

def PlayLoop():
    if getattr(PlayLoop, "has_run", True):
        #run only once
        PlayLoop.has_run = False
    
    bet_amount = PrintChipsBetting()

    #deal first card for dealer
    table.DealDealerCard(deck.DealCard())     
    table.ShowOrHide(False)
    choice = PrintTable("BlackJack", [], table.dealer_cards, table.player_cards)

    #deal first card for Player
    table.DealPlayerCard(deck.DealCard()) 
    choice = PrintTable("BlackJack", [], table.dealer_cards, table.player_cards)

    #deal second dealer card
    table.DealDealerCard(deck.DealCard())
    choice = PrintTable("BlackJack", [], table.dealer_cards, table.player_cards)

    #deal second player Card
    table.DealPlayerCard(deck.DealCard()) 
    if table.player_total == 21:
        return Win()

    choice = PrintTable("BlackJack", ["hit", "stand", "double"], table.dealer_cards, table.player_cards)

    while table.keep_going == True:
        #if player chooses hit
        if choice == 0:
            table.DealPlayerCard(deck.DealCard()) 

            if table.player_total > 21:
                return Lose()

            choice = PrintTable("BlackJack", ["hit", "stand", "double"], table.dealer_cards, table.player_cards)

        #if player chooses stand
        elif choice == 1:
            table.ShowOrHide(True)
            PrintTable("BlackJack", [], table.dealer_cards, table.player_cards)
            time.sleep(0.75)
            
            while True:
                if table.dealer_total >= 17:
                    break
                table.DealDealerCard(deck.DealCard()) 
                PrintTable("BlackJack", [], table.dealer_cards, table.player_cards)

            if table.dealer_total > 21:
                return Win()
            elif table.dealer_total >= table.player_total:
                return Lose()
            else:
                return Win()

        #if player chooses to double
        elif choice == 2:
            if player.chips < player.bet_amount * 2:
                print("You dont have enough chips to do this")
                choice = PrintTable("BlackJack", ["hit", "stand", "double"], table.dealer_cards, table.player_cards)
                continue

            player.SetBetAmount(player.bet_amount * 2)
            table.DealPlayerCard(deck.DealCard())
            PrintTable("BlackJack", [], table.dealer_cards, table.player_cards)
            choice = 1
            continue

while True:
    result = PlayLoop()

    if result == "Restart":
        continue
    elif result == "Quit":
        break
    else:
        break

clear_buffer()