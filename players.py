import random


class Player:
    def __init__(self, env):
        self.env = env

    def get_move(self):
        pass


class RandomPlayer(Player):
    def get_move(self):
        pos = random.choice(self.env.available_moves())
        return pos


class HumanPlayer(Player):
    def get_move(self):
        pos = int(input("\n"))
        return pos
