#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Heading
*******
About this module...


Contents
********
    * :func:`filename2metadata()`: Extracts metadata from a filename.
    * :func:`metadata2fname()`: Generates filename from metadata.
"""

import logging
import os
from parse import *

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(name)s: %(message)s')


def fname2metadata(filename, pattern='{author}_{title}'):
    """Extracts metadata from a filename.
    
    With this function you can create a dictionary containing metadata.
    Only the filename's basepath without any extensions will be considered.
    Furthermore, you have to specifiy the pattern of the filename.
    
    Args:
        filename (str): The name of a text file, with or without path as prefix
            and extension as suffix, respectively.
        pattern (str), optional: The filename's pattern. Write describing tokens
            within braces, those will be you dictionary's keys. Defaults to
            ``{author}_{title}``.
    
    Returns:
        A ``Result`` object (instanced by :module:`parse`), meaning an ordered
        dictionary with describers as keys and metadata as values.
        
    Example:
        >>> filename = 'corpus/Goethe_1816_Stella.txt'
        >>> pattern = '{author}_{year}_{title}'
        >>> fname2metadata(filename=filename,
        ...                pattern=pattern)
        <Result () {'author': 'Goethe', 'year': '1816', 'title': 'Stella'}>
    """
    log.debug("Extracting metadata from file '{0}' with pattern '{1}' ...".format(filename, pattern)) 
    basename, _ = os.path.splitext(os.path.basename(filename))
    return parse(pattern, basename)

def metadata2fname(dataset, pattern='{author}_{title}'):
    """Construct a filename from a metadata set and a pattern.
    
    Args:
        dataset (dict-like): A metadata set, referenced keys subscriptable.
        pattern (str), optional: a general pattern for the desired filename.
            Data keys between braces. Default to "{author}_{title}". 

    Returns:
        A string.
    """
    return pattern.format(**dataset)
