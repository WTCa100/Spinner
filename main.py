from tkinter import *
from tkinter import ttk

import logging

from core.game import Game
from helpers.stats_helper import dump_statistics

logger = logging.getLogger("MainLoop")
logging.basicConfig(format="%(levelname)s (%(asctime)s) %(filename)s:%(lineno)s > %(msg)s", level=logging.DEBUG)

LUCKY_NUMBER = 13

class App():

    def _dump_stats(self, detailed=True):
        game_info = self.game.turn_snapshots
        dump_statistics(game_info, detailed)

    def _create_menus(self):
        main_menu_bar = Menu(self.root)
        game_menu = Menu(main_menu_bar)
        game_menu.add_command(label="Reset", command=self.game.reset)
        game_menu.add_command(label="Borrow money", command=self.game.loan)

        stats_menu = Menu(main_menu_bar)
        stats_menu.add_command(label="Dump final statistics", command=lambda: self._dump_stats(detailed=False))
        stats_menu.add_command(label="Dump detailed statistics", command=lambda: self._dump_stats())
        main_menu_bar.add_cascade(menu=game_menu, label="Game")
        main_menu_bar.add_cascade(menu=stats_menu, label="Stats")
        self.root['menu'] = main_menu_bar

    def _run(self):
        # This is function is a prepare function which gather information before starting main event loop.
        def proceed(self, popup_window):
            if len(self.player_name.get()):
                popup_window.destroy()
                self.game = Game(self.root, self.player_name)
                self._create_menus()
                return
            invalid_name_label = ttk.Label(master=popup_window, text="Please provide a user name!", foreground="Red")
            invalid_name_label.grid(column=0, row=2)
            popup_window.unbind("<Return>")

        name_getter_window = Toplevel()
        name_getter_window.wm_title("Insert your name:")
        name_getter_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        ttk.Label(name_getter_window, text="Name:").grid(column=0, row=0)
        name_entry = ttk.Entry(name_getter_window, textvariable=self.player_name)
        name_entry.grid(column=1, row=0)
        Tk.focus_force(name_entry)
        ttk.Button(name_getter_window, text="Done", command= lambda: proceed(self, name_getter_window)).grid(column=0, row=1)
        name_getter_window.bind("<Return>", func= lambda e: proceed(self, name_getter_window))

    def __init__(self, root: Tk):
        self.root = root
        self.root.wm_title("Slot machine game")
        self.root.geometry("640x480")
        self.root.resizable(False, False)
        self.player_name = StringVar(value="Jane Doe")

        self._run()

root = Tk()
App(root=root)
root.mainloop()
