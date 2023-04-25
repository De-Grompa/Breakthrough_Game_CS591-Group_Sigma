from model import *

# This is the alpha_beta_agent.py file
# 
# Class AlphaBetaAgent (decides the next move for the AI)
class AlphaBetaAgent:
    def __init__(self, boardmatrix, turn, depth, function, type=0):
        self.boardmatrix = boardmatrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type

        self.nodes = 0
        self.piece_num = 0
    # max_value function
    def maximum_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.is_goal_state() != 0:
            return state.utility(self.turn)
        v = MINFLOAT
        actions = state.available_actions()

        if self.turn == 1:
            actions = sorted(state.available_actions(), key=lambda action: self.orderaction(action, state), reverse=True)
        else:
            actions = sorted(state.available_actions(), key=lambda action: self.orderaction(action, state))

        for action in actions:
            self.nodes += 1

            v = max(v, self.minimum_value(state.transfer(action), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    # min_value function
    def minimum_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.is_goal_state() != 0:
            return state.utility(self.turn)
        v = MAXFLOAT
        actions = state.available_actions()

        if self.turn == 1:
            actions = sorted(state.available_actions(), key=lambda action: self.orderaction(action, state))
        else:
            actions = sorted(state.available_actions(), key=lambda action: self.orderaction(action, state), reverse=True)

        for action in actions:
            self.nodes += 1

            v = min(v, self.maximum_value(state.transfer(action), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    # alpha_beta_decision function
    def alpha_beta_decision(self):
        final_action = None
        if self.type == 0:
            initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function)
        else:
            initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function, height=5, width=10)
        v = MINFLOAT
        for action in initialstate.available_actions():
            self.nodes += 1

            new_state = initialstate.transfer(action)
            if new_state.is_goal_state():
                final_action = action
                break
            minresult = self.minimum_value(new_state, MINFLOAT, MAXFLOAT, 1)
            if minresult > v:
                final_action = action
                v = minresult
        #print("this is v: ", v)
        if self.turn == 1:
            self.piece_num = initialstate.transfer(final_action).white_num
        elif self.turn == 2:
            self.piece_num = initialstate.transfer(final_action).black_num
        print(final_action.getString())
        return initialstate.transfer(final_action), self.nodes, self.piece_num

    # order actions to make more pruning
    def orderaction(self, action, state):
        y = action.coordinate[0]
        x = action.coordinate[1]
        #pruning for white
        if action.turn == 1:
            if action.direction == 1:
                if (y - 1, x - 1) in state.white_positions:
                    return 2
            if action.direction == 2:
                if (y - 1, x) in state.white_positions:
                    return 2
            if action.direction == 2:
                if (y - 1, x + 1) in state.white_positions:
                    return 2
        ##pruning for black
        elif action.turn == 2:
            if action.direction == 1:
                if (y + 1, x - 1) in state.black_positions:
                    return 2
            if action.direction == 2:
                if (y + 1, x) in state.black_positions:
                    return 2
            if action.direction == 2:
                if (y + 1, x + 1) in state.black_positions:
                    return 2
        return 0