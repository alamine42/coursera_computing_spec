# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui, random, math

secret_number = 1000
secret_range = 100
remaining_guesses = 1

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global secret_range
    global remaining_guesses
    
    print ''
    print 'New game with range [0, ' + str(secret_range) +')'
    
    # Compute the max number of allowed guesses
    remaining_guesses = int(math.ceil(math.log(secret_range, 2)))
    print 'You are allowed ' + str(remaining_guesses) + ' guesses.'

    secret_number = random.randint(0, secret_range - 1)
    
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global secret_range
    secret_range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_range
    secret_range = 1000
    new_game()

def decrement_guesses():
    global remaining_guesses
    remaining_guesses -= 1
    if remaining_guesses > 0:
        print 'You have ' + str(remaining_guesses) + ' guesses remaining.'
    else:
        print 'You have 0 guesses remaining. You lost.'
    
def input_guess(guess):
    # main game logic goes here	
    print ''
    print 'Guess was ' + guess
    guess_num = int(guess)
    
    if remaining_guesses > 0:
        if guess_num < secret_number:
            print 'Higher'
            decrement_guesses()
        elif guess_num > secret_number:
            print 'Lower'
            decrement_guesses()
        else:
            print 'Correct'
            new_game()
            
    else:
        print 'You are not allowed any more guesses!'
        print 'Please start a new game.'

    
# create frame
frame = simplegui.create_frame("Guess the number", 300, 300)

# register event handlers for control elements and start frame
inp_guess = frame.add_input('Guess', input_guess, 50)
button_100 = frame.add_button('Range [0, 100)', range100, 100)
button_1000 = frame.add_button('Range [0, 1000)', range1000, 100)

frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric

