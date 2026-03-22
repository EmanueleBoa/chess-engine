from typing import Dict

import chess

from heuristic.features.feature_evaluator import FeatureEvaluator

KING_CENTRALIZATION = 20.0
KING_PAWN_PROXIMITY = 10.0

CENTER_SQUARES = [chess.D4, chess.E4, chess.D5, chess.E5]


class KingEndgameEvaluator(FeatureEvaluator):
    def __init__(self, params: Dict[str, float]):
        self.king_centralization = params.get("king_centralization", KING_CENTRALIZATION)
        self.king_pawn_proximity = params.get("king_pawn_proximity", KING_PAWN_PROXIMITY)

    def evaluate(self, board: chess.Board, color: bool, phase_value: float = 1.0) -> float:
        score = 0.0
        king_square = board.king(color)

        min_dist_to_center = min(chess.square_distance(king_square, square) for square in CENTER_SQUARES)
        score += (4 - min_dist_to_center) * self.king_centralization

        pawns = board.pawns & board.occupied_co[color]
        if pawns:
            pawn_list = list(chess.scan_forward(pawns))
            min_dist_to_pawn = min(chess.square_distance(king_square, pawn_square) for pawn_square in pawn_list)
            score += (7 - min_dist_to_pawn) * self.king_pawn_proximity

        return (1 - phase_value) * score
