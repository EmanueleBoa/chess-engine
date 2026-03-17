import chess


def is_central_file(file: int) -> bool:
    return file == 3 or file == 4


def is_king_too_advanced(king_rank: int, color: bool) -> bool:
    return (color == chess.WHITE and king_rank > 1) or (color == chess.BLACK and king_rank < 6)
