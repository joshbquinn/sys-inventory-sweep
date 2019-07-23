#!/usr/bin/env python

import windows_system as ws
import dict_factory as dict_f
import unittest
import sys

@unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")

class WindowsSystemSweepTests(unittest.TestCase):

    def setUp(self):
        """Fixtures to create variables required for the tests"""
        self.test_windows_cmdlet = 'powershell.exe '
        self.test_windows_cmdlet2 = 'systeminfo'
        self.test_category = 'SysInfo'

    def tearDown(self):
        """Fixtures to remove any created variables"""
        self.test_windows_cmdlet = None
        self.test_windows_cmdlet2 = None

    def test_wcli_runs(self):
        """Smoke test: Check that subprocess command runs"""
        ws.windows_cli(self.test_windows_cmdlet, self.test_windows_cmdlet2)

    def test_wcli_returns_string(self):
        self.test_string = ws.windows_cli(self.test_windows_cmdlet, self.test_windows_cmdlet2)
        self.assertIsInstance(self.test_string, str)

    def test_wcli_returns_correct_data(self):
        self.test_string = ws.windows_cli(self.test_windows_cmdlet, self.test_windows_cmdlet2)
        self.clean_data = dict_f.clean_string(self.test_string)
        self.data = dict_f.two_column_dict(self.test_category, self.clean_data)
        print(self.data)
        self.assertRegex(self.test_string, 'Host Name')

    # def test_serialize_json(list_object):
    #     return json.loads(list_object)
    #
    # def test_deserialize_json(dictionary_object):
    #     return json.dumps(dictionary_object, indent=4)


if __name__ == '__main__':
    unittest.main()
