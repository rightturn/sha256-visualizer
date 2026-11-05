import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Explainer():
    def __init__(self, main_frame, clock=0, input='', input_base='text', chunks_count=1, last_clock=100, master_clock=0):
        self.clock = clock
        self.input = input
        self.input_base = input_base
        self.chunks_count = chunks_count
        self.last_clock = last_clock
        self.master_clock = master_clock

        self.container = main_frame
        self.clear_scrolled_frame()

        # Message block would be calculated here; placeholder for now
        self.message_block = {'LBinary': '101010', 'L': len(input), 'K': 0, 'result': 'binary_message_block'}

        self.setup_ui()

    def setup_ui(self):
        self.label = ttk.Label(self.container, text='', bootstyle="warning", justify=LEFT, wraplength=500)
        self.label.pack(fill=BOTH, expand=True, padx=0, pady=0)

        self.update_text()

    def update_text(self):
        if self.clock == 0:
            text = f"1. Encode the input to binary using UTF-8\n and append a single '1' to it.\n" if self.input_base == 'text' else "1. Append a single '1' to the input.\n"
            text += f"2. Prepend that binary to the message block.\n"
            text += f"3. Append the original message length\n ({self.message_block['LBinary']}, {self.message_block['L']} in decimal) at the end of the\n message block as a 64-bit big-endian integer.\n"
            text += f"4. Add {self.message_block['K']} zeros between the encoded message\n and the length integer so that the message\n block is a multiple of 512.\n"
            text += f"In this case {self.message_block['L']} + 1 + {self.message_block['K']} + 64 = {len(self.message_block['result'])}\n"
        elif self.clock == 1:
            text = f"1. Break the message block into 512-bit chunks.\n In our case {self.chunks_count} chunk{'' if self.chunks_count == 1 else 's'}.\n"
            text += f"2. Create a 64-entry message schedule array\n w[0..63] of 32-bit words.\n"
            text += f"3. Copy the {ordinal(self.master_clock // 113 + 1)} chunk into the 1st 16 words\n w[0..15] of the message schedule array.\n"
        elif 2 <= self.clock <= 49:
            text = f"1. Calculate:\n"
            text += f"w{self.clock + 14} = w{self.clock - 2} + σ0 + w{self.clock + 7} + σ1 \n"

            text += f"σ0 = (w{self.clock - 1} rightrotate 7) xor\n"
            text += f"(w{self.clock - 1} rightrotate 18) xor\n"
            text += f"(w{self.clock - 1} rightshift 3) \n"

            text += f"σ1 = (w{self.clock + 12} rightrotate 17) xor\n"
            text += f"(w{self.clock + 12} rightrotate 19) xor\n"
            text += f"(w{self.clock + 12} rightshift 10)\n"

        elif self.clock == 50:
            text = f"1. Initialize hash value h0 to h7: first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19.\n"
            text += f"2. Initialize array of K constants: first 32 bits of the fractional parts of the cube roots of the first 64 primes 2..311.\n"
            text += f"3. Initialize working variables to initial hash value: a = h0, b = h1, c = h2, d = h3, e = h4, f = h5, g = h6, h = h7.\n"
            text += f"4. Update working variables as:\n"
            text += f"h = g, g = f, f = e, e = d + Temp1, d = c, c = b, b = a, a = Temp1 + Temp2.\n"
            text += f"Temp1 = h + Σ1 + Choice + k{self.clock - 50} + w{self.clock - 50}\n"
            text += f"Temp2 = Σ0 + Majority\n"
        else:
            text = f"1. Update working variables as:\n"
            text += f"h = g, g = f, f = e, e = d + Temp1, d = c, c = b, b = a, a = Temp1 + Temp2.\n"
            text += f"Temp1 = h + Σ1 + Choice + k{self.clock - 50} + w{self.clock - 50}\n"
            text += f"Temp2 = Σ0 + Majority\n"

        self.label.config(text=text)

    def clear_scrolled_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def advance_step(self):
        if self.clock < self.last_clock:
            self.clock += 1
            self.update_text()

    def go_back_step(self):
        if self.clock > 0:
            self.clock -= 1
            self.update_text()

    def run_steps(self):
        for _ in range(self.last_clock - self.clock):
            self.advance_step()

def ordinal(n):
    return f"{n}{'th' if 11<=n%100<=13 else {1:'st', 2:'nd', 3:'rd'}.get(n%10, 'th')}"
