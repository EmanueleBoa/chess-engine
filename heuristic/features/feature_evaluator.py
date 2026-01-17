from abc import ABC, abstractmethod

import chess


class FeatureEvaluator(ABC):
    @abstractmethod
    def evaluate(self, board: chess.Board, color: bool, **kwargs) -> float:
        """
        Evaluate a feature of a chess position for the given color.

        Args:
            board: The chess board to evaluate
            color: The color to evaluate for (True for White, False for Black)
            **kwargs: Additional parameters that specific implementations may require

        Returns:
            A float score representing the evaluation of the feature for the given color
        """
        pass
