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

    COLOR_PALLET = [
        "#00ffff",
        "#dc143c",
        "#ff00ff",
        "#00ff00",
        "#9370db",
        "#00008b",
        "#6b8e23",
        "#2e8b57"
    ]
    color_pointer = 0

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

    def _get_color(self):
        current_color = self.COLOR_PALLET[self.color_pointer]

        if self.color_pointer == len(self.COLOR_PALLET) - 1:
            self.color_pointer = 0
        else:
            self.color_pointer += 1

        return current_color

    def _set_defalt_slot_style(self):
        for col in self.slot_matrix:
            for row in self.slot_matrix:
                self.slot_matrix[col][row].reset_slot_color()

    def _color_winning_slots(self, winning_symbol_code: int):
        color = self._get_color()
        for col in self.slot_matrix:
            for row in self.slot_matrix:
                current_slot = self.slot_matrix[col][row]
                if current_slot.number_var.get() == winning_symbol_code:
                    current_slot.change_color_winner(color)

    def _calculate_win(self, wager: IntVar, slot_combination: dict[int, int]):
        win = 0

        if not wager:
            return win

        for number, occurances in slot_combination.items():
            if occurances > 1 and number != LUCKY_NUMBER:
                win += wager * occurances
                self._color_winning_slots(number)
                logger.debug(f"Winning symbol code: {number}. Occurances: {occurances}")

        if LUCKY_NUMBER in slot_combination.keys():
            # Power the win!
            logger.debug(f"LUCKY NUMBER present: {slot_combination.keys()}")
            win *= slot_combination[LUCKY_NUMBER] + 1 if win else wager * slot_combination[LUCKY_NUMBER]
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