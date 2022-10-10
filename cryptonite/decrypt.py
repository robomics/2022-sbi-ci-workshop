# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

from cryptonite.encrypt import encrypt
from cryptonite.utils import is_ascii


def decrypt(text, offset: int) -> str:
    """
    Decrypt ASCII text by shifting each characted by the offset param.
    :param text: a string-like object containing encrypted text.
    :param offset: a non-zero integer. Multiples of 127 will raise an error.
    :return: plain text.
    """
    if not is_ascii(text):
        raise RuntimeError("text does not use ASCII encoding.")

    num_ascii_chars = 127
    offset = offset % num_ascii_chars
    if offset == 0:
        return text

    return encrypt(text, -offset)
