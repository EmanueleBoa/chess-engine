from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator
from heuristic.features.utils import is_outpost  # Assuming this is optimized

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

        self.seventh_rank_mask = {
            chess.WHITE: chess.BB_RANK_7,
            chess.BLACK: chess.BB_RANK_2
        }

    def evaluate(self, board: chess.Board, color: bool, **kwargs) -> float:
        score = 0.0

        own_pieces = board.occupied_co[color]
        pawns = board.pawns & own_pieces
        knights = board.knights & own_pieces
        bishops = board.bishops & own_pieces
        rooks = board.rooks & own_pieces

        enemy_pawns = board.pawns & board.occupied_co[not color]

        if bishops.bit_count() >= 2:
            score += self.bishop_pair

        for square in chess.scan_forward(knights):
            if is_outpost(board, square, color):
                score += self.knight_outpost

        rank_7_mask = self.seventh_rank_mask[color]
        for square in chess.scan_forward(rooks):
            if (1 << square) & rank_7_mask:
                score += self.rook_7th_rank

            file = chess.square_file(square)
            file_mask = chess.BB_FILES[file]
            if not (file_mask & pawns):
                if not (file_mask & enemy_pawns):
                    score += self.rook_open
                else:
                    score += self.rook_open / 2.0

        if bishops & chess.BB_LIGHT_SQUARES:
            pawn_count = (pawns & chess.BB_LIGHT_SQUARES).bit_count()
            if pawn_count > 2:
                score -= (pawn_count - 2) * self.bad_bishop
        if bishops & chess.BB_DARK_SQUARES:
            pawn_count = (pawns & chess.BB_DARK_SQUARES).bit_count()
            if pawn_count > 2:
                score -= (pawn_count - 2) * self.bad_bishop

        trapped_knights = knights & chess.BB_CORNERS
        for square in chess.scan_forward(trapped_knights):
            if int(board.attacks(square)).bit_count() < 3:
                score -= self.trapped_piece

        king_square = board.king(color)
        occupied = board.occupied
        if color == chess.WHITE:
            if king_square == chess.G1 and (rooks & (1 << chess.H1)):
                if (occupied & (1 << chess.F1)):
                    score -= self.trapped_piece
        else:
            if king_square == chess.G8 and (rooks & (1 << chess.H8)):
                if (occupied & (1 << chess.F8)):
                    score -= self.trapped_piece

        if rooks.bit_count() >= 2:
            for square in chess.scan_forward(rooks):
                file_mask = chess.BB_FILES[chess.square_file(square)]
                if board.attacks(square) & rooks & file_mask:
                    score += self.rook_battery / 2.0

        return score
