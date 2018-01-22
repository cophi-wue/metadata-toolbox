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
    * :func:`rearrange_filename()`: Changes file_format {author}_{title} to {title}_{format}
    * :func:`readMetadataFromCsv()`: reads metadata from CSV-file.
    * :func:`path_smart_rename()`: renames files to filenames that can include folders.
"""

import logging
import os
import re
import csv
import warnings
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
        {'author': 'Goethe', 'year': '1816', 'title': 'Stella'}
    """
    log.debug("Extracting metadata from filename '{0}' with pattern '{1}' ...".format(fname, pattern)) 
    basename, _ = os.path.splitext(os.path.basename(fname))
    metadata = parse(pattern, basename)
    if metadata is not None:
        return metadata.named
    else:
        raise ValueError("The pattern '{0}' did not match the structure of '{1}'.".format(pattern, fname))


def metadata2fname(dataset, pattern='{author}_{title}'):
    """Construct a filename from a metadata set and a pattern.
    
    Args:
        dataset (dict-like): A metadata set, referenced keys subscriptable.
        pattern (str), optional: a general pattern for the desired filename.
            Data keys between braces. Default to "{author}_{title}". 

    Returns:
        A string.
    """
    return pattern.format_map(dataset)

def rearrange_filename(file_path):
    """Changes filename format form {author}_{title} to {title}_{format}

    	   args: file_path: path to a textfile
    	   returns: newly formatet path to file (str)

    	   example:

    		folder/goehte_novelle.txt -> folder/novelle_goehte.txt

        >>> file_path = 'folder/goehte_novelle.txt'
        >>> rearrange_filename(file_path=file_path)
        'folder/novelle_goehte.txt'
    	"""
    path = re.sub("\/[^\/]+$", "", file_path)
    old_name = re.sub(".*\/|\..*", "", file_path)
    file_ending = re.sub(".*\.", "", file_path)
    nameparts = old_name.split("_")
    new_filepath = path + "/" + str(nameparts[1]) + "_" + str(nameparts[0]) + "." + file_ending
    return new_filepath

def datamodel2csv(datamodel, fn):
    '''Writes Datamodel to csv file.
    
    With this function, you can write metadata information of a list of documents to a csv file, where:
    documents == list
    Metadata field == dict.key
    metadata information = dict[key]
    
    Args:
        datamodel[dict]: list of dicts; each dict contains metadata of one document
        fn(str): directory to save csv.
    
    Returns: -
    
    
    To Do:
        make list comprehension
        write tests
        test
        
    '''
    
    headerList = []
    for header in datamodel:
        for headeritem in header.keys():
            if not headeritem in headerList:
                headerList.append(headeritem)
    with open (fn,'w', encoding = 'utf-8',) as f:
        dictwriterObject = csv.DictWriter(f, entry.keys)
        dictwriterObject.writeheader()        
        for entry in datamodel:
            dictwriterObject.writerow(entry)
    
def readMetadataFromCsv(datalocation, datafieldnames = None, **kwargs):
    '''Reads CSV-file to datamodel.
    
    With this function, you can read metadata information from a csv file.
    
    Args:
        datalocation (str): a string defining where to finde the CSV-file
        datafieldnames (list or None): if None, the values of the first line of the file are used as fildnames; alternativly you can define a list of fildnames
        further args get handet over to func csv.DictReader
    
    Returns: a list of dicts; each dict representing the data of one document
    
    
    To Do:
        write tests
        test
        
    '''

    corpusdata = []
    with open(datalocation, newline = '') as csvfile:
        tablereader = csv.DictReader(csvfile, fieldnames = datafieldnames, **kwargs)
        for row in tablereader:
            corpusdata.append(row) 

    ##Auf mögliche Eingabefehler hinweisen
    if len(corpusdata) == 0:
        warnings.warn("CSV-File is empty.")
    elif len(corpusdata[0]) == 1:
        warnings.warn("CSV-File has only 1 column. Please check delimiter.")

    return corpusdata
    
def path_smart_rename(old_fname, new_fname):
    """Renames a file from old_fname to new_fname & deals with paths in names.
    
    Args:
        old_fname: A string describing the path to the file to be renamed.
        new_fname: A string describing the desired new filename and location.

    Returns:
        –

    To Do:
        * potentially clean up previously used empty folders after renaming?
    """
    old_dirs, _ = os.path.split(old_fname)
    new_dirs, _ = os.path.split(new_fname)
    if new_dirs:
        os.makedirs(new_dirs, exist_ok=True)
    os.rename(old_fname, new_fname)
    if old_dirs:
        try:
            os.removedirs(old_dirs)
            log.info('Recursively removed empty directories from {0}.'.format(old_dirs))
        except OSError:
            log.debug('Failed removing {0} recursively because it’s not empty.'.format(old_dirs))

def renameCorpusFiles(metalist, fields, seperator):
    """Takes metadata fields and creates new filenames for corpus files

    Args:
        metalist: List of dicts containing meatdatainforamtion and at least a field for filenames
        fields: List of fields to be used for new filenames
        seperator: String to separte different fields in new filenames

    Returns:
        updated list of dicts with containing new filenames

    To Do:
        * Warning for missing values in given fields?
        * Option to set placeholder for these missing values
    """
    updated_metalist = list()
    # iterate over meta_dicts
    for meta_dict in metalist:

        # get file extension
        try:
            file_extension = os.path.splitext(meta_dict["filename"])[1]
        except KeyError:
            log.debug('Missing field \'filename\' in metadata.'.format(meta_dict))

        # get path
        path = os.path.dirname(meta_dict["filename"])

        new_filename = ""
        #  iterate over field_pattern
        for field in fields:
            try:
                new_filename += str(meta_dict[field]) + str(seperator)
            except KeyError:
                log.debug('Field is not defined in metadata:'.format(field))
            
        # remove last seperator
        new_filename = re.sub(re.escape(seperator) + "$", "", new_filename)
        # join to path+extention
        new_filename = os.path.join(path, new_filename) + file_extension

        # rename file
        path_smart_rename(meta_dict["filename"], new_filename)

        # update meta_dict
        meta_dict["filename"] = new_filename
        updated_metalist.append(meta_dict)

    return updated_metalist
