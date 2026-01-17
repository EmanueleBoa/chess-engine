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

    def evaluate_move(self, board: chess.Board, move: chess.Move) -> float:
        score = 0.0
        if board.is_capture(move):
            victim_piece = board.piece_at(move.to_square)
            attacker_piece = board.piece_at(move.from_square)
            if victim_piece and attacker_piece:
                victim_value = self._get_piece_value(victim_piece.piece_type)
                attacker_value = self._get_piece_value(attacker_piece.piece_type)
                score += 10 * victim_value - attacker_value

        if move.promotion:
            score += self._get_piece_value(chess.QUEEN)

        return score

    def _get_piece_value(self, piece_type: chess.PieceType) -> float:
        return self.material_evaluator.get_piece_value(piece_type)
