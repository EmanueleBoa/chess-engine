from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator

MOBILITY_KNIGHT = 4
MOBILITY_BISHOP = 3
MOBILITY_ROOK = 2
MOBILITY_QUEEN = 1


class PieceMobilityEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, float]):
        self.piece_to_weight_mg: Dict[chess.PieceType, float] = {
            chess.KNIGHT: params.get("mobility_knight_mg", MOBILITY_KNIGHT),
            chess.BISHOP: params.get("mobility_bishop_mg", MOBILITY_BISHOP),
            chess.ROOK: params.get("mobility_rook_mg", MOBILITY_ROOK),
            chess.QUEEN: params.get("mobility_queen_mg", MOBILITY_QUEEN)
        }
        self.piece_to_weight_eg: Dict[chess.PieceType, float] = {
            chess.KNIGHT: params.get("mobility_knight_eg", MOBILITY_KNIGHT),
            chess.BISHOP: params.get("mobility_bishop_eg", MOBILITY_BISHOP),
            chess.ROOK: params.get("mobility_rook_eg", MOBILITY_ROOK),
            chess.QUEEN: params.get("mobility_queen_eg", MOBILITY_QUEEN)
        }

    def evaluate(self, board: chess.Board, color: bool, phase_value: float = 1.0) -> float:
        mg_score = 0.0
        eg_score = 0.0
        for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            for square in board.pieces(piece_type, color):
                mobility = len(board.attacks(square))
                mg_score += mobility * self.piece_to_weight_mg[piece_type]
                eg_score += mobility * self.piece_to_weight_eg[piece_type]
        return phase_value * mg_score + (1 - phase_value) * eg_score
