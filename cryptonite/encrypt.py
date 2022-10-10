# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT
from cryptonite.utils import is_ascii


def __encrypt_char(c: str, offset: int, num_ascii_chars: int = 127):
    return chr(abs((ord(c) + offset) % num_ascii_chars))


def encrypt(text, offset: int) -> str:
    """
    Encrypt ASCII text by shifting each characted by the offset param.
    :param text: a string-like object with the message to be encrypted. Should not contain non-ASCII characters.
    :param offset: a non-zero integer. Multiples of 127 will raise an error.
    :return: encrypted text
    """
    if not is_ascii(text):
        raise RuntimeError("text does not use ASCII encoding.")

    if offset == 0:
        raise RuntimeError("invalid offset: offset must be a non-zero integral number")

    num_ascii_chars = 127
    offset = offset % num_ascii_chars
    if offset == 0:
        raise RuntimeError(f"invalid offset: offset is a multiple of {num_ascii_chars}."
                           " Encrypted text would be identical to plain text!")

    return "".join(map(str, [__encrypt_char(c, offset) for c in text]))
