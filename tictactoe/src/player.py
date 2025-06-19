from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def play(self, game, retry) -> (int, int):
        raise NotImplementedError("Please implement your own")

    @abstractmethod
    def learn(self, game):
        raise NotImplementedError("Please implement your own")

    @abstractmethod
    def say_something(self, game, result):
        raise NotImplementedError("Please implement your own")