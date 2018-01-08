#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append('..')
from metadata_toolbox import utils

FNAME = 'refcor/English/dickens_expectations.txt'
DATASET = {'author': 'dickens',
           'title': 'expectations',
           'foo': 'A',
           'bar': 'B'}

class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_fname2metadata(self):
        metadata = utils.fname2metadata(FNAME, '{author}_{title}')
        self.assertTrue(metadata.__getitem__('author') == 'dickens' and
                        metadata.__getitem__('title') == 'expectations')

        # ValueError when pattern does not match fname
        with self.assertRaises(ValueError):
            metadata = utils.fname2metadata(FNAME, '{author}/{title}')

    def test_metadata2fname(self):
        # defaults to {author}_{title}
        fname = utils.metadata2fname(DATASET)
        self.assertTrue(fname == 'dickens_expectations')

        # draws keys from supplied dict according to pattern
        fname = utils.metadata2fname(DATASET, '{foo}_{bar}')
        self.assertTrue(fname == 'A_B')

        # KeyError when pattern key not in metadata dict
        with self.assertRaises(KeyError):
            fname = utils.metadata2fname(DATASET, '{foo}_{baz}')

    def test_rearrange_filename(self):
        
        new_filename = utils.rearrange_filename(FNAME)
        self.assertTrue(new_filename == "refcor/English/expectations_dickens.txt")

if __name__ == '__main__':
    unittest.main()
