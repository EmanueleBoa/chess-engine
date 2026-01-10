from engine.board import Board
from engine.node import Node
from heuristic.evaluator import Evaluator


class MCTS:
    def __init__(self, evaluator: Evaluator, exploration_strength: float = 1.0):
        self.evaluator: Evaluator = evaluator
        self.exploration_strength: float = exploration_strength

    def search_move(self, board: Board, iterations: int = 1000, print_stats: bool = False):
        # Create root node with initial position info
        outcome = board.get_outcome()
        untried_moves = [] if outcome is not None else board.get_legal_moves()
        root = Node(untried_moves=untried_moves, outcome=outcome)

        # Create a working board for tree traversal (only one copy!)
        working_board = board.copy()

        for _ in range(iterations):
            # Selection & Expansion phase
            node = root
            move_count = 0

            # Selection: traverse down the tree using UCT
            while not node.is_terminal() and node.is_fully_expanded():
                node = node.get_best_child(self.exploration_strength)
                working_board.push(node.move)
                move_count += 1

            # Expansion: expand a new child if not terminal
            if not node.is_terminal():
                node = node.expand(working_board)
                move_count += 1

            # Evaluation: get value for the leaf node
            value = self.get_value(node, working_board)

            # Backpropagation: update statistics up the tree
            node.backpropagate(value)

            # Unmove: restore board to root position
            for _ in range(move_count):
                working_board.pop()

        # Print statistics if requested
        if print_stats:
            for child in root.children:
                print(child.move, child.visits, child.get_exploitation_term())

        # Return the best move (exploitation only, no exploration)
        best_child = root.get_best_child(exploration_strength=0.0)
        return best_child.move

    def get_value(self, node: Node, board: Board) -> float:
        if node.is_terminal():
            return node.outcome
        return self.evaluator.evaluate(board)
