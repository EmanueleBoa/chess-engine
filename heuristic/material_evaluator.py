from typing import Dict

import chess

from heuristic.evaluator import Evaluator


class MaterialEvaluator(Evaluator):
    def __init__(self, knight_value: float = 3, bishop_value: float = 3, rook_value: float = 5, queen_value: float = 9,
                 king_value: float = 200):
        super().__init__()
        self.piece_to_value: Dict[chess.PieceType, float] = {
            chess.PAWN: 1,
            chess.KNIGHT: knight_value,
            chess.BISHOP: bishop_value,
            chess.ROOK: rook_value,
            chess.QUEEN: queen_value,
            chess.KING: king_value,
        }

    @classmethod
    def from_dict(cls, params: Dict[str, float]):
        return cls(
            knight_value=params["knight_value"],
            bishop_value=params["bishop_value"],
            rook_value=params["rook_value"],
            queen_value=params["queen_value"],
            king_value=params["king_value"]
        )

    def evaluate_board(self, board: chess.Board) -> float:
        score = 0.0
        for piece, value in self.piece_to_value.items():
            score += len(board.pieces(piece, board.turn)) * value
            score -= len(board.pieces(piece, not board.turn)) * value
        return score

    def evaluate_move(self, board: chess.Board, move: chess.Move) -> float:
        score = 0.0
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            if victim and attacker:
                score += 10 * self.piece_to_value[victim.piece_type] - self.piece_to_value[attacker.piece_type]

        if move.promotion:
            score += self.piece_to_value[chess.QUEEN]

        return score

    def get_checkmate_score(self) -> float:
        return self.piece_to_value[chess.KING]
