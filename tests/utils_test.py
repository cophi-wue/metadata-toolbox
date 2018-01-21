#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import shutil
from unittest.mock import patch
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

if __name__ == '__main__':
    unittest.main()
