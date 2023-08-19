from game_controller import GameController
from ai import AI

PIXEL_WIDTH = 500
SIZE = 15
TARGETLEN = 5
BORDERRATIO = 0.1
BORDER = PIXEL_WIDTH * BORDERRATIO
BLOCK = PIXEL_WIDTH - 2 * BORDER
UNIT_WIDTH = BLOCK / (SIZE - 1)
BG_COLOR = (140, 100, 0)
ELLIPSE_SIZE = 0.5 * UNIT_WIDTH
HORIZ_MID = 250
VERT_MID = 250
WHITE = 255
FONT_SIZE = 36
DRAW = 0
HUMAN = 1
AINUM = 2
CONTINUE = -1
WAIT = 1000
TIMENUM = 0

field = (PIXEL_WIDTH, PIXEL_WIDTH)
gc = GameController(SIZE, TARGETLEN)


def setup():
    """
    Setup the board background
    """
    TIMENUM = 0
    size(*field)
    strokeWeight(5)
    background(*BG_COLOR)
    fill(*BG_COLOR)
    rect(BORDER, BORDER, BLOCK, BLOCK)
    for i in range(SIZE):
        line(BORDER + i * UNIT_WIDTH, BORDER, BORDER + i * UNIT_WIDTH, PIXEL_WIDTH - BORDER)
        line(BORDER, BORDER + i * UNIT_WIDTH, PIXEL_WIDTH - BORDER, BORDER + i * UNIT_WIDTH)


def draw():
    """
    Draw the enviroment and stones
    """
    if gc.game_reuslt() == CONTINUE:
        if gc.cur_step % AINUM == 0:
            gc.allowMousePress = True
        else:
            if millis() - startTime >= 100:
                ai = AI(gc)
                px, py = ai.best_choice(gc)
                gc.drop_stone(px, py, ELLIPSE_SIZE, 'AI', BORDER, UNIT_WIDTH)
    if gc.game_reuslt() == HUMAN:
        # record the winner name
        answer = input('enter your name')
        gc.winner = str(answer)
        if answer:
            print('hi ' + answer)
        elif answer == '':
            print('[empty string]')
        else:
            # Canceled dialog will print None
            print(answer) 
        gc.record_winner(gc.winner)
        final_word = answer + " Wins!"
        fill(WHITE)
        textSize(FONT_SIZE)
        textAlign(CENTER)
        text(final_word, HORIZ_MID, VERT_MID)
        noLoop()
    if gc.game_reuslt() == AINUM:
        fill(WHITE)
        textSize(FONT_SIZE)
        textAlign(CENTER)
        text("AI Wins", HORIZ_MID, VERT_MID)
        noLoop()
    if gc.game_reuslt() == DRAW:
        fill(WHITE)
        textSize(FONT_SIZE)
        textAlign(CENTER)
        text("It's a draw", HORIZ_MID, VERT_MID)
        noLoop()


def mousePressed():
    """
    1. Drop the stone to the nearest when mouse is pressed
    2. Auto-switch the color when there are two human players
    3. Display end text in terminal when the board is full
    """
    gc.choose_nearast(mouseX, mouseY, BORDER, PIXEL_WIDTH, UNIT_WIDTH)
    global startTime
    startTime = millis()


def input(self, message=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)
