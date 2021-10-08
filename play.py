from game import Game
from tictactoe import TicTacToe
from players import RandomPlayer, HumanPlayer, TreePlayerV1, TreePlayerV2, TreePlayerV3


# env = TicTacToe(5, 4)
# player1 = RandomPlayer(env)
# player2 = HumanPlayer(env)

# game = Game(env, player1, player2, verbose=True)
# game.play()

# win_stats = {-1: 0, 0: 0, 1: 0}

# for _ in range(100):
#     env = TicTacToe(5, 4)
#     player1 = RandomPlayer(env)
#     player2 = RandomPlayer(env)

#     game = Game(env, player1, player2, verbose=True)
#     game.play()
#     win_stats[game.winner] += 1

# print(win_stats)

# env = TicTacToe(3, 3)
# player1 = TreePlayerV1(env)
# player2 = HumanPlayer(env)

# game = Game(env, player1, player2, verbose=True)
# game.play()

env = TicTacToe(3, 3)
player1 = TreePlayerV1(env)
player2 = HumanPlayer(env)

game = Game(env, player1, player2, verbose=True)
game.play()


# win_stats = {-1: 0, 0: 0, 1: 0}

# for _ in range(100):
#     env = TicTacToe(3, 3)
#     player1 = TreePlayerV1(env)
#     player2 = RandomPlayer(env)

#     game = Game(env, player1, player2, verbose=True)
#     game.play()
#     win_stats[game.winner] += 1

# print(win_stats)
