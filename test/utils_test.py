#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append('..')
from metadata_toolbox import utils

FILENAME = 'refcor/English/dickens_expectations.txt'


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_filename2metadata(self):
        metadata = utils.filename2metadata(FILENAME, '{author}_{title}')
        self.assertTrue(metadata.__getitem__('author') == 'dickens' and
                        metadata.__getitem__('title') == 'expectations')


if __name__ == '__main__':
    unittest.main()
