from tkinter import *
from tkinter import ttk
import logging

from slot import Slot
from image_helper.image_helper import ImageHelper

logger = logging.getLogger("GameLogger")

LUCKY_NUMBER = 13

class Game:
    mainframe: ttk.Frame
    panel_frame: ttk.Frame
    machine_frame: ttk.Frame
    image_helper: ImageHelper

    balance: IntVar
    wager: IntVar
    spin_n: int
    slot_matrix: list[list[Slot]]

    def __init__(self, master, image_helper):
        self.mainframe = ttk.Frame(master=master)
        self.mainframe.pack()

        self.machine_frame = ttk.Frame(master=self.mainframe)
        self.machine_frame.pack()

        self.image_helper = image_helper
        self.balance.set(100)
        self.wager.set(10)
        self.spin_n = 0
        for col in range(3):
            for row in range(3):
                self.slot_matrix[col][row] = Slot(self.machine_frame, n_tkVar=IntVar(0), pos=(col, row), image_helper=self.image_helper)

    def _set_defalt_slot_style(self):
        for col in self.numbers_lbl:
            for row in self.numbers_lbl:
                self.numbers_lbl[col][row].reset_slot_color()

    def _validate_wager(self, P):
        return str.isdigit(P)

    def restart(self):
        self.balance.set(100)
        self.wager.set(10)

    def _calculate_win(self, numbers_dict: dict, wager: int):
        win = 0

        if not wager:
            return win

        if LUCKY_NUMBER in numbers_dict.keys():
            # Power the win!
            logger.debug(f"LUCKY NUMBER present: {numbers_dict.keys()}")
            win += pow(wager, numbers_dict[LUCKY_NUMBER] + 1)

        for number, occurances in numbers_dict.items():
            logger.debug(f"Number of occurances of {number} -> {occurances}")
            if occurances > 1 and number != LUCKY_NUMBER:
                win += wager * occurances
        return win

    def spin(self):
        self._set_defalt_slot_style()
        balance_numeric = self.balance.get()
        wager_numeric = self.wager.get()

        if balance_numeric < wager_numeric:
            logger.info(f"Cannot spin! {balance_numeric} < {wager_numeric}")
            return

        balance_numeric -= wager_numeric
        numbers_generated = {}
        for column in self.numbers:
            for row in self.numbers:
                generated = self.numbers_lbl[column][row].generate()
                if generated in numbers_generated:
                    numbers_generated[generated] += 1
                else:
                    numbers_generated[generated] = 1

                if generated == LUCKY_NUMBER:
                    self.numbers_lbl[column][row].change_color_to_lucky()

                self.numbers[column][row].set(generated)
        # very simple winning calculation
        win = self._calculate_win(numbers_dict=numbers_generated, wager=wager_numeric)
        logger.info(f"Won {win} from wager {wager_numeric}. New balance {balance_numeric + win} old balance {balance_numeric}")
        self.balance.set(balance_numeric + win)
        self.spin_n += 1