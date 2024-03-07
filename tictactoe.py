import random
class TicTacToe():
    
    def __init__(self, players: list):
        self.x = players.pop(random.randint(0,1))
        self.o = players[0]
        self.currenturn = self.o
        self.board = [[" " for x in range(3)] for i in range(3)]

    def print_board(self):
        """Returns a string of the current board

        Returns:
            str: String of the current boaard
        """
        board_str = ""
        for i in range(3):
            for j in range(3):
                board_str += self.board[i][j]
                if j < 2:
                    board_str += "|"
            board_str += "\n"
            if i < 2:
                board_str += "-" * 5 + "\n"
        return board_str
    
    def get_x(self):
        return self.x
    
    def get_o(self):
        return self.o
    
    def get_current_turn(self):
        return self.currenturn
    
    def _change_turn(self):
        if self.currenturn == self.o:
            self.currenturn = self.x
        else:
            self.currenturn = self.o

    def play_move(self, player, move):
        pass
