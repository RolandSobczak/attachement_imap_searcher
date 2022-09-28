import pytest


@pytest.fixture
def config() -> dict:
    return {
        'host': 'test.com',
        'port': 1111,
        'username': 'test@test.com',
        'password': 'test',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'mail': 'test@test.com',
    }