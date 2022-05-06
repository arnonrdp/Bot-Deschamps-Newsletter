import logging
from os import getenv
from time import sleep
from imap_tools import MailBox, MailMessageFlags, A
from post_tweet import twitter_connect


def mail_connect():
    mailbox = MailBox('imap.gmail.com').login(getenv('MAIL'),
                                              getenv('PASS'),
                                              initial_folder='INBOX')
    print('\nPrint – Gmail: conexão bem-sucedida!')
    logging.debug("Hello World")
    logger1 = logging.getLogger("module_1")
    logger2 = logging.getLogger("module_2")

    logger1.debug("Module 1 debugger")
    logger2.debug("Module 2 debugger")
    read_email(mailbox)


def read_email(mailbox):
    mail_list = [i.uid for i in mailbox.fetch()]
    prepare_mail(mailbox) if mail_list else countdown(900)


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


def countdown(t):
    print('Nenhum e-mail encontrado. Tentando novamente em 15 minutos.')
    while t:
        minutes, seconds = divmod(t, 60)
        time_format = '{:02d}:{:02d}'.format(minutes, seconds)
        print('\r', time_format, end='')
        sleep(1)
        t -= 1
    mail_connect()
