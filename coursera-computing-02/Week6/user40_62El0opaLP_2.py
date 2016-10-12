# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# Initialize Player and Dealer's hands, as well as deck
GAME_DECK = None
PLAYER_HAND = None
DEALER_HAND = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        msg = 'Hand contains: '
        for c in self.cards:
            msg += str(c) + ' '
        return msg
    
    def __len__(self):
        return len(self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        hand_value = 0
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        for card in self.cards:
            card_rank = card.get_rank()
            if card_rank == 'A':
                if hand_value + 11 > 21:
                    hand_value += 1
                else:
                    hand_value += 11
            else:
                hand_value += VALUES[card_rank]
                
        return hand_value
   
    def draw(self, canvas, pos):
        for idx, card in enumerate(self.cards):
            pos[0] += CARD_SIZE[0]
            card.draw(canvas, pos)
            if idx >= 4:
                break
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.all_cards = []
        
        for suit in SUITS:
            for rank in RANKS:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.all_cards)

    def deal_card(self):
        card_dealt = self.all_cards.pop()
        return card_dealt
    
    def __str__(self):
        msg = 'Deck contains '
        for c in self.all_cards:
            msg += str(c) + ' '
        return msg



#define event handlers for buttons
def deal():
    global outcome, in_play, score
    global GAME_DECK, PLAYER_HAND, DEALER_HAND
        
    if in_play and (len(PLAYER_HAND) > 2 or len(DEALER_HAND) > 2):
        score -= 1
        outcome = 'You busted'
    else:
        in_play = True
        outcome = 'Hit or Stand?'
        
    GAME_DECK = Deck()
    GAME_DECK.shuffle()
    
    # Initialize the Player and Dealer hands
    PLAYER_HAND = Hand()
    DEALER_HAND = Hand()
    
    # Deal one card to Player
    PLAYER_HAND.add_card(GAME_DECK.deal_card())
    # Deal one card to Dealer
    DEALER_HAND.add_card(GAME_DECK.deal_card())
    # Deal one card to Player
    PLAYER_HAND.add_card(GAME_DECK.deal_card())
    # Deal one card to Dealer
    DEALER_HAND.add_card(GAME_DECK.deal_card())

def hit():
    global outcome, in_play, score
    global GAME_DECK, PLAYER_HAND, DEALER_HAND
    
    # if the hand is in play, hit the player
    if in_play:
        PLAYER_HAND.add_card(GAME_DECK.deal_card())
        
        if PLAYER_HAND.get_value() > 21:
            outcome = "You have busted. New deal?"
            in_play = False
            score -= 1
    
def stand():
    global outcome, in_play, score
    global GAME_DECK, PLAYER_HAND, DEALER_HAND
    
    if in_play:
        if DEALER_HAND.get_value() >= 17:
            outcome = 'Dealer busts'
            score += 1
            in_play = False
        else:
            while DEALER_HAND.get_value() < 17:
                DEALER_HAND.add_card(GAME_DECK.deal_card())
                if DEALER_HAND.get_value() >= 17:
                    outcome = "Dealer busts"
                    score += 1
                    in_play = False
                elif DEALER_HAND.get_value() >= PLAYER_HAND.get_value():
                    outcome = "Dealer wins"
                    score -= 1
                    in_play = False             

# draw handler    
def draw(canvas):
    canvas.draw_text('Blackjack', (200,50), 48, 'Black')
    canvas.draw_text('Player', (20, 150), 20, 'Black')
    canvas.draw_text('Dealer', (20, 350), 20, 'Black')
    canvas.draw_text(outcome, (100,500), 32, 'Black')
    # test to make sure that card.draw works, replace with your code below
    PLAYER_HAND.draw(canvas, [25, 100])
    DEALER_HAND.draw(canvas, [25, 300])
    canvas.draw_text('Score: ' + str(score), (450, 70), 32, 'Black')
    
    if in_play:
        canvas.draw_image(card_back, 
                      [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], 
                      CARD_BACK_SIZE, 
                      [25 + CARD_BACK_SIZE[0] + CARD_BACK_CENTER[0], 300 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
