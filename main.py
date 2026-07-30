from tkinter import *
from tkinter import ttk
import random
import logging

LUCKY_NUMBER = 13

class Slots():
    def _calculate_win(self, numbers_dict: dict, wager: int):
        win = 0
        if LUCKY_NUMBER in numbers_dict.keys():
            # Power the win!
            print(f"DEBUG: LUCKY NUMBER present: {numbers_dict.keys()}")
            win += pow(wager, numbers_dict[LUCKY_NUMBER] + 1)

        for number, occurances in numbers_dict.items():
            print(f"DEBUG: Number of occurances of {number} -> {occurances}")
            if occurances > 1 and number != LUCKY_NUMBER:
                win += wager * occurances
        return win


    def _spin(self, *args):
        balance_numeric = self.balance.get()
        wager_numeric = self.wager.get() # for now
        if balance_numeric < wager_numeric:
            print(f"DEBUG: Cannot spin! {balance_numeric} < {wager_numeric}")
            return
        balance_numeric -= wager_numeric
        numbers_generated = {}
        for column in self.numbers:
            for row in self.numbers:
                generated = random.randint(0, 99)
                if generated in numbers_generated:
                    numbers_generated[generated] += 1
                else:
                    numbers_generated[generated] = 1
                self.numbers[column][row].set(generated)
        # very simple winning calculation
        win = self._calculate_win(numbers_dict=numbers_generated, wager=wager_numeric)
        print(f"DEBUG: Won {win} from wager {wager_numeric}. New balance {balance_numeric + win} old balance {balance_numeric}")
        self.balance.set(balance_numeric + win)

    def __init__(self, root: Tk):
        root.title = "Slot machine game"
        root.geometry("640x480")
        
        mainframe = ttk.Frame(root, borderwidth=1, border=1, padding=(10, 10, 10, 10))
        mainframe.grid(column=0, row=0, padx=25, pady=25)
        ttk.Label(mainframe, text="Slot machine").grid(column=1, row=3)

        slot_frame = ttk.Frame(root, borderwidth=1, border=1, relief="solid")
        slot_frame.grid(column=0, row=1, padx=20)

        self.numbers = {}
        for col in range(3):
            self.numbers[col] = []
            for row in range(3):
                self.numbers[col].append(IntVar(value=0))
                ttk.Label(slot_frame, textvariable=self.numbers[col][row], borderwidth=1, border=1, relief="raised", background="yellow").grid(column=col, row=row, padx=25, pady=5)

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
        ttk.Entry(balance_frame, textvariable=self.wager).grid(column=1, row=3)

        root.bind("<Return>", self._spin)

root = Tk()
Slots(root=root)
root.mainloop()
