# -*- coding: utf-8 -*-
"""
:authors: GitBib
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 GitBib
"""
from .pyasstosrt import Subtitle
from .time import Time
from .dialogue import Dialogue

VERSION = (1, 1, 2)
__version__ = ".".join(map(str, VERSION))

__author__ = 'GitBib'
__email__ = 'pyasstosrt@bnff.website'

__all__ = [
    "Subtitle", "Time", "Dialogue"
]
