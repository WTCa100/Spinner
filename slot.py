from tkinter import *
from tkinter import ttk

import random

class Slot:
    number_var: IntVar
    weight: float
    symbol: str
    position: tuple[int, int]
    frame: ttk.Frame

    def __init__(self, root: ttk.Frame, n_tkVar: IntVar, pos: tuple[int, int]):
        self.number_var = n_tkVar
        number_value = self.number_var.get()
        # Temporar logic for now
        if number_value % 2 == 0:
            w = 0.5
        else:
            w = 1

        # We will have to add some switches later on here
        s = f"Symbol_{number_value}"
        self.position = pos
        self.frame = ttk.Label(root, textvariable=self.number_var, borderwidth=1, border=1, relief="raised", background="yellow")
        self.frame.grid(column=self.position[0], row=self.position[1], padx=25, pady=5) # Magic numbers for now

    def __eq__(self, other):
        return self.number == other

    def generate(self):
        generated = random.randint(0, 19)
        self.number_var.set(generated)
        return generated

    def change_color_to_lucky(self):
        self.frame.configure(background="green")

    def reset_slot_color(self):
        self.frame.configure(background="yellow")
