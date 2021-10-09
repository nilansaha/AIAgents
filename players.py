import random
from copy import deepcopy
from utils import save_model, load_model


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


class FirstMovePlayer(Player):
    """
    In a squared board there is a good advantage of starting in the middle
    because it allows for maximum positions to connect. This simple player
    just starts with that position but then goes on a randomly playing
    """

    def __init__(self, env):
        super().__init__(env)
        self.first_move = True

    def get_move(self):
        if self.first_move:
            self.first_move = False
            return 12
        pos = random.choice(self.env.available_moves())
        return pos


class Node:
    def __init__(self, val):
        self.value = val
        self.children = {}
        self.points = 0


class TreePlayerV1(Player):
    """
    The player generates the entire game tree and gives 1 point to each terminal
    node(move) that results in a win for player1 (0). Every parent node
    inherits the sum of the points of their children and it gets propagated to the top

    Remark: Does pretty well in a 3 X 3. Against a human always draws unless the other player
    makes a mistake. Has great stats with a random player so pretty good. But obviously
    extremely slow and not scalable if the grid is bigger and that is why we need algorithms
    that can generalize and not memorize

    Upon further inspection there is definitely weakness in it because sometimes it chooses
    not to take the winning move and makes a move that will increase its chances of winning in
    the next move. Which makes sense because of how we are awarding points.
    Let us assume there are two nodes on a level - one of them is a terminal node and that move
    grants win so it gets 1 point. There is another node which is not a terminal node but only
    one of its children wins the game so in turn this particular node also gets awarded 1 point
    because the point gets propagated to it. Adding a notion of points based on faster
    wins should definitely solve this. One way of solving this is also by normalizing the
    propagated score to the parent by dividing with the number of children. Terminal nodes
    can one complete point but non-terminal nodes on the same level is less likely to get 1 point
    as well

    Stats on a game with RandomPlayer = {Draw: 149, TreePlayerV1: 826, RandomPlayer: 25}
    """

    model = None

    def __init__(self, env):
        super().__init__(env)
        if not TreePlayerV1.model:
            model = load_model("tree_player_v1")
            if not model:
                model = self._generate_game_tree()
                save_model(model, "tree_player_v1")
            TreePlayerV1.model = model

    def _generate_game_tree(self):
        def helper(node, env):
            moves = env.available_moves()
            for move in moves:
                child_node = Node(move)
                frozen_env = deepcopy(env)
                done, winner = frozen_env.move(move)
                node.children[move] = child_node
                if not done:
                    helper(child_node, frozen_env)
                else:
                    if winner == 0:
                        child_node.points = 1

            for child in node.children.values():
                node.points += child.points

            return node

        node = Node(-1)
        return helper(node, self.env)

    def get_move(self):
        node = self.model
        for move in self.env.move_history:
            node = node.children[move]

        sorted_moves = sorted(
            node.children.items(), key=lambda x: x[1].points, reverse=True
        )
        # print([(move, node.points) for move, node in sorted_moves])
        best_move = sorted_moves[0][0]
        return best_move


class TreePlayerV2(Player):
    """
    The player generates the entire game tree and gives 1 point to each terminal
    node(move) that results in a win for player1 (0). Every parent node
    inherits the sum of the points of their children normalized by the number of children
    it has. It gets propagated to the top

    Remark: Does extremely well in a 3 X 3. Against a human always draws unless the other player
    makes a mistake. Has insanely good stats with the random player. But obviously
    extremely slow and not scalable if the grid is bigger and that is why we need algorithms
    that can generalize and not memorize

    Remarks: Does not have any weakness at all

    Stats on a game with RandomPlayer = {Draw: 6, TreePlayerV2: 994, RandomPlayer: 0}
    """

    model = None

    def __init__(self, env):
        super().__init__(env)
        if not TreePlayerV2.model:
            model = load_model("tree_player_v2")
            if not model:
                model = self._generate_game_tree()
                save_model(model, "tree_player_v2")
            TreePlayerV2.model = model

    def _generate_game_tree(self):
        def helper(node, env):
            moves = env.available_moves()
            for move in moves:
                child_node = Node(move)
                frozen_env = deepcopy(env)
                done, winner = frozen_env.move(move)
                node.children[move] = child_node
                if not done:
                    helper(child_node, frozen_env)
                else:
                    if winner == 0:
                        child_node.points = 1

            total_child_points = sum([child.points for child in node.children.values()])
            node.points = total_child_points / len(node.children)

            return node

        node = Node(-1)
        return helper(node, self.env)

    def get_move(self):
        node = self.model
        for move in self.env.move_history:
            node = node.children[move]

        sorted_moves = sorted(
            node.children.items(), key=lambda x: x[1].points, reverse=True
        )
        # print([(move, node.points) for move, node in sorted_moves])
        best_move = sorted_moves[0][0]
        return best_move
