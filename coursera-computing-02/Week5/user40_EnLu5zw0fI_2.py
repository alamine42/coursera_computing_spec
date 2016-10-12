# implementation of card game - Memory

import simplegui
import random

# Initialize game variables
all_cards = []
exposed = []
turns = 0

# Indices to keep track of last two selected cards
selected_idx_1 = None
selected_idx_2 = None

# helper function to initialize globals
def new_game():
    global all_cards, exposed, state, turns
    state = 0
    turns = 0
    label.set_text('Turn=' + str(turns))
    
    # Generate new deck of cards and shuffle it
    first_7_cards = range(8)
    second_7_cards = range(8)
    all_cards = first_7_cards + second_7_cards
    random.shuffle(all_cards)
    
    # Reset the exposed list
    exposed = [False for i in range(16)]
    
# define event handlers
def mouseclick(pos):
    global exposed, state, selected_idx_1, selected_idx_2, turns
    global label
    
    card_selected = pos[0] // 50
    if not exposed[card_selected]:
        exposed[card_selected] = True
    
        if state == 0:
            state = 1
            selected_idx_1 = card_selected
        elif state == 1:
            state = 2
            selected_idx_2 = card_selected
            turns += 1
            label.set_text('Turn=' + str(turns))
        else:
            state = 1
            
            if all_cards[selected_idx_1] != all_cards[selected_idx_2]:
                exposed[selected_idx_1] = False
                exposed[selected_idx_2] = False
                
            selected_idx_1 = card_selected
            selected_idx_2 = None
                            
# cards are logically 50x100 pixels in size    
def draw(canvas):

    card_center = [15, 55]
    cover_center = [25, 50]
    
    for idx, card in enumerate(all_cards):
        if exposed[idx]:
            canvas.draw_text(str(card), card_center, 32, 'White')
        else:
            canvas.draw_polygon(
                [[cover_center[0] - 25, cover_center[1] - 50], 
                 [cover_center[0] + 25, cover_center[1] - 50], 
                 [cover_center[0] + 25, cover_center[1] + 50], 
                 [cover_center[0] - 25, cover_center[1] + 50]], 
                                1, 'Yellow', 'Green')

        card_center[0] += 50
        cover_center[0] += 50


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric