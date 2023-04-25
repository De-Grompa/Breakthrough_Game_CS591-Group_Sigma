initial_boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [2, 2, 2, 2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2, 2, 2, 2]]

MAXFLOAT = float("inf")
MINFLOAT = float("-inf")
MAXTUPLE = (MAXFLOAT, MAXFLOAT)
MINTUPLE = (MINFLOAT, MINFLOAT)

# Direction: 1 = left, 2 = middle, 3 = right
def single_move(initial_pos, direction, turn):
    # turn 1 = white
    if turn == 1: 
        if direction == 1:
            return initial_pos[0] + 1, initial_pos[1] - 1
        elif direction == 2:
            return initial_pos[0] + 1, initial_pos[1]
        elif direction == 3:
            return initial_pos[0] + 1, initial_pos[1] + 1
    # turn 2 = black
    elif turn == 2:
        if direction == 1:
            return initial_pos[0] - 1, initial_pos[1] - 1
        elif direction == 2:
            return initial_pos[0] - 1, initial_pos[1]
        elif direction == 3:
            return initial_pos[0] - 1, initial_pos[1] + 1

# Switch turn
def switch_turn(turn):
    if turn == 1:
        return 2
    elif turn == 2:
        return 1

# Define action class
class Action:
    def __init__(self, initial_pos, direction, turn):
        self.initial_pos = initial_pos
        self.direction = direction
        self.turn = turn
    def getString(self):
        return self.initial_pos, self.direction, self.turn
    def getPosition_x(self):
        return self.initial_pos[0]

# Define state class
class State:
    def __init__(self, 
                 boardmatrix=None,
                 black_position=None,
                 white_position=None,
                 black_num=0,
                 white_num=0,
                 turn=1,
                 function=0,
                 width=8,
                 height=8):
        self.width = width
        self.height = height
        if black_position is None:
            self.black_position_list = []
        else:
            self.black_position_list = black_position
        if white_position is None:
            self.white_position_list = []
        else:
            self.white_position_list = white_position
        self.black_num = black_num
        self.white_num = white_num
        self.turn = turn
        self.function = function
        if boardmatrix is not None:
            for i in range(self.height):
                for j in range(self.width):
                    if boardmatrix[i][j] == 1:
                        self.black_position_list.append((i, j))
                        self.black_num += 1
                    if boardmatrix[i][j] == 2:
                        self.white_position_list.append((i, j))
                        self.white_num += 1

# Define t