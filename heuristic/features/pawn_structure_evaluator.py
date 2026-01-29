from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator

PAWN_PASSED_MG = 5.0
PAWN_PASSED_EG = 10.0
PAWN_ISOLATED_MG = 15.0
PAWN_ISOLATED_EG = 20.0
PAWN_DOUBLED_MG = 10.0
PAWN_DOUBLED_EG = 15.0
PAWN_CONNECTED_MG = 5.0
PAWN_CONNECTED_EG = 8.0
PAWN_PHALANX_MG = 3.0
PAWN_PHALANX_EG = 5.0


class PawnStructureEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, float]):
        self.passed_mg = params.get("pawn_passed_mg", PAWN_PASSED_MG)
        self.passed_eg = params.get("pawn_passed_eg", PAWN_PASSED_EG)
        self.isolated_mg = params.get("pawn_isolated_mg", PAWN_ISOLATED_MG)
        self.isolated_eg = params.get("pawn_isolated_eg", PAWN_ISOLATED_EG)
        self.doubled_mg = params.get("pawn_doubled_mg", PAWN_DOUBLED_MG)
        self.doubled_eg = params.get("pawn_doubled_eg", PAWN_DOUBLED_EG)
        self.connected_mg = params.get("pawn_connected_mg", PAWN_CONNECTED_MG)
        self.connected_eg = params.get("pawn_connected_eg", PAWN_CONNECTED_EG)
        self.phalanx_mg = params.get("pawn_phalanx_mg", PAWN_PHALANX_MG)
        self.phalanx_eg = params.get("pawn_phalanx_eg", PAWN_PHALANX_EG)

    def evaluate(self, board: chess.Board, color: bool, *, phase_value: float = 1.0) -> float:
        pawn_mask = int(board.pieces(chess.PAWN, color))
        enemy_pawn_mask = int(board.pieces(chess.PAWN, not color))
        bb_files = list(chess.BB_FILES)

        mg_score = 0.0
        eg_score = 0.0
        for square in board.pieces(chess.PAWN, color):
            file, rank = chess.square_file(square), chess.square_rank(square)
            relative_rank = rank if color == chess.WHITE else 7 - rank

            if self._is_passed(file, rank, enemy_pawn_mask, color, bb_files):
                mg_score += (relative_rank ** 2) * self.passed_mg
                eg_score += (relative_rank ** 2) * self.passed_eg

            if self._is_isolated(file, pawn_mask, bb_files):
                mg_score -= self.isolated_mg
                eg_score -= self.isolated_eg

            if self._is_doubled(file, pawn_mask, bb_files):
                mg_score -= self.doubled_mg
                eg_score -= self.doubled_eg

            if self._is_connected(square, pawn_mask, color):
                bonus_multiplier = 1.0 + (relative_rank / 7.0)
                mg_score += self.connected_mg * bonus_multiplier
                eg_score += self.connected_eg * bonus_multiplier

            if self._is_phalanx(square, pawn_mask):
                mg_score += self.phalanx_mg
                eg_score += self.phalanx_eg

        return phase_value * mg_score + (1 - phase_value) * eg_score

    @staticmethod
    def _is_passed(file, rank, enemy_pawns, color, bb_files) -> bool:
        for adjacent_file in range(max(0, file - 1), min(7, file + 1) + 1):
            file_mask = int(bb_files[adjacent_file])
            if color == chess.WHITE:
                stop_mask = file_mask & ~((1 << (8 * (rank + 1))) - 1)
            else:
                stop_mask = file_mask & ((1 << (8 * rank)) - 1)
            if stop_mask & enemy_pawns: return False
        return True

    @staticmethod
    def _is_isolated(file, pawn_mask, bb_files) -> bool:
        adjacent_files = 0
        if file > 0: adjacent_files |= int(bb_files[file - 1])
        if file < 7: adjacent_files |= int(bb_files[file + 1])
        return not (adjacent_files & pawn_mask)

    @staticmethod
    def _is_doubled(file, pawn_mask, bb_files) -> bool:
        return (int(bb_files[file]) & pawn_mask).bit_count() > 1

    @staticmethod
    def _is_connected(square, pawn_mask, color) -> bool:
        file = chess.square_file(square)
        support_rank = chess.square_rank(square) - (1 if color == chess.WHITE else -1)

        if support_rank < 0 or support_rank > 7:
            return False

        for adjacent_file in [file - 1, file + 1]:
            if 0 <= adjacent_file <= 7:
                if (1 << chess.square(adjacent_file, support_rank)) & pawn_mask:
                    return True
        return False

    @staticmethod
    def _is_phalanx(square, pawn_mask) -> bool:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        # We only check the right side to avoid double-counting the pair
        if file < 7:
            if (1 << chess.square(file + 1, rank)) & pawn_mask:
                return True
        return False
