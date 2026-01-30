from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator
from heuristic.features.utils import is_friendly_pawn, is_king_too_advanced, is_central_file

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

    def evaluate(self, board: chess.Board, color: bool, *, phase_value: float = 1.0) -> float:
        if phase_value < PHASE_MINIMUM_VALUE:
            return 0

        king_square = board.king(color)
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)

        score = - self.get_king_attacked_penalty(board, color, king_square) * self.attacked_weight

        if is_central_file(king_file):
            return score
        if is_king_too_advanced(king_rank, color):
            return score

        step = 1 if color == chess.WHITE else -1
        for file in range(max(0, king_file - 1), min(7, king_file + 1) + 1):
            piece_at_file = board.piece_at(chess.square(file, king_rank + step))
            if is_friendly_pawn(piece_at_file, color):
                score += self.shield_bonus
            else:
                score -= self.shield_penalty

        return phase_value * score

    @staticmethod
    def get_king_attacked_penalty(board: chess.Board, color: bool, king_square: chess.Square):
        enemy_color = not color
        total_attack_units = 0
        num_attackers = 0

        king_zone_mask = chess.BB_KING_ATTACKS[king_square]

        for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            enemies = board.pieces(piece_type, enemy_color)
            for enemy_square in enemies:
                if board.attacks(enemy_square) & king_zone_mask:
                    num_attackers += 1
                    total_attack_units += ATTACKER_VALUES[piece_type]

        if num_attackers <= 1:
            return 0

        return num_attackers * total_attack_units
