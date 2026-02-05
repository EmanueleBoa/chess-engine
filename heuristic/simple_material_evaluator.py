import chess

from heuristic.evaluator import Evaluator
from heuristic.features.material_evaluator import MaterialEvaluator


class SimpleMaterialEvaluator(Evaluator):
    def __init__(self, material_evaluator: MaterialEvaluator):
        self.material_evaluator = material_evaluator

    def evaluate_board(self, board: chess.Board) -> float:
        own_score = self.material_evaluator.evaluate(board, board.turn)
        enemy_score = self.material_evaluator.evaluate(board, not board.turn)
        return own_score - enemy_score
