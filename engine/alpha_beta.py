from typing import List

import chess

from heuristic.evaluator import Evaluator


class AlphaBeta:
    def __init__(self, evaluator: Evaluator):
        self.evaluator: Evaluator = evaluator

    def get_best_move(self, board: chess.Board, depth: int = 3) -> chess.Move:
        best_move = None
        max_eval = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for move in self.order_moves(board):
            board.push(move)
            score = -self.negamax(board, depth - 1, -beta, -alpha)
            board.pop()

            if score > max_eval:
                max_eval = score
                best_move = move

            alpha = max(alpha, score)

        return best_move

    def negamax(self, board: chess.Board, depth: int, alpha: float, beta: float) -> float:
        if board.is_checkmate():
            return -(self.evaluator.get_checkmate_score() + depth)

        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        if depth == 0:
            return self.quiescence_search(board, alpha, beta)

        max_eval = -float('inf')
        for move in self.order_moves(board):
            board.push(move)
            score = - self.negamax(board, depth - 1, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > max_eval:
                max_eval = score
            if score > alpha:
                alpha = score

        return max_eval

    def quiescence_search(self, board: chess.Board, alpha: float, beta: float) -> float:
        """
        Continues searching captures until the position is 'quiet'
        to avoid the horizon effect.
        """
        stand_pat = self.evaluator.evaluate_board(board)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in self.order_moves(board):
            if board.is_capture(move):
                board.push(move)
                score = -self.quiescence_search(board, -beta, -alpha)
                board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha

    def order_moves(self, board: chess.Board) -> List[chess.Move]:
        """
        Ranks moves to evaluate the most promising ones first.
        Captures are prioritized (MVV-LVA).
        """
        moves = list(board.legal_moves)
        return sorted(moves, key=lambda move: self.evaluator.evaluate_move(board, move), reverse=True)
