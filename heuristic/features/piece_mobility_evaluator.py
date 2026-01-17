from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator

MOBILITY_KNIGHT = 4
MOBILITY_BISHOP = 3
MOBILITY_ROOK = 2
MOBILITY_QUEEN = 1


class PieceMobilityEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, float]):
        self.piece_to_weight: Dict[chess.PieceType, float] = {
            chess.KNIGHT: params.get("mobility_knight", MOBILITY_KNIGHT),
            chess.BISHOP: params.get("mobility_bishop", MOBILITY_BISHOP),
            chess.ROOK: params.get("mobility_rook", MOBILITY_ROOK),
            chess.QUEEN: params.get("mobility_queen", MOBILITY_QUEEN)
        }

    def evaluate(self, board: chess.Board, color: bool, *, phase_value: float = 1.0) -> float:
        score = 0.0
        for piece_type, mobility_weight in self.piece_to_weight.items():
            for square in board.pieces(piece_type, color):
                score += len(board.attacks(square)) * mobility_weight
        return phase_value * score
