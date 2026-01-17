from typing import Optional

import chess


def is_friendly_pawn(piece: Optional[chess.Piece], color: bool) -> bool:
    if piece is None:
        return False
    return piece.piece_type == chess.PAWN and piece.color == color


def is_central_file(file: int) -> bool:
    return file == 3 or file == 4


def is_king_too_advanced(king_rank: int, color: bool) -> bool:
    return (color == chess.WHITE and king_rank > 1) or (color == chess.BLACK and king_rank < 6)


def is_seventh_rank(rank: int, color: bool) -> bool:
    return (color == chess.WHITE and rank == 6) or (color == chess.BLACK and rank == 1)


def is_outpost(board: chess.Board, square: chess.Square, color: bool):
    rank = chess.square_rank(square)
    relative_rank = rank if color == chess.WHITE else 7 - rank
    if relative_rank < 3 or relative_rank > 5:
        return False

    file = chess.square_file(square)
    pawn_rank = rank - (1 if color == chess.WHITE else -1)
    for adjacent_file in [file - 1, file + 1]:
        if 0 <= adjacent_file <= 7:
            piece = board.piece_at(chess.square(adjacent_file, pawn_rank))
            if is_friendly_pawn(piece, color):
                return True
    return False
