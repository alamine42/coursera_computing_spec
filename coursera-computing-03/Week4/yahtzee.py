"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_all_orderings(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                if item not in new_sequence:
                    new_sequence.append(item)
                new_sequence.sort()
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def convert_ordering_to_hand(ordering, hand):
    """
    This function takes a list of indices (or hand dice positions) and turns
    them into a list of dice values (ordered)
    """
    order = list(ordering)
    hand_selection = [hand[dummy_idx] for dummy_idx in order]
    return tuple(hand_selection)

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    max_score = 0
    for possible_score in [1, 2, 3, 4, 5, 6, 7, 8]:
        occurences = hand.count(possible_score)
        new_score = occurences * possible_score
        if new_score > max_score:
            max_score = new_score
        
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    die_outcomes = range(1, num_die_sides + 1)
    all_seqs = gen_all_sequences(die_outcomes, num_free_dice)

    total_scores = 0
    for seq in list(all_seqs):
        seq_score = score(list(seq) + list(held_dice))
        total_scores += seq_score

    return total_scores / float(len(all_seqs))

def sort_holds(holds, max_hold_length):
    """
    Takes a list of holds and returns them sorted by size increasing
    """
    sorted_holds = []
    for hold_length in range(0, max_hold_length+1):
        for hold in holds:
            if len(hold) == hold_length:
                sorted_holds.append(hold)
    return sorted_holds


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    hand_length = len(hand)
    print('Length of hand is %d' % hand_length)
    all_holds = [()]
    for ordering in gen_all_orderings(range(0, hand_length), hand_length):
        all_holds.append(convert_ordering_to_hand(ordering, hand))

    # all_holds.sort(key=lambda h: len(h))
    sorted_holds = sort_holds(all_holds, hand_length)
    return set(sorted_holds)



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    max_expected_value = 0
    best_hold = ()
    
    for possible_hold in gen_all_holds(hand):
        num_free_dice = len(hand) - len(possible_hold)
        possible_hold_exp_val = expected_value(possible_hold, num_die_sides, num_free_dice)
        if possible_hold_exp_val > max_expected_value:
            max_expected_value = possible_hold_exp_val
            best_hold = possible_hold
            
    return (max_expected_value, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 8
    hand = (3, 3)
    
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    

