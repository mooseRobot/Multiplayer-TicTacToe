import random
class TicTacToe():
    
    def __init__(self, players: list):
        self.x = players.pop(random.choice(players))
        self.o = players[0]
        self.currenturn = self.o
        self.board = [["" for x in range(3)] for i in range(3)]

    def print_board(self):
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