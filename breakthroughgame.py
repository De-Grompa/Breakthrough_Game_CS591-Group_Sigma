import pygame
import sys, os, math
from minimax import *
from model import *
from alpha_beta import *
import time

class BreakthroughGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 700, 560
        self.cellSize = int(560/8)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([255, 255, 255])
        # Create board and pieces
        self.board = 0
        self.blackpiece = 0
        self.whitepiece = 0
        self.outline = 0
        self.reset = 0
        self.winner = 0
        self.computer = None

        # Status 0: Origin; 1: Ready to move; 2: Moved
        self.status = 0
        self.turn = 1

        # Set variables for moving
        self.origin_x = 0
        self.origin_y = 0
        self.dest_x = 0
        self.dest_y = 0

        # Matrix for the board, 0 for empty, 1 for black, 2 for white
        self.board_matrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1], 
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0], 
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [2, 2, 2, 2, 2, 2, 2, 2],
                             [2, 2, 2, 2, 2, 2, 2, 2]]

        self.total_nodes_black = 0
        self.total_nodes_white = 0
        self.total_time_black = 0
        self.total_time_white = 0
        self.total_steps_black = 0
        self.total_steps_white = 0
        self.eat_piece = 0

        # Title
        pygame.display.set_caption("Breakthrough Game")

        # Initialize pygame clock
        self.clock = pygame.time.Clock()
        self.initgraphics()

    def run(self):
        self.clock.tick(60)

        # Track the total game tree nodes for each player

        # Clear the screen
        self.screen.fill([255, 255, 255])

        if self.status == 5:

            # Black's turn
            if self.turn == 1:
                start = time.process_time()
                # 1 - minimax, 2 - alpha-beta, (1 - offHeuristic1, 2 - defHeuristic1, 3 - offHeuristic2, 4 - defHeuristic2)
                self.ai_move(2,3)
                self.total_time_black += (time.process_time() - start)
                self.total_steps_black += 1
                print('total_steps_black = ', self.total_steps_black,
                      'total_gametree_nodes_black = ', self.total_nodes_black,
                      'nodes_per_move_black = ', self.total_nodes_black/self.total_steps_black,
                      'time_per_move_black = ', self.total_time_black/self.total_steps_black,
                      'have_eaten = ', self.eat_piece)
            # White's turn
            elif self.turn == 2:
                start = time.process_time()
                # (1 - minimax, 2 - alpha-beta), (1 - offHeuristic1, 2 - defHeuristic1, 3 - offHeuristic2, 4 - defHeuristic2)
                self.ai_move(2,2)
                self.total_time_white += (time.process_time() - start)
                self.total_steps_white += 1
                print('total_steps_white = ', self.total_steps_white,
                      'total_gametree_nodes_white = ', self.total_nodes_white,
                      'nodes_per_move_white = ', self.total_nodes_white/self.total_steps_white,
                      'time_per_move_white = ', self.total_time_white/self.total_steps_white,
                      'have_eaten = ', self.eat_piece)

        #Perform event handling
        for event in pygame.event.get():
            # Quit the game if the user presses the close button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Reset game if the user presses the reset button
            elif event.type == pygame.MOUSEBUTTONDOWN and self.isreset(event.pos):
                self.board_matrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                                     [1, 1, 1, 1, 1, 1, 1, 1],
                                     [0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0],
                                     [2, 2, 2, 2, 2, 2, 2, 2],
                                     [2, 2, 2, 2, 2, 2, 2, 2]]
                self.turn = 1
                self.status = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and self.iscomputer(event.pos):
                self.ai_move_alphabeta(1)

            elif event.type == pygame.MOUSEBUTTONDOWN and self.isauto(event.pos):
                self.status = 5

            # ===========================================
            # If the user clicks on the board
            elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 0:
                x, y = event.pos
                coor_x = math.floor(y/self.cellSize)
                coor_y = math.floor(x/self.cellSize)
                if self.board_matrix[coor_x][coor_y] == self.turn:
                    self.status = 1
                    self.origin_x = math.floor(y / self.cellSize)
                    self.origin_y = math.floor(x / self.cellSize)
            # Check whether the piece can move, otherwise select another piece
            elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 1:
                x, y = event.pos
                self.dest_x = math.floor(y / self.cellSize)
                self.dest_y = math.floor(x / self.cellSize)
                if self.isabletomove():
                    self.movepiece()
                    if (self.dest_x == 7 and self.board_matrix[self.dest_x][self.dest_y] == 1) \
                            or (self.dest_x == 0 and self.board_matrix[self.dest_x][self.dest_y] == 2):
                        self.status = 3
                    elif self.board_matrix[self.dest_x][self.dest_y] == self.board_matrix[self.origin_x][self.origin_y]:
                        self.origin_x = self.dest_x
                        self.origin_y = self.dest_y
        self.display()
        #update the screen
        pygame.display.flip()

    # Load the images and rescacle them
    def initgraphics(self):
        self.board = pygame.image.load_extended(os.path.join('src', 'chessboard.jpg'))
        self.board = pygame.transform.scale(self.board, (560, 560))
        self.blackcircle = pygame.image.load_extended(os.path.join('src', 'blackcircle.png'))
        self.blackcircle = pygame.transform.scale(self.blackcircle, (self.cellSize- 20, self.cellSize - 20))
        self.whitecircle = pygame.image.load_extended(os.path.join('src', 'whitecircle.png'))
        self.whitecircle = pygame.transform.scale(self.whitecircle, (self.cellSize - 20, self.cellSize - 20))
        self.outline = pygame.image.load_extended(os.path.join('src', 'square-outline.png'))
        self.outline = pygame.transform.scale(self.outline, (self.cellSize, self.cellSize))
        self.reset = pygame.image.load_extended(os.path.join('src', 'reset.jpg'))
        self.reset = pygame.transform.scale(self.reset, (80, 80))
        self.winner = pygame.image.load_extended(os.path.join('src', 'winner.png'))
        self.winner = pygame.transform.scale(self.winner, (250, 250))
        self.computer = pygame.image.load_extended(os.path.join('src', 'computer.png'))
        self.computer = pygame.transform.scale(self.computer, (80, 80))
        self.auto = pygame.image.load_extended(os.path.join('src', 'auto.png'))
        self.auto = pygame.transform.scale(self.auto, (80, 80))

    # display the graphics in the window
    def display(self):
        self.screen.blit(self.board, (0, 0))
        self.screen.blit(self.reset, (590, 50))
        self.screen.blit(self.computer, (590, 200))
        self.screen.blit(self.auto, (590, 340))
        #Check if the board has a 1, insert a black circle. If the board has a 2, insert a white circle
        for i in range(8):
            for j in range(8):
                if self.board_matrix[i][j] == 1:
                    self.screen.blit(self.blackcircle, (self.cellSize * j + 10, self.cellSize * i + 10))
                elif self.board_matrix[i][j] == 2:
                    self.screen.blit(self.whitecircle, (self.cellSize * j + 10, self.cellSize * i + 10))
        if self.status == 1:
            # Character can only move downward
            if self.board_matrix[self.origin_x][self.origin_y] == 1:
                x1 = self.origin_x + 1
                y1 = self.origin_y - 1
                x2 = self.origin_x + 1
                y2 = self.origin_y + 1
                x3 = self.origin_x + 1
                y3 = self.origin_y
                # Down-left
                if y1 >= 0 and self.board_matrix[x1][y1] != 1:
                    self.screen.blit(self.outline,
                                     (self.cellSize * y1, self.cellSize * x1))
                # Down-right
                if y2 <= 7 and self.board_matrix[x2][y2] != 1:
                    self.screen.blit(self.outline,
                                     (self.cellSize * y2, self.cellSize * x2))
                # Down
                if x3 <= 7 and self.board_matrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.cellSize * y3, self.cellSize * x3))

            # Character can only move upward
            if self.board_matrix[self.origin_x][self.origin_y] == 2:
                x1 = self.origin_x - 1
                y1 = self.origin_y - 1
                x2 = self.origin_x - 1
                y2 = self.origin_y + 1
                x3 = self.origin_x - 1
                y3 = self.origin_y
                # Up-left
                if y1 >= 0 and self.board_matrix[x1][y1] != 2:
                    self.screen.blit(self.outline,
                                     (self.cellSize * y1, self.cellSize * x1))
                # Up-right
                if y2 <= 7 and self.board_matrix[x2][y2] != 2:
                    self.screen.blit(self.outline,
                                     (self.cellSize * y2, self.cellSize * x2))
                # Up
                if x3 >= 0 and self.board_matrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.cellSize * y3, self.cellSize * x3))
        if self.status == 3:
            self.screen.blit(self.winner, (100, 100))

    # Function to move the piece
    def movepiece(self):
        self.board_matrix[self.dest_x][self.dest_y] = self.board_matrix[self.origin_x][self.origin_y]
        self.board_matrix[self.origin_x][self.origin_y] = 0
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.status = 0

    # Function to check if the board is reset
    def isreset(self, pos):
        x, y = pos
        if 670 >= x >= 590 and 50 <= y <= 130:
            return True
        return False

    # Function to check if the computer is selected
    def iscomputer(self, pos):
        x, y = pos
        if 590 <= x <= 670 and 200 <= y <= 280:
            return True
        return False

    # Function to check if the auto button is selected
    def isauto(self, pos):
        x, y = pos
        if 590 <= x <= 670 and 340 <= y <= 420:
            return True
        return False

    # Function to check if the piece can move
    def isabletomove(self):
        if (self.board_matrix[self.origin_x][self.origin_y] == 1
            and self.board_matrix[self.dest_x][self.dest_y] != 1
            and self.dest_x - self.origin_x == 1
            and self.origin_y - 1 <= self.dest_y <= self.origin_y + 1
            and not (self.origin_y == self.dest_y and self.board_matrix[self.dest_x][self.dest_y] == 2)) \
            or (self.board_matrix[self.origin_x][self.origin_y] == 2
                and self.board_matrix[self.dest_x][self.dest_y] != 2
                and self.origin_x - self.dest_x == 1
                and self.origin_y - 1 <= self.dest_y <= self.origin_y + 1
                and not (self.origin_y == self.dest_y and self.board_matrix[self.dest_x][self.dest_y] == 1)):
            return 1
        return 0

    # Function to move the piece automatically
    def ai_move(self, searchtype, evaluation):
        if searchtype == 1:
            return self.ai_move_minimax(evaluation)
        elif searchtype == 2:
            return self.ai_move_alphabeta(evaluation)
    
    # Function to move the piece using minimax
    def ai_move_minimax(self, function_type):
        board, nodes, piece = MinimaxAgent(self.board_matrix, self.turn, 3, function_type).minimax_decision()
        self.board_matrix = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_black += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_white += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.is_goal_state():
            self.status = 3

    # Function to move the piece using alpha-beta
    def ai_move_alphabeta(self, function_type):
        board, nodes, piece = AlphaBetaAgent(self.board_matrix, self.turn, 4, function_type).alpha_beta_decision()
        self.board_matrix = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_black += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_white += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.is_goal_state():
            self.status = 3

    # Function to check if the game is over
    # If the game is over, return True, else return False
    def is_goal_state(self, base=0):
        if base == 0:
            if 2 in self.board_matrix[0] or 1 in self.board_matrix[7]:
                return True
            else:
                for line in self.board_matrix:
                    if 1 in line or 2 in line:
                        return False
            return True
        else:
            count = 0
            for i in self.board_matrix[0]:
                if i == 2:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.board_matrix[7]:
                if i == 1:
                    count += 1
            if count == 3:
                return True
            count1 = 0
            count2 = 0
            for line in self.board_matrix:
                for i in line:
                    if i == 1:
                        count1 += 1
                    elif i == 2:
                        count2 += 1
            if count1 <= 2 or count2 <= 2:
                return True
        return False

def main():
    game = BreakthroughGame()
    while 1:
        game.run()


if __name__ == '__main__':
    main()