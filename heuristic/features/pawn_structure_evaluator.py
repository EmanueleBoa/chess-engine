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

        self.front_spans = {chess.WHITE: [0] * 64, chess.BLACK: [0] * 64}
        self.support_masks = {chess.WHITE: [0] * 64, chess.BLACK: [0] * 64}

        self._precompute_masks()

    def evaluate(self, board: chess.Board, color: bool, *, phase_value: float = 1.0) -> float:
        pawns = board.pawns & board.occupied_co[color]
        enemy_pawns = board.pawns & board.occupied_co[not color]

        mg_score = 0.0
        eg_score = 0.0

        file_occupancy = self._get_file_occupancy(pawns)

        color_front_spans = self.front_spans[color]
        color_support_masks = self.support_masks[color]

        for square in chess.scan_forward(pawns):
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            relative_rank = rank if color == chess.WHITE else 7 - rank

            if not (color_front_spans[square] & enemy_pawns):
                mg_score += (relative_rank ** 2) * self.passed_mg
                eg_score += (relative_rank ** 2) * self.passed_eg

            adjacent_files_mask = 0
            if file > 0: adjacent_files_mask |= (1 << (file - 1))
            if file < 7: adjacent_files_mask |= (1 << (file + 1))
            if not (adjacent_files_mask & file_occupancy):
                mg_score -= self.isolated_mg
                eg_score -= self.isolated_eg

            if (chess.BB_FILES[file] & pawns).bit_count() > 1:
                mg_score -= self.doubled_mg
                eg_score -= self.doubled_eg

            if color_support_masks[square] & pawns:
                bonus_multiplier = (1.0 + (relative_rank / 7.0))
                mg_score += self.connected_mg * bonus_multiplier
                eg_score += self.connected_eg * bonus_multiplier

        phalanxes = pawns & (pawns << 1) & ~chess.BB_FILE_A
        num_phalanx = phalanxes.bit_count()
        mg_score += num_phalanx * self.phalanx_mg
        eg_score += num_phalanx * self.phalanx_eg

        return phase_value * mg_score + (1 - phase_value) * eg_score

    @staticmethod
    def _get_file_occupancy(pawns: int) -> int:
        occupancy = 0
        for i in range(8):
            if pawns & chess.BB_FILES[i]:
                occupancy |= (1 << i)
        return occupancy

    def _precompute_masks(self):
        for square in range(64):
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            adjacent_files = chess.BB_FILES[file]
            if file > 0: adjacent_files |= chess.BB_FILES[file - 1]
            if file < 7: adjacent_files |= chess.BB_FILES[file + 1]

            self.front_spans[chess.WHITE][square] = adjacent_files & ~((1 << (8 * (rank + 1))) - 1)
            self.front_spans[chess.BLACK][square] = adjacent_files & ((1 << (8 * rank)) - 1)

            for color in [chess.WHITE, chess.BLACK]:
                support_mask = 0
                rank_offset = -1 if color == chess.WHITE else 1
                support_rank = rank + rank_offset

                if 0 <= support_rank <= 7:
                    if file > 0: support_mask |= (1 << chess.square(file - 1, support_rank))
                    if file < 7: support_mask |= (1 << chess.square(file + 1, support_rank))

                self.support_masks[color][square] = support_mask
