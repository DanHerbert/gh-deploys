import os

import yaml

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_PATH, 'config.yaml')

def get_config():
    """Gets the config object from disk."""
    with open(CONFIG_PATH, mode='rt', encoding='utf-8') as file_handle:
        return yaml.safe_load(file_handle)