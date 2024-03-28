import pygame as pg
from graphics import Window, Button, QuitButton, TextList, TextBox

# Graphics constants.
# These specify the color, proportions and layout of the widgets 
# in the graphics window.
MARGIN = 40            # the width of the margins of the window (in pixels)
LEFTBAR_WIDTH = 200    # the width of the left bar of the window (in pixels)
RIGHTBAR_WIDTH = 160   # the width of the right bar of the window (in pixels)
TOPBAR_HEIGHT = 200    # the height of the top bar of the window (in pixels)
BOTTOMBAR_HEIGHT = 90  # the height of the bottom bar of the window (in pixels)
BUTTON_SPACING = 10    # the spacing between the RESET and QUIT buttons (in pixels)

# Derived graphics constants.
WINDOW_WIDTH = MARGIN*3 + LEFTBAR_WIDTH + RIGHTBAR_WIDTH
WINDOW_HEIGHT = MARGIN*3 + TOPBAR_HEIGHT + BOTTOMBAR_HEIGHT
QUIT_BUTTON_HEIGHT = (BOTTOMBAR_HEIGHT - BUTTON_SPACING) // 2
LEFTBAR_X = MARGIN
RIGHTBAR_X = MARGIN*2 + LEFTBAR_WIDTH
TOPBAR_Y = MARGIN
BOTTOMBAR_Y = MARGIN*2 + TOPBAR_HEIGHT 

class Game:
    def __init__(self, title):
        """Initializes a new, very boring game."""
        self._window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, title)
        self._reset_button = Button(RIGHTBAR_X, BOTTOMBAR_Y, 
                                    RIGHTBAR_WIDTH, QUIT_BUTTON_HEIGHT, "RESET")
        self._quit_button = QuitButton(RIGHTBAR_X, BOTTOMBAR_Y + QUIT_BUTTON_HEIGHT + BUTTON_SPACING, 
                                       RIGHTBAR_WIDTH, QUIT_BUTTON_HEIGHT)
        self._window.add_widget(self._reset_button)
        self._window.add_widget(self._quit_button)        
        self._upper_right = TextList(RIGHTBAR_X, TOPBAR_Y, 
                                     RIGHTBAR_WIDTH, TOPBAR_HEIGHT)
        self._upper_right.reset_words(["I'M", "A", "TEXTLIST!"])            
        self._window.add_widget(self._upper_right)
        self._lower_left = TextBox(LEFTBAR_X, BOTTOMBAR_Y, 
                                   LEFTBAR_WIDTH, BOTTOMBAR_HEIGHT,
                                   msg="I'm a textbox!",
                                   font_size=20)                
        self._window.add_widget(self._lower_left)

    def get_playarea_x(self):
        """Returns the x-coordinate of the upper left corner of the play area."""
        return LEFTBAR_X

    def get_playarea_y(self):
        """Returns the y-coordinate of the upper left corner of the play area."""
        return TOPBAR_Y

    def get_playarea_width(self):
        """Returns the width of the play area."""
        return LEFTBAR_WIDTH
    
    def get_playarea_height(self):
        """Returns the height of the play area."""
        return TOPBAR_HEIGHT

    def play(self):
        """Checks for and responds to user events (e.g. mouse clicks, keypresses).
        
        If an event occurs, it is handled by the .handle_events method. In other
        words, the .handle_events method determines what should happen when a
        particular event occurs. Therefore, YOU SHOULD NOT OVERRIDE the .play method,
        but rather override the .handle_event method to make the game respond
        appropriately to events.  
        """
        quit_now = False
        reset_now = False
        while not (quit_now or reset_now):
            events = self._window.check_events() 
            for event in events:
                self.handle_event(event)  
            quit_now = self._quit_button.check_if_pushed()
            reset_now = self._reset_button.check_if_pushed()         
            self._window.refresh()
        return not reset_now
    
    def handle_event(self, event):
        """Responds to events.
        
        In a generic Game, nothing happens when an event occurs, unless you press 
        the ESC key, in which case the message "hello!!!!" is printed to the Terminal.

        That is pretty useless behavior, so THIS METHOD SHOULD BE OVERRIDDEN BY
        CHILD CLASSES.
        """
        if event.type == pg.KEYDOWN and event.key == 27: # ESC was pressed
            print("hello!!!!")   

    
def play_game():
    """Starts a boring game!"""
    quit_now = False
    while not quit_now:
        game = Game("fun game")
        quit_now = game.play()


if __name__ == "__main__":
    play_game()