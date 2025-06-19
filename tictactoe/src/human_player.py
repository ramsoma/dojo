import sys

from .player import Player


class HumanPlayer(Player):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def play(self, game, retry=False) -> (int, int):
        message = f"Please enter a slot to play between 0 and {game.gridsize**2 -1}" if not retry else \
                    "Invalid slot. Please re-enter a slot to play."
        print(message)
        while True:
            slot = sys.stdin.readline()
            try:
                slot = int(slot)
                if slot >= 0 and slot < game.gridsize**2:
                    break
                else:
                    raise ValueError()
            except ValueError:
                print("Please enter a valid number.")

        return slot // game.gridsize, slot % game.gridsize

    def learn(self, state):
        pass

    def say_something(self, game, result):
        print(f"Do you have anything to say {self.name}?")
        human_input = sys.stdin.readline()