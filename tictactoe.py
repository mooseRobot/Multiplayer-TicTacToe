import random
class TicTacToe():
    
    def __init__(self, players: list):
        # self.x = [players.pop(random.randint(0,1)), "x"]
        # self.o = [players[0], "o"]
        self.players = {
            "o": players.pop(random.randint(0,1)),
            "x": players[0]
        }
        self.currenturn = "o"
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
        return self.players["x"]
    
    def get_o(self):
        return self.players["o"]
    
    def get_current_turn(self):
        return self.currenturn
    
    def _change_turn(self):
        if self.currenturn == "o":
            self.currenturn = "x"
        else:
            self.currenturn = "o"

    def _is_player_turn(self, player):
        return player == self.players[self.currenturn]
    
    def _validate_move(self, move):
        # check if the move is within boundaries
        x_coord = move[0]
        y_coord = move[1]

        # Check valid boundaries
        if not 0 <= x_coord < 3:
            return False
        if not 0 <= y_coord < 3:
            return False
        
        # Check is the spot is open
        if move[y_coord][x_coord] != " ":
            return False
        return True
    
    def _winner_check(self):
        winner = False
        for i in range(3):
            # Check each row
            row = self.board[i]
            if len(set(row)) == 1 and row[0] != ' ':
                return f"{self.players[row[0]]}' won!"
            
            # check column
            if self.board[0][i] == self.board[1][i] and self.board[0][i] == self.board[2][i]:
                return

        # Check column

        # Check diagnols
        pass


    def _draw_check(self):
        for row in self.board:
            if row.count(" ") > 0:
                return True
        return False


    def place_move(self, player, move: list) -> str:
        if not self._is_player_turn(player):
            return f"It is {self.get_current_turn()}'s turn"  # Change wording on this
        
        if not self._validate_move(move):
            return "Invalid move"
        
        x_coord = move[0]
        y_coord = move[1]
        self.board[y_coord][x_coord] = self.get_current_turn()
        
        # Change turn
        self._change_turn()

        # Check for winner

        # Check for draw


