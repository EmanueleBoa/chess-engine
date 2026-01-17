from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator
from heuristic.features.utils import is_outpost, is_seventh_rank

BISHOP_PAIR = 40
ROOK_OPEN = 20
ROOK_7TH_RANK = 40
KNIGHT_OUTPOST = 35


class StrategicBonusEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, float]):
        self.bishop_pair = params.get("bishop_pair", BISHOP_PAIR)
        self.rook_open = params.get("rook_open", ROOK_OPEN)
        self.rook_7th_rank = params.get("rook_7th_rank", ROOK_7TH_RANK)
        self.knight_outpost = params.get("knight_outpost", KNIGHT_OUTPOST)

    def evaluate(self, board: chess.Board, color: bool, **kwargs) -> float:
        score = 0.0
        score += self._bishop_pair_bonus(board, color)
        score += self._knight_outpost_bonus(board, color)
        score += self._rook_activity_bonus(board, color)
        return score

    def _bishop_pair_bonus(self, board: chess.Board, color: bool) -> float:
        if len(board.pieces(chess.BISHOP, color)) < 2:
            return 0
        return self.bishop_pair

    def _knight_outpost_bonus(self, board: chess.Board, color: bool) -> float:
        score = 0
        for square in board.pieces(chess.KNIGHT, color):
            if is_outpost(board, square, color):
                score += self.knight_outpost
        return score

    def _rook_activity_bonus(self, board: chess.Board, color: bool) -> float:
        own_pawn_mask = int(board.pieces(chess.PAWN, color))
        enemy_pawn_mask = int(board.pieces(chess.PAWN, not color))
        bb_files = list(chess.BB_FILES)

        score = 0
        for square in board.pieces(chess.ROOK, color):
            rank = chess.square_rank(square)
            if is_seventh_rank(rank, color):
                score += self.rook_7th_rank

            file = chess.square_file(square)
            is_file_free_from_own_pawns = not (int(bb_files[file]) & own_pawn_mask)
            is_file_free_from_enemy_pawns = not (int(bb_files[file]) & enemy_pawn_mask)
            if is_file_free_from_own_pawns:
                if is_file_free_from_enemy_pawns:
                    score += self.rook_open
                else:
                    score += self.rook_open / 2

        return score
