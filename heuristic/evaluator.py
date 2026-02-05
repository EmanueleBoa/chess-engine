from abc import ABC, abstractmethod

import chess

from heuristic.features.material_evaluator import PAWN_VALUE, KNIGHT_VALUE, BISHOP_VALUE, ROOK_VALUE, QUEEN_VALUE

PIECE_TO_VALUE = {
    chess.PAWN: PAWN_VALUE,
    chess.KNIGHT: KNIGHT_VALUE,
    chess.BISHOP: BISHOP_VALUE,
    chess.ROOK: ROOK_VALUE,
    chess.QUEEN: QUEEN_VALUE
}


class Evaluator(ABC):
    @abstractmethod
    def evaluate_board(self, board: chess.Board) -> float:
        """
        Evaluate a chess position for the color to move.

        Args:
            board: The chess board to evaluate

        Returns:
            A float score representing the evaluation of the board for the color to move
        """
        pass

    @staticmethod
    def evaluate_move(board: chess.Board, move: chess.Move) -> float:
        """
        Captures (MVV-LVA) and promotions are prioritized.
        """
        score = 0.0
        if board.is_capture(move):
            score += Evaluator.evaluate_capture(board, move)

        if move.promotion:
            score += PIECE_TO_VALUE[chess.QUEEN]

        return score

    @staticmethod
    def evaluate_capture(board: chess.Board, move: chess.Move) -> float:
        victim_piece = board.piece_at(move.to_square)
        attacker_piece = board.piece_at(move.from_square)
        if victim_piece and attacker_piece:
            victim_value = PIECE_TO_VALUE.get(victim_piece.piece_type, 0.)
            attacker_value = PIECE_TO_VALUE.get(attacker_piece.piece_type, 0.)
            return 10 * victim_value - attacker_value
        return 0.0
