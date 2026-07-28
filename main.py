from tkinter import *
from tkinter import ttk
import random

LUCKY_NUMBER = 13

def calculate_win(numbers_dict: dict, wager: int):
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

def spin(*args):
    balance_numeric = balance.get()
    wager_numeric = wager.get() # for now
    if balance_numeric < wager_numeric:
        print(f"DEBUG: Cannot spin! {balance_numeric} < {wager_numeric}")
        return
    balance_numeric -= wager_numeric
    numbers_generated = {}
    for column in numbers:
        for row in numbers:
            generated = random.randint(0, 99)
            if generated in numbers_generated:
                numbers_generated[generated] += 1
            else:
                numbers_generated[generated] = 1
            numbers[column][row].set(generated)
    # very simple winning calculation
    win = calculate_win(numbers_dict=numbers_generated, wager=wager_numeric)
    print(f"DEBUG: Won {win} from wager {wager_numeric}. New balance {balance_numeric + win} old balance {balance_numeric}")
    balance.set(balance_numeric + win)

root = Tk()
root.title("Spinner")
root.geometry("640x480")

mainframe = ttk.Frame(root, borderwidth=1, border=1, padding=(10, 10, 20, 20))
mainframe.grid(column=0, row=0, padx=25, pady=25, sticky=(W,S,N,E))
ttk.Label(mainframe, text="Slot machine").grid(column=1, row=3)

slot_frame = ttk.Frame(root, borderwidth=1, border=1, relief="solid")
slot_frame.grid(column=0, row=1, sticky=(W, S, N, E), padx=20)
numbers = {}
for col in range(3):
    numbers[col] = []
    for row in range(3):
        numbers[col].append(IntVar(value=0))
        ttk.Label(slot_frame, textvariable=numbers[col][row], borderwidth=2, relief="raised", background="yellow").grid(column=col, row=row, padx=25, pady=5, sticky=W)

spinning_frame = ttk.Frame(root, borderwidth=1, border=1, relief="ridge")
spinning_frame.grid(column=0, row=2)
ttk.Button(spinning_frame, text="! ! !Spin! ! !", command=spin).grid(column=2, row=0)

balance_frame = ttk.Frame(root, borderwidth=1, border=1, relief="groove")
balance_frame.grid(column=1, row=0)
balance = IntVar(value=100)
wager = IntVar(value=10)
ttk.Label(balance_frame, text="Your balance:").grid(column=0, row=1)
ttk.Label(balance_frame, textvariable=balance).grid(column=0, row=2)
ttk.Label(balance_frame, text="Wager:").grid(column=0, row=3)
ttk.Entry(balance_frame, textvariable=wager).grid(column=1, row=3)

root.bind("<Return>", spin)

root.mainloop()