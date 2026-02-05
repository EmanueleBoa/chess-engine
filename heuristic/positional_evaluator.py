import chess

from heuristic.evaluator import Evaluator
from heuristic.features.king_safety_evaluator import KingSafetyEvaluator
from heuristic.features.material_evaluator import MaterialEvaluator
from heuristic.features.pawn_structure_evaluator import PawnStructureEvaluator
from heuristic.features.phase_evaluator import PhaseEvaluator
from heuristic.features.piece_mobility_evaluator import PieceMobilityEvaluator
from heuristic.features.piece_square_evaluator import PieceSquareEvaluator
from heuristic.features.strategic_bonus_evaluator import StrategicBonusEvaluator


class PositionalEvaluator(Evaluator):
    def __init__(self,
                 material_evaluator: MaterialEvaluator,
                 piece_mobility_evaluator: PieceMobilityEvaluator,
                 pawn_structure_evaluator: PawnStructureEvaluator,
                 king_safety_evaluator: KingSafetyEvaluator,
                 strategic_bonus_evaluator: StrategicBonusEvaluator,
                 piece_square_evaluator: PieceSquareEvaluator):
        self.material_evaluator = material_evaluator
        self.piece_mobility_evaluator = piece_mobility_evaluator
        self.pawn_structure_evaluator = pawn_structure_evaluator
        self.king_safety_evaluator = king_safety_evaluator
        self.strategic_bonus_evaluator = strategic_bonus_evaluator
        self.piece_square_evaluator = piece_square_evaluator

    def evaluate_board(self, board: chess.Board) -> float:
        phase_value = PhaseEvaluator.evaluate(board)
        own_score = self._get_color_score(board, board.turn, phase_value)
        enemy_score = self._get_color_score(board, not board.turn, phase_value)
        return own_score - enemy_score

    def _get_color_score(self, board: chess.Board, color: bool, phase_value: float) -> float:
        score = 0.0
        score += self.material_evaluator.evaluate(board, color)
        score += self.piece_mobility_evaluator.evaluate(board, color, phase_value=phase_value)
        score += self.pawn_structure_evaluator.evaluate(board, color, phase_value=phase_value)
        score += self.king_safety_evaluator.evaluate(board, color, phase_value=phase_value)
        score += self.strategic_bonus_evaluator.evaluate(board, color)
        score += self.piece_square_evaluator.evaluate(board, color, phase_value=phase_value)
        return score
