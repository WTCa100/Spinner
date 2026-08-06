from tkinter import *
from tkinter import ttk

import logging

from image_helper.image_helper import ImageHelper
from machine import Machine
from player import Player

logger = logging.getLogger("MainLoop")
logging.basicConfig(format="%(levelname)s (%(asctime)s) %(filename)s:%(lineno)s > %(msg)s", level=logging.DEBUG)

LUCKY_NUMBER = 13

class App():
    def _validate_wager(self, P):
        return str.isdigit(P)

    def _reset(self, event=None):
        self.player.reset_stats()
        self.machine.reset_spin_count()
        self.wager.set(10)
        self.win_loose_ratio.set(0.0)

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

    def __init__(self, root: Tk):
        root.wm_title("Slot machine game")
        root.geometry("640x480")
        image_helper = ImageHelper()

        main_menu_bar = Menu(root)
        game_menu = Menu(main_menu_bar)
        game_menu.add_command(label="Reset", command=self._reset)
        main_menu_bar.add_cascade(menu=game_menu, label="Game")
        root['menu'] = main_menu_bar

        self.mainframe = ttk.Frame(root, borderwidth=1, border=1, padding=(10, 10, 10, 10))
        self.mainframe.grid(column=0, row=0, padx=25, pady=25, sticky=NSEW)
        self.machine = Machine(self.mainframe, image_helper)
        ttk.Button(self.mainframe, text="! ! !Spin! ! !", command=self._spin).grid(column=0, row=2)


        balance_frame = ttk.Frame(root, borderwidth=1, border=1, relief="groove")
        balance_frame.grid(column=1, row=0)
        self.player = Player(initial_balance=100, name="Jane Doe")
        self.wager = IntVar(value=10)
        self.payout = IntVar(value=0)
        ttk.Label(balance_frame, text="Your balance:").grid(column=0, row=0)
        ttk.Label(balance_frame, textvariable=self.player.balance).grid(column=1, row=0)
        ttk.Label(balance_frame, text="Wager:").grid(column=0, row=1)
        validation_cmd = self.mainframe.register(self._validate_wager)
        ttk.Entry(balance_frame, textvariable=self.wager, validate="all", validatecommand=(validation_cmd, "%P")).grid(column=1, row=1)
        ttk.Label(balance_frame, text="Payout:").grid(column=0, row=2)
        ttk.Label(balance_frame, textvariable=self.payout).grid(column=1, row=2)

        player_frame = ttk.Frame(root, borderwidth=1, border=1, relief="groove")
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



        root.bind("<Return>", self._spin)
        root.bind("R", self._reset)
        root.bind("r", self._reset)

root = Tk()
App(root=root)
root.mainloop()
