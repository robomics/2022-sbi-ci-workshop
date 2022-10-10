#!/usr/bin/env python

# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

from __future__ import absolute_import

import argparse
import os
import sys
from typing import Union

from setuptools_scm import get_version

from . import decrypt, encrypt


def read_key_from_env() -> Union[str, None]:
    return os.environ.get("CRYPTONITE_KEY")


def make_cli() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser()
    subparsers = cli.add_subparsers(help="subcmd", dest="command")
    encrypt_cmd = subparsers.add_parser("encrypt",
                                        help="Encrypt message received from stdin and output to stdout.")

    decrypt_cmd = subparsers.add_parser("decrypt",
                                        help="Decrypt message received from stdin and output to stdout.")

    [c.add_argument("--version", action="version", version=f"%(prog)s v{get_version()}") for c in [cli, decrypt_cmd, encrypt_cmd]]

    key_required = read_key_from_env() is None
    encrypt_cmd.add_argument("-k", "--key", type=int, help="Encryption key.", required=key_required)
    decrypt_cmd.add_argument("-k", "--key", type=int, help="Decryption key.", required=key_required)

    return cli


def parse_and_validate_args(cli) -> dict:
    args = vars(cli.parse_args())
    if args["command"] is None:
        cli.print_help()
        return None

    if args["key"] is None:
        key = read_key_from_env()
        if key is None:
            raise RuntimeError("Failed to read key from CRYPTONITE_KEY env variable")
        args["key"] = int(key)

    return args


def read_next_chunk(chunk_size=64 * 1024) -> str:
    assert int(chunk_size) > 0
    return sys.stdin.read(chunk_size)


def main() -> int:
    cli = make_cli()

    try:
        args = parse_and_validate_args(cli)
        if not args:
            return 1
    except RuntimeError as excp:
        print(f"CLI parsing failed with the following error: {excp}", file=sys.stderr)
        return 1

    key = args["key"]
    assert key

    if args["command"] == "encrypt":
        def fx(text):
            return encrypt.encrypt(text, key)
    else:
        assert args["command"] == "decrypt"

        def fx(text):
            return decrypt.decrypt(text, key)

    try:
        buff = read_next_chunk()
        while buff != "":
            print(fx(buff), end="")
            buff = read_next_chunk()

    except RuntimeError as excp:
        operation = args["command"].capitalize() + "ion"
        print(f"{operation} failed due to the following error: {excp}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.stdin.reconfigure(encoding="utf-8")
    main()
