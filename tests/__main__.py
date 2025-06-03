import unittest
import tests.test_database_connectors
import tests.test_source_connectors

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests((loader.loadTestsFromModule(tests.test_database_connectors),
                loader.loadTestsFromModule(tests.test_source_connectors)))


unittest.TextTestRunner().run(suite)
