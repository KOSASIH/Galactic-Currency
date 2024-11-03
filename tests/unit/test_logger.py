# tests/unit/test_logger.py

import unittest
import os
from utils.logger import Logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger(log_file='test.log')

    def test_logging_info(self):
        self.logger.info("This is an info message.")
        self.assertTrue(os.path.exists('test.log'))

    def test_logging_error(self):
        self.logger.error("This is an error message.")
        with open('test.log', 'r') as f:
            logs = f.read()
            self.assertIn("This is an error message.", logs)

    def tearDown(self):
        if os.path.exists('test.log'):
            os.remove('test.log')

if __name__ == '__main__':
    unittest.main()
