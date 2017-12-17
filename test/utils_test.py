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


if __name__ == '__main__':
    unittest.main()
