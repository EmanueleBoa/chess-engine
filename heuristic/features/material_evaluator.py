from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator

PAWN_VALUE = 100
KNIGHT_VALUE = 320
BISHOP_VALUE = 330
ROOK_VALUE = 500
QUEEN_VALUE = 900


class MaterialEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, float]):
        self.piece_to_value: Dict[chess.PieceType, float] = {
            chess.PAWN: params.get("pawn_value", PAWN_VALUE),
            chess.KNIGHT: params.get("knight_value", KNIGHT_VALUE),
            chess.BISHOP: params.get("bishop_value", BISHOP_VALUE),
            chess.ROOK: params.get("rook_value", ROOK_VALUE),
            chess.QUEEN: params.get("queen_value", QUEEN_VALUE)
        }

    def evaluate(self, board: chess.Board, color: bool, **kwargs) -> float:
        score = 0.0
        for piece, value in self.piece_to_value.items():
            score += len(board.pieces(piece, color)) * value
        return score

    def get_piece_value(self, piece_type: chess.PieceType) -> float:
        return self.piece_to_value.get(piece_type, 0.0)
