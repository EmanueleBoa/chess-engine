from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator
from heuristic.features.utils import is_king_too_advanced, is_central_file

PHASE_MINIMUM_VALUE = 0.1

KING_SHIELD = 15
KING_OPEN = 20
KING_ATTACKED = 5

ATTACKER_VALUES = {
    chess.KNIGHT: 2,
    chess.BISHOP: 2,
    chess.ROOK: 3,
    chess.QUEEN: 5
}


class KingSafetyEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, float]):
        self.shield_bonus = params.get("king_shield", KING_SHIELD)
        self.shield_penalty = params.get("king_open", KING_OPEN)
        self.attacked_weight = params.get("king_attacked", KING_ATTACKED)

        self.shield_masks = {chess.WHITE: [0] * 64, chess.BLACK: [0] * 64}
        self._precompute_shields()

    def evaluate(self, board: chess.Board, color: bool, *, phase_value: float = 1.0) -> float:
        if phase_value < PHASE_MINIMUM_VALUE:
            return 0

        king_square = board.king(color)
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)

        penalty = self.get_king_attacked_penalty(board, color, king_square)
        score = -penalty * self.attacked_weight

        if is_central_file(king_file) or is_king_too_advanced(king_rank, color):
            return score

        shield_mask = self.shield_masks[color][king_square]
        friendly_pawns = board.pawns & board.occupied_co[color]
        pawns_in_shield = (shield_mask & friendly_pawns).bit_count()

        num_files = bin(shield_mask).count('1')
        score += (pawns_in_shield * self.shield_bonus) - ((num_files - pawns_in_shield) * self.shield_penalty)

        return phase_value * score

    @staticmethod
    def get_king_attacked_penalty(board: chess.Board, color: bool, king_square: chess.Square):
        enemy_color = not color
        king_zone_mask = chess.BB_KING_ATTACKS[king_square]

        num_attackers = 0
        total_attack_units = 0

        for piece_type, value in ATTACKER_VALUES.items():
            enemies = board.pieces(piece_type, enemy_color)
            for enemy_sq in enemies:
                if board.attacks(enemy_sq) & king_zone_mask:
                    num_attackers += 1
                    total_attack_units += value

        if num_attackers <= 1:
            return 0

        return num_attackers * total_attack_units

    def _precompute_shields(self):
        for square in range(64):
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            for color in [chess.WHITE, chess.BLACK]:
                step = 1 if color == chess.WHITE else -1
                shield_rank = rank + step

                if 0 <= shield_rank <= 7:
                    mask = 0
                    for f in range(max(0, file - 1), min(7, file + 1) + 1):
                        mask |= (1 << chess.square(f, shield_rank))
                    self.shield_masks[color][square] = mask
