import random
import numpy as np
from game import Game
from tictactoe import TicTacToe
from players import RandomPlayer

games = []

for _ in range(10000):
    env = TicTacToe(3, 3)
    player1 = RandomPlayer(env)
    player2 = RandomPlayer(env)

    game = Game(env, player1, player2, verbose=True)
    game.play()

    if env.done and env.winner == 0:
        non_winning_state = random.choice(env.state_history[:-1])
        winning_state = env.state_history[-1]

        winning_info = winning_state + [1]
        non_winning_info = non_winning_state + [0]

        games.append(winning_info)
        games.append(non_winning_info)

games = np.array(games)
print(games)

np.savetxt("games_data.out", games, delimiter=",", fmt="%i")

loaded_games = np.loadtxt("games_data.out", delimiter=",", dtype=int)
print(loaded_games)
print(len(loaded_games))

board_state = loaded_games[1, 0:-1]
outcome = loaded_games[1, -1]

print()
print(board_state)
print(outcome)
