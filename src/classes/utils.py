import binascii
from typing import List

class Utils:
    @staticmethod
    def string_to_binary(string: str) -> str:
        byte_array = string.encode('utf-8')
        return ''.join(f'{byte:08b}' for byte in byte_array)

    @staticmethod
    def hex_to_binary(hex_str: str) -> str:
        decimal_values = [int(hex_str[i:i + 2], 16) for i in range(0, len(hex_str), 2)]
        return ''.join(f'{value:08b}' for value in decimal_values)

    @staticmethod
    def hex_to_string(hex_str: str) -> str:
        bytes_object = bytes.fromhex(hex_str)
        return bytes_object.decode('utf-8')

    @staticmethod
    def string_to_hex(string: str) -> str:
        return binascii.hexlify(string.encode('utf-8')).decode('utf-8')

    @staticmethod
    def binary_to_hex(binary: str) -> str:
        return f'{int(binary, 2):x}'

    @staticmethod
    def binary_to_string(binary: str) -> str:
        decimal_values = [int(binary[i:i + 8], 2) for i in range(0, len(binary), 8)]
        bytes_object = bytes(decimal_values)
        return bytes_object.decode('utf-8')

    @staticmethod
    def decimal_to_binary(decimal: int) -> str:
        return f'{decimal:b}'

    @staticmethod
    def binary_to_decimal(binary: str) -> int:
        return int(binary, 2)

    @staticmethod
    def append_one_bit(input_str: str) -> str:
        return input_str + '1'

    @staticmethod
    def is_multiple_of_512(input_num: int) -> bool:
        return input_num % 512 == 0

    @staticmethod
    def calculate_k(L: int) -> int:
        K = 0
        while not Utils.is_multiple_of_512(L + 1 + K + 64):
            K += 1
        return K

    @staticmethod
    def return_64_bit(number: str) -> str:
        return number.zfill(64)

    @staticmethod
    def padding(input_str: str, base: str = 'text') -> str:
        if base == 'text':
            input_str = Utils.string_to_binary(input_str)
        elif base == 'hex':
            input_str = Utils.hex_to_binary(input_str)
        L = len(input_str)
        K = Utils.calculate_k(L)
        L64 = Utils.return_64_bit(Utils.decimal_to_binary(L))
        return Utils.append_one_bit(input_str) + L64.zfill(K + 64)

    @staticmethod
    def padding_explained(input_str: str, base: str = 'text') -> dict:
        if base == 'text':
            input_str = Utils.string_to_binary(input_str)
        L = len(input_str)
        K = Utils.calculate_k(L)
        L64 = Utils.return_64_bit(Utils.decimal_to_binary(L))
        result = Utils.append_one_bit(input_str) + L64.zfill(K + 64)
        return {
            'input': input_str,
            'L': L,
            'LBinary': Utils.decimal_to_binary(L),
            'K': K,
            'L64': L64,
            'result': result,
            'inputAppended': Utils.append_one_bit(input_str)
        }

    @staticmethod
    def chunk_string(s: str, length: int = 512) -> List[str]:
        return [s[i:i + length] for i in range(0, len(s), length)]

    @staticmethod
    def rotate_right(value: int, r: int) -> int:
        bit_width = 32
        rotation = r & (bit_width - 1)
        bit_mask = (2 ** bit_width) - 1
        return ((value >> rotation) | ((value << (bit_width - rotation)) & bit_mask))

    @staticmethod
    def ordinal(i: int) -> str:
        j = i % 10
        k = i % 100
        if j == 1 and k != 11:
            return f'{i}st'
        if j == 2 and k != 12:
            return f'{i}nd'
        if j == 3 and k != 13:
            return f'{i}rd'
        return f'{i}th'
