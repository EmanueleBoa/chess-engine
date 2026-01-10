from typing import List, Optional

import chess


class Board(chess.Board):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_legal_moves(self) -> List[chess.Move]:
        return list(self.legal_moves)

    def get_outcome(self) -> Optional[int]:
        if self.is_checkmate():
            return -1
        if self.is_draw():
            return 0
        return None

    def is_draw(self) -> bool:
        return self.is_stalemate() or self.is_insufficient_material() or self.is_fifty_moves() or self.is_repetition(3)
