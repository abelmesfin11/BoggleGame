from bogglecube import BoggleCube
from gambler import Shuffler, PredictableShuffler, SixSidedDie, PredictableDie

# The sixteen letter cubes provided with the standard game of Boggle.
CUBE_FACES = [("A", "A", "C", "I", "O", "T"),  # cube 0
              ("T", "Y", "A", "B", "I", "L"),  # cube 1
              ("J", "M", "O", "Qu", "A", "B"), # cube 2
              ("A", "C", "D", "E", "M", "P"),  # cube 3
              ("A", "C", "E", "L", "S", "R"),  # cube 4
              ("A", "D", "E", "N", "V", "Z"),  # cube 5
              ("A", "H", "M", "O", "R", "S"),  # cube 6
              ("B", "F", "I", "O", "R", "X"),  # cube 7
              ("D", "E", "N", "O", "S", "W"),  # cube 8
              ("D", "K", "N", "O", "T", "U"),  # cube 9
              ("E", "E", "F", "H", "I", "Y"),  # cube 10
              ("E", "G", "I", "N", "T", "V"),  # cube 11
              ("E", "G", "K", "L", "U", "Y"),  # cube 12
              ("E", "H", "I", "N", "P", "S"),  # cube 13
              ("E", "L", "P", "S", "T", "U"),  # cube 14
              ("G", "I", "L", "R", "U", "W")]  # cube 15
    
class BoggleBoard:
    """A BoggleBoard represents a 4x4 grid of BoggleCube objects."""
    
    def __init__(self, lexicon):
        """Initializes a new BoggleBoard.
        
        Parameters
        ----------
        lexicon : set[str]
            The set of valid Boggle words.
        """
        self._lexicon = lexicon
        
        self._cubes = [] 
        for i in range(len(CUBE_FACES)):
            cube = BoggleCube(i, CUBE_FACES[i], board=self)
            self._cubes.append(cube)

        self._grid_dict = {} # Relates cube_id with row,col
        self._change_grid(self._cubes)
        self._selected_cubes = []
        self._found = [] # list of words that are in lexicon
               
    def get_cube(self, row, col):
        """Returns the BoggleCube currently at the specified row and column.
        
        Parameters
        ----------
        row : int
            The desired row (should be between 0 and 3)
        col : int
            The desired column (should be between 0 and 3)
        
        Returns
        -------
        BoggleCube
            the cube currently at the specified row and column.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.get_cube(0, 0).get_letter()
        'A'
        >>> board.get_cube(3, 3).get_letter()
        'G'
        """
        return self._cubes[row * 4 + col] 
    
    def _change_grid(self, c_list):
        """ Resets the grid. We have cube_id as key and row, column as value """
        for row in range(4):
            for col in range(4):
                cube = self.get_cube(row, col)
                self._grid_dict[cube.get_id()] = (row, col)
           
    def shake_cubes(self, shuffler=Shuffler(), die=SixSidedDie()):
        """Shakes the cubes.
        
        First, the cubes should be shuffled by the provided Shuffler.
        Then, each cube should be independently rolled using the provided SixSidedDie.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.get_cube(0, 0).get_letter()
        'U'
        >>> board.get_cube(1, 2).get_letter()
        'T'
        """
        self._cubes = shuffler.shuffle(self._cubes) # list of cubes are shuffled first
        for c in self._cubes: # every cube is rolled
            c.roll(die)
        self._change_grid(self._cubes) # updates the dictionary

    def adjacent(self, cube1, cube2):
        """Determines whether two cubes are adjacent.
        
        Two cubes are adjacent if they are vertically, horizontally, or diagonally adjacent.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.adjacent(board.get_cube(1, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(1, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 2), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 2), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(1, 2), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(3, 2), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(2, 0), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(3, 1), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(2, 0), board.get_cube(0, 1))
        False
        """   
        row1, col1 = self._grid_dict[cube1.get_id()]
        row2, col2 = self._grid_dict[cube2.get_id()]

        if row1 == row2 and col1 == col2: # cube is not adjacent to itself
            return False
        if abs(row1 - row2) > 1 or abs(col1 - col2) > 1:
            return False
        return True
     


    #$need to reset word so far so that previous letters aren't kept


    def unselect_all(self):
        """Sets the status of all cubes to 'unselected'.
        
        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.get_cube(0, 0).set_status("selected")
        >>> board.get_cube(2, 3).set_status("selected")
        >>> board.unselect_all()
        >>> board.get_cube(0, 0).get_status()
        'unselected'
        >>> board.get_cube(2, 3).get_status()
        'unselected'
        """        
        for cube in self._cubes:
            cube.set_status('unselected')

    def _submit_word(self, word):
        """ Updates board when a word is submitted """
        if word not in self._found and word in self._lexicon: # word shouldn't be repeated and must be in lexicon
            self._found.append(word)
        self._selected_cubes = [] 
        self.unselect_all() # resets the board

    def _previous_cube(self):
        """ Returns the most recently selected cube if selected cubes is not empty """
        if self._selected_cubes:
            return self._selected_cubes[-1]
        
    def _select_cube(self, current, previous=None):
        """ Updates the state of the board and cube when selected """
        if previous is not None:
            previous.set_status('selected')
        current.set_status('most recently selected')
        self._selected_cubes.append(current)
   
#$need to check whether cube has already been selected!


    def report_selection(self, cube_id):
        """Reports that the cube with the specified id has been selected by the player.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        >>> board = BoggleBoard({'GET', 'PUT', 'APT'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.report_selection(13)
        >>> board.report_selection(12)
        >>> board.report_selection(9)
        >>> board.get_word_so_far()
        'PUT'
        >>> board.report_selection(9)
        >>> board.get_completed_words()
        ['PUT']
        >>> board.get_word_so_far()
        ''
        >>> board.report_selection(13)
        >>> board.report_selection(12)
        >>> board.report_selection(11)
        >>> board.get_word_so_far()
        'PU'
        >>> board.report_selection(12)
        >>> board.get_completed_words()
        ['PUT']
        >>> board.get_word_so_far()
        ''
        """
        row, col = self._grid_dict[cube_id]
        current = self.get_cube(row,col)
        previous = self._previous_cube()
        
        if not previous or self.adjacent(current, previous): # cube selected for the first time or is adjacent
            self._select_cube(current, previous)
        elif current == previous: # same cube selected twice in a row and therefore word is submitted 
            self._submit_word(self.get_word_so_far())
 
    def get_completed_words(self):
        """Returns the list of completed words.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        See doctests for `report_selection` to get an example of the intended behavior.
        """
        return self._found

    def get_word_so_far(self):
        """Returns the word corresponding to the letters selected so far.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        See doctests for `report_selection` to get an example of the intended behavior.
        
        """
        word = ""
        for cube in self._selected_cubes:
            word += cube.get_letter()
        return word
        
    def __str__(self):
        """A string representation of the BoggleBoard."""
        row_strs = []
        for row in range(4):
            column = [str(self.get_cube(row, col)) for col in range(4)]
            row_strs.append(' '.join(column))
        return '\n'.join(row_strs)

if __name__ == "__main__":
    from doctest import testmod
    testmod()




