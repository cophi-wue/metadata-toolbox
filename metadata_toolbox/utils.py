#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Heading
*******
About this module...


Contents
********
    * :func:`example_function()`: About this function...
"""

import logging
from parse import *

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(name)s: %(message)s')
