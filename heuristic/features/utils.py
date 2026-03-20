import chess


def is_central_file(file: int) -> bool:
    return file == 3 or file == 4


def is_king_too_advanced(king_rank: int, color: bool) -> bool:
    return (color == chess.WHITE and king_rank > 1) or (color == chess.BLACK and king_rank < 6)


def is_on_same_diagonal(square1: int, square2: int) -> bool:
    file1, rank1 = chess.square_file(square1), chess.square_rank(square1)
    file2, rank2 = chess.square_file(square2), chess.square_rank(square2)

    return (rank1 - file1 == rank2 - file2) or (rank1 + file1 == rank2 + file2)


def is_on_same_line(square1: int, square2: int) -> bool:
    is_same_file = chess.square_file(square1) == chess.square_file(square2)
    is_same_rank = chess.square_rank(square1) == chess.square_rank(square2)
    return is_same_file or is_same_rank
