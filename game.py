class Game:
    def __init__(self, env, player1, player2, verbose=False):
        self.env = env
        self.player1 = player1
        self.player2 = player2
        self.verbose = verbose
        self.done = False
        self.winner = -1

    def play(self):
        while True:
            pos = self.player1.get_move()
            self.done, self.winner = self.env.move(pos)
            if self.verbose:
                print()
                self.env.render()
            if self.done:
                break

            pos = self.player2.get_move()
            self.done, self.winner = self.env.move(pos)
            if self.verbose:
                print()
                self.env.render()
            if self.done:
                break

        if self.verbose:
            print("\nWinner", self.winner)
