#!/usr/bin/env python

import os
from datetime import datetime
import unittest
import directory_management as d_mgmt


class DirectoryManagementTest(unittest.TestCase):
    """Unit tests for all methods within the directory_management module"""

    def setUp(self):
        """Fixtures that create a file path string to test directory_management methods with."""
        self.sample_dir_name = 'test_directory'

    def tearDown(self):
        """Fixture that deletes the files used by the test methods"""
        try:
            os.rmdir(self.sample_dir_name)
        except:
            pass

    def test_unique_directory(self):
        """Test a unique name string has been created and is not Null"""
        name = d_mgmt.unique_name(self.sample_dir_name)
        self.assertRegex(name, r'\d+', "String object should contain dateTime")
        self.assertIsNotNone(name, "Object is None. A unique dorectory name with a Datetime string should be returned.")
        print(name)

    def test_create_directory(self):
        """Test ``create_directory()`` method"""
        test_dir = self.sample_dir_name
        d_mgmt.create_directory(self.sample_dir_name)
        assert os.path.exists(test_dir)


if __name__ == '__main__':
    unittest.main()
