from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator

PAWN_PASS_MG = 5.0
PAWN_PASS_EG = 10.0
PAWN_ISOLATED_MG = 15.0
PAWN_ISOLATED_EG = 20.0
PAWN_DOUBLED_MG = 10.0
PAWN_DOUBLED_EG = 15.0


class PawnStructureEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, float]):
        self.passed_mg = params.get("pawn_passed_mg", PAWN_PASS_MG)
        self.passed_eg = params.get("pawn_passed_eg", PAWN_PASS_EG)
        self.isolated_mg = params.get("pawn_isolated_mg", PAWN_ISOLATED_MG)
        self.isolated_eg = params.get("pawn_isolated_eg", PAWN_ISOLATED_EG)
        self.doubled_mg = params.get("pawn_doubled_mg", PAWN_DOUBLED_MG)
        self.doubled_eg = params.get("pawn_doubled_eg", PAWN_DOUBLED_EG)

    def evaluate(self, board: chess.Board, color: bool, *, phase_value: float = 1.0) -> float:
        pawn_mask = int(board.pieces(chess.PAWN, color))
        enemy_pawn_mask = int(board.pieces(chess.PAWN, not color))
        bb_files = list(chess.BB_FILES)

        mg_score = 0.0
        eg_score = 0.0
        for square in board.pieces(chess.PAWN, color):
            file, rank = chess.square_file(square), chess.square_rank(square)

            if self._is_passed(file, rank, enemy_pawn_mask, color, bb_files):
                relative_rank = rank if color == chess.WHITE else 7 - rank
                mg_score += (relative_rank ** 2) * self.passed_mg
                eg_score += (relative_rank ** 2) * self.passed_eg

            if self._is_isolated(file, pawn_mask, bb_files):
                mg_score -= self.isolated_mg
                eg_score -= self.isolated_eg

            if self._is_doubled(file, pawn_mask, bb_files):
                mg_score -= self.doubled_mg
                eg_score -= self.doubled_eg

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
