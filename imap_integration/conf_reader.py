"""Parse yaml conf file to python"""

from pathlib import Path
import yaml


CONF_PATH = Path('conf.yaml')
CONF_ENCODING = 'utf-8'

def parse_config(config_path: Path = CONF_PATH):
    """Parse file from config_path to array with dict objects contains imap configuration"""
    with open(config_path, 'r', encoding=CONF_ENCODING) as config:
        config = yaml.safe_load(config)
        return config['accounts']
