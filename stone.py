

class Stone(object):
    """
    create the stone shape, color, etc.
    """
    def __init__(self, x, y, ellipse_size, player):
        """
        Initialize square
        Number Number Color --> SnakeSquare
        """
        self._x = x
        self._y = y
        self._WHITE = (255, 255, 255)
        self._BLACK = (0, 0, 0)
        self._ELLIPSE_SIZE = ellipse_size
        self.player = player

    def display(self, border, unit_width):
        """
        Display stone according to player and size
        """
        if self.player == "Human":
            strokeWeight(5)
            fill(*self._BLACK)
            stroke(*self._BLACK)
            ellipse(border + self._x * unit_width,
                    border + self.y * unit_width,
                    self._ELLIPSE_SIZE,
                    self._ELLIPSE_SIZE)
        if self.player == "AI":
            strokeWeight(5)
            fill(*self._WHITE)
            stroke(*self._BLACK)
            ellipse(border + self._x * unit_width,
                    border + self.y * unit_width,
                    self._ELLIPSE_SIZE,
                    self._ELLIPSE_SIZE)

    # Getters and setters
    @property
    def x(self):
        """
        Getter for x value
        None --> Number
        """
        return self._x

    @x.setter
    def x(self, val):
        """
        Setter for x value
        Number --> None
        """
        self._x = val

    @property
    def y(self):
        """
        Getter for y value
        None --> Number
        """
        return self._y

    @y.setter
    def y(self, val):
        """
        Setter for y value
        Number --> None
        """
        self._y = val
