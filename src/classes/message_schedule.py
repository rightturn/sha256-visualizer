import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

class MessageSchedule:
    def __init__(self, main_frame, data, base=2, labels=None, current_chunk=1):
        self.data = data
        self.base = base
        self.labels = labels if labels is not None else []
        self.current_chunk = current_chunk
        self.first_loop_starts_at = 14
        self.second_loop_starts_at = 50
        self.clock = 0

        self.container = main_frame
        # self.container.pack(fill=tk.BOTH, expand=True)

        self.clear_scrolled_frame()
        
        # self.title = ttk.Label(self.container, text=f"Message schedule - {self.ordinal(self.current_chunk)} chunk", font='bold')
        # self.title.pack(pady=10)

        self.message_frames = []
        for key, word in enumerate(data):
            frame = ttk.Frame(self.container)
            frame.pack(fill=tk.X, pady=0)

            label_text = f"{self.labels}{key}" if isinstance(self.labels, str) else self.labels[key] if self.labels else f"W{key}"
            label = ttk.Label(frame, text=label_text, width=3, anchor=tk.W, font=("Helvetica", 11) )
            label.pack(side=tk.LEFT, padx=0)

            binary_word = self.convert_to_base(word)
            binary_label = ttk.Label(frame, text=binary_word, width=40, anchor=tk.W, font=("Helvetica", 12))
            binary_label.pack(side=tk.LEFT)

            arrow_label = ttk.Label(frame, text=" ", width=2)
            arrow_label.pack(side=tk.LEFT, padx=5)

            self.message_frames.append((frame, binary_label, arrow_label))

    def clear_scrolled_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def update_display(self, clock):
        self.clock = clock

        for key, (frame, binary_label, arrow_label) in enumerate(self.message_frames):
            color = self.get_focus_color(key, clock)
            direction = self.get_arrow_direction(key, clock)

            binary_label.config(foreground=color)
            arrow_label.config(text=direction)

            if clock == 0 and key > 15:
                binary_label.config(foreground='gray')
            else:
                binary_label.config(foreground=color)

    def convert_to_base(self, number):
        if self.base == 2:
            return format(number, '032b')
        elif self.base == 10:
            return str(number)
        elif self.base == 16:
            return format(number, '08x')
        else:
            raise ValueError("Unsupported base")

    def ordinal(self, n):
        return "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

    def get_focus_color(self, key, clock):
        if clock + self.first_loop_starts_at == key and clock < 50 and clock > 1:
            return "white"
        if clock - 15 + self.first_loop_starts_at == key and clock < 50 and clock > 1:
            return "red"
        if clock - 2 + self.first_loop_starts_at == key and clock < 50 and clock > 1:
            return "green"
        if clock - 16 + self.first_loop_starts_at == key and clock < 50 and clock > 1:
            return "blue"
        if clock - 7 + self.first_loop_starts_at == key and clock < 50 and clock > 1:
            return "yellow"
        if clock - self.second_loop_starts_at == key:
            return "yellow"

        return "gray"

    def get_arrow_direction(self, key, clock):
        if clock + self.first_loop_starts_at == key and clock < 50 and clock > 1:
            return "◄"
        if clock - 15 + self.first_loop_starts_at == key and clock < 50 and clock > 1:
            return "►"
        if clock - 2 + self.first_loop_starts_at == key and clock < 50 and clock > 1:
            return "►"
        if clock - 16 + self.first_loop_starts_at == key and clock < 50 and clock > 1:
            return "►"
        if clock - 7 + self.first_loop_starts_at == key and clock < 50 and clock > 1:
            return "►"
        if clock - self.second_loop_starts_at == key:
            return "►"

        return "  "

# Example usage:
# root = ttk.Window(themename="darkly")
# data = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
# labels = "w"

# schedule = MessageSchedule(root, data, base=2, labels=labels, current_chunk=1)
# schedule.update_display(clock=14)

# root.mainloop()
