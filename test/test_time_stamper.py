#!/usr/bin/env python

import unittest
from time_stamper import time_stamp


class TestTimeStamper(unittest.TestCase):
    """Class to test the methods within time_stamper module"""

    def test_time_stamp_test_runs(self):
        """Smoke test: test the file runs."""
        time_stamp()

    def test_time_stamp_returns_correct_time(self):
        """Assertion: test the correct time is produced"""
        time = time_stamp()[:-3]
        print(time)
        time2 = time_stamp()[:-3]
        print(time2)
        self.assertEqual(time, time2)


if __name__ == '__main__':
    unittest.main()
