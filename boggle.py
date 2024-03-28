from graphics import Button
from game import Game
import pygame as pg
from boggleboard import BoggleBoard
from gambler import Shuffler, NonShuffler, SixSidedDie, PredictableDie
from lexicon import read_lexicon
from graphics import *


class CubeGraphic(Button):

    def __init__(self, cube, x, y, width):
        """Initializes a visual representation of a BoggleCube.
        
        THIS METHOD IS INCOMPLETE.

        You should modify this initialization method so that
        the CubeGraphic behaves in the manner described by the
        assignment.
    
        Parameters
        ----------
        cube : BoggleCube
            the BoggleCube that this graphic represents
        x : int
            x-coordinate of the upper left corner
        y : int
            y-coordinate of the upper left corner
        width : int
            the width of the visual representation (in pixels)
        """
        super().__init__(x, y, width, width, cube.get_letter()) 
        self._cube = cube
                                            
    def draw(self):
        """Returns a visual representation of the cube for the graphics window.
        
        THIS METHOD IS INCOMPLETE.

        Right now, all this method does is call its parent's .draw method.
        You should change this method so that CubeGraphic objects appear
        on the screen as described by the assignment.
        """ 
        self._font_color = "black"
        if self._cube.get_status() == 'most recently selected':
            self._up_color = "green"
        elif self._cube.get_status() == 'selected':
            self._up_color = "blue"
        else: 
            self._up_color = "gray"
        return super().draw()
    
    def notify(self, event):
        """Notification that a user event (e.g. a mouse click) has occurred.
        
        THIS METHOD IS INCOMPLETE.

        Right now, all this method does is call its parent's .notify method.
        You should change this method so that CubeGraphic objects behave
        in the manner described by the assignment.
        """
        super().notify(event)
        if self.check_if_pushed() == True:
            self._cube.select()
            self.reset()
        
class BoggleGame(Game):

    def __init__(self, lexicon, shuffler, die):
        """Initializes a new game of Boggle.
        
        THIS METHOD IS INCOMPLETE. Right now, it creates several generic
        Widgets that should be replaced by the more specific Widgets
        found in graphics.py. You should modify this method as needed
        so that the BoggleGame behaves in the manner described by the 
        assignment.

        Parameters
        ----------
        lexicon : set[str]
            A set of valid Boggle words.
        die : SixSidedDie
            A six-sided die that we can use to generate random numbers from 0 to 5.
        shuffler : Shuffler
            An object that shuffles a list (used for shuffling the BoggleCubes)        
        """
        super().__init__("Boggle!")   
        self._board = BoggleBoard(lexicon)
        self._board.shake_cubes(shuffler, die)
        
        # Dimensions of the play area
        x = self.get_playarea_x()
        y = self.get_playarea_y()
        width = self.get_playarea_width()
        height = self.get_playarea_height()
        
        # Dimension of each cube 
        cube_size = width / 4

        # Used to place CubeGraphics in the play area
        for i in range(4):
            for j in range(4):
                cube = self._board.get_cube(i, j)
                cube_x = x + i * cube_size
                cube_y = y + j * cube_size
                cube_graphic = CubeGraphic(cube, cube_x, cube_y, cube_size)
                self._window.add_widget(cube_graphic)

#$dont need elif because if the esc key is not hit, then
#$you know you want to update 

    def handle_event(self, event):
        """Handles user events (e.g. mouse clicks, keyboard presses).
        
        THIS METHOD IS INCOMPLETE. Right now, this method only does two things: 
        - it prints "ESC was pushed" when the user pushes the ESC button.
        - it prints the (x,y)-coordinates of where a mouse click occurred
        
        You should modify this method so that the BoggleGame behaves 
        as described by the assignment.
        """
        if event.type == pg.KEYDOWN and event.key == 27: # ESC was pressed
            # print("ESC was pressed!") 
            self._board.unselect_all()
        #$ don't need this check, can just have the code below run everytime
        #$ this will fix the delay in clicking
        elif event.type == pg.MOUSEBUTTONDOWN: 
            event_x, event_y = event.pos[0], event.pos[1]
            # print("Mouse click detected at (" + str(event_x) + ", " + str(event_y) + ")")
            self._upper_right.reset_words(self._board.get_completed_words())
            self._lower_left.reset_message(self._board.get_word_so_far())
                
def play_boggle(shuffler, die):
    """Starts a game of Boggle!
    
    DO NOT CHANGE.
    """
    lexicon = read_lexicon('bogwords.txt')
    quit_now = False
    while not quit_now:
        game = BoggleGame(lexicon, shuffler, die)
        quit_now = game.play()
 

if __name__ == "__main__":
     play_boggle(NonShuffler(), PredictableDie(0)) 
    # replace the above line with the following line, when you want to play a random game:  
    #play_boggle(Shuffler(), SixSidedDie())
    
