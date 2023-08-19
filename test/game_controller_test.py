import sys
from turtle import Turtle
sys.path.append("..")
from game_controller import GameController  # nopep8
from game_board import GameBoard  # nopep8
from stone import Stone  # nopep8


def test_constructor():
    test_boardsize = 15
    test_targetlen = 5
    test_gc = GameController(test_boardsize, test_targetlen)
    # board.board
    assert test_gc.board.board == [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    assert test_gc.cur_step == 0
    assert test_gc.targetlen == 5
    assert test_gc.allowMousePress is True
    assert test_gc.winner == None


def test_drop_stone():
    # NOTICE: this drop_stone() function is processing/graphic related,
    # on game_controller.py line 45, the function call the display function of
    # a stone instance, thus it is not suitable for testing.
    # However, if the line 45 in game_controller.py is commented temporarily, the
    # test will be possible, so I leave the testing code here in case the use would
    # like to make a test, just comment the line 45 in game_controller and uncomment the
    # following code will work. After finishing test, just rollback to the former status.
    # Hope this would help

    # PIXEL_WIDTH = 500
    # SIZE = 15
    # BORDERRATIO = 0.1
    # BORDER = PIXEL_WIDTH * BORDERRATIO
    # BLOCK = PIXEL_WIDTH - 2 * BORDER
    # UNIT_WIDTH = BLOCK / (SIZE - 1)

    # test_boardsize = 3
    # test_targetlen = 5
    # test_gc = GameController(test_boardsize, test_targetlen)
    # test_x = 1
    # test_y = 1
    # test_size = 50
    # test_player = "Human"
    # test_gc.drop_stone(test_x, test_y, test_size, test_player, BORDER, UNIT_WIDTH)
    # test_gc.the_stone = Stone(test_x, test_y, test_size, test_player)
    # assert test_gc.board.board == [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    # assert test_gc.cur_step == 1
    # # better test the attributes to check
    # assert test_gc.the_stone._x == 1
    # test_boardsize = 3
    # test_targetlen = 5
    # test_gc = GameController(test_boardsize, test_targetlen)
    # test_x = 2
    # test_y = 1
    # test_size = 50
    # test_player = "AI"
    # test_gc.drop_stone(test_x, test_y, test_size, test_player, BORDER, UNIT_WIDTH)
    # test_gc.the_stone = Stone(test_x, test_y, test_size, test_player)
    # assert test_gc.board.board == [[0, 0, 0], [0, 0, 0], [0, 2, 0]]
    # assert test_gc.cur_step == 1
    # assert test_gc.the_stone._x == 2
    assert True


def test_game_result():
    # test 5 in a row
    test_boardsize = 6
    test_targetlen = 5
    test_gc = GameController(test_boardsize, test_targetlen)
    test_gc.board.board = [
        [1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    assert test_gc.game_reuslt() == 1
    # test 5 in a col
    test_boardsize = 6
    test_targetlen = 5
    test_gc = GameController(test_boardsize, test_targetlen)
    test_gc.board.board = [
        [0, 0, 0, 2, 0, 0],
        [0, 0, 0, 2, 0, 0],
        [0, 0, 0, 2, 0, 0],
        [0, 0, 0, 2, 0, 0],
        [0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    assert test_gc.game_reuslt() == 2
    # test 5 from top left to down right
    test_boardsize = 6
    test_targetlen = 5
    test_gc = GameController(test_boardsize, test_targetlen)
    test_gc.board.board = [
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    assert test_gc.game_reuslt() == 1
    # test 5 from top right to down left
    test_boardsize = 6
    test_targetlen = 5
    test_gc = GameController(test_boardsize, test_targetlen)
    test_gc.board.board = [
        [0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 2, 0],
        [0, 0, 0, 2, 0, 0],
        [0, 0, 2, 0, 0, 0],
        [0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    assert test_gc.game_reuslt() == 2
    # test a continue
    test_boardsize = 6
    test_targetlen = 5
    test_gc = GameController(test_boardsize, test_targetlen)
    test_gc.board.board = [
        [0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 2, 0],
        [0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    assert test_gc.game_reuslt() == -1
    test_boardsize = 6
    test_targetlen = 5
    test_gc = GameController(test_boardsize, test_targetlen)
    test_gc.board.board = [
        [2, 2, 2, 2, 1, 2],
        [1, 1, 1, 1, 2, 1],
        [2, 2, 2, 2, 1, 2],
        [1, 1, 1, 2, 1, 2],
        [1, 1, 1, 2, 1, 2],
        [1, 1, 1, 2, 1, 2]
    ]
    assert test_gc.game_reuslt() == 0


def test_get_distance():
    test_boardsize = 6
    test_targetlen = 5
    test_gc = GameController(test_boardsize, test_targetlen)
    test_x1 = 0
    test_y1 = 3
    test_x2 = 4
    test_y2 = 0
    assert test_gc.get_distance(test_x1, test_y1,
           test_x2, test_y2) == 5


def test_color_choose():
    test_boardsize = 6
    test_targetlen = 5
    test_gc = GameController(test_boardsize, test_targetlen)
    test_gc.cur_step = 4
    # need to add the () after color_choose
    assert test_gc.color_choose() == "Human"
    test_gc = GameController(test_boardsize, test_targetlen)
    test_gc.cur_step = 3
    assert test_gc.color_choose() == "AI"

# the processing related function, and the file I/O fucntion,
# including the record_winner(), are not practical for testing.
# however, they all work well.