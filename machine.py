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
        self.frame = ttk.Frame(borderwidth=2, relief="solid")
        self.frame.grid()
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
                if generated in spin_result:
                    spin_result[generated] += 1
                else:
                    spin_result[generated] = 1
        return self._calculate_win(wager, spin_result)