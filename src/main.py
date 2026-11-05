import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *
import hashlib
from classes.utils import Utils
from classes.message_schedule import MessageSchedule
from classes.explainer import Explainer
from classes.sigma import Sigma
from classes.wordresult import WordResult
from pathlib import Path

# Define the K constants used in SHA-256
k = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

PATH = Path(__file__).parent / 'assets/sha_icons'

class SHA256Visualizer:
    def __init__(self, root):
        self.root = root

        self.icon_play = ttk.PhotoImage(file=PATH / "icons8_play_24px.png")
        self.icon_cancel = ttk.PhotoImage(file=PATH / "icons8_cancel_24px.png")
        self.icon_single_right = ttk.PhotoImage(file=PATH / "icons8_single_right_24px.png")
        self.icon_single_left = ttk.PhotoImage(file=PATH / "icons8_single_left_24px.png")

        self.input = ""
        self.clock = 0
        self.chunks_count = 1

        self.create_layout()
        
    def create_layout(self):

        # Create a frame for the main layout
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=BOTH, expand=True)

        # Input Text Frame
        input_text_frame = ttk.Frame(main_frame, padding="5")
        input_text_frame.grid(row=0, column=0, columnspan=4, sticky="ew")
        input_text_label = ttk.Label(input_text_frame, text="Input Text")
        input_text_label.pack(side=LEFT)

        self.input_text_entry = ttk.Entry(input_text_frame, width=140)
        self.input_text_entry.pack(side=LEFT, fill=X, expand=True)
        self.input_text_entry.bind("<KeyRelease>", self.onInputChange)

        # Control Buttons
        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.grid(row=0, column=3, sticky="ew")

        ttk.Button(
            master = control_frame,
            # image=self.icon_single_right,
            text="NEXT",
            width=5,
            command=self.on_clock
            ).pack(side=RIGHT, padx=2)

        self.clock_print = ttk.Label(control_frame, text=f"Step: {self.clock}")
        self.clock_print.pack(side=RIGHT)

        ttk.Button(
            master = control_frame,
            # image=self.icon_single_left,
            text="BACK",
            width=5,
            command=self.on_clock_back
            ).pack(side=RIGHT, padx=2)

        # Message block Frame
        self.message_block_frame = ttk.Labelframe(main_frame, text="Message block", padding="5")
        self.message_block_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.message_block_text = ttk.Text(self.message_block_frame, height=20, width=10)
        self.message_block_text.pack(fill=BOTH, expand=True)

        # Explainer Frame
        self.explainer_frame = ttk.Labelframe(main_frame, text="Explainer", padding="5",height=10)
        self.explainer_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.explainer_sf = ScrolledFrame(self.explainer_frame, autohide=True,width=15)
        self.explainer_sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Message Schedule Frame
        self.message_schedule_frame = ttk.Labelframe(main_frame, text="Message Schedule", padding="0")
        self.message_schedule_frame.grid(row=1, column=1,rowspan=2, padx=0, pady=0, sticky="nsew")
        self.sf = ScrolledFrame(self.message_schedule_frame, autohide=True,width=10)
        self.sf.pack(fill=BOTH, expand=YES, padx=0, pady=0)

        # Message Schedule Calculation Frame
        self.message_schedule_calc_frame = ttk.Labelframe(main_frame, text="Message Schedule Calculation", padding="5")
        self.message_schedule_calc_frame.grid(row=1, column=2, columnspan=2,padx=5, pady=5, sticky="nsew")

        self.message_schedule_calc_frame_sf = ScrolledFrame(self.message_schedule_calc_frame, autohide=True,width=10)
        self.message_schedule_calc_frame_sf.pack(fill=BOTH, expand=YES, padx=0, pady=0)


        # K Constants Frame
        # self.k_constants_frame = ttk.Labelframe(main_frame, text="K Constants", padding="5")
        # self.k_constants_frame.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")
        # self.k_constants_text = ttk.Text(self.k_constants_frame, height=20, width=30)
        # self.k_constants_text.pack(fill=BOTH, expand=True)
        # self.k_constants_text.insert(END, "\n".join(f"{k:08x}" for k in K))

        # self.explainer_text = ttk.Text(self.explainer_frame, height=15, width=30)
        # self.explainer_text.pack(fill=BOTH, expand=True)
        # self.explainer_text.insert(END, self.get_explainer_text())

        # Compression Calculation Frame
        self.compression_calc_frame = ttk.Labelframe(main_frame, text="Compression Calculation", padding="5")
        self.compression_calc_frame.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.compression_calc_text = ttk.Text(self.compression_calc_frame, height=15, width=30)
        self.compression_calc_text.pack(fill=BOTH, expand=True)

        # SHA256 Hash Label
        hash_label_frame = ttk.Frame(main_frame, padding="5")
        hash_label_frame.grid(row=3, column=0, columnspan=4, sticky="ew")
        sha256_label = ttk.Label(hash_label_frame, text="Sha256: ", bootstyle="secondary")
        sha256_label.pack(side=LEFT)
        self.sha256_hash = ttk.Label(hash_label_frame, text="", bootstyle="light")
        self.sha256_hash.pack(side=LEFT)
    
    def on_clock(self):


        first_loop = self.firstLoop(self.clock)
        second_loop = self.secondLoop(self.clock)
        chunks_loop = self.chunksLoop(self.clock)

        result = self.shaStepped(self.input, first_loop, second_loop, chunks_loop)

        if self.clock < self.last_clock():
            self.clock += 1

        data = result['w']

        labels = "w"

        schedule = MessageSchedule(self.sf, data=data, base=2, labels='w', current_chunk=chunks_loop)
        schedule.update_display(clock=self.clock)

        explainer = Explainer(self.explainer_sf, clock=self.clock)

        if self.clock < 50 and self.clock >= 0:
            sigma_clock = self.clock+15

            self.clear_scrolled_frame()
            sigma1 = Sigma(self.message_schedule_calc_frame_sf, data, base='bin', clock=sigma_clock , rotations=(7, 18),shift=3,clock_shift = 16,row = 0)
            sigma2 = Sigma(self.message_schedule_calc_frame_sf, data, base='bin', clock=sigma_clock , rotations=(17, 19),shift=10,clock_shift = 3,row = 1)

            first_loop = self.firstLoop(self.clock)
            WordResult(self.message_schedule_calc_frame_sf, data, first_loop)

        
        self.clock_print.config(text=f"Step: {self.clock}")

        # Update the GUI or variables with the results

        # w_view = result['w']
        # final_hash = result['hash']
        # hs = result['hs']
        # hs_before = result['hsBefore']
        # letters = result['letters']
        # letters_before = result['lettersBefore']

    def on_clock_back(self):

        if self.clock == 0:
            return


        if self.clock <= self.last_clock():
            self.clock -= 1

        value = self.input
        if self.clock == 1:
            value = ''

        first_loop = self.firstLoop(self.clock - 2)
        second_loop = self.secondLoop(self.clock - 2)
        chunks_loop = self.chunksLoop(self.clock)

        result = self.shaStepped(value, first_loop, second_loop, chunks_loop)

        data = result['w']

        labels = "w"

        schedule = MessageSchedule(self.sf, data=data, base=2, labels='w', current_chunk=chunks_loop)
        schedule.update_display(clock=self.clock)

        explainer = Explainer(self.explainer_sf, clock=self.clock)

        if self.clock < 50 and self.clock >= 0:
            sigma_clock = self.clock+15

            self.clear_scrolled_frame()
            sigma1 = Sigma(self.message_schedule_calc_frame_sf, data, base='bin', clock=sigma_clock , rotations=(7, 18),shift=3,clock_shift = 16,row = 0)
            sigma2 = Sigma(self.message_schedule_calc_frame_sf, data, base='bin', clock=sigma_clock , rotations=(17, 19),shift=10,clock_shift = 3,row = 1)

            first_loop = self.firstLoop(self.clock)
            WordResult(self.message_schedule_calc_frame_sf, data, first_loop)

        
        self.clock_print.config(text=f"Step: {self.clock}")
        # Update the GUI or variables with the results

        # w_view = result['w']
        # final_hash = result['hash']
        # hs = result['hs']
        # hs_before = result['hsBefore']
        # letters = result['letters']
        # letters_before = result['lettersBefore']

    def onInputChange(self, event=None):

        value = self.input_text_entry.get()
        
        if not value:
            return
        
        self.input = value

        self.paddedInput = Utils.padding(value)

        if self.clock == 0:
            value = ''

        self.message_block_text.delete(1.0, END)
        self.message_block_text.insert(END, self.paddedInput)

        tick = self.clock

        first_loop = self.firstLoop(0)
        second_loop = self.secondLoop(self.clock)
        chunks_loop = self.chunksLoop(self.clock)

        result = self.shaStepped(value, first_loop, second_loop, chunks_loop)

        data = result['w']
        labels = "w"

        schedule = MessageSchedule(self.sf, data=data, base=2, labels='w', current_chunk=chunks_loop)
        schedule.update_display(clock=tick)

        explainer = Explainer(self.explainer_sf, clock=self.clock)


    def shaStepped(self,message, first_loop, second_loop, chunks_loop):
        h0 = 0x6a09e667
        h1 = 0xbb67ae85
        h2 = 0x3c6ef372
        h3 = 0xa54ff53a
        h4 = 0x510e527f
        h5 = 0x9b05688c
        h6 = 0x1f83d9ab
        h7 = 0x5be0cd19

        s0, s1, S1, S0, a, b, c, d, e, f, g, h, ch, temp1, temp2, maj = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        w = [0] * 64
        hs_before = []
        letters_before = []

        input = Utils.padding(message)
        chunks = self.chunkString(input) 
        
        for n in range(chunks_loop):
            chunk = chunks[n]

            w = [0] * 64

            for i, message_word in enumerate(self.chunkString(chunk, 32)):
                w[i] = int(message_word, 2)

            first_loop_for_current_chunk = 63 if n < chunks_loop - 1 else first_loop
            for i in range(16, first_loop_for_current_chunk + 1):
                s0 = Utils.rotate_right(w[i - 15], 7) ^ Utils.rotate_right(w[i - 15], 18) ^ (w[i - 15] >> 3)
                s1 = Utils.rotate_right(w[i - 2], 17) ^ Utils.rotate_right(w[i - 2], 19) ^ (w[i - 2] >> 10)
                w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF

            a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

            second_loop_for_current_chunk = 63 if n < chunks_loop - 1 else second_loop
            for i in range(second_loop_for_current_chunk + 1):
                S1 = Utils.rotate_right(e, 6) ^ Utils.rotate_right(e, 11) ^ Utils.rotate_right(e, 25)
                ch = (e & f) ^ (~e & g)
                temp1 = (h + S1 + ch + k[i] + w[i]) & 0xFFFFFFFF
                S0 = Utils.rotate_right(a, 2) ^ Utils.rotate_right(a, 13) ^ Utils.rotate_right(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xFFFFFFFF

                letters_before = [a, b, c, d, e, f, g, h]

                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFF

            hs_before = [h0, h1, h2, h3, h4, h5, h6, h7]

            h0 = (h0 + a) & 0xFFFFFFFF
            h1 = (h1 + b) & 0xFFFFFFFF
            h2 = (h2 + c) & 0xFFFFFFFF
            h3 = (h3 + d) & 0xFFFFFFFF
            h4 = (h4 + e) & 0xFFFFFFFF
            h5 = (h5 + f) & 0xFFFFFFFF
            h6 = (h6 + g) & 0xFFFFFFFF
            h7 = (h7 + h) & 0xFFFFFFFF

        hash_value = ''.join(f'{x:08x}' for x in [h0, h1, h2, h3, h4, h5, h6, h7])

        return {
            'w': w,
            's0': s0,
            's1': s1,
            'S1': S1,
            'ch': ch,
            'temp1': temp1,
            'S0': S0,
            'maj': maj,
            'temp2': temp2,
            'letters': [a, b, c, d, e, f, g, h],
            'hash': hash_value,
            'chunks': chunks,
            'hs': [h0, h1, h2, h3, h4, h5, h6, h7],
            'hsBefore': hs_before,
            'lettersBefore': letters_before
        }

    def clear_scrolled_frame(self):
        for widget in self.message_schedule_calc_frame_sf.winfo_children():
            widget.destroy()

    def last_clock(self):
        if self.chunks_count == 1:
            return 113

        return 113 + 114 * (self.chunks_count - 1)  

    
    def firstLoop(self,clock):
        step = clock % 114  # 115

        if step + 16 < 64:
            return 15 + step
        return 63

    def secondLoop(self,clock):
        step = clock % 114  # 115
        
        if 49 <= step < 113:
            return step - 49
        
        if step >= 113:
            return 63
        return 0

    def chunksLoop(self,clock):
        if clock < 114:
            return 1
        
        return (clock // 114) + 1  # 115
    
    def chunkString(self,input_str, chunk_size=512):
        """Chunk the input string into chunks of the specified size."""
        return [input_str[i:i + chunk_size] for i in range(0, len(input_str), chunk_size)]

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    root.title("SHA-256 Visualizer")
    app = SHA256Visualizer(root)
    root.mainloop()