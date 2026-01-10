import math
from typing import Optional, List

import chess

from engine.board import Board


class Node:
    """
    MCTS Node using move/unmove pattern for efficiency.

    Instead of storing a full board copy in each node, we only store the move.
    The board state is reconstructed by applying moves from the root during tree traversal.
    This eliminates expensive board.copy() calls during expansion.
    """
    __slots__ = (
        'parent', 'move', 'children', 'untried_moves',
        'outcome', 'visits', 'log_visits', 'total_value', 'mean_value'
    )

    def __init__(self, parent: Optional["Node"] = None, move: Optional[chess.Move] = None,
                 untried_moves: Optional[List[chess.Move]] = None, outcome: Optional[int] = None):
        self.parent = parent
        self.move = move
        self.children = []
        self.untried_moves = untried_moves if untried_moves is not None else []
        self.outcome = outcome
        self.visits: int = 0
        self.log_visits: float = 0.0
        self.total_value: float = 0.0
        self.mean_value: float = 0.0

    def is_fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0

    def is_terminal(self) -> bool:
        return self.outcome is not None

    def expand(self, board: Board) -> "Node":
        move = self.untried_moves.pop()
        board.push(move)

        # Check outcome and get legal moves for the new position
        outcome = board.get_outcome()
        untried_moves = [] if outcome is not None else board.get_legal_moves()

        child = Node(parent=self, move=move, untried_moves=untried_moves, outcome=outcome)
        self.children.append(child)
        return child

    def get_best_child(self, exploration_strength: float = 1.0) -> "Node":
        return max(self.children, key=lambda node: node.uct(exploration_strength))

    def backpropagate(self, value: float):
        self.visits += 1
        self.total_value += value
        self.mean_value = self.total_value / self.visits
        self.log_visits = math.log(self.visits)
        if self.parent:
            self.parent.backpropagate(-value)

    def uct(self, exploration_strength: float) -> float:
        return self.get_exploitation_term() + exploration_strength * self.get_exploration_term()

    def get_exploration_term(self) -> float:
        return math.sqrt(self.parent.log_visits / self.visits)

    def get_exploitation_term(self) -> float:
        return -self.mean_value

    def get_most_visited_child(self) -> "Node":
        return max(self.children, key=lambda node: node.visits)
