from boggleboard import BoggleBoard
from boggle import read_lexicon
from colorama import Fore, Back, Style
from gambler import SixSidedDie, PredictableDie
from gambler import Shuffler, NonShuffler

def cube_str(cube):
    colors = {'most recently selected': Fore.GREEN,
              'selected': Fore.BLUE,
              'unselected': Fore.WHITE}
    return colors[cube.get_status()] + cube.get_letter()

def display_boggle_board(board):
    row_strs = []
    for row in range(4):
        column = [cube_str(board.get_cube(row, col)) for col in range(4)]
        row_strs.append(' '.join(column))
    print('\n'.join(row_strs))
   
def play_text_game(shuffler, die):
    lex = read_lexicon('bogwords.txt')
    board = BoggleBoard(lex)
    board.shake_cubes(shuffler, die)
    keep_going = True
    while keep_going:
        display_boggle_board(board)
        if len(board.get_completed_words()) > 0:
            print('COMPLETED WORDS: ' + str(board.get_completed_words()))
        print('')
        cube_row = input("Choose a row (0-3): ")
        cube_col = input("Choose a column (0-3): ")
        if cube_row == 'q' or cube_col == 'q':
            keep_going = False
        else:
            cube = board.get_cube(int(cube_row), int(cube_col))
            cube.select()

if __name__ == "__main__":
    die = PredictableDie(0)
    shuffler = NonShuffler()
    play_text_game(shuffler, die)

