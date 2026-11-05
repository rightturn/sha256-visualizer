import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Sigma:
    def __init__(self, main_frame, w, base='bin', clock=0, clock_shift=0, rotations=(7, 18), shift=3, sigma_index=0, color='primary', background_color='light',row = 0):
        self.w = w
        self.base = base
        self.clock = clock
        self.clock_shift = clock_shift
        self.rotations = rotations
        self.shift = shift
        self.sigma_index = sigma_index
        self.color = color
        self.background_color = background_color

        self.container = main_frame
        self.row = row
        # self.clear_scrolled_frame()

        self.setup_ui()

    def setup_ui(self):
        self.label_frame = ttk.Frame(self.container)
        self.label_frame.grid(row=self.row, column=0, sticky="ew")

        self.value_frame = ttk.Frame(self.container)
        self.value_frame.grid(row=self.row, column=1, sticky="ew")

        self.update_display()

    def update_display(self):
        input_value = self.w[self.clock - self.clock_shift]

        rotate1 = self.rotate_right(input_value, self.rotations[0])
        rotate2 = self.rotate_right(input_value, self.rotations[1])
        shift_op = input_value >> self.shift
        xor = rotate1 ^ rotate2 ^ shift_op

        if self.base == 'bin':
            display_text = f"W{self.clock - self.clock_shift}\n"
            display_value = f"{self.decimal_to_binary(input_value)}\n"

            display_text += f"right rotate {self.rotations[0]}\n"
            display_value += f"{self.decimal_to_binary(rotate1)} XOR\n"
            
            display_text += f"right rotate {self.rotations[1]}\n"
            display_value += f"{self.decimal_to_binary(rotate2)} XOR\n"

            display_text += f"right shift {self.shift}\n"
            display_value += f"{self.decimal_to_binary(shift_op)} XOR\n"

            display_text += f"σ{self.sigma_index}:\n"
            display_value += f"{self.decimal_to_binary(xor)}\n"



        self.label = ttk.Label(self.label_frame, text=display_text, bootstyle=f"{self.color}-inverse", justify=LEFT, wraplength=500)
        self.label.pack(fill=BOTH, expand=True, padx=0, pady=0)

        self.value = ttk.Label(self.value_frame, text=display_value, bootstyle=f"{self.color}-inverse", justify=LEFT, wraplength=500)
        self.value.pack(fill=BOTH, expand=True, padx=0, pady=0)

    def clear_scrolled_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    @staticmethod
    def rotate_right(value, shift):
        return (value >> shift) | (value << (32 - shift)) & 0xFFFFFFFF

    @staticmethod
    def decimal_to_binary(value):
        return format(value, '032b')

    def advance_step(self):
        if self.clock < len(self.w):
            self.clock += 1
            self.update_display()

    def go_back_step(self):
        if self.clock > 0:
            self.clock -= 1
            self.update_display()

    def run_steps(self):
        for _ in range(len(self.w) - self.clock):
            self.advance_step()

# Example usage:
# root = ttk.Window(themename="darkly")
# w = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
# sigma = Sigma(root, w, base='bin', clock=1)
# root.mainloop()
