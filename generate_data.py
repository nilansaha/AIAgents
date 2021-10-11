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
training_games = games[:-200]
testing_games = games[-200:]

np.savetxt("training_games.out", training_games, delimiter=",", fmt="%i")
np.savetxt("testing_games.out", testing_games, delimiter=",", fmt="%i")

print("Training Games size", len(training_games))
print("Testing Games size", len(testing_games))
