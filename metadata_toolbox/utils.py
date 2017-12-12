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
import os
from parse import *

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(name)s: %(message)s')


def filename2metadata(filename, pattern='{author}_{title}'):
    basename, _ = os.path.splitext(os.path.basename(filename))
    return parse(pattern, basename)
