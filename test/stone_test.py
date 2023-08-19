import sys
sys.path.append("..")
from stone import Stone  # nopep8


def test_constructor():
    test_x = 1
    test_y = 2
    test_ez = 50
    test_player = "Human"
    test_stone = Stone(test_x, test_y, test_ez, test_player)
    assert test_stone._x == 1
    assert test_stone._y == 2
    assert test_stone._WHITE == (255, 255, 255)
    assert test_stone._BLACK == (0, 0, 0)
    assert test_stone._ELLIPSE_SIZE == 50
    assert test_stone.player == "Human"
    assert test_stone.x == 1
    assert test_stone.y == 2
