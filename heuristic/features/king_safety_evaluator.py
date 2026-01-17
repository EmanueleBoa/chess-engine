from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator
from heuristic.features.utils import is_friendly_pawn, is_king_too_advanced, is_central_file

KING_SHIELD = 15
KING_OPEN = 20


class KingSafetyEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, float]):
        self.shield_bonus = params.get("king_shield", KING_SHIELD)
        self.shield_penalty = params.get("king_open", KING_OPEN)

    def evaluate(self, board: chess.Board, color: bool, *, phase_value: float = 1.0) -> float:
        king_square = board.king(color)
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)

        if is_central_file(king_file):
            return 0
        if is_king_too_advanced(king_rank, color):
            return 0

        score = 0
        step = 1 if color == chess.WHITE else -1
        for file in range(max(0, king_file - 1), min(7, king_file + 1) + 1):
            piece_at_file = board.piece_at(chess.square(file, king_rank + step))
            if is_friendly_pawn(piece_at_file, color):
                score += self.shield_bonus
            else:
                score -= self.shield_penalty
        return phase_value * score
