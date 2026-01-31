from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator
from heuristic.features.utils import is_outpost, is_seventh_rank

BISHOP_PAIR = 40
ROOK_OPEN = 20
ROOK_7TH_RANK = 40
KNIGHT_OUTPOST = 35
BAD_BISHOP = 15.0
TRAPPED_PIECE = 50.0
ROOK_BATTERY = 25.0

LIGHT_SQUARES = chess.BB_LIGHT_SQUARES
DARK_SQUARES = chess.BB_DARK_SQUARES


class StrategicBonusEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, float]):
        self.bishop_pair = params.get("bishop_pair", BISHOP_PAIR)
        self.rook_open = params.get("rook_open", ROOK_OPEN)
        self.rook_7th_rank = params.get("rook_7th_rank", ROOK_7TH_RANK)
        self.knight_outpost = params.get("knight_outpost", KNIGHT_OUTPOST)
        self.bad_bishop = params.get("bad_bishop", BAD_BISHOP)
        self.trapped_piece = params.get("trapped_piece", TRAPPED_PIECE)
        self.rook_battery = params.get("rook_battery", ROOK_BATTERY)

    def evaluate(self, board: chess.Board, color: bool, **kwargs) -> float:
        score = 0.0
        score += self._bishop_pair_bonus(board, color)
        score += self._knight_outpost_bonus(board, color)
        score += self._rook_activity_bonus(board, color)
        score += self._bad_bishop_penalty(board, color)
        score += self._trapped_pieces_penalty(board, color)
        score += self._rook_battery_bonus(board, color)
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

    def _bad_bishop_penalty(self, board: chess.Board, color: bool) -> float:
        pawn_bb = board.pawns & (board.occupied_co[color])
        bishop_bb = board.bishops & (board.occupied_co[color])

        score = 0.0

        if bishop_bb & LIGHT_SQUARES:
            pawn_count = bin(pawn_bb & LIGHT_SQUARES).count('1')
            if pawn_count > 2:
                score -= (pawn_count - 2) * self.bad_bishop

        if bishop_bb & DARK_SQUARES:
            pawn_count = bin(pawn_bb & DARK_SQUARES).count('1')
            if pawn_count > 2:
                score -= (pawn_count - 2) * self.bad_bishop

        return score

    def _trapped_pieces_penalty(self, board: chess.Board, color: bool) -> float:
        score = 0.0
        for square in board.pieces(chess.KNIGHT, color):
            if (1 << square) & chess.BB_CORNERS:
                if len(board.attacks(square)) < 3:
                    score -= self.trapped_piece

        king_sq = board.king(color)
        if color == chess.WHITE:
            if king_sq == chess.G1 and board.piece_at(chess.H1) == chess.Piece(chess.ROOK, True):
                if board.piece_at(chess.F1) and board.piece_at(chess.F1).piece_type != chess.KING:
                    score -= self.trapped_piece
        else:
            if king_sq == chess.G8 and board.piece_at(chess.H8) == chess.Piece(chess.ROOK, False):
                if board.piece_at(chess.F8) and board.piece_at(chess.F8).piece_type != chess.KING:
                    score -= self.trapped_piece
        return score

    def _rook_battery_bonus(self, board: chess.Board, color: bool) -> float:
        rooks = board.rooks & board.occupied_co[color]
        if bin(rooks).count('1') < 2:
            return 0.0

        score = 0.0
        for square in chess.scan_forward(rooks):
            file_mask = chess.BB_FILES[chess.square_file(square)]
            other_rooks_on_file = (rooks & file_mask) & ~(1 << square)

            if board.attacks(square) & other_rooks_on_file:
                score += self.rook_battery / 2.0

        return score
