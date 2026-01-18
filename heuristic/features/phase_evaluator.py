import chess

KNIGHT_VALUE = 1
BISHOP_VALUE = 1
ROOK_VALUE = 2
QUEEN_VALUE = 4

MAX_VALUE = 2 * QUEEN_VALUE + 4 * ROOK_VALUE + 4 * BISHOP_VALUE + 4 * KNIGHT_VALUE

PIECE_TO_VALUE = {
    chess.KNIGHT: KNIGHT_VALUE,
    chess.BISHOP: BISHOP_VALUE,
    chess.ROOK: ROOK_VALUE,
    chess.QUEEN: QUEEN_VALUE
}


class PhaseEvaluator:
    """
    Evaluates the phase of the game based on the number of minor and major pieces remaining.
    """

    @staticmethod
    def evaluate(board: chess.Board) -> float:
        """
        Returns a value between 0 and 1, where 1 is the opening and 0 is the endgame.
        """
        score = 0.0
        for piece, value in PIECE_TO_VALUE.items():
            score += (len(board.pieces(piece, True)) + len(board.pieces(piece, False))) * value
        return min(1.0, score / MAX_VALUE)
