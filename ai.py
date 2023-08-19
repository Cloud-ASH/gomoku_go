# -*- coding: utf-8 -*-
from copy import deepcopy


# score
HUNDRED = 100
NINETY = 90
EIGHTY = 80
SEVENTY = 70
SIXTY = 60
FIFTY = 50
THIRTY = 30
TWENTY = 20
# stone patterns
TEN = 10
ZERO = 0
FIVE = 5
FOUR = 4
THREE = 3
TWO = 2
ONE = 1
# stone row
ONELEN = 1
TWOLEN = 2
THREELEN = 3
FOURLEN = 4
FIVELEN = 5
# stone player
HUMAN = 1
AINUM = 2
EMPTY = 0
# status
DRAW = 0
CONTINUE = -1

RADIUS = 5
MODNUM = 2


class AI:
    '''
    A class represent the ai player
    '''

    def __init__(self, gc):
        self.gc = gc
        self.win_matrix = []

    def best_choice(self, gc):
        '''
        Return the best position based on current situation
        '''
        assume_gc = deepcopy(gc)
        dic = {}
        available_ls = self.accerlerate(assume_gc)

        for i in available_ls:
            if assume_gc.board.board[i[0]][i[1]] == EMPTY:
                assume_gc.board.board[i[0]][i[1]] = AINUM
                self.gc.cur_step += 1
                score = self.scoring(assume_gc.board)
                dic[(i[0], i[1])] = score
                assume_gc.board.board[i[0]][i[1]] = EMPTY
                self.gc.cur_step -= 1

        arranged_dic = sorted(
            dic.items(),
            key=lambda x: x[1],
            reverse=True
        )
        print("Step", self.gc.cur_step + 1)

        return arranged_dic[0][0]

    def accerlerate(self, gc):
        '''
        Reduce the number position that needs to be checked
        Only check those has stones within radius
        '''
        radius = RADIUS
        ls = []
        for i in range(gc.board.boardsize):
            for j in range(gc.board.boardsize):
                if gc.board.board[i][j] == EMPTY and\
                   self.check_neighbor(gc.board, i, j, radius):
                    ls.append([i, j])
        return ls

    def check_neighbor(self, board, x, y, radius):
        """
        Check the neighbors of position with a stone
        """
        begin_x, end_x = (x - radius), (x + radius)
        begin_y, end_y = (y - radius), (y + radius)

        for i in range(begin_x, end_x + 1):
            for j in range(begin_y, end_y + 1):
                if (i >= 0) and (i < board.boardsize) and (j >= 0) and\
                   (j < board.boardsize):
                    if board.board[i][j] != EMPTY:
                        return True

    def scoring(self, board):
        '''
        Evaluate each situation and give scores
        Check every situation based on a declining score trend
        If matched with a higher score, return
        '''
        # 5 in a row
        for x in range(board.boardsize - board.target_len):
            for y in range(board.boardsize):
                check_1 = 0
                check_2 = 0
                for i in range(0, board.target_len):
                    if board.board[x + i][y] == HUMAN:
                        check_1 += 1
                    if board.board[x + i][y] == AINUM:
                        check_2 += 1
                if check_1 == FIVE:
                    return -HUNDRED
                if check_2 == FIVE:
                    return HUNDRED

        # 5 in a column
        for y in range(board.boardsize - board.target_len):
            for x in range(board.boardsize):
                check_1 = 0
                check_2 = 0
                for i in range(0, board.target_len):
                    if board.board[x][y + i] == HUMAN:
                        check_1 += 1
                    if board.board[x][y + i] == AINUM:
                        check_2 += 1
                if check_1 == FIVE:
                    return -HUNDRED
                if check_2 == FIVE:
                    return HUNDRED

        # 5 from top right to down left
        for x in range(board.boardsize - board.target_len + 1):
            for y in range(board.boardsize - board.target_len + 1):
                check_1 = 0
                check_2 = 0
                for i in range(0, board.target_len):
                    if board.board[x + i][y + board.target_len
                       - 1 - i] == HUMAN:
                        check_1 += 1
                    if board.board[x + i][y + board.target_len
                       - 1 - i] == AINUM:
                        check_2 += 1
                if check_1 == board.target_len:
                    return -HUNDRED
                if check_2 == board.target_len:
                    return HUNDRED

        # 5 from top left to down right
        for x in range(board.boardsize - board.target_len + 1):
            for y in range(board.boardsize - board.target_len + 1):
                check_1 = 0
                check_2 = 0
                for i in range(0, board.target_len):
                    if board.board[x + board.target_len - 1 - i][y
                       + board.target_len - 1 - i] == HUMAN:
                        check_1 += 1
                    if board.board[x + board.target_len - 1 - i][y
                       + board.target_len - 1 - i] == AINUM:
                        check_2 += 1
                if check_1 == board.target_len:
                    return -HUNDRED
                if check_2 == board.target_len:
                    return HUNDRED

        four_human = 0
        four_ai = 0

        # notation: e stands for empty,
        # o stands for one side, i is the other side
        # eg: eooooi

        # horizontal
        for x in range(board.boardsize - board.target_len):
            for y in range(board.boardsize):
                check_1 = 0
                check_2 = 0
                for i in range(0, board.target_len):
                    if board.board[x + i][y] == HUMAN:
                        check_1 += 1
                    if board.board[x + i][y] == AINUM:
                        check_2 += 1
                # four in a 5-row, eoooo or oeooo or ooeoo etc.
                if (check_1 == FOUR) & (check_2 == ZERO):
                    four_human += 1
                if (check_2 == FOUR) & (check_1 == ZERO):
                    four_ai += 1

        # vertical
        for x in range(board.boardsize):
            for y in range(board.boardsize - board.target_len):
                check_1 = 0
                check_2 = 0
                for i in range(0, board.target_len):
                    if board.board[x][y + i] == HUMAN:
                        check_1 += 1
                    if board.board[x][y + i] == AINUM:
                        check_2 += 1
                # four in a 5-row, eoooo or oeooo or ooeoo etc.
                if (check_1 == FOUR) & (check_2 == ZERO):
                    four_human += 1
                if (check_2 == FOUR) & (check_1 == ZERO):
                    four_ai += 1

        # top right to down left
        for x in range(board.boardsize - board.target_len + 1):
            for y in range(board.boardsize - board.target_len + 1):
                check_1 = 0
                check_2 = 0
                for i in range(0, board.target_len):
                    if board.board[x + i][y + board.target_len
                       - 1 - i] == HUMAN:
                        check_1 += 1
                    if board.board[x + i][y + board.target_len
                       - 1 - i] == AINUM:
                        check_2 += 1
                # four in a 5-row, eoooo or oeooo or ooxoo etc.
                if (check_1 == FOUR) & (check_2 == ZERO):
                    four_human += 1
                if (check_2 == FOUR) & (check_1 == ZERO):
                    four_ai += 1

        # top left to down right
        for x in range(board.boardsize - board.target_len + 1):
            for y in range(board.boardsize - board.target_len + 1):
                check_1 = 0
                check_2 = 0
                for i in range(0, board.target_len):
                    if board.board[x + board.target_len - 1 - i][y
                       + board.target_len - 1 - i] == HUMAN:
                        check_1 += 1
                    if board.board[x + board.target_len - 1 - i][y
                       + board.target_len - 1 - i] == AINUM:
                        check_2 += 1
                # four in a 5-row, eoooo or oeooo or ooeoo etc.
                if (check_1 == FOUR) & (check_2 == ZERO):
                    four_human += 1
                if (check_2 == FOUR) & (check_1 == ZERO):
                    four_ai += 1

        # need to specify whose turn it is
        # notic: live four: eooooe & double half four: 2 of eooooi(or ooeooi)
        # these two situation are equivalent when search, both result in +2
        # for four_human(or ai)
        # and we will give them the same score, both are quite late-stage

        # human's turn
        if self.gc.cur_step % MODNUM == 0:
            if four_human >= TWO:
                return -NINETY
            if (four_ai >= TWO) and (four_human == ZERO):
                return NINETY
        # ai's turn
        else:
            if four_ai >= TWO:
                return NINETY
            if (four_human >= TWO) and (four_ai == ZERO):
                return -NINETY

        three_human = 0
        three_ai = 0
        # here we define (Live Three) as eoooe or eoeooe or eooeoe
        # Live three has the power to become live four, which is very
        # threatful to the opposite, more dangerous than half four.

        # eoooe
        # horizontal
        for x in range(board.boardsize - board.target_len):
            for y in range(board.boardsize):
                if (board.board[x][y] == EMPTY) and\
                   (board.board[x + ONELEN][y] == HUMAN) and\
                   (board.board[x + TWOLEN][y] == HUMAN) and\
                   (board.board[x + THREELEN][y] == HUMAN) and\
                   (board.board[x + FOURLEN][y] == EMPTY):
                    three_human += 1
                if (board.board[x][y] == EMPTY) and\
                   (board.board[x + ONELEN][y] == AINUM) and\
                   (board.board[x + TWOLEN][y] == AINUM) and\
                   (board.board[x + THREELEN][y] == AINUM) and\
                   (board.board[x + FOURLEN][y] == EMPTY):
                    three_ai += 1
        # vertical
        for y in range(board.boardsize - board.target_len):
            for x in range(board.boardsize):
                if (board.board[x][y] == EMPTY) and\
                   (board.board[x][y + ONELEN] == HUMAN) and\
                   (board.board[x][y + TWOLEN] == HUMAN) and\
                   (board.board[x][y + THREELEN] == HUMAN) and\
                   (board.board[x][y + FOURLEN] == EMPTY):
                    three_human += 1
                if (board.board[x][y] == EMPTY) and\
                   (board.board[x][y + ONELEN] == AINUM) and\
                   (board.board[x][y + TWOLEN] == AINUM) and\
                   (board.board[x][y + THREELEN] == AINUM) and\
                   (board.board[x][y + FOURLEN] == EMPTY):
                    three_ai += 1
        # top right to down left
        for x in range(board.boardsize - board.target_len + 1):
            for y in range(board.boardsize - board.target_len + 1):
                if (board.board[x][y + board.target_len - ONELEN] == EMPTY)\
                    and\
                   (board.board[x + ONELEN][y + board.target_len - TWOLEN]
                    == HUMAN) and\
                   (board.board[x + TWOLEN][y + board.target_len - THREELEN]
                    == HUMAN) and\
                   (board.board[x + THREELEN][y + board.target_len - FOURLEN]
                    == HUMAN) and\
                   (board.board[x + FOURLEN][y + board.target_len - FIVELEN]
                   == EMPTY):
                    three_human += 1
                if (board.board[x][y + board.target_len - ONELEN] == EMPTY)\
                    and\
                   (board.board[x + ONELEN][y + board.target_len - TWOLEN]
                    == AINUM) and\
                   (board.board[x + TWOLEN][y + board.target_len - THREELEN]
                    == AINUM) and\
                   (board.board[x + THREELEN][y + board.target_len - FOURLEN]
                    == AINUM) and\
                   (board.board[x + FOURLEN][y + board.target_len - FIVELEN]
                   == EMPTY):
                    three_ai += 1
        # top left to down right
        for x in range(board.boardsize - board.target_len + 1):
            for y in range(board.boardsize - board.target_len + 1):
                if (board.board[x + board.target_len - ONELEN]
                   [y + board.target_len - ONELEN] == EMPTY) and\
                   (board.board[x + board.target_len - TWOLEN]
                   [y + board.target_len - TWOLEN] == HUMAN) and\
                   (board.board[x + board.target_len - THREELEN]
                   [y + board.target_len - THREELEN] == HUMAN) and\
                   (board.board[x + board.target_len - FOURLEN]
                   [y + board.target_len - FOURLEN] == HUMAN) and\
                   (board.board[x + board.target_len - FIVELEN]
                   [y + board.target_len - FIVELEN] == EMPTY):
                    three_human += 1
                if (board.board[x + board.target_len - ONELEN]
                   [y + board.target_len - ONELEN] == EMPTY) and\
                   (board.board[x + board.target_len - TWOLEN]
                   [y + board.target_len - TWOLEN] == AINUM) and\
                   (board.board[x + board.target_len - THREELEN]
                   [y + board.target_len - THREELEN] == AINUM) and\
                   (board.board[x + board.target_len - FOURLEN]
                   [y + board.target_len - FOURLEN] == AINUM) and\
                   (board.board[x + board.target_len - FIVELEN]
                   [y + board.target_len - FIVELEN] == EMPTY):
                    three_ai += 1

        # eoeooe or eooeoe
        # we need to search 6 to account for
        # all the possible three conditions
        # horizontal
        for x in range(board.boardsize - board.target_len - 1):
            for y in range(board.boardsize):
                check_1 = 0
                check_2 = 0
                if (board.board[x][y] == EMPTY) and\
                   (board.board[x + board.target_len][y] == EMPTY):
                    for i in range(1, board.target_len):
                        if board.board[x + i][y] == HUMAN:
                            check_1 += 1
                        if board.board[x + i][y] == AINUM:
                            check_2 += 1
                    if (check_1 == THREE) & (check_2 == ZERO):
                        three_human += 1
                    if (check_2 == THREE) & (check_1 == ZERO):
                        three_ai += 1
        # vertical
        for y in range(board.boardsize - board.target_len - 1):
            for x in range(board.boardsize):
                check_1 = 0
                check_2 = 0
                if (board.board[x][y] == EMPTY) and\
                   (board.board[x][y + board.target_len] == EMPTY):
                    for i in range(1, board.target_len):
                        if board.board[x][y + i] == HUMAN:
                            check_1 += 1
                        if board.board[x][y + i] == AINUM:
                            check_2 += 1
                    if (check_1 == THREE) & (check_2 == ZERO):
                        three_human += 1
                    if (check_2 == THREE) & (check_1 == ZERO):
                        three_ai += 1
        # top right to down left
        for x in range(board.boardsize - board.target_len):
            for y in range(board.boardsize - board.target_len):
                check_1 = 0
                check_2 = 0
                if (board.board[x][y + board.target_len] == EMPTY) and\
                   (board.board[x + board.target_len][y] == EMPTY):
                    for i in range(1, board.target_len):
                        if board.board[x + i][y + board.target_len - i]\
                           == HUMAN:
                            check_1 += 1
                        if board.board[x + i][y + board.target_len - i]\
                           == AINUM:
                            check_2 += 1
                    if (check_1 == THREE) & (check_2 == ZERO):
                        three_human += 1
                    if (check_2 == THREE) & (check_1 == ZERO):
                        three_ai += 1
        # top right to down left
        for x in range(board.boardsize - board.target_len):
            for y in range(board.boardsize - board.target_len):
                check_1 = 0
                check_2 = 0
                if (board.board[x + board.target_len]
                   [y + board.target_len] == EMPTY) and\
                   (board.board[x][y] == EMPTY):
                    for i in range(1, board.target_len):
                        if board.board[x + board.target_len - i][y +
                           board.target_len - i] == HUMAN:
                            check_1 += 1
                        if board.board[x + board.target_len - i][y +
                           board.target_len - i] == AINUM:
                            check_2 += 1
                    if (check_1 == THREE) & (check_2 == ZERO):
                        three_human += 1
                    if (check_2 == THREE) & (check_1 == ZERO):
                        three_ai += 1

        # half four + live three
        # half four
        # double live three
        # single live three

        # situation1: combination of 1 half-four and 1 three
        # human's turn
        if self.gc.cur_step % MODNUM == 0:
            if (four_human >= ONE) and (three_human >= ONE):
                return -EIGHTY
            if (four_ai >= ONE) and (three_ai >= ONE):
                return EIGHTY
        # ai's turn
        else:
            if (four_ai >= ONE) and (three_ai >= ONE):
                return EIGHTY
            if (four_human >= ONE) and (three_human >= ONE):
                return -EIGHTY

        # situation2: 1 half four, which means four_human(ai) is 1
        # (if it is a live four, the four_human(ai) will be at least 2
        # due to the 5-in-a-row search method)
        # human's turn
        if self.gc.cur_step % MODNUM == 0:
            if (four_human >= ONE):
                return -SEVENTY
            if (four_ai >= ONE):
                return SEVENTY
        # ai's turn
        else:
            if (four_ai >= ONE):
                return SEVENTY
            if (four_human >= ONE):
                return -SEVENTY

        # situation3: 2 live three
        # human's turn
        if self.gc.cur_step % MODNUM == 0:
            if (three_human > THREE):
                return -SIXTY
            if (three_ai > THREE):
                print(three_ai)
                return SIXTY
        # ai's turn
        else:
            if (three_ai > THREE):
                return SIXTY
            if (three_human > THREE):
                return -SIXTY

        # situation4: 1 live three
        # human's turn
        if self.gc.cur_step % MODNUM == 0:
            if (three_human >= ONE):
                return -FIFTY
            if (three_ai >= ONE):
                return FIFTY
        # ai's turn
        else:
            if (three_ai >= ONE):
                return FIFTY
            if (three_human >= ONE):
                return -FIFTY

        sleep_three_human = 0
        sleep_three_ai = 0
        # here we define (Sleep Three) as: ioeooe, iooeoe, ioooee
        # or: eooeoi, eoeooi, eeoooi,
        # notice: ieoooe/eoooei is actually a live three, so it does not need
        # to be considered
        # horizontal
        for x in range(board.boardsize - board.target_len):
            for y in range(board.boardsize):
                check_1 = 0
                check_2 = 0
                if ((board.board[x][y] == HUMAN) and
                   (board.board[x + board.target_len][y] == EMPTY))\
                   or ((board.board[x][y] == EMPTY) and
                   (board.board[x + board.target_len][y] == HUMAN)):
                    for i in range(1, board.target_len):
                        if board.board[x + i][y] == HUMAN:
                            check_1 += 1
                        if board.board[x + i][y] == AINUM:
                            check_2 += 1
                    if (check_2 == THREE) & (check_1 == ZERO):
                        sleep_three_ai += 1
                check_1 = 0
                check_2 = 0
                if ((board.board[x][y] == AINUM) and
                   (board.board[x + board.target_len][y] == 0))\
                   or ((board.board[x][y] == 0) and
                   (board.board[x + board.target_len][y] == AINUM)):
                    for i in range(1, board.target_len):
                        if board.board[x + i][y] == HUMAN:
                            check_1 += 1
                        if board.board[x + i][y] == AINUM:
                            check_2 += 1
                    if (check_1 == THREE) & (check_2 == ZERO):
                        sleep_three_human += 1

        # vertical
        for y in range(board.boardsize - board.target_len - 1):
            for x in range(board.boardsize):
                check_1 = 0
                check_2 = 0
                if ((board.board[x][y] == HUMAN) and
                   (board.board[x][y + board.target_len] == EMPTY))\
                   or ((board.board[x][y] == EMPTY) and
                   (board.board[x][y + board.target_len] == HUMAN)):
                    for i in range(1, board.target_len):
                        if board.board[x][y + i] == HUMAN:
                            check_1 += 1
                        if board.board[x][y + i] == AINUM:
                            check_2 += 1
                    if (check_2 == THREE) & (check_1 == ZERO):
                        sleep_three_ai += 1
                check_1 = 0
                check_2 = 0
                if ((board.board[x][y] == AINUM) and
                   (board.board[x][y + board.target_len] == EMPTY))\
                   or ((board.board[x][y] == EMPTY) and
                   (board.board[x][y + board.target_len] == AINUM)):
                    for i in range(1, board.target_len):
                        if board.board[x][y + i] == HUMAN:
                            check_1 += 1
                        if board.board[x][y + i] == AINUM:
                            check_2 += 1
                    if (check_1 == THREE) & (check_2 == ZERO):
                        sleep_three_human += 1
        # top right to down left
        for x in range(board.boardsize - board.target_len):
            for y in range(board.boardsize - board.target_len):
                check_1 = 0
                check_2 = 0
                if ((board.board[x][y + board.target_len] == HUMAN) and
                   (board.board[x + board.target_len][y] == EMPTY))\
                   or ((board.board[x][y + board.target_len] == EMPTY) and
                   (board.board[x + board.target_len][y] == HUMAN)):
                    for i in range(1, board.target_len):
                        if board.board[x + i][y + board.target_len - i]\
                           == HUMAN:
                            check_1 += 1
                        if board.board[x + i][y + board.target_len - i]\
                           == AINUM:
                            check_2 += 1
                    if (check_2 == THREE) & (check_1 == ZERO):
                        sleep_three_ai += 1
                check_1 = 0
                check_2 = 0
                if ((board.board[x][y + board.target_len] == AINUM) and
                   (board.board[x + board.target_len][y] == EMPTY))\
                   or ((board.board[x][y + board.target_len] == EMPTY) and
                   (board.board[x + board.target_len][y] == AINUM)):
                    for i in range(1, board.target_len):
                        if board.board[x + i][y + board.target_len - i]\
                           == HUMAN:
                            check_1 += 1
                        if board.board[x + i][y + board.target_len - i]\
                           == AINUM:
                            check_2 += 1
                    if (check_2 == THREE) & (check_1 == ZERO):
                        sleep_three_ai += 1
        # top right to down left
        for x in range(board.boardsize - board.target_len):
            for y in range(board.boardsize - board.target_len):
                check_1 = 0
                check_2 = 0
                if (board.board[x + board.target_len]
                   [y + board.target_len] == HUMAN)\
                   and (board.board[x][y] == EMPTY)\
                   or (board.board[x + board.target_len][y + board.target_len]
                   == EMPTY) and\
                   (board.board[x][y] == HUMAN):
                    for i in range(1, board.target_len):
                        if board.board[x + board.target_len - i][y +
                           board.target_len - i] == HUMAN:
                            check_1 += 1
                        if board.board[x + board.target_len - i][y +
                           board.target_len - i] == AINUM:
                            check_2 += 1
                    if (check_2 == THREE) & (check_1 == ZERO):
                        sleep_three_ai += 1
                check_1 = 0
                check_2 = 0
                if (board.board[x + board.target_len]
                   [y + board.target_len] == AINUM)\
                   and (board.board[x][y] == EMPTY)\
                   or\
                   board.board[x + board.target_len][y + board.target_len]\
                   == EMPTY and board.board[x][y] == AINUM:
                    for i in range(1, board.target_len):
                        if board.board[x + board.target_len - i][y +
                           board.target_len - i] == HUMAN:
                            check_1 += 1
                        if board.board[x + board.target_len - i][y +
                           board.target_len - i] == AINUM:
                            check_2 += 1
                    if (check_1 == THREE) & (check_2 == ZERO):
                        sleep_three_human += 1

        # scoring for sleep three
        # human's turn
        if self.gc.cur_step % MODNUM == 0:
            if (sleep_three_human >= ONE):
                return -THIRTY
            if (sleep_three_ai >= ONE):
                return THIRTY
        # ai's turn
        else:
            if (sleep_three_ai >= ONE):
                return THIRTY
            if (sleep_three_human >= ONE):
                return -THIRTY

        # second:
        # in a five position row, as long as the first and last are
        # not black(1) or white(2) at the same time, any permutation
        # of two black(1)/white(2) with (three empty(0))(live two)
        # or (two empty(0) and 1 different color)(sleep two) will be fine

        # horizontal
        # live two：eoeoe, eeooe, eooee
        two_human = 0
        two_ai = 0
        for x in range(board.boardsize - board.target_len):
            for y in range(board.boardsize):
                check_1 = 0
                check_2 = 0
                if (board.board[x][y] == EMPTY) and\
                   (board.board[x + board.target_len - 1][y] == EMPTY):
                    for i in range(0, board.target_len):
                        if board.board[x + i][y] == HUMAN:
                            check_1 += 1
                        if board.board[x + i][y] == AINUM:
                            check_2 += 1
                    if (check_1 == TWO) & (check_2 == ZERO):
                        two_human += 1
                    if (check_2 == TWO) & (check_1 == ZERO):
                        two_ai += 1
        # vertical
        for x in range(board.boardsize):
            for y in range(board.boardsize - board.target_len):
                check_1 = 0
                check_2 = 0
                if ((board.board[x][y] == EMPTY) and
                   (board.board[x][y + board.target_len - 1] == EMPTY)):
                    for i in range(0, board.target_len):
                        if board.board[x][y + i] == HUMAN:
                            check_1 += 1
                        if board.board[x][y + i] == AINUM:
                            check_2 += 1
                    if (check_1 == TWO) & (check_2 == ZERO):
                        two_human += 1
                    if (check_2 == TWO) & (check_1 == ZERO):
                        two_ai += 1

        # top right to down left
        for x in range(board.boardsize - board.target_len + 1):
            for y in range(board.boardsize - board.target_len + 1):
                check_1 = 0
                check_2 = 0
                if (board.board[x][y + board.target_len - 1] == EMPTY) and\
                   (board.board[x + board.target_len - 1][y] == EMPTY):
                    for i in range(0, board.target_len):
                        if board.board[x + i][y + board.target_len - 1 - i]\
                           == HUMAN:
                            check_1 += 1
                        if board.board[x + i][y + board.target_len - 1 - i]\
                           == AINUM:
                            check_2 += 1
                    if (check_1 == TWO) & (check_2 == ZERO):
                        two_human += 1
                    if (check_2 == TWO) & (check_1 == ZERO):
                        two_ai += 1

        # top left to down right
        for x in range(board.boardsize - board.target_len + 1):
            for y in range(board.boardsize - board.target_len + 1):
                check_1 = 0
                check_2 = 0
                if (board.board[x + board.target_len - 1]
                   [y + board.target_len - 1] == EMPTY) and\
                   (board.board[x][y] == EMPTY):
                    for i in range(0, board.target_len):
                        if board.board[x + board.target_len - 1 - i][y
                           + board.target_len - 1 - i] == HUMAN:
                            check_1 += 1
                        if board.board[x + board.target_len - 1 - i][y
                           + board.target_len - 1 - i] == AINUM:
                            check_2 += 1
                    if (check_1 == TWO) & (check_2 == ZERO):
                        two_human += 1
                    if (check_2 == TWO) & (check_1 == ZERO):
                        two_ai += 1

        # scoring for live two
        # human's turn
        if self.gc.cur_step % MODNUM == 0:
            if (two_human >= ONE):
                return -TWENTY
            if (two_ai >= ONE):
                return TWENTY
        # ai's turn
        else:
            if (two_ai >= ONE):
                return TWENTY
            if (two_human >= ONE):
                return -TWENTY

        # sleep two
        # not both 0, or both 1
        # not 1 and 2
        # can only be 0,1 or 0,2
        sleep_two_human = 0
        sleep_two_ai = 0

        # horizontal
        for x in range(board.boardsize - board.target_len):
            for y in range(board.boardsize):
                check_1 = 0
                check_2 = 0
                if (board.board[x][y] != board.board
                   [x + board.target_len - 1][y]
                   and board.board[x][y] + board.board
                   [x + board.target_len - 1][y] <= 2):
                    for i in range(0, board.target_len):
                        if board.board[x + i][y] == HUMAN:
                            check_1 += 1
                        if board.board[x + i][y] == AINUM:
                            check_2 += 1
                    if (check_1 == TWO) & (check_2 == ZERO):
                        sleep_two_human += 1
                    if (check_2 == TWO) & (check_1 == ZERO):
                        sleep_two_ai += 1

        # vertical
        for x in range(board.boardsize):
            for y in range(board.boardsize - board.target_len):
                check_1 = 0
                check_2 = 0
                if (board.board[x][y] != board.board
                   [x][y + board.target_len - 1]
                   and board.board[x][y] + board.board
                   [x][y + board.target_len - 1] <= 2):
                    for i in range(0, board.target_len):
                        if board.board[x][y + i] == HUMAN:
                            check_1 += 1
                        if board.board[x][y + i] == AINUM:
                            check_2 += 1
                    if (check_1 == TWO) & (check_2 == ZERO):
                        sleep_two_human += 1
                    if (check_2 == TWO) & (check_1 == ZERO):
                        sleep_two_ai += 1

        # top right to down left
        for x in range(board.boardsize - board.target_len + 1):
            for y in range(board.boardsize - board.target_len + 1):
                check_1 = 0
                check_2 = 0
                if (board.board[x + board.target_len - 1][y] != board.board
                   [x][y + board.target_len - 1]
                   and board.board[x + board.target_len - 1][y] + board.board
                   [x][y + board.target_len - 1] <= 2):
                    for i in range(0, board.target_len):
                        if board.board[x + i][y + board.target_len
                           - 1 - i] == HUMAN:
                            check_1 += 1
                        if board.board[x + i][y + board.target_len
                           - 1 - i] == AINUM:
                            check_2 += 1
                    if (check_1 == TWO) & (check_2 == ZERO):
                        sleep_two_human += 1
                    if (check_2 == TWO) & (check_1 == ZERO):
                        sleep_two_ai += 1

        # top left to down right
        for x in range(board.boardsize - board.target_len + 1):
            for y in range(board.boardsize - board.target_len + 1):
                check_1 = 0
                check_2 = 0
                if (board.board[x][y] != board.board
                   [x + board.target_len - 1][y + board.target_len - 1]
                   and board.board[x][y] + board.board
                   [x + board.target_len - 1][y + board.target_len - 1] <= 2):
                    for i in range(0, board.target_len):
                        if board.board[x + board.target_len - 1 - i][y
                           + board.target_len - 1 - i] == HUMAN:
                            check_1 += 1
                        if board.board[x + board.target_len - 1 - i][y
                           + board.target_len - 1 - i] == AINUM:
                            check_2 += 1
                    if (check_1 == TWO) & (check_2 == ZERO):
                        sleep_two_human += 1
                    if (check_2 == TWO) & (check_1 == ZERO):
                        sleep_two_ai += 1

        # scoring for sleep two
        # human's turn
        if self.gc.cur_step % MODNUM == 0:
            if (sleep_two_human >= ONE):
                return -TEN
            if (sleep_two_ai >= ONE):
                return TEN
        # ai's turn
        else:
            if (sleep_two_ai >= ONE):
                return TEN
            if (sleep_two_human >= ONE):
                return -TEN

        return ZERO
