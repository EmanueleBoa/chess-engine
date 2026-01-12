from abc import ABC, abstractmethod


class Evaluator(ABC):
    @abstractmethod
    def evaluate_board(self, board) -> float:
        pass

    @abstractmethod
    def evaluate_move(self, board, move) -> float:
        pass

    @abstractmethod
    def get_checkmate_score(self) -> float:
        pass
