#!/usr/bin/env python

import re
from itertools import zip_longest
import unittest
import dict_factory as dict_factory


class DictFactoryTests(unittest.TestCase):
    """Tests for the methods within the dict_factory module"""

    def setUp(self):
        """Fixture that creates a list and strings for dict_factory methods to use."""

        self.sample_string = 'A string of a string to test.'
        self.sample_list = ['a', 'list', 'of', 'strings', 'to', 'test']
        self.sample_category_name = 'Test Category'
        self.sample_dirty_string = 'Architecture:        x86_64\n' \
                                 'CPU op-mode(s):      32-bit, 64-bit\n' \
                                 'Byte Order:          Little Endian'
        self.sample_multiple_column_string = 'NAME    MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT\n'\
                                            'loop0     7:0    0  89.3M  1 loop /snap/core/6673\n'\
                                            'loop1     7:1    0 140.7M  1 loop /snap/gnome-3-26-1604/82\n'

    def tearDown(self):

        try:
            self.sample_list = None
            self.sample_string = None
            self.sample_category_name = None
            self.sample_dirty_string = None
            self.sample_multiple_column_string = None

        except:
            pass

    def test_two_column_dict_runs(self):
        """Basic smoke test: Does function run."""
        dict_factory.two_column_dict(self.sample_category_name, self.sample_list)

    def test_multiple_column_dict_runs(self):
        """Basic smoke test: Does function run."""
        dict_factory.multiple_column_dict(self.sample_category_name, self.sample_string)

    def test_clean_list_runs(self):
        """Basic smoke test: Does function run."""
        dict_factory.clean_string(self.sample_dirty_string)

    def test_multiple_column_dict_returns_dict(self):
        """Check that a dictionary is return from a string"""
        test = dict_factory.multiple_column_dict(self.sample_category_name, self.sample_multiple_column_string)
        print(test)
        self.assertIsInstance(test, dict)

    def test_two_column_dict_returns_dict(self):
        """Check that a dictionary object is returned"""
        test = dict_factory.two_column_dict(self.sample_category_name, self.sample_list)
        print(test)
        self.assertIsInstance(test, dict)

    def test_clean_string(self):
        """Check that ``clean_string()`` removes specified regex delimiters."""

        delimiters = "\n"
        test = dict_factory.clean_string(self.sample_dirty_string)

        self.assertRegex(self.sample_dirty_string, delimiters)

        self.assertNotRegex(str(test), delimiters)

        self.assertTrue(str(test) != self.sample_dirty_string)
        print(str(test),  self.sample_dirty_string )

    def test_make_a_dict_returns_a_dict(self):
        """Check that a dict is returned from the method"""
        test_dict = dict_factory.make_dict(self.sample_list, self.sample_category_name)
        self.assertIsInstance(test_dict, dict)
        print(test_dict)


if __name__ == '__main__':
    unittest.main()
