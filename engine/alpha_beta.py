from typing import List, Dict

import chess

from heuristic.evaluator import Evaluator

CHECKMATE_SCORE = 10000
DRAW_SCORE = 0


class AlphaBeta:
    def __init__(self, evaluator: Evaluator):
        self.evaluator: Evaluator = evaluator
        self.transposition_table: Dict[int, dict] = {}

    def get_best_move(self, board: chess.Board, depth: int = 3) -> chess.Move:
        best_move = None
        max_eval = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for move in self.order_moves(board):
            board.push(move)
            # if board.can_claim_draw():
            #     score = -CHECKMATE_SCORE
            # else:
            #     score = -self.negamax(board, depth - 1, -beta, -alpha)
            score = -self.negamax(board, depth - 1, -beta, -alpha)
            board.pop()

            if score > max_eval:
                max_eval = score
                best_move = move

            alpha = max(alpha, score)

        return best_move

    def evaluate_root_moves(self, board: chess.Board, depth: int) -> Dict[chess.Move, float]:
        scores = {}
        for move in board.legal_moves:
            board.push(move)
            score = -self.negamax(board, depth - 1, -float('inf'), float('inf'))
            board.pop()
            scores[move] = score
        return scores

    def negamax(self, board: chess.Board, depth: int, alpha: float, beta: float) -> float:
        if board.is_checkmate():
            return -(CHECKMATE_SCORE + depth)

        if board.is_stalemate() or board.is_insufficient_material():
            return DRAW_SCORE

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

        for move in self.order_captures(board):
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
        """
        moves = list(board.legal_moves)
        return sorted(moves, key=lambda move: self.evaluator.evaluate_move(board, move), reverse=True)

    def order_captures(self, board: chess.Board) -> List[chess.Move]:
        """
        Ranks captures to evaluate the most promising ones first.
        """
        moves = list(board.generate_legal_captures())
        return sorted(moves, key=lambda move: self.evaluator.evaluate_capture(board, move), reverse=True)
