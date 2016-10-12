"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    marker = 0
    merged_line = [0 for tile in line]
    
    # In order to look for a match, we need to hold the source somewhere
    # This variable gets reset after each match
    compare_tile = None
    
    for i in range(len(line)):
        # Ignoring zero's altogether
        if line[i] == 0:
            continue
        
        # If we don't have a source tile to compare to, we assign one
        if compare_tile is None:
            compare_tile = line[i]
            continue
        
        # If we find a match for the source tile, we sum both up, store
        # the sum in the merged line, then reset the source tile
        if line[i] == compare_tile:
            merged_line[marker] = line[i] + compare_tile
            marker += 1
            compare_tile = None
        else:
            # If we hit a different number before we hit a match,
            # we copy the value of the source tile to the merged line
            # and assign a new value for the source tile
            merged_line[marker] = compare_tile
            compare_tile = line[i]
            marker += 1
   
    # Finally, if we run out of tiles to compare to the source tile,
    # we simply copy it to the merged line
    if compare_tile is not None:
        merged_line[marker] = compare_tile
    
    return merged_line