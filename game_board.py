ZERO = 0


class GameBoard:
    """
    A class representing the board
    """
    def __init__(self, boardsize, targetlen):
        self.boardsize = boardsize
        self.target_len = targetlen
        self.board = [[ZERO for x in range(self.boardsize)]
                      for y in range(self.boardsize)]
