# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

from cryptonite.decrypt import decrypt
from cryptonite.encrypt import encrypt


def test_encrypt():
    plain_text = "I am Superman. I stand for truth, for justice, and for the future."

    offset = 1
    expected = "J!bn!Tvqfsnbo/!J!tuboe!gps!usvui-!gps!kvtujdf-!boe!gps!uif!gvuvsf/"

    assert encrypt(plain_text, offset) == expected


def test_decrypt():
    encrypted_text = "Ajm\x1bompoc\x1b\\i_\x1bepnod^`\x1c"
    offset = -5

    expected = "For truth and justice!"

    assert decrypt(encrypted_text, offset) == expected
