# SHA-256 Visualizer

A desktop app that shows **how SHA-256 works, step by step**. Type a message and watch the padding,
the 64-word message schedule and the 64 compression rounds unfold one step at a time, with the
intermediate values shown in binary or hex.

![CI](https://github.com/rightturn/sha256-visualizer/actions/workflows/ci.yml/badge.svg)

Built with Python and [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) (themed Tkinter).

## What you can see
- **Message block:** the input converted to bits and padded to a multiple of 512 bits
  (the appended `1`, the zero padding and the 64-bit length)
- **Message schedule:** the 16 input words expanded to 64 words using the σ0 / σ1 functions
- **Compression:** the working variables `a` to `h` updated each round using the round constants `K`
- **Explainer:** a plain-language description of what the current step does
- **NEXT / BACK** buttons to move through the algorithm, so you can go forward and back at your own pace

## Run it
Requires Python 3.9+ with Tkinter (included with most Python installers; on Debian/Ubuntu
`sudo apt install python3-tk`).

```bash
pip install -r requirements.txt
python src/main.py
```
`ttkbootstrap` is pinned below 2.0 because version 2 reorganised the modules this app imports.

## Tests
```bash
pip install -r requirements-dev.txt
python -m pytest -q
```
The tests need no display. They check the helper functions (padding, chunking, rotation, conversions)
and, as a correctness check, build a complete SHA-256 **from those helpers** and compare it with
Python's `hashlib` for 8 inputs, including the awkward padding lengths 55, 56 and 64 bytes
and non-ASCII text. The 64 round constants were also verified against their definition
(fractional parts of the cube roots of the first 64 primes).

The GUI itself is checked only by a headless start-up and NEXT/BACK smoke test run during
development; it has no automated GUI tests.

## Project layout
```
src/main.py              the application window and the step logic
src/classes/utils.py     padding, chunking, bit rotation and conversions (pure functions)
src/classes/*.py         widgets for the message schedule, σ functions, word results and explainer
src/assets/sha_icons/    button icons (see Credits)
tests/                   unit tests
```

## Credits
Button icons are from [Icons8](https://icons8.com). Please follow Icons8's licence and attribution
terms if you reuse them.

## License
MIT
