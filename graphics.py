import pygame as pg


class Window:
    """A graphics window.
    
    A Window can host zero or more Widgets, which are each graphical
    objects that can potentially be interacted with. Example Widgets
    include Buttons and TextBoxes (see below).
    """

    def __init__(self, width, height, caption, bg_color="white"):
        """Initializes a graphics window with the specified dimensions.
        
        Parameters
        ----------
        width : int
            the width of the window (in pixels)
        height : int
            the height of the window (in pixels)
        caption : str
            the title that appears at the top of the window
        bg_color : str
            the background color of the window        
        """
        pg.init()
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()
        self._screen = pg.display.set_mode((width, height))
        self._bg_color = bg_color
        self._widgets = []
        self.refresh()
        self._callbacks = []

    def set_recurring_event(self, interval, func):
        """Calls the provided function at specified intervals.
        
        Parameters
        ----------
        interval : int
            the time interval between function calls (in milliseconds)
        func : function
            the function to call after each time interval
        """
        self._callbacks.append((interval, func))
        pg.time.set_timer(pg.USEREVENT + len(self._callbacks) - 1, interval)

    def add_widget(self, widget):
        """Adds a new widget to the graphics window."""
        self._widgets.append(widget)
        self.refresh()

    def refresh(self):
        """Redraws the window and its contents."""
        self._screen.fill(self._bg_color)
        for widget in self._widgets:
            drawing = widget.draw()
            self._screen.blit(drawing, widget.get_position())
        pg.display.flip()

    def notify(self, event):
        """Notification of a user event (e.g. a mouseclick).
        
        In response to a user event, the Window simply relays the event
        to its widgets.        
        """
        if event.type >= pg.USEREVENT and event.type <= pg.USEREVENT + len(self._callbacks):
            interval, callback = self._callbacks[event.type - pg.USEREVENT]
            pg.time.set_timer(event, interval)
            callback()
        for widget in self._widgets:
            widget.notify(event)

    def check_events(self):
        """Checks if any events have occurred since the last time .check_events was called.
        
        If so, then every widget is notified of the event (by calling its .notify method).
        """
        self.clock.tick(60)
        events = list(pg.event.get())
        for event in events:
            self.notify(event)
        return events


class Widget:
    """A Widget can be drawn in a Window and can respond to user events.
    
    Widget is intended to be an abstract base class. In other words, 
    typically we want to create child classes of Widget that have more
    specialized behavior than a generic Widget, which ignores user events
    and is drawn as a plain gray rectangle.

    To do different things in response to user events, a child class should
    override the .notify method.

    To be drawn differently than a generic Widget, a child class should
    override the .draw method.
    """

    def __init__(self, x, y, width, height):
        """Initializes a Widget with a specific location and dimensions.
        
        Parameters
        ----------
        x : int
            x-coordinate of the upper-left corner of the Widget
        y : int
            y-coordinate of the upper-left corner of the Widget
        width : int
            the width (in pixels) of the Widget
        height : int
            the height (in pixels) of the Widget        
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def get_position(self):
        """Gets the (x, y) location of the upper-left corner."""
        return (self._x, self._y)

    def draw(self):
        """Creates a graphical representation that can be placed on a Window."""
        return None

    def notify(self, event):
        """Notification of a user event."""
        pass


class ExampleWidget(Widget):
    """A Widget can be drawn in a Window and can respond to user events.
    
    Widget is intended to be an abstract base class. In other words, 
    typically we want to create child classes of Widget that have more
    specialized behavior than a generic Widget, which ignores user events
    and is drawn as a plain gray rectangle.

    To do different things in response to user events, a child class should
    override the .notify method.

    To be drawn differently than a generic Widget, a child class should
    override the .draw method.
    """

    def draw(self):
        """Creates a graphical representation that can be placed on a Window."""
        graphic = pg.Surface((self._width, self._height))
        graphic.fill("gray")
        myfont = pg.font.SysFont("monospace", 14)
        text = myfont.render("WIDGET", 1, "black")
        text_w, text_h = text.get_size()
        graphic.blit(text, 
                     (self._width // 2 - text_w // 2, 
                      self._height // 2 - text_h // 2))
        return graphic

    def notify(self, event):
        """Notification of a user event."""
        if event.type == pg.MOUSEBUTTONDOWN:
            print("Mouse down detected here: " + str(event.pos))
        elif event.type == pg.KEYDOWN and event.key == 27: # ESC was pressed
            print("ESC was pushed!")


class TextBox(Widget):

    def __init__(self, x, y, width, height, msg, 
                 bg_color="light blue", font_name="monospace", 
                 font_size=30, font_color="black"):
        """Initializes a TextBox.
        
        Parameters
        ----------
        x : int
            x-coordinate of the upper-left corner of the TextBox
        y : int
            y-coordinate of the upper-left corner of the TextBox
        width : int
            the width (in pixels) of the TextBox
        height : int
            the height (in pixels) of the TextBox
        msg : str
            the text displayed in the TextBox
        bg_color : str
            the background color of the TextBox
        font_name : str
            the name of the typeface used for the text
        font_size : int
            the size of the typeface used for the text
        font_color : str
            the color of the typeface used for the text
        """
        super().__init__(x, y, width, height)
        self._msg = msg
        self._bg_color = bg_color
        self._font = pg.font.SysFont(font_name, font_size)
        self._font_color = font_color

    def reset_message(self, msg):
        """Resets the text to another message."""
        self._msg = msg

    def draw(self):
        """Creates a graphical representation that can be placed on a Window."""
        graphic = pg.Surface((self._width, self._height))
        graphic.fill(self._bg_color)
        text = self._font.render(self._msg, 1, self._font_color)
        text_w, text_h = text.get_size()
        graphic.blit(text, 
                     (self._width // 2 - text_w // 2, 
                      self._height // 2 - text_h // 2))
        return graphic



class Button(TextBox):
    """A Button is a TextBox that notices when it is clicked on.
    
    After the user clicks on the button, the method .check_if_pushed()
    will return True until the button is reset (i.e. until the method .reset()
    is called).
    """

    def __init__(self, x, y, width, height, label,
                 up_color="black", down_color="dark gray",
                 font_name="monospace", font_size=30, 
                 font_color="white"):
        """Initializes a Button.
        
        Parameters
        ----------
        x : int
            x-coordinate of the upper-left corner of the Button
        y : int
            y-coordinate of the upper-left corner of the Button
        width : int
            the width (in pixels) of the Button
        height : int
            the height (in pixels) of the Button
        label : str
            the text displayed on the button
        up_color : str
            the color of the button when it is "up", i.e. unpressed
        down_color : str
            the color of the button while it is "down", i.e. pressed
        font_name : str
            the name of the typeface used for the label
        font_size : int
            the size of the typeface used for the label
        font_color : str
            the color of the typeface used for the label
        """
        super().__init__(x, y, width, height, label,
                         up_color, font_name, font_size, font_color)
        self._up_color = up_color
        self._down_color = down_color
        self._is_down = False
        self._recently_pushed = False
                       
    def check_if_pushed(self):
        """Checks whether the button has been pushed since it was last reset."""
        return self._recently_pushed
    
    def reset(self):
        """Resets the "pushed" status of the button."""
        self._recently_pushed = False

    def draw(self):
        """Creates a graphical representation that can be placed on a Window."""
        if self._is_down:
            self._bg_color = self._down_color 
        else:
            self._bg_color = self._up_color
        return super().draw()

    def notify(self, event):
        """Notification of a user event.
        
        After the user clicks on the button, the method .check_if_pushed()
        will return True until the button is reset (i.e. until the method .reset()
        is called).
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            event_x, event_y = event.pos
            in_x_range = self._x < event_x < self._x + self._width
            in_y_range = self._y < event_y < self._y + self._height
            if in_x_range and in_y_range:
                self._is_down = True
        elif event.type == pg.MOUSEBUTTONUP and self._is_down:
            self._is_down = False
            self._recently_pushed = True


class QuitButton(Button):
    """A convenient subclass of Button that allows you to quit a program."""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "QUIT")

    def notify(self, event):
        super().notify(event)
        if event.type == pg.QUIT:
            self._recently_pushed = True


class Square(Widget):
    """A Square is just a square."""

    def __init__(self, x, y, width,
                 outline_color="black", fill_color="red"):
               
        super().__init__(x, y, width, width)
        self._outline_color = outline_color
        self._fill_color = fill_color

    def draw(self):
        """Creates a graphical representation that can be placed on a Window."""
        graphic = pg.Surface((self._width, self._height))
        graphic.fill(self._outline_color)
        pg.draw.rect(graphic, self._fill_color, pg.Rect(1, 1, self._width-2, self._width-2))        
        return graphic

class TextList(Widget):

    def __init__(self, x, y, width, height,
                 bg_color="light green",
                 font_name="monospace", 
                 font_size=12,
                 font_color="black"):
        """Initializes a TextList.
        
        Parameters
        ----------
        x : int
            x-coordinate of the upper-left corner of the TextList
        y : int
            y-coordinate of the upper-left corner of the TextList
        width : int
            the width (in pixels) of the TextList
        height : int
            the height (in pixels) of the TextList
        bg_color : str
            the background color of the TextList
        font_name : str
            the name of the typeface used for the text
        font_size : int
            the size of the typeface used for the text
        font_color : str
            the color of the typeface used for the text
        """
        super().__init__(x, y, width, height)
        self._font_color = font_color
        self._font_name = font_name
        self._font_size = font_size
        self._bg_color = bg_color
        self._words = []

    def reset_words(self, words):
        """Resets the list of words."""
        self._words = words

    def draw(self):
        """Creates a graphical representation that can be placed on a Window."""
        graphic = pg.Surface((self._width, self._height))
        graphic.fill(self._bg_color)
        myfont = pg.font.SysFont(self._font_name, self._font_size)
        y_position = 2
        for word in self._words:
            text = myfont.render(word, 1, self._font_color)
            text_w, text_h = text.get_size()
            graphic.blit(text, (self._width // 2 - text_w // 2, y_position))
            y_position += text_h + 1
        return graphic
    
