from tkinter import *
from tkinter import ttk

import logging

from core.game import Game

logger = logging.getLogger("MainLoop")
logging.basicConfig(format="%(levelname)s (%(asctime)s) %(filename)s:%(lineno)s > %(msg)s", level=logging.DEBUG)

LUCKY_NUMBER = 13

class App():
    def _run(self):
        # This is function is a prepare function which gather information before starting main event loop.
        def proceed(self, popup_window):
            if len(self.player_name.get()):
                popup_window.destroy()
                self.game = Game(self.root, self.player_name)
                return
            invalid_name_label = ttk.Label(master=popup_window, text="Please provide a user name!", foreground="Red")
            invalid_name_label.grid(column=0, row=2)

        name_getter_window = Toplevel()
        name_getter_window.wm_title("Insert your name:")
        name_getter_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        Tk.focus_force(name_getter_window)
        ttk.Label(name_getter_window, text="Name:").grid(column=0, row=0)
        ttk.Entry(name_getter_window, textvariable=self.player_name).grid(column=1, row=0)
        ttk.Button(name_getter_window, text="Done", command= lambda: proceed(self, name_getter_window)).grid(column=0, row=1)

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
