"""Tests for the pure helper functions (no GUI needed)."""
import hashlib

import pytest

from classes.utils import Utils

# SHA-256 round constants: first 32 bits of the fractional parts of the cube roots of the first 64 primes.
def _round_constants():
    from decimal import Decimal, getcontext

    getcontext().prec = 80
    primes, n = [], 2
    while len(primes) < 64:
        if all(n % p for p in primes):
            primes.append(n)
        n += 1
    return [int((Decimal(p) ** (Decimal(1) / Decimal(3)) % 1) * 2**32) for p in primes]


K = _round_constants()
H0 = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]
MASK = 0xFFFFFFFF


def reference_sha256(text: str) -> str:
    """A compact SHA-256 built on the visualizer's own helpers (padding, chunking, rotation)."""
    padded = Utils.padding(text)
    h = H0[:]
    for chunk in Utils.chunk_string(padded, 512):
        w = [int(chunk[i : i + 32], 2) for i in range(0, 512, 32)]
        for i in range(16, 64):
            s0 = Utils.rotate_right(w[i - 15], 7) ^ Utils.rotate_right(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = Utils.rotate_right(w[i - 2], 17) ^ Utils.rotate_right(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w.append((w[i - 16] + s0 + w[i - 7] + s1) & MASK)
        a, b, c, d, e, f, g, hh = h
        for i in range(64):
            big_s1 = Utils.rotate_right(e, 6) ^ Utils.rotate_right(e, 11) ^ Utils.rotate_right(e, 25)
            ch = (e & f) ^ (~e & MASK & g)
            t1 = (hh + big_s1 + ch + K[i] + w[i]) & MASK
            big_s0 = Utils.rotate_right(a, 2) ^ Utils.rotate_right(a, 13) ^ Utils.rotate_right(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            t2 = (big_s0 + maj) & MASK
            hh, g, f, e, d, c, b, a = g, f, e, (d + t1) & MASK, c, b, a, (t1 + t2) & MASK
        h = [(x + y) & MASK for x, y in zip(h, [a, b, c, d, e, f, g, hh])]
    return "".join(f"{x:08x}" for x in h)


@pytest.mark.parametrize("text", ["", "abc", "hello world", "a" * 55, "a" * 56, "a" * 64, "The quick brown fox " * 20, "héllo wörld"])
def test_helpers_reproduce_real_sha256(text):
    assert reference_sha256(text) == hashlib.sha256(text.encode()).hexdigest()


def test_padding_of_abc_matches_fips_180_4_example():
    padded = Utils.padding("abc")
    assert len(padded) == 512
    assert padded[:24] == "011000010110001001100011"  # "abc"
    assert padded[24] == "1"  # the appended 1 bit
    assert int(padded[-64:], 2) == 24  # message length in bits


@pytest.mark.parametrize("length", [0, 1, 55, 56, 63, 64, 119, 120])
def test_padding_is_always_a_multiple_of_512_bits(length):
    assert len(Utils.padding("x" * length)) % 512 == 0


def test_hex_input_is_padded_like_the_same_text():
    assert Utils.padding("616263", base="hex") == Utils.padding("abc")


def test_conversions_round_trip():
    assert Utils.binary_to_string(Utils.string_to_binary("Zoë")) == "Zoë"
    assert Utils.hex_to_string(Utils.string_to_hex("hi")) == "hi"
    assert Utils.binary_to_decimal(Utils.decimal_to_binary(1234)) == 1234
    assert Utils.hex_to_binary("0f") == "00001111"


def test_rotate_right_is_a_32_bit_rotation():
    assert Utils.rotate_right(0b1, 1) == 0x80000000
    assert Utils.rotate_right(0x12345678, 32) == 0x12345678
    assert Utils.rotate_right(0x12345678, 8) == 0x78123456


def test_calculate_k_and_chunking():
    assert Utils.calculate_k(24) == 423  # 24 + 1 + 423 + 64 = 512
    assert Utils.chunk_string("a" * 1100, 512) == ["a" * 512, "a" * 512, "a" * 76]


def test_ordinal_suffixes():
    assert [Utils.ordinal(n) for n in (1, 2, 3, 4, 11, 12, 13, 21, 22, 23)] == [
        "1st", "2nd", "3rd", "4th", "11th", "12th", "13th", "21st", "22nd", "23rd",
    ]
