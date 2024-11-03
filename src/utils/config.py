# utils/config.py

import os
import json

class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from a JSON file and environment variables."""
        config = {}

        # Load from JSON file
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config.update(json.load(f))

        # Override with environment variables
        for key, value in os.environ.items():
            if key.startswith('APP_'):  # Only load variables that start with APP_
                config[key[4:]] = value  # Remove 'APP_' prefix

        return config

    def get(self, key, default=None):
        """Get a configuration value by key."""
        return self.config.get(key, default)

# Example usage
if __name__ == "__main__":
    config = Config()
    print("Database URL:", config.get('DATABASE_URL', 'Not set'))
    print("API Key:", config.get('API_KEY', 'Not set'))
