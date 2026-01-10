import math
from typing import Dict

import chess

from engine.board import Board
from heuristic.evaluator import Evaluator


class MaterialEvaluator(Evaluator):
    def __init__(self, knight_value: float = 3, bishop_value: float = 3, rook_value: float = 5, queen_value: float = 9,
                 scale: float = 5.0):
        super().__init__()
        self.knight_value = knight_value
        self.bishop_value = bishop_value
        self.rook_value = rook_value
        self.queen_value = queen_value
        self.scale = scale

    @classmethod
    def from_dict(cls, params: Dict[str, float]):
        return cls(
            knight_value=params["knight_value"],
            bishop_value=params["bishop_value"],
            rook_value=params["rook_value"],
            queen_value=params["queen_value"],
            scale=params["scale"]
        )

    def evaluate(self, board: Board) -> float:
        score = self.evaluate_material(board)
        return math.tanh(score / self.scale)

    def evaluate_material(self, board: chess.Board) -> float:
        piece_values = {
            chess.PAWN: 1.0,
            chess.KNIGHT: self.knight_value,
            chess.BISHOP: self.bishop_value,
            chess.ROOK: self.rook_value,
            chess.QUEEN: self.queen_value,
            chess.KING: 0.0
        }

        score = 0.0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                score += value if piece.color == board.turn else -value

        return score

    # def evaluate_material(self, board: chess.Board) -> float:
    #     score = 0.0
    #     score += len(board.pieces(chess.PAWN, board.turn))
    #     score -= len(board.pieces(chess.PAWN, not board.turn))
    #     score += len(board.pieces(chess.KNIGHT, board.turn)) * self.knight_value
    #     score -= len(board.pieces(chess.KNIGHT, not board.turn)) * self.knight_value
    #     score += len(board.pieces(chess.BISHOP, board.turn)) * self.bishop_value
    #     score -= len(board.pieces(chess.BISHOP, not board.turn)) * self.bishop_value
    #     score += len(board.pieces(chess.ROOK, board.turn)) * self.rook_value
    #     score -= len(board.pieces(chess.ROOK, not board.turn)) * self.rook_value
    #     score += len(board.pieces(chess.QUEEN, board.turn)) * self.queen_value
    #     score -= len(board.pieces(chess.QUEEN, not board.turn)) * self.queen_value
    #     return score
