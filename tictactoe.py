import numpy as np
from copy import deepcopy


class TicTacToe:
    def __init__(self, board_size, n_spot_win):
        self.board_size = board_size
        self.n_spot_win = n_spot_win
        self.total_spots = board_size ** 2
        self.state = [-1] * self.total_spots
        self.turn = 0
        self.done = False
        self.winner = -1
        self.move_history = []
        self.state_history = [[-1] * self.total_spots]

    def is_win(self):
        def _check_sequential_win(sequence):
            last_spot = sequence[0]
            counter = 1

            for spot in sequence[1:]:
                if spot == last_spot and last_spot != -1:
                    counter += 1
                    if counter == self.n_spot_win:
                        return True
                else:
                    last_spot = spot
                    counter = 1
            return False

        # checking row sequences
        row_sequences = np.array(self.state).reshape(self.board_size, self.board_size)
        for row in row_sequences:
            if _check_sequential_win(row):
                return True

        # checking column sequences
        column_sequences = row_sequences.transpose()
        for column in column_sequences:
            if _check_sequential_win(column):
                return True

        # checking left slope sequences
        np_state = np.reshape(self.state, (self.board_size, self.board_size))
        for i in range(-self.board_size + 1, self.board_size):
            seq = np_state.diagonal(i)
            if len(seq) >= self.n_spot_win and _check_sequential_win(seq):
                return True

        # checking right slope sequences
        flipped_np_state = np.flip(np_state, 1)
        for i in range(-self.board_size + 1, self.board_size):
            seq = flipped_np_state.diagonal(i)
            if len(seq) >= self.n_spot_win and _check_sequential_win(seq):
                return True

        return False

    def move(self, pos):
        if self.state[pos] != -1:
            raise Exception("Illegal move. Spot already occupied")

        self.state[pos] = self.turn
        self.move_history.append(pos)
        self.state_history.append(deepcopy(self.state))

        if self.is_win():
            self.done = True
            self.winner = self.turn
        else:
            if len(self.available_moves()) > 0:
                self.done = False
            else:
                self.done = True

        self.turn = 1 - self.turn
        return self.done, self.winner

    def available_moves(self):
        if not self.done:
            return [pos for pos, val in enumerate(self.state) if val == -1]
        return []

    def render(self):
        formatted_state = np.array(self.state).reshape(self.board_size, self.board_size)
        print(
            np.array_str(formatted_state)
            .replace("[[", " ")
            .replace("[", "")
            .replace("]", "")
            .replace("-1", " .")
        )


env = TicTacToe(5, 4)
env.move(6)
env.move(0)
env.move(7)
env.move(1)
env.move(8)
env.move(2)
env.move(9)
env.render()
print("Win", env.is_win())

done = False
winner = None
env = TicTacToe(5, 4)
while not done:
    print()
    pos = int(input())
    done, winner = env.move(pos)
    env.render()

print("Winner", winner)
