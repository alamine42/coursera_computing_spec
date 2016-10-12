"""
Clone of 2048 game.
"""
# import standard modules
import random

import poc_2048_gui
# import test_suite

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code
    marker = 0
    merged_line = [0 for dummy_tile in line]
    
    # In order to look for a match, we need to hold the source somewhere
    # This variable gets reset after each match
    compare_tile = None
    
    for idx in range(len(line)):
        # Ignoring zero's altogether
        if line[idx] == 0:
            continue
        
        # If we don't have a source tile to compare to, we assign one
        if compare_tile is None:
            compare_tile = line[idx]
            continue
        
        # If we find a match for the source tile, we sum both up, store
        # the sum in the merged line, then reset the source tile
        if line[idx] == compare_tile:
            merged_line[marker] = line[idx] + compare_tile
            marker += 1
            compare_tile = None
        else:
            # If we hit a different number before we hit a match,
            # we copy the value of the source tile to the merged line
            # and assign a new value for the source tile
            merged_line[marker] = compare_tile
            compare_tile = line[idx]
            marker += 1
   
    # Finally, if we run out of tiles to compare to the source tile,
    # we simply copy it to the merged line
    if compare_tile is not None:
        merged_line[marker] = compare_tile
    
    return merged_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._initial_tile_dict = {}
        self.reset()
        self.setup_inital_tile_dict()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[ 0 for dummy_col in range(self._grid_width) ] \
                     for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def setup_inital_tile_dict(self):
        """
        Figure out the indices for the initial tiles in each direction,
        and store them in a dictionary.
        """
        self._initial_tile_dict[UP] = [(0, col) for col in range(self._grid_width)]
        self._initial_tile_dict[DOWN] = [(self._grid_height - 1, col) for col in range(self._grid_width)]

        self._initial_tile_dict[LEFT] = [(row, 0) for row in range(self._grid_height)]
        self._initial_tile_dict[RIGHT] = [(row, self._grid_width - 1) for row in range(self._grid_height)]

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_str = ''
        for row in self._grid:
            for col in row:
                cell_val = str(col) if col != 0 else ' '
                grid_str = grid_str + cell_val + ' , '
            grid_str = grid_str[:-2] + '\n\n'
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        tile_moved = False
        # For each initial tile, iterate through the list of tiles that
        # starts with that initial tile and goes in the opposite of the
        # direction specified
        for initial_tile in self._initial_tile_dict[direction]:
            list_to_merge = []
            merged_list = []

            row_idx, col_idx = initial_tile[0], initial_tile[1]
            list_to_merge.append(self._grid[row_idx][col_idx])
            # This allows us to calculate how many items will be in our merge list
            steps = abs(OFFSETS[direction][0]*self._grid_height + OFFSETS[direction][1]*self._grid_width)
            for dummy_counter in range(1, steps):
                row_idx = row_idx + OFFSETS[direction][0]
                col_idx = col_idx + OFFSETS[direction][1]
                list_to_merge.append(self._grid[row_idx][col_idx])

            merged_list = merge(list_to_merge)

            row_idx, col_idx = initial_tile[0], initial_tile[1]
            self._grid[row_idx][col_idx] = merged_list[0]
            for dummy_counter in range(1, steps):
                row_idx = row_idx + OFFSETS[direction][0]
                col_idx = col_idx + OFFSETS[direction][1]
                if self._grid[row_idx][col_idx] != merged_list[dummy_counter]:
                    tile_moved = True
                self._grid[row_idx][col_idx] = merged_list[dummy_counter]

        if tile_moved:
            self.new_tile()


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        row = random.randint(0, self._grid_height - 1)
        col = random.randint(0, self._grid_width - 1)
        while self._grid[row][col] != 0:
            row = random.randint(0, self._grid_height - 1)
            col = random.randint(0, self._grid_width - 1)
        
        tile_val = 2 if random.randint(0, 9) != 4 else 4
        self._grid[row][col] = tile_val

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

# new_game = TwentyFortyEight(5, 4)
# test_suite.run_suite(new_game, 5, 4)
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
