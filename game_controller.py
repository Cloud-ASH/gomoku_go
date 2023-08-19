from game_board import GameBoard
from stone import Stone
import re

HUMAN = 1
AINUM = 2
DRAW = 0
CONTINUE = -1
EMPTY = 0
FIVE = 5
HALF = 0.5
WIN = 1
TWO = 2


class GameController():
    '''
    Game controller class
    '''

    def __init__(self, boardsize=15, targetlen=5):
        '''
        Initialize game Controller
        '''
        self.board = GameBoard(boardsize, targetlen)
        self.targetlen = targetlen
        self.cur_step = 0
        self.allowMousePress = True
        self.winner = None

    def drop_stone(self, x, y, size, player, BORDER, UNIT_WIDTH):
        '''
        Drop the stone on the board
        '''
        # check if the position is occupied
        if self.board.board[x][y] == EMPTY:
            if player == "Human":
                self.board.board[x][y] = HUMAN
                self.cur_step += 1
                self.the_stone = Stone(x, y, size, "Human")
                return self.the_stone
            if player == "AI":
                self.board.board[x][y] = AINUM
                self.cur_step += 1
                self.the_stone = Stone(x, y, size, "AI")
                self.the_stone.display(BORDER, UNIT_WIDTH)
                return self.the_stone
        if self.board.board[x][y] != EMPTY:
            print("Position occupied, please try agian")
            # allow an extra try
            self.allowMousePress = True
            return

    def game_reuslt(self):
        '''
        Assess the status of game
        -1 stans for playing, 0 stands for draw,
        1 stands for human winner (black)
        2 stands for AI winner (white)
        '''
        # 5 in a row
        for x in range(self.board.boardsize - self.board.target_len):
            for y in range(self.board.boardsize):
                check_1 = 0
                check_2 = 0
                for i in range(0, self.board.target_len):
                    if self.board.board[x + i][y] == HUMAN:
                        check_1 += 1
                    if self.board.board[x + i][y] == AINUM:
                        check_2 += 1
                if check_1 == FIVE:
                    return HUMAN
                if check_2 == FIVE:
                    return AINUM

        # 5 in a column
        for y in range(self.board.boardsize - self.board.target_len):
            for x in range(self.board.boardsize):
                check_1 = 0
                check_2 = 0
                for i in range(0, self.board.target_len):
                    if self.board.board[x][y + i] == HUMAN:
                        check_1 += 1
                    if self.board.board[x][y + i] == AINUM:
                        check_2 += 1
                if check_1 == FIVE:
                    return HUMAN
                if check_2 == FIVE:
                    return AINUM

        # 5 from top right to down left
        for x in range(self.board.boardsize - self.board.target_len + 1):
            for y in range(self.board.boardsize - self.board.target_len + 1):
                check_1 = 0
                check_2 = 0
                for i in range(0, self.board.target_len):
                    if self.board.board[x + i][y + self.board.target_len
                       - 1 - i] == HUMAN:
                        check_1 += 1
                    if self.board.board[x + i][y + self.board.target_len
                       - 1 - i] == AINUM:
                        check_2 += 1
                if check_1 == self.targetlen:
                    return HUMAN
                if check_2 == self.targetlen:
                    return AINUM

        # 5 from top left to down right
        for x in range(self.board.boardsize - self.board.target_len + 1):
            for y in range(self.board.boardsize - self.board.target_len + 1):
                check_1 = 0
                check_2 = 0
                for i in range(0, self.board.target_len):
                    if self.board.board[x + self.board.target_len - 1 - i][y
                       + self.board.target_len - 1 - i] == HUMAN:
                        check_1 += 1
                    if self.board.board[x + self.board.target_len - 1 - i][y
                       + self.board.target_len - 1 - i] == AINUM:
                        check_2 += 1
                if check_1 == self.targetlen:
                    return HUMAN
                if check_2 == self.targetlen:
                    return AINUM

        # determine whether it is a draw or continue to play
        for x in range(self.board.boardsize):
            for y in range(self.board.boardsize):
                # if there is a position that is not occupied
                # then continue to play
                if self.board.board[x][y] == EMPTY:
                    return CONTINUE
        # draw
        return DRAW

    def get_distance(self, x1, y1, x2, y2):
        """
        Get the distance between two points
        """
        return ((x2 - x1)**TWO + (y2 - y1)**TWO)**(HALF)

    @property
    def allowMousePress(self):
        """
        Getter for allowKeyPress
        None --> Boolean
        """
        return self._allowMousePress

    # Setter decorator. @property with the same
    # name must be defined above.
    @allowMousePress.setter
    def allowMousePress(self, value):
        """
        Setter for allowKeyPress
        Boolean --> None
        """
        self._allowMousePress = value

    def choose_nearast(self, mouseX, mouseY, BORDER, PIXEL_WIDTH, UNIT_WIDTH):
        """
        1. Drop the stone to the nearest when mouse is pressed
        2. Auto-switch the color when there are two human players
        3. Display end text in terminal when the board is full
        """
        ELLIPSE_SIZE = HALF * UNIT_WIDTH
        if self.allowMousePress is True:
            if (BORDER <= mouseX <= (PIXEL_WIDTH - BORDER)) and\
               (BORDER <= mouseY <= (PIXEL_WIDTH - BORDER)):
                for i in range(self.board.boardsize):
                    for j in range(self.board.boardsize):
                        if self.get_distance(BORDER + i * UNIT_WIDTH,
                           BORDER + j * UNIT_WIDTH, mouseX,
                           mouseY) < HALF * UNIT_WIDTH:
                            player = self.color_choose()
                            self.drop_stone(i, j, ELLIPSE_SIZE, player,
                                            BORDER, UNIT_WIDTH)
                            self.the_stone.display(BORDER, UNIT_WIDTH)
                            print("I choose", i, j)
            self.end_text()
            self.allowMousePress = False

    def color_choose(self):
        """
        Choose the color of the stone for each step
        """
        if self.cur_step % TWO == 0:
            player = "Human"
        else:
            player = "AI"
        return player

    def end_text(self):
        """
        Display the end text in terminal
        """
        if self.game_reuslt() != CONTINUE:
            print("It's an end.")

    def record_winner(self, name):
        '''
        Record the winner
        '''
        f = open('scores.txt', 'r+')
        dic = {}
        has_record = False
        for line in f:
            # if len(line) != 0:
            # match the name and winning time of each line
            player = re.findall(r"^([\w\d\s]+)(?:[\s][0-9])$", line)
            score = re.findall(r"^(?:[\w\d\s]+[\s])([0-9])$", line)
            player = ''.join(player)
            if player == '':
                continue
            score = ''.join(score)
            score = int(score)
            # if the new winner has be recorded,
            # increment the winning time by 1
            if name == player:
                has_record = True
                score += 1
                new_score = str(score)
                line = re.sub(r"([0-9])$", new_score, line)
                # collect the winner and new winning time
            dic[player] = score
            # if the winner hasn't been recorded
            # add the name and winning time (1)
        if has_record is False:
            dic[name] = WIN
        # update and organize the winner and numbers
        sorted_list = sorted(
            dic.items(),
            key=lambda x: x[1],
            reverse=True
        )
        f.close()

        # reopen the txt and rewrite all the records
        with open('scores.txt', 'r+') as f:
            for i in sorted_list:
                write_name = str(i[0])
                write_number = str(i[1])
                to_write = write_name + ' ' + write_number
                f.write(to_write)
                f.write('\n')
