from abc import ABC, abstractmethod

import chess


class FeatureEvaluator(ABC):
    @abstractmethod
    def evaluate(self, board: chess.Board, color: bool, phase_value: float) -> float:
        """
        Evaluate a feature of a chess position for the given color.

        Args:
            board: The chess board to evaluate
            color: The color to evaluate for (True for White, False for Black)
            phase_value: The phase of the game (0 for endgame, 1 for opening)

        Returns:
            A float score representing the evaluation of the feature for the given color
        """
        pass
