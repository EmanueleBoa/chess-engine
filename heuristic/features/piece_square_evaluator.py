from typing import Dict, List

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator

PAWN_TABLE = list(reversed([
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]))

KNIGHT_TABLE = list(reversed([
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]))

BISHOP_TABLE = list(reversed([
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]))

ROOK_TABLE = list(reversed([
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, 10, 10, 10, 10, 5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 0, 5, 5, 0, 0, 0
]))

QUEEN_TABLE = list(reversed([
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]))

KING_TABLE = list(reversed([
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20
]))

KING_ENDGAME_TABLE = list(reversed([
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]))


class PieceSquareEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, List[float]]):
        self.pst_tables_mg: Dict[chess.PieceType, List[float]] = {
            chess.PAWN: params.get("pawn_square_table_mg", PAWN_TABLE),
            chess.KNIGHT: params.get("knight_square_table_mg", KNIGHT_TABLE),
            chess.BISHOP: params.get("bishop_square_table_mg", BISHOP_TABLE),
            chess.ROOK: params.get("rook_square_table_mg", ROOK_TABLE),
            chess.QUEEN: params.get("queen_square_table_mg", QUEEN_TABLE),
            chess.KING: params.get("king_square_table_mg", KING_TABLE)
        }
        self.pst_tables_eg: Dict[chess.PieceType, List[float]] = {
            chess.PAWN: params.get("pawn_square_table_eg", PAWN_TABLE),
            chess.KNIGHT: params.get("knight_square_table_eg", KNIGHT_TABLE),
            chess.BISHOP: params.get("bishop_square_table_eg", BISHOP_TABLE),
            chess.ROOK: params.get("rook_square_table_eg", ROOK_TABLE),
            chess.QUEEN: params.get("queen_square_table_eg", QUEEN_TABLE),
            chess.KING: params.get("king_square_table_eg", KING_ENDGAME_TABLE)
        }

    def evaluate(self, board: chess.Board, color: bool, phase_value: float = 1.0) -> float:
        score = 0.0

        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            for square in board.pieces(piece_type, color):
                idx = square if color == chess.WHITE else square ^ 56
                mg_score = self.pst_tables_mg[piece_type][idx]
                eg_score = self.pst_tables_eg[piece_type][idx]
                score += phase_value * mg_score + (1 - phase_value) * eg_score

        return score
