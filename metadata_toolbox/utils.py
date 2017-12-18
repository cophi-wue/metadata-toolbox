#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Heading
*******
About this module...


Contents
********
    * :func:`fname2metadata()`: Extracts metadata from a filename.
    * :func:`metadata2fname()`: Generates filename from metadata.
"""

import logging
import os
import re
from parse import *

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(name)s: %(message)s')


def fname2metadata(fname, pattern='{author}_{title}'):
    """Extract metadata from a filename.
    
    With this function you can create a dictionary containing metadata.
    Only the filename's basepath without any extensions will be considered.
    Furthermore, you have to specifiy the pattern of the filename.
    
    Args:
        fname (str): The name of a text file, with or without path as prefix
            and extension as suffix, respectively.
        pattern (str), optional: The filename's pattern. Write describing tokens
            within braces, those will be you dictionary's keys. Defaults to
            ``{author}_{title}``.
    
    Returns:
        A ``Result`` object (instanced by :module:`parse`), meaning an ordered
        dictionary with describers as keys and metadata as values.
    
    Todo:
        * Find an appropriate exception instance.
        
    Example:
        >>> fname = 'corpus/Goethe_1816_Stella.txt'
        >>> pattern = '{author}_{year}_{title}'
        >>> fname2metadata(fname=fname,
        ...                pattern=pattern)
        <Result () {'author': 'Goethe', 'year': '1816', 'title': 'Stella'}>
    """
    log.debug("Extracting metadata from filename '{0}' with pattern '{1}' ...".format(fname, pattern)) 
    basename, _ = os.path.splitext(os.path.basename(fname))
    metadata = parse(pattern, basename)
    if metadata is not None:
        return metadata
    else:
        raise Exception("The pattern '{0}' did not match the structure of '{1}'.".format(pattern, fname))


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

def rearrange_filename(file_path):
    """Changes filename format form {author}_{title} to {title}_{format}

    	   args: file_path: path to a textfile
    	   returns: newly formatet path to file (str)

    	   example:

    		goehte_novelle.txt -> novelle_goehte.txt
    	"""
    path = re.sub("\/[^\/]+$", "", file_path)
    old_name = re.sub(".*\/|\..*", "", file_path)
    file_ending = re.sub(".*\.", "", file_path)
    nameparts = old_name.split("_")
    new_filepath = path + "/" + str(nameparts[1]) + "_" + str(nameparts[0]) + "." + file_ending
    return new_filepath

