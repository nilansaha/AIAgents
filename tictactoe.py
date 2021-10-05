import numpy as np


class TicTacToe:
    def __init__(self, board_size, n_spot_win):
        self.board_size = board_size
        self.n_spot_win = n_spot_win
        self.total_spots = board_size ** 2
        self.state = [-1] * self.total_spots
        self.turn = 0
        self.done = False
        self.winner = False
        self.move_history = []
        self.state_history = [[-1] * self.total_spots]

    def render(self):
        formatted_state = np.array(self.state).reshape(self.board_size, self.board_size)
        print(
            np.array_str(formatted_state)
            .replace("[[", " ")
            .replace("[", "")
            .replace("]", "")
        )
