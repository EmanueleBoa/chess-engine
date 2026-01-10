from abc import ABC, abstractmethod


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, board) -> float:
        pass
