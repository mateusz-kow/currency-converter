import task.utils.setup_logging
import unittest
import tests.test_currency_converter
import tests.test_database_updater

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(tests.test_currency_converter))
suite.addTest(loader.loadTestsFromModule(tests.test_database_updater))

unittest.TextTestRunner().run(suite)
