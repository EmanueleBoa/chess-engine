import math
from typing import Optional

import chess


class Node:
    __slots__ = (
        'board', 'parent', 'move', 'children', 'untried_moves',
        'outcome', 'visits', 'log_visits', 'total_value', 'mean_value'
    )

    def __init__(self, board: chess.Board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.outcome = self.get_outcome()
        self.untried_moves = [] if self.outcome is not None else list(board.legal_moves)
        self.visits: int = 0
        self.log_visits: float = 0.0
        self.total_value: float = 0.0
        self.mean_value: float = 0.0

    def is_fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0

    def is_terminal(self) -> bool:
        return self.outcome is not None

    def expand(self) -> "Node":
        move = self.untried_moves.pop()
        next_board = self.board.copy()
        next_board.push(move)
        child = Node(next_board, parent=self, move=move)
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

    def tree_policy(self, exploration_strength: float = 1.0) -> "Node":
        node = self
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return node.expand()
            node = node.get_best_child(exploration_strength)
        return node

    def uct(self, exploration_strength: float) -> float:
        return self.get_exploitation_term() + exploration_strength * self.get_exploration_term()

    def get_exploration_term(self) -> float:
        return math.sqrt(self.parent.log_visits / self.visits)

    def get_exploitation_term(self) -> float:
        return - self.mean_value

    def get_most_visited_child(self) -> "Node":
        return max(self.children, key=lambda node: node.visits)

    def get_outcome(self) -> Optional[int]:
        if self.board.is_checkmate():
            return -1
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        if self.board.is_fifty_moves() or self.board.is_repetition(3):
            return 0
        return None
