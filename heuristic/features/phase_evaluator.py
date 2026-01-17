from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator

KNIGHT_VALUE = 1
BISHOP_VALUE = 1
ROOK_VALUE = 2
QUEEN_VALUE = 4

MAX_VALUE = 2 * QUEEN_VALUE + 4 * ROOK_VALUE + 4 * BISHOP_VALUE + 4 * KNIGHT_VALUE


class PhaseEvaluator(FeatureEvaluator):
    def __init__(self):
        self.piece_to_value: Dict[chess.PieceType, float] = {
            chess.KNIGHT: KNIGHT_VALUE,
            chess.BISHOP: BISHOP_VALUE,
            chess.ROOK: ROOK_VALUE,
            chess.QUEEN: QUEEN_VALUE
        }

    def evaluate(self, board: chess.Board, color: bool, **kwargs) -> float:
        """
        Returns a value between 0 and 1, where 1 is the opening and 0 is the endgame.
        """
        score = 0.0
        for piece, value in self.piece_to_value.items():
            score += (len(board.pieces(piece, True)) + len(board.pieces(piece, False))) * value
        return min(1.0, score / MAX_VALUE)
