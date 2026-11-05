import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from tkinter import StringVar
from tkinter import Tk

# Utility functions
def decimal_to_binary(value):
    return bin(value)[2:].zfill(32)

def rotate_right(value, amount):
    return ((value >> amount) | (value << (32 - amount))) & 0xFFFFFFFF

def display_hex(value):
    hex_value = format(value & 0xFFFFFFFF, '08x')
    return ' '.join(hex_value[i:i+2] for i in range(0, len(hex_value), 2))

class WordResult():
    def __init__(self, main_frame, w, first_loop, base = 'bin'):
        self.w = w
        self.first_loop = first_loop
        self.base = base

        self.container = main_frame

        self.create_widgets()

    def create_widgets(self):
        w16 = self.w[self.first_loop - 17]
        w7 = self.w[self.first_loop - 8]

        rotate7 = rotate_right(self.w[self.first_loop - 16], 7)
        rotate18 = rotate_right(self.w[self.first_loop - 16], 18)
        shift3 = self.w[self.first_loop - 16] >> 3
        s0 = rotate7 ^ rotate18 ^ shift3

        rotate17 = rotate_right(self.w[self.first_loop - 3], 17)
        rotate19 = rotate_right(self.w[self.first_loop - 3], 19)
        shift10 = self.w[self.first_loop - 3] >> 10
        s1 = rotate17 ^ rotate19 ^ shift10

        sum_result = (w16 + s0 + w7 + s1) % (2 ** 32)

        column_number = 1
        if self.base == 'hex':
            ttk.Label(self.container, text=display_hex(w16)).grid(row=2, column=column_number, sticky='w')
            ttk.Label(self.container, text=display_hex(s0)).grid(row=3, column=column_number, sticky='w')
            ttk.Label(self.container, text=display_hex(w7)).grid(row=4, column=column_number, sticky='w')
            ttk.Label(self.container, text=display_hex(s1)).grid(row=5, column=column_number, sticky='w')
            ttk.Label(self.container, text=display_hex(sum_result)).grid(row=6, column=column_number, sticky='w')
        elif self.base == 'bin':

            ttk.Label(self.container, text=f"W{self.first_loop - 17}", style='success.TLabel').grid(row=2, column=0, sticky='w')
            ttk.Label(self.container, text=decimal_to_binary(w16), style='success.TLabel').grid(row=2, column=column_number, sticky='w')

            ttk.Label(self.container, text=f"σ0").grid(row=3, column=0, sticky='w')
            ttk.Label(self.container, text=decimal_to_binary(s0) + " +").grid(row=3, column=column_number, sticky='w')

            ttk.Label(self.container, text=f"W{self.first_loop - 8}", style='warning.TLabel').grid(row=4, column=0, sticky='w')
            ttk.Label(self.container, text=decimal_to_binary(w7) + " +", style='warning.TLabel').grid(row=4, column=column_number, sticky='w')

            ttk.Label(self.container, text=f"σ1").grid(row=5, column=0, sticky='w')
            ttk.Label(self.container, text=decimal_to_binary(s1) + " +").grid(row=5, column=column_number, sticky='w')

            ttk.Label(self.container, text=f"W{self.first_loop - 1}", style='info.TLabel').grid(row=6, column=0, sticky='w')
            ttk.Label(self.container, text=decimal_to_binary(sum_result), style='info.TLabel').grid(row=6, column=column_number, sticky='w')

# if __name__ == "__main__":
#     root = Tk()
#     style = Style(theme='darkly')
#     w = [0] * 64  # Replace this with actual values
#     first_loop = 17  # Replace this with actual value
#     base = 'bin'  # Change to 'bin' for binary representation

#     frame = WordResult(root, w, first_loop, base)
#     frame.pack(padx=10, pady=10)

#     root.mainloop()
