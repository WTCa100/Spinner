from tkinter import *
from tkinter import ttk
import logging

from slot import Slot

logger = logging.getLogger("SlotLog")
logging.basicConfig(format="%(levelname)s (%(asctime)s) %(filename)s:%(lineno)s > %(msg)s", level=logging.DEBUG)

LUCKY_NUMBER = 13

class Slots():

    def _set_defalt_slot_style(self):
        for col in self.numbers_lbl:
            for row in self.numbers_lbl:
                self.numbers_lbl[col][row].reset_slot_color()

    def _validate_wager(self, P):
        return str.isdigit(P)

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

    def _spin(self, *args):
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

    def __init__(self, root: Tk):
        root.wm_title("Slot machine game")
        root.geometry("640x480")

        self.mainframe = ttk.Frame(root, borderwidth=1, border=1, padding=(10, 10, 10, 10))
        self.mainframe.grid(column=0, row=0, padx=25, pady=25, sticky=NSEW)
        ttk.Label(self.mainframe, text="Slot machine").grid(column=1, row=3)

        slot_frame = ttk.Frame(root, borderwidth=1, border=1, relief="solid")
        slot_frame.grid(column=0, row=1, padx=20)

        self.numbers = {}
        self.numbers_lbl: dict[int, list[Slot]] = {}
        for col in range(3):
            self.numbers[col] = []
            self.numbers_lbl[col] = []
            for row in range(3):
                self.numbers[col].append(IntVar(value=0))
                self.numbers_lbl[col].append(Slot(slot_frame, self.numbers[col][row], (col, row)))
        self._set_defalt_slot_style()
        spinning_frame = ttk.Frame(root, borderwidth=1, border=1, relief="ridge")
        spinning_frame.grid(column=0, row=2)
        ttk.Button(spinning_frame, text="! ! !Spin! ! !", command=self._spin).grid(column=2, row=0)

        balance_frame = ttk.Frame(root, borderwidth=1, border=1, relief="groove")
        balance_frame.grid(column=1, row=0)
        self.balance = IntVar(value=100)
        self.wager = IntVar(value=10)
        ttk.Label(balance_frame, text="Your balance:").grid(column=0, row=1)
        ttk.Label(balance_frame, textvariable=self.balance).grid(column=0, row=2)
        ttk.Label(balance_frame, text="Wager:").grid(column=0, row=3)

        validation_cmd = self.mainframe.register(self._validate_wager)
        ttk.Entry(balance_frame, textvariable=self.wager, validate="all", validatecommand=(validation_cmd, "%P")).grid(column=1, row=3)

        root.bind("<Return>", self._spin)

root = Tk()
Slots(root=root)
root.mainloop()
