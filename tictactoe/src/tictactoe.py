import enum
import pickle
import sys

import numpy as np
import yaml


class Result(enum.Enum):
    WIN = 1
    LOSS = 0
    DRAW = 2
    INPROGRESS = 3


class TicTacToe:

    def __init__(self, player_1, player_2, is_interactive):
        self.gridsize = 3
        self.state = self.init_board(self.gridsize)
        self.players = [player_1, player_2]
        self.symbols = ['X', 'O']
        self.winner = None
        self.is_interactive = is_interactive
        self.results = [Result.INPROGRESS, Result.INPROGRESS]
        self.states = [",".join(self.state.reshape(-1))]
        self.moves = []

    def play(self):
        i = 0
        for i in range(9):
            current_player = self.players[i % 2]
            retry = False
            while True:
                idx = current_player.play(self, retry)
                x, y = idx[0], idx[1]
                if self.is_valid(x, y):
                    break
                retry = True

            self.update_state(self.symbols[i % 2], x, y)
            self.moves.append([x, y])
            if self.is_interactive:
                self.print_board()
            if self.wins(current_player):
                if self.is_interactive:
                    print(f" {self.players[i % 2].name} wins!")
                self.winner = current_player
                self.results[i % 2] = Result.WIN
                self.results[(i + 1) % 2] = Result.LOSS
                break
            self.states.append(",".join(self.state.reshape(-1)))

        if self.winner is None and self.is_interactive:
            print("Its a DRAWWWWW..")
            self.results = [Result.DRAW, Result.DRAW]

    def update_state(self, symbol, x, y):
        self.state[x, y] = symbol

    def is_valid(self, x, y):
        return self.state[x, y] == ' '

    def wins(self, current_player):
        symbol = self.symbols[current_player.id]
        series = [symbol] * 3
        if np.all(self.state[0, :] == series) or np.all(self.state[1, :] == series) or np.all(
                self.state[2, :] == series):
            return True
        if np.all(self.state[:, 0] == series) or np.all(self.state[:, 1] == series) or np.all(
                self.state[:, 2] == series):
            return True
        if np.all(np.diagonal(self.state) == series) or np.all(self.state[:, ::-1].diagonal() == series):
            return True

    def init_board(self, n):
        return np.array([[' ' for i in range(n)] for j in range(n)])

    def print_board(self):
        print("------")
        for i in range(self.gridsize):
            print("|".join(self.state[i,:]))
            print("------")

if __name__ == '__main__':
    from .qlearning_agent import QLearningAgent
    from .human_player import HumanPlayer

    interactive = True
    bot_config = yaml.safe_load(open('config/bot_config.yaml'))
    print("Please enter your name.")
    name = sys.stdin.readline().strip()
    print("Please specify which bot you want to play against.")
    for i, ibot_config in enumerate(bot_config):
        print(f"{i}: {ibot_config['name']}")

    bot_name = sys.stdin.readline().strip()
    ibot_config = [b for b in bot_config if b['name'] == bot_name][0]

    player1 = HumanPlayer(0, name=name)
    player2 = QLearningAgent(1,
                             experience = ibot_config['experience'],
                             learning=ibot_config['learning'],
                             name=ibot_config['name'],
                             personality=ibot_config['personality'],
                             example_quotes = ibot_config['example_quotes'])
    if interactive:
        print(player2.say_something(None, "Greeting and Game start."))
    win, loss, draw = 0, 0, 0
    for i in range(1500):
        game = TicTacToe(player_1=player1, player_2=player2, is_interactive=interactive)
        game.play()
        if game.winner == player2:
            win +=1
        elif game.winner == player1:
            loss +=1
        else:
            draw +=1
        #player1.learn(game)
        player2.learn(game)
        if interactive:
            print(player2.say_something(game,game.results[1]))
            player1.say_something(game, game.results[0])
        if i%100 == 0:
            print(i, win, loss, draw)
            win, loss, draw = 0, 0, 0
    #pickle.dump(player1.Q, open("player0.pkl", "wb"))
    pickle.dump(player2.Q, open(f"pickles/player1_{player2.experience}.pkl", "wb"))
    print(win, loss, draw)