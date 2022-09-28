"""Provides better but simple interface for IMAP Manager"""

import imaplib
import email
from email.header import decode_header
import re


class ImapManager:
    """Context manager for imap services"""

    def __init__(self, host: str, username: str, password: str, port: int = imaplib.IMAP4_SSL_PORT):
        """Collects pass for imap account"""
        self.server = imaplib.IMAP4_SSL(host=host, port=port)
        self.username = username
        self.password = password

    def __enter__(self):
        """Sends login to server and return imap connection"""
        self.server.login(self.username, self.password)
        return self.server

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Calls close method if status is selected"""
        if self.server.state == 'SELECTED':
            self.server.close()


class ImapFetcher:
    """Simple interface provides some actions for IMAP"""
    def __init__(self, config: dict):
        """collects config and initializes ImapManager object"""
        self.config = config
        with ImapManager(
            host=config['host'],
            username=config['username'],
            password=config['password'],
            port=config['port']
        ) as connection:
            self.connection = connection

    def fetch_mails_ids(self, inbox: str) -> tuple:
        """Fetch all ids in inbox and returns it in tuple"""
        self.connection.select(inbox)
        return tuple(self.connection.search(None, 'ALL')[1][0].split())

    def fetch_msg(self, inbox: str, msg_id: bytes):
        """Provides tuple with subject and sender email"""
        self.connection.select(inbox)
        _, msg = self.connection.fetch(msg_id, '(RFC822)')
        message = email.message_from_bytes(msg[0][1])
        subject, subject_encoding = decode_header(message['Subject'])[0]
        if subject_encoding is not None:
            subject = subject.decode('utf-8')
        email_from, from_encoding = decode_header(message['From'])[0]
        if from_encoding is not None:
            email_from = email_from.decode('utf-8')
        return subject, email_from

    def fetch_msg_filenames(self, inbox: str, msg_id: bytes) -> tuple:
        """Returns tuple with filenames of message attachments"""
        self.connection.select(inbox)
        _, msg = self.connection.fetch(msg_id, '(RFC822)')
        message = email.message_from_bytes(msg[0][1])
        files = tuple(msg.get_filename() for msg in message.walk())
        return tuple(filter(lambda filename: filename is not None, files))

    def check_filename(self, inbox: str, msg_id: bytes, regex) -> tuple:
        """Returns tuple with filenames which pass to regex"""
        filenames = self.fetch_msg_filenames(inbox, msg_id)
        output = []
        for filename in filenames:
            if re.match(regex, filename):
                output.append(filename)
        return tuple(output)

    @property
    def inboxes(self):
        """Fetch names of all inboxes in account"""
        return tuple(inbox.decode().split('"')[-2] for inbox in self.connection.list()[1])
