import yaml
from pathlib import Path


CONF_PATH = Path('conf.yaml')
CONF_ENCODING = 'utf-8'

def parse_config(config_path: Path = CONF_PATH):
    with open(config_path, 'r', encoding=CONF_ENCODING) as config:
        config = yaml.safe_load(config)
        return config['accounts']