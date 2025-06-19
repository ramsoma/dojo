import enum
import pickle
import random
from random import randint

import numpy as np
from collections import defaultdict
from .player import Player
from .tictactoe import Result
from openai import OpenAI


class Rewards(enum.Enum):
    WIN = 1.0
    LOSS = -1.0
    DRAW = 0.5


class QLearningAgent(Player):
    def __init__(self, id, name, experience, personality, learning, example_quotes):
        self.alpha = learning / 1000
        self.id = id
        self.iter = 0#1_0000_0000
        self.Q = defaultdict()
        self.name = name
        self.personality = personality
        self.example_quotes = example_quotes
        self.experience = experience
        try:
             with open(f"pickles/player{id}_{experience}.pkl",'rb') as file:
                 self.Q = pickle.load(file)
        except FileNotFoundError:
             self.Q = defaultdict()


    def play(self, game, retry=False) -> (int, int):
        state = ",".join(game.state.reshape(-1))

        if state not in self.Q or random.random() > (1. - self.iter / 10000):
            return np.array([randint(0, game.gridsize - 1), randint(0, game.gridsize - 1)])
        arr = self.Q[state]
        order = np.dstack(np.unravel_index(np.argsort(arr.ravel()), (3, 3))).reshape((9,2))[::-1]
        for i in range(order.shape[0]):
            if game.is_valid(order[i,0], order[i,1]):
                return order[i]


    def learn(self, game):
        result = game.results[self.id]
        reward = Rewards.WIN.value if result.value == Result.WIN.value \
            else (Rewards.LOSS.value if result.value == Result.LOSS.value else Rewards.DRAW.value)
        strt = len(game.moves) - 2 if result.value == Result.LOSS.value else (len(game.moves)-1  if result.value == Result.WIN.value
                                                                  else len(game.moves) - (1 + self.id))
        for i in range(len(game.moves) // 2):
            #import pdb; pdb.set_trace()
            move_idx = strt - 2 * i
            state = game.states[move_idx]
            move = game.moves[move_idx]
            if state not in self.Q:
                self.Q[state] = np.random.random((game.gridsize, game.gridsize))
            self.Q[state][move[0], move[1]] = self.Q[state][move[0], move[1]] * (1 - self.alpha) + self.alpha * reward
            #sign = -1.0 if result != Result.DRAW else 1.0
            reward *= 0.95

    def say_something(self, game, result):
        client = OpenAI()
        result_str = result
        if type(result) is Result:
            result_str = "won" if result.value == Result.Win.value else \
                    "lost" if result.value == Result.LOSS.value else "draw"
        prompt = f"""
        You are a tic-tact-toe playing bot. Your name is {self.name}. Your personality is {self.personality}.
        You are playing with a 10 year old and you must use simple language.
        Some example quotes are:
        {self.example_quotes}
        You just {result_str} your game. What would you say? 
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            stream=False,
        )
        return response.choices[0].message.content
