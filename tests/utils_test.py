#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import glob
import csv
import shutil
import json
import pytest
from unittest.mock import patch, Mock, mock_open
sys.path.append('..')
from metadata_toolbox import utils

FNAME = 'refcor/English/dickens_expectations.txt'
DATASET = {'author': 'dickens',
           'title': 'expectations',
           'foo': 'A',
           'bar': 'B',
           'filename':'refcor/English/dickens_expectations.txt'}

class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_fname2metadata(self):
        metadata = utils.fname2metadata(FNAME, '{author}_{title}')
        self.assertTrue(metadata['author'] == 'dickens' and
                        metadata['title'] == 'expectations')

        # ValueError when pattern does not match fname
        with self.assertRaises(ValueError):
            metadata = utils.fname2metadata(FNAME, '{author}/{title}')

    def test_metadata2fname_default(self):
        # defaults to {author}_{title}
        fname = utils.metadata2fname(DATASET)
        self.assertTrue(fname == 'dickens_expectations')

    def test_metadata2fname_dict(self):
        # draws keys from supplied dict according to pattern
        fname = utils.metadata2fname(DATASET, '{foo}_{bar}')
        self.assertTrue(fname == 'A_B')

    def test_metadata2fname_keyerror(self):
        # KeyError when pattern key not in metadata dict
        with self.assertRaises(KeyError):
            fname = utils.metadata2fname(DATASET, '{foo}_{baz}')

    def test_rearrange_filename(self):
        
        new_filename = utils.rearrange_filename(FNAME)
        self.assertTrue(new_filename == "refcor/English/expectations_dickens.txt")


    @patch('os.rename', return_value=None)
    def test_renameCorpusFiles(self,os_fn_rename):
        updated_metalist = utils.renameCorpusFiles([DATASET], ['foo', 'title', 'author'], "_-_")

        # how to test lists of dicts??
        self.assertDictEqual(updated_metalist[0], {'author': 'dickens',
           'title': 'expectations',
           'foo': 'A',
           'bar': 'B',
           'filename':'refcor/English/A_-_expectations_-_dickens.txt'})

class IOTestCase(unittest.TestCase):
    def setUp(self):
        os.mkdir('tmp')
        os.chdir('tmp')

    def tearDown(self):
        os.chdir('..')
        shutil.rmtree('tmp')

    def test_basic_rename(self):
        # rename from and to a plain file name
        open('a', 'w').close()

        utils.path_smart_rename('a', 'b')

        self.assertTrue(os.path.isfile('b'))

    def test_rename_to_path(self):
        # rename from plain file name to file name in new subfolder
        open('a', 'w').close()

        utils.path_smart_rename('a', 'foo/b')

        self.assertTrue(os.path.isfile('foo/b'))

    def test_rename_with_empty_path(self):
        # causing a subfolder to be empty by renaming
        os.mkdir('foo')
        open('foo/a', 'w').close()

        utils.path_smart_rename('foo/a', 'b')

        self.assertTrue(os.path.isfile('b'))
        self.assertFalse(os.path.isdir('foo'))

    def test_rename_with_nonempty_path(self):
        # not removing a non-empty subfolder after renaming (and no OSError from os.removedirs())
        os.mkdir('foo')
        open('foo/a', 'w').close()
        open('foo/b', 'w').close()

        utils.path_smart_rename('foo/a', 'b')

        self.assertTrue(os.path.isfile('b'))
        self.assertTrue(os.path.isdir('foo'))


    def test_load_sidecar(self):
        # have fname, load sidecar
        fname = 'foo.xml'
        with open('foo.json', 'w') as f:
            json.dump(DATASET, f)

        self.assertTrue(utils.read_sidecar(fname) == {**DATASET, **{'_from': 'sidecar'}})

    def test_load_nonexisting_sidecar(self):
        # have fname, no sidecar -> raises IOError
        fname = 'foo.xml'
        with self.assertRaises(FileNotFoundError):
            metadata = utils.read_sidecar(fname)

    def test_save_sidecar(self):
        # have metadata, write sidecar
        metadata = {**DATASET, **{'_from': 'sidecar', 'filename': 'foo.xml'}}
        utils.write_sidecar(metadata)

        self.assertTrue(os.path.isfile('foo.json'))
        with open('foo.json') as f:
            jsonfile = json.load(f)
        self.assertTrue(jsonfile == {**DATASET, **{'filename': 'foo.xml'}})

    @staticmethod
    def createTestCSV():
        # creates some CSV-data on which the functions can be tested
        with open('test.csv', 'w') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(['Titel', 'Autor', 'Erscheinungsjahr', 'ISBN'])
            csvwriter.writerow(['Titel1', 'Autor1', 'Jahr1', 'ISBN1'])
            csvwriter.writerow(['Titel2', 'Autor2', 'Jahr2', 'ISBN2'])
    
    def test_readMetadataFromCsv(self):
        IOTestCase.createTestCSV()
        assert utils.readMetadataFromCsv('test.csv') == [{'Titel':'Titel1', 'Autor':'Autor1', 'Erscheinungsjahr':'Jahr1', 'ISBN':'ISBN1'},{'Titel':'Titel2', 'Autor':'Autor2', 'Erscheinungsjahr':'Jahr2', 'ISBN':'ISBN2'}]


class UseCases(unittest.TestCase):
    def setUp(self):
        self.tokens = Mock(return_value=['This', 'is', 'a', 'document']) # generated by user, e.g. with `nltk.tokenize()`
    
    def test_reading_processing_writing(self):
        # Step 1: Creating a list of filepaths
        with patch('glob.glob', return_value=[FNAME]) as mock_glob:
            files = glob.glob('refcor/English') # basename of `FNAME`
            assert files == [FNAME]
    
        # Step 2: Reading text files and saving content in a list (or any other iterable)
        documents = []
        with patch('builtins.open', mock_open(read_data="This is a document.")) as mock_file:
            for file in files:
                with open(file, 'r') as f:
                    document = f.read()
                assert document == "This is a document."
                mock_file.assert_called_with(file, 'r')
                documents.append(document)

        # Step 3: Tokenizing documents
        tokenized_documents = []
        for document in documents:
            tokenized_documents.append(self.tokens.return_value)

        # Step 4: Getting metadata from filenames
        metadata = []
        for fname in files:
            metadata.append(utils.fname2metadata(fname, '{author}_{title}'))
        
        # Step 5: Modifying metadata and saving with corresponding document in a dictionary
        data = {}
        for metadata, document in zip(metadata, tokenized_documents):
            fname = utils.metadata2fname(metadata, '{title}') # old filename: {author}_{title}
            data[fname] = '\n'.join(document)
        
        # Step 6: Saving modified data
        for fname, document in data.items():
            with patch('builtins.open', mock_open(), create=True) as mock_file:
                with open(fname, 'w') as f:
                    f.write(document)
                mock_file.assert_called_with(fname, 'w')
                mock_file().write.assert_called_with('This\nis\na\ndocument') # new document structure (newlines and no punctuations)

if __name__ == '__main__':
    unittest.main()
