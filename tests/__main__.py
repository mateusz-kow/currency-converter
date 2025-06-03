import unittest
import tests.test_sql_database_connector
import tests.test_json_database_connector

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests((loader.loadTestsFromModule(tests.test_json_database_connector),
               loader.loadTestsFromModule(tests.test_sql_database_connector)))


unittest.TextTestRunner().run(suite)
