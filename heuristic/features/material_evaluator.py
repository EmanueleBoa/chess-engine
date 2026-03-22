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
        self.piece_to_value_mg: Dict[chess.PieceType, float] = {
            chess.PAWN: params.get("pawn_value_mg", PAWN_VALUE),
            chess.KNIGHT: params.get("knight_value_mg", KNIGHT_VALUE),
            chess.BISHOP: params.get("bishop_value_mg", BISHOP_VALUE),
            chess.ROOK: params.get("rook_value_mg", ROOK_VALUE),
            chess.QUEEN: params.get("queen_value_mg", QUEEN_VALUE)
        }
        self.piece_to_value_eg: Dict[chess.PieceType, float] = {
            chess.PAWN: params.get("pawn_value_eg", PAWN_VALUE),
            chess.KNIGHT: params.get("knight_value_eg", KNIGHT_VALUE),
            chess.BISHOP: params.get("bishop_value_eg", BISHOP_VALUE),
            chess.ROOK: params.get("rook_value_eg", ROOK_VALUE),
            chess.QUEEN: params.get("queen_value_eg", QUEEN_VALUE)
        }

    def evaluate(self, board: chess.Board, color: bool, phase_value: float = 1.0) -> float:
        score = 0.0
        for piece in self.piece_to_value_mg.keys():
            piece_count = len(board.pieces(piece, color))
            mg_value = self.piece_to_value_mg[piece]
            eg_value = self.piece_to_value_eg[piece]
            interpolated_value = mg_value * phase_value + eg_value * (1 - phase_value)
            score += piece_count * interpolated_value
        return score
