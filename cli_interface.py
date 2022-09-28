"""Comand Line Interface for 'imap_integration' module"""

import click
from imap_integration import imap_fetch, conf_reader


@click.command(context_settings={
    'ignore_unknown_options': True,
})
@click.option('-a', '--account', type=click.INT, default=1)
@click.option('-m', '--mode', type=click.Choice(['inbox', 'message', 'search']), default='inbox')
@click.option('-i', '--inbox', default='Inbox')
@click.option('-r', '--regex')
def main(account: int = 1, mode: str = 'inbox', inbox: str = 'Inbox', regex: str = ''):
    """Main cli app function"""
    config = conf_reader.parse_config()[account-1]
    imap = imap_fetch.ImapFetcher(config)
    match mode:
        case 'inbox':
            for output in imap.inboxes:
                print('- ', output, '\n')
        case 'message':
            ids = imap.fetch_mails_ids(inbox)
            for msg_id in ids:
                subject, email_from = imap.fetch_msg(inbox, msg_id)
                print('- ', subject, '- ', email_from, '\n')
        case 'search':
            if regex:
                ids = imap.fetch_mails_ids(inbox)
                for msg_id in ids:
                    output = imap.check_filename(inbox, msg_id=msg_id, regex=regex)
                    if output:
                        subject, email_from = imap.fetch_msg(inbox, msg_id)
                        print(f'- {subject} - {email_from} - {output}')
            else:
                print('This mode require "--regex" argument')


if __name__ == '__main__':
    main()
