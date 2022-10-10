# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

from __future__ import absolute_import

from importlib.metadata import version, PackageNotFoundError

import cryptonite.decrypt
import cryptonite.encrypt
import cryptonite.utils

try:
    __version__ = version("cryptonite")
except PackageNotFoundError:
    # package is not installed
    pass
