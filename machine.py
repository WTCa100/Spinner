from tkinter import *
from tkinter import ttk

import logging

from image_helper.image_helper import ImageHelper
from slot import Slot

LUCKY_NUMBER = 13
logger = logging.getLogger("MachineLog")

class Machine:
    frame: ttk.Frame
    image_helper: ImageHelper
    slot_matrix: dict[int, list[Slot]]

    def __init__(self, master, image_helper):
        ttk.Label(master, text="Slot machine").grid(column=0, row=0)
        self.frame = ttk.Frame(master, borderwidth=2, relief="solid")
        self.frame.grid(column=0, row=1)

        spinning_frame = ttk.Frame(master)
        spinning_frame.grid(column=0, row=3)
        self.spin_count = IntVar(value=0)
        spin_counter_text = ttk.Label(spinning_frame, text="Spins: ")
        spin_counter = ttk.Label(spinning_frame, textvariable=self.spin_count)
        spin_counter_text.grid(column=0, row=3)
        spin_counter.grid(column=1, row=3)

        self.image_helper = image_helper
        self.slot_matrix = {}
        for col in range(3):
            self.slot_matrix[col] = [None, None, None]
            for row in range(3):
                self.slot_matrix[col][row] = Slot(self.frame, n_tkVar=IntVar(value=0), pos=(col, row), image_helper=self.image_helper)

        self._set_defalt_slot_style()

    def _set_defalt_slot_style(self):
        for col in self.slot_matrix:
            for row in self.slot_matrix:
                self.slot_matrix[col][row].reset_slot_color()

    def _calculate_win(self, wager: IntVar, slot_combination: dict[int, int]):
        win = 0

        if not wager:
            return win

        if LUCKY_NUMBER in slot_combination.keys():
            # Power the win!
            logger.debug(f"LUCKY NUMBER present: {slot_combination.keys()}")
            win += pow(wager, slot_combination[LUCKY_NUMBER] + 1)

        for number, occurances in slot_combination.items():
            logger.debug(f"Number of occurances of {number} -> {occurances}")
            if occurances > 1 and number != LUCKY_NUMBER:
                win += wager * occurances
        return win

    def spin(self, wager: int) -> int:
        self._set_defalt_slot_style()
        spin_result = {}
        for col in range(3):
            for row in range(3):
                generated = self.slot_matrix[col][row].generate()
                if generated == LUCKY_NUMBER:
                    self.slot_matrix[col][row].change_color_to_lucky()
                if generated in spin_result:
                    spin_result[generated] += 1
                else:
                    spin_result[generated] = 1
        self.spin_count.set(self.spin_count.get() + 1)
        win = self._calculate_win(wager, spin_result)
        logger.info(f"Spin {self.spin_count.get()} concluded with: wager={wager} win={win}")
        return win

    def reset_spin_count(self):
        self.spin_count.set(0)