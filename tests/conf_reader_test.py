from pathlib import Path
from ..imap_integration import conf_reader

def parse_config_test():
    assert conf_reader.parse_config(Path('tests/conf.yaml')) == [{
        'host': 'test.com',
        'port': 1111,
        'username': 'test@test.com',
        'password': 'test',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'mail': 'test@test.com',
    }]
