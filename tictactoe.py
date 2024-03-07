import random


class TicTacToe():

    def __init__(self, players: list):
        # self.x = [players.pop(random.randint(0,1)), "x"]
        # self.o = [players[0], "o"]
        self.players = {
            "o": players.pop(random.randint(0, 1)),
            "x": players[0]
        }
        self.currenturn = "o"
        self.board = [[" " for x in range(3)] for i in range(3)]
        self.winner = False

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

    def get_current_player_name(self):
        return self.players[self.get_current_turn()]

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
        if self.board[y_coord][x_coord] != " ":
            return False
        return True

    def _winner_check(self):
        for i in range(3):
            # Check each row

            if len(set(self.board[i])) == 1 and self.board[i][0] != ' ':
                return f"{self.players[self.board[i][0]]}' won!"

            # check column
            column_set = set()
            for row in self.board:
                column_set.add(row[i])
            if len(column_set) == 1 and self.board[0][i] != ' ':
                return f"{self.players[self.board[i][0]]} won!"

        # Check diagonals
        if len(set(self.board[i][i] for i in range(3))) == 1 and self.board[0][0] != ' ':
            return f"{self.players[self.board[0][0]]} won!"
        if len(set(self.board[i][2-i] for i in range(3))) == 1 and self.board[0][2] != ' ':
            return f"{self.players[self.board[0][2]]} won!"
        return None

    def _draw_check(self):
        for row in self.board:
            if row.count(" ") > 0:
                return False
        return True

    def play_move(self, player, move: list) -> tuple:
        """Plays a move

        Args:
            player (obj): any obj/type that identifies a player.
            move (list): [x, y]

        Returns:
            tuple: (return string, boolean whether or not the game is still going)
        """
        # Prevent players from making additional moves
        if self.winner:
            return ("Game over", True)

        if not self._is_player_turn(player):
            # Change wording on this
            return (f"It is {self.get_current_player_name()}'s turn", False)

        if not self._validate_move(move):
            return ("Invalid move", False)

        x_coord = move[0]
        y_coord = move[1]
        self.board[y_coord][x_coord] = self.get_current_turn()

        # Change turn
        self._change_turn()

        # Check for winner
        winner = self._winner_check()
        if winner is not None:
            self.winner = True
            return (winner, True)

        # Check for draw
        if self._draw_check():
            self.winner = True
            return ("Draw!", True)
        return (f"{self.get_current_player_name()} turn", False)
