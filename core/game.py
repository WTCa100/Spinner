from tkinter import *
from tkinter import ttk

import logging

from core.slot import Slot
from core.machine import Machine
from core.player import Player
from image_helper.image_helper import ImageHelper

logger = logging.getLogger("Game")
logging.basicConfig(format="%(levelname)s (%(asctime)s) %(filename)s:%(lineno)s > %(msg)s", level=logging.DEBUG)

class Game:

    def _validate_wager(self, P):
        return str.isdigit(P)

    def reset(self, event=None):
        self.player.reset_stats()
        self.machine.reset_spin_count()
        self.wager.set(10)
        self.win_loose_ratio.set(0.0)

    def loan(self, event=None):
        current_player_balance = self.player.balance.get()
        new_player_balance =  current_player_balance + 1000
        logger.info(f"Loan taken with current player balance: {current_player_balance} -> {new_player_balance}")
        self.player.balance.set(new_player_balance)

    def _spin(self, *args):
        balance_numeric = self.player.balance.get()
        wager_numeric = self.wager.get()

        if balance_numeric < wager_numeric:
            return

        balance_numeric -= wager_numeric
        win = self.machine.spin(wager=wager_numeric)

        logger.debug(f"Won: {win}")
        if win > 0:
            self.player.n_wins.set(self.player.n_wins.get() + 1)
        else:
            self.player.n_looses.set(self.player.n_looses.get() + 1)
        self.win_loose_ratio.set(self.player.n_wins.get() / self.machine.spin_count.get())

        balance_numeric += win
        self.player.balance.set(balance_numeric)
        self.payout.set(win)

    def __init__(self, root: Tk, player_name: StringVar):
        self.root = root
        image_helper = ImageHelper()

        self.mainframe = ttk.Frame(self.root, borderwidth=1, border=1, padding=(10, 10, 10, 10))
        self.mainframe.grid(column=0, row=0, padx=25, pady=25, sticky=NSEW)
        self.machine = Machine(self.mainframe, image_helper)
        ttk.Button(self.mainframe, text="! ! !Spin! ! !", command=self._spin).grid(column=0, row=2)

        balance_frame = ttk.Frame(self.root, borderwidth=1, border=1, relief="groove")
        balance_frame.grid(column=1, row=0)
        self.player = Player(initial_balance=100, name=player_name.get())
        self.wager = IntVar(value=10)
        self.payout = IntVar(value=0)
        ttk.Label(balance_frame, text="Your balance:").grid(column=0, row=0)
        ttk.Label(balance_frame, textvariable=self.player.balance).grid(column=1, row=0)
        ttk.Label(balance_frame, text="Wager:").grid(column=0, row=1)
        validation_cmd = self.mainframe.register(self._validate_wager)
        ttk.Entry(balance_frame, textvariable=self.wager, validate="all", validatecommand=(validation_cmd, "%P")).grid(column=1, row=1)
        ttk.Label(balance_frame, text="Payout:").grid(column=0, row=2)
        ttk.Label(balance_frame, textvariable=self.payout).grid(column=1, row=2)

        player_frame = ttk.Frame(self.root, borderwidth=1, border=1, relief="groove")
        player_frame.grid(column=1, row=1)
        ttk.Label(player_frame, text="Name:").grid(column=0, row=0)
        ttk.Label(player_frame, textvariable=self.player.name).grid(column=1, row=0)
        ttk.Label(player_frame, text="Wins:").grid(column=0, row=1)
        ttk.Label(player_frame, textvariable=self.player.n_wins).grid(column=1, row=1)
        ttk.Label(player_frame, text="Looses:").grid(column=0, row=2)
        ttk.Label(player_frame, textvariable=self.player.n_looses).grid(column=1, row=2)
        ttk.Label(player_frame, text="Ratio:").grid(column=0, row=3)
        self.win_loose_ratio = DoubleVar(value=0)
        ttk.Label(player_frame, textvariable=self.win_loose_ratio).grid(column=1, row=3)


        self.root.bind("<Return>", self._spin)
        self.root.bind("R", self.reset)
        self.root.bind("r", self.reset)
        self.root.bind("B", self.loan)
        self.root.bind("b", self.loan)