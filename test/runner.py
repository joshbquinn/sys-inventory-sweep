# test/runner.py
import unittest

# import your test modules
import test_dict_factory
import test_directory_management
import test_file_management
import test_linux_system
import test_windows_system
import test_time_stamper

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_dict_factory))
suite.addTests(loader.loadTestsFromModule(test_directory_management))
suite.addTests(loader.loadTestsFromModule(test_file_management))
suite.addTests(loader.loadTestsFromModule(test_linux_system))
suite.addTests(loader.loadTestsFromModule(test_windows_system))
suite.addTests(loader.loadTestsFromModule(test_time_stamper))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
