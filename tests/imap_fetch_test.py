from unittest.mock import MagicMock, Mock
import imaplib
import pytest
from ..imap_integration import imap_fetch
from .fixtures import config


def imap_manager_test(config):
    imaplib.IMAP4_SSL = Mock()
    with imap_fetch.ImapManager(
        host=config['host'],
        username=config['username'],
        password=config['password'],
        port=config['port']
    ), pytest.raises(Exception) as imap:
        imaplib.IMAP4_SSL.assert_called_with(host=config['host'], port=config['port'])
        imaplib.IMAP4_SSL().login.assert_called_with(config['username'], config['password'])
        imap.server.state = 'SELECTED'
        raise Exception()
        imaplib.IMAP4_SSL().close.assert_called()


def inboxes_fetch_test(config):
    imap = imap_fetch.ImapFetcher(config)
    imap.connection.list = MagicMock(return_value=(
        'OK',
        (
            b'(\\Archive \\HasNoChildren) "/" "Archive"',
            b'(\\Sent \\HasNoChildren) "/" "Sent"',
            b'(\\Trash \\HasNoChildren) "/" "Trash"'
        )
    ))
    assert imap.inboxes == ('Archive', 'Sent', 'Trash')

def fetch_mails_ids_test(config):
    imaplib.IMAP4_SSL = Mock()
    imap = imap_fetch.ImapFetcher(config)
    imap.connection.search = MagicMock(return_value=('OK', [b'1 2 3']))
    imap.connection.select = Mock()
    assert imap.fetch_mails_ids('Sent') == (b'1', b'2', b'3')
