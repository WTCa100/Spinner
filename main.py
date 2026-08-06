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

    def _spin(self, *args):
        balance_numeric = self.player.balance.get()
        wager_numeric = self.wager.get()
        balance_numeric -= wager_numeric
        win = self.machine.spin(wager=wager_numeric)
        balance_numeric += win
        self.player.balance.set(balance_numeric)

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
        ttk.Label(balance_frame, text="Your balance:").grid(column=0, row=1)
        ttk.Label(balance_frame, textvariable=self.player.balance).grid(column=0, row=2)
        ttk.Label(balance_frame, text="Wager:").grid(column=0, row=3)

        validation_cmd = self.mainframe.register(self._validate_wager)
        ttk.Entry(balance_frame, textvariable=self.wager, validate="all", validatecommand=(validation_cmd, "%P")).grid(column=1, row=3)

        root.bind("<Return>", self._spin)
        root.bind("R", self._reset)
        root.bind("r", self._reset)

root = Tk()
App(root=root)
root.mainloop()
