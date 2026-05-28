from colorama import Fore, Back, Style, init
from textual.app import App
from textual.widgets import Label, Static
import random

# Initialize colorama (needed for Windows)
init(autoreset=True)

#♠♥♦♣
#print(Fore.RED + "This is red text")

class Deck():
    deck_of_cards = ['1♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠',
                     '1♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',
                     '1♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',
                     '1♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣']

    def __init__(self):
        self.cards = Deck.deck_of_cards
        self.dealt_cards = []
        random.shuffle(self.cards)

    def Shuffle(self):
        random.shuffle(self.cards)

    def DealCard(self):
        self.dealt_cards.append(self.cards[0])
        return self.cards.pop(0)

class Table(App):
    CSS_PATH = "styles.tcss"

    def compose(self):
        self.dealer = ['A♠', '6♣']
        self.player = ['7♣', '9♣']
        self.grid = [
            [Static("", classes="empty"), Static(self.dealer[0], classes="card"), Static(self.dealer[1], classes="card"), Static("", classes="empty")],
            [Static("", classes="empty"), Static(self.player[0], classes="card"), Static(self.player[1], classes="card"), Static("", classes="empty")]]
        for row in self.grid:
            for slot in row:
                yield slot
        
    def on_key(self, event):
        match event.key:
            case "q":
                exit()

if __name__ == "__main__":
    table = Table()
    table.run()

deck = Deck()
