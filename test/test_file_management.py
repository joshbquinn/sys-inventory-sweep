#!/usr/bin/env python

import unittest
import file_management as fm
import os
import json


class FileManagementTests(unittest.TestCase):

    def setUp(self):
        """Fixture to create json file from string and dictionary object to test write to file methods."""
        self.test_file_name = 'testFile.json'
        self.test_dict = {}
        self.test_dict = {"header":
                              {"SubHeader":
                                   {"Key1": "value1", "Key2": "value2", "Key3": "value3", "Key4": "value4"}}}

    def tearDown(self):
        """Fixtures to remove string and dictionary objects. """
        self.test_dict = None
        try:
            os.remove(self.test_file_name)
        except:
            pass

    def test_write_json_file(self):
        """Smoke test: test the file runs."""
        fm.write_json_file(self.test_file_name, self.test_dict)

    def test_write_json_file_creates_json_file(self):
        """Check the file is created and exists """
        fm.write_json_file(self.test_file_name, self.test_dict)
        assert os.path.exists(self.test_file_name)

    def test_file_created_is_json(self):
        """Check whether the file created is json"""
        fm.write_json_file(self.test_file_name, self.test_dict)
        with open(self.test_file_name, mode="r") as f:
            json_dict = json.load(f)
            self.assertIsInstance(json_dict, dict)
        f.close()


if __name__ == '__main__':
    unittest.main()
