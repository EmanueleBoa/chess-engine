from abc import ABC, abstractmethod

import chess


class Evaluator(ABC):
    @abstractmethod
    def evaluate_board(self, board: chess.Board) -> float:
        """
        Evaluate a chess position for the color to move.

        Args:
            board: The chess board to evaluate

        Returns:
            A float score representing the evaluation of the board for the color to move
        """
        pass

    @abstractmethod
    def evaluate_move(self, board: chess.Board, move: chess.Move) -> float:
        """
        Evaluate a chess move from the given board.

        Args:
            board: The chess board to evaluate
            move: The move to evaluate

        Returns:
            A float score representing the evaluation of the move
        """
        pass
