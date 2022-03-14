from os import getenv
from imap_tools import MailBox, MailMessageFlags, A
from post_tweet import twitter_connect


def mail_connect():
    mailbox = MailBox('imap.gmail.com').login(getenv('MAIL'),
                                              getenv('PASS'),
                                              initial_folder='INBOX')
    print('Gmail: conexão bem-sucedida!')
    read_email(mailbox)


def read_email(mailbox):
    mail_list = [i.uid for i in mailbox.fetch()]
    prepare_mail(mailbox) if mail_list else print('Nenhum e-mail encontrado.')


def prepare_mail(mailbox):
    posts = []
    for msg in mailbox.fetch(A(from_='newsletter@filipedeschamps.com.br')):
        posts = msg.text.replace('*', '').split('\r\n\r\n')
        posts = posts[2:-3]
        mark_as_read(mailbox)
        archive_message(mailbox, msg.uid)
    twitter_connect(posts)


def mark_as_read(mailbox):
    flags = (MailMessageFlags.ANSWERED, MailMessageFlags.FLAGGED)
    mailbox.flag(mailbox.fetch(A(seen=False)), flags, True)
    mailbox.flag(mailbox.fetch("SENTON 01-Jan-2021"), MailMessageFlags.SEEN, False)
    print('E-mail marcado como lido.')


def archive_message(mailbox, msg_uid):
    move_to = 'Tweeted'
    mailbox.move(msg_uid, move_to)
    print('E-mail arquivado.')
