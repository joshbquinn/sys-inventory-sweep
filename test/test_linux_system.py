#!/usr/bin/env python

import linux_system as linux
import dict_factory as dict_f
import unittest
import sys

@unittest.skipUnless(sys.platform.startswith("lin"), "requires Linux")

class LinuxSystemTests(unittest.TestCase):

    def setUp(self):
        """Fixtures to create variables required for the tests"""
        self.test_bash_command = 'lscpu'
        self.test_category = 'CPU '

    def tearDown(self):
        """Fixtures to remove any created variables"""
        self.test_bash_command = None

    def test_bash_runs(self):
        """Smoke test: Check that subprocess command runs"""
        linux.bash(self.test_bash_command)

    def test_bash_returns_string(self):
        self.test_string = linux.bash(self.test_bash_command)
        self.assertIsInstance(self.test_string, str)

    def test_bash_returns_correct_data(self):
        self.test_string = linux.bash(self.test_bash_command)
        self.clean_data = dict_f.clean_string(self.test_string)
        self.data = dict_f.two_column_dict(self.test_category, self.clean_data)
        print(self.data)
        self.assertRegex(self.test_string, 'cpu')

    def test_netdev_runs(self):
        linux.netdev()


if __name__ == '__main__':
    unittest.main()
