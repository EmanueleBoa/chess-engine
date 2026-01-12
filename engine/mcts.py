import math

import chess

from engine.node import Node
from heuristic.evaluator import Evaluator


class MCTS:
    def __init__(self, evaluator: Evaluator, exploration_strength: float = 1.0, scale: float = 5.0):
        self.evaluator: Evaluator = evaluator
        self.exploration_strength: float = exploration_strength
        self.scale: float = scale

    def get_best_move(self, board: chess.Board, iterations: int = 1000, print_stats: bool = False) -> chess.Move:
        root = Node(board)

        for _ in range(iterations):
            node = root.tree_policy(exploration_strength=self.exploration_strength)
            value = self.get_value(node)
            node.backpropagate(value)

        if print_stats:
            for child in root.children:
                print(child.move, child.visits, child.get_exploitation_term())

        best_child = root.get_best_child(exploration_strength=0.0)
        return best_child.move

    def get_value(self, node: Node) -> float:
        if node.is_terminal():
            return node.outcome
        return math.tanh(self.evaluator.evaluate_board(node.board) / self.scale)
