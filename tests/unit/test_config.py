# tests/unit/test_config.py

import unittest
import json
import os
from utils.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config_file = 'test_config.json'
        with open(self.config_file, 'w') as f:
            json.dump({"DATABASE_URL": "sqlite:///test.db"}, f)
        self.config = Config(config_file=self.config_file)

    def test_get_config_value(self):
        db_url = self.config.get('DATABASE_URL')
        self.assertEqual(db_url, "sqlite:///test.db")

    def test_get_non_existent_key(self):
        non_existent = self.config.get('NON_EXISTENT_KEY', 'default_value')
        self.assertEqual(non_existent, 'default_value')

    def tearDown(self):
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

if __name__ == '__main__':
    unittest.main()
