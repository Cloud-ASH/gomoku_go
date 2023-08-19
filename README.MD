1) What data structures you’ll need (lists, dictionaries, etc.)
- List of lists: represents the board, records stone locations

What classes you’ll define
- GameController
- AI
- Gameboard
- Stone


2) What functions you’ll need (methods within classes, 
or other functions that exist outside of any class)
- GameController
    · drop_stone
    · game_result
    · get_distance
    · allowMousePress
    · choose_nearest
    · color_choose
    · end_text
- AI
    · update
    · _choose_coord
    · _four_stones
    · _three_stones
    · _two_stones
    · _one_stone
    · _focus_on_self
- Gameboard
- Stone
    · display
    · x
    · y


3) A short description of each class and function/method
- GameController: controls the overall flow of the game at top level
    · drop_stone: place a stone on board
    · game_result: access the status of the game, whether it's continuing to play
        a draw, human as the winner, or AI as the winner
    · get_distance: return the distance between two points
    · allowMousePress: getter and setter for allowMousePress
    · choose_nearest: drop the stone to the nearest intersection when mouse is pressed,
        auto-switch the color when there are two human players (for the part 1 demo), 
        display the end text
    · color_choose: choose the color of the stone for each step
    · end_text: display the end text when the game is over
- AI: represents the AI and contains the logic to play and win
    · update: choose the next position to place the stone and do it
    · _choose_coord: score coords and return top scored coord
    · _four_stones: check if there is any four stones in line placed by human 
	    that AI could still place one stone to prevent human from winning
    · _three_stones: check if there is any three stones in line placed by human
	    if so, AI must place one on either side (priority could matter)
    · _two_stones: similar to three stones, but checks if there is two stones in line
    · _one_stone: check for any stone placed alone by the human, if any neighbor spot
        could make it three or four or five. If so, AI must stop it. 
    · _focus_on_self: if AI has already checked all possible cases that 
        the human could outperform it, it will then focus on itself and seek for 
        the most advantageous choice.
- Gameboard: generates the chess board as the list of lists
- Stone: visualizes stones with certain characteristics
    · display: display the stone given who the player is and what the color of stone is
    · x: getter and setter for x value
    · y: getter and setter for y value

A bullet-pointed pseudocode of your driver: 
Tell us about the flow of control, and think about the following cases:
    When the user makes a move
    When it’s the computer’s turn
    When game over status is assessed
- Flow of control:
    Part 1. HW11:
    Currently, we only have two human player, Black and White.
    The flow of control is as follows:
    1. Black mouse pressed, then the mousePressed() in pyde file works:
        1.1 It initializes a GameController instance (with a GameBoard instance in it)
        1.2 It forward the parameter mouseX, mouseY, BORDER, PIXEL_WIDTH, UNIT_WIDTH into 
        GameController, activates the choose_nearest() function
        1.3 The choose_nearest() function converts mouseX, mouseY into coorditnates 
        of the board, activates drop_stone() function
        1.4 The drop_stone() fucntion store a value into the GameBoard instance in 
        GameController, create a Stone instance which displays itself on graphic interface, 
        increase self.cur_step by 1
        1.5 The GameController check whether the game ends, if not, 
        set self.allowMousePress = False, end this round.
    2. In the Draw() of pyde file, the self.allowMousePress is reset to Ture, when mouse is 
    pressed, mousePressed runs again
        2.1 What is different this time is: self.cur_step is 1 more than last time, 
        the choose_color() in GameController works, switch the color to White
    3. The game continues to run, until the board is filled, the end_text() in GameController 
    works, print("It's an end")


    Part 2. HW12:
    Full version:
    1. Human mouse pressed, then the mousePressed() in pyde file works and the folloing 
    step is the same as above.
    2. game_result() in GameController works, evaluate the current situation, if returns 
    0(draw), 1(Human wins), 2(AI wins), the game ends, end_text is printed
    if returns -1(continue), set self.allowMousePress = False, terminate human round.
    3. scoring function in AI class works, measureing the current board, give each pattern 
    (i.e. 5 in a row, 4 in a row, 3 in a row, etc.) a score, the most urgent pattern receives the highest score
    4. choose highest score function in AI class works, finds the most urgent pattern, returns 
    a (x, y) coorditnate to prevent human player from winning
    5. the (x, y) coorditnate is forwarded to drop_stone() in GameController, a white stone is 
    placed on the board, AI round ends

    Then, human round again, until game_result() detects that there is an end. 
    The end_text print("It's an end")

