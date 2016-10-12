"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 50         # Number of trials to run
SCORE_CURRENT = 2.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
# Add your functions here.

def mc_trial(board, player):
    """
    Takes a board and a player and plays out a full game through
    random moves, until there is a winner or it's a tie
    """
    
    # Keep going until someone wins or there is a draw
    while True:
        # Get the list of remaining empty squares (tuples)
        list_of_empty_squares = board.get_empty_squares()
        squares_remaining = len(list_of_empty_squares)
        
        # Choose one of the remaining empty squares at random
        square_tuple_idx = random.randint(0, squares_remaining-1)
        square_tuple = list_of_empty_squares[square_tuple_idx]
        
        # Current player makes a move to the chosen square
        board.move(square_tuple[0], square_tuple[1], player)
        
        # If someone wins or it's a tie, end game
        if board.check_win() is not None:
            break
            
        # Switch player
        if player == provided.PLAYERX:
            player = provided.PLAYERO
        else:
            player = provided.PLAYERX


def mc_update_scores(scores, board, player):
    """
    Takes a current board and a current player, then calculates scores
    by checking how many squares the current vs the other player occupies
    """
    if board.check_win() == provided.DRAW:
        mc_update_scores_helper(scores, board, player, 0, 0)
    elif board.check_win() == player:
        mc_update_scores_helper(scores, board, player, SCORE_CURRENT, -SCORE_OTHER)
    else:
        mc_update_scores_helper(scores, board, player, -SCORE_CURRENT, SCORE_OTHER)    
            
def mc_update_scores_helper(scores, board, player, current_score, other_score):
    """
    Takes a current board, a current player, and a score amount for 
    the current player, a score amount for the other player, then
    adds everything up to produce a score grid.
    """
    square = 0
    for dummy_i in range(0, len(scores)):
        for dummy_j in range(0, len(scores)):
            square = board.square(dummy_i, dummy_j)
            if square == provided.EMPTY:
                continue
            elif square == player:
                scores[dummy_i][dummy_j] += current_score
            else:
                scores[dummy_i][dummy_j] += other_score

def get_best_move(board, scores):
    """
    Takes a current board and current scores (from multiple MC trials)
    and figures out a best next move. 
    """
    empty_squares_list = board.get_empty_squares()
    if len(empty_squares_list) == 0:
        return
    squares_scores_list = []
    for empty_square in empty_squares_list:
        square_score_tuple = (empty_square[0], empty_square[1], 
                              scores[empty_square[0]][empty_square[1]])
        squares_scores_list.append(square_score_tuple)
    # print(squares_scores_list)
    highest_score_square = sorted(squares_scores_list, key=lambda x: x[2], reverse = True)[0]
    return (highest_score_square[0], highest_score_square[1])

def mc_move(board, player, trials):
    """
    Takes a current board and a current player, and figures out which 
    next move to make by running a number of MC trials, and updating 
    the score grid after each one.
    """
    dim = board.get_dim()
    scores = reset_scores(dim)
    for dummy_i in range(0, trials):
        board_copy = board.clone()
        mc_trial(board_copy, player)
        mc_update_scores(scores, board_copy, player)
    next_move = get_best_move(board, scores)
    return next_move

def print_scores(scores):
    """
    Prints scores in a readable format
    """
    for dummy_row in scores:
        print(dummy_row)

def reset_scores(dim):
    """
    Reset score grid to 0's
    """
    scores = [[0 for dummy_idx in range(0, dim)] for dummy_idx2 in range(0, dim)]
    return scores
        
def print_winner(board):
    """
    Print winning player
    """
    if board.check_win() == provided.PLAYERX:
        print('Player X wins!')
    elif board.check_win() == provided.PLAYERO:
        print('Player O wins!')
    else:
        print('It\'s a draw!')

def print_turn_info(player, squares_left):
    """
    Print some information about the current turn
    """
    if player == provided.PLAYERX:
        print('Game is in progress. Player X\'s turn.. ')
    else:
        print('Game is in progress. Player O\'s turn.')
    print('There are %d squares remaining.\n' % squares_left)

def simulate_game(dim):
    """
    Function for simulating a console game
    """
    board = provided.TTTBoard(dim)
    print(board)

    player = provided.PLAYERX
    while True:
        next_move = mc_move(board, player, 10)
        print('Next move: (%d, %d)' % (next_move[0], next_move[1]))
        board.move(next_move[0], next_move[1], player)
        print(board)
         # If someone wins or it's a tie, end game
        if board.check_win() is not None:
            break

        # Switch player
        if player == provided.PLAYERX:
            player = provided.PLAYERO
        else:
            player = provided.PLAYERX

    print_winner(board)
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
# simulate_game(3)
provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
