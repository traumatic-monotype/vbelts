# -*- coding: utf-8 -*-
"""Utilities for v-belt dimensioning.
Copyright (C) 2020 Glademir Karpinski Junior <gkarpinskijr@gmail.com>,
Hector Balke Nodari <hectornodari@gmail.com>

Redistribution and use in source and binary forms, with or without modification, are permitted provided
that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and
the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or
promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

vbelts provides functions that allow the computation of complex factors in v-belt dimensioning."""

import os

from vbelts import belt
from vbelts import length
from vbelts import util
from vbelts import power
from vbelts import speed
# from . import force
from vbelts import pulley

from .belt import *
from .length import *
from .util import *
from .power import *
from .speed import *
# from .force import *
from .pulley import *

__all__ = ['belt', 'length', 'util', 'power', 'speed', 'pulley']

try:
    vbelts_dir = os.path.dirname(__file__)
    vbelts_data_dir = os.path.join(vbelts_dir, 'data')
except:
    pass