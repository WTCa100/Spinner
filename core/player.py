from tkinter import *

class Player:
    balance: IntVar
    n_wins: IntVar
    n_looses: IntVar
    name: StringVar


    def __init__(self, initial_balance, name):
        self.balance = IntVar(value=initial_balance)
        self.n_wins = IntVar(value=0)
        self.n_looses = IntVar(value=0)
        self.name = StringVar(value=name)

    def reset_stats(self):
        self.balance.set(100)
        self.n_wins.set(0)
        self.n_looses.set(0)
