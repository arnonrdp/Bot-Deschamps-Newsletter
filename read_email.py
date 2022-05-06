from os import getenv
from time import sleep
from imap_tools import A, MailBox, MailMessageFlags
from post_tweet import twitter_connect

attempts = 0


def mail_connect():
    mailbox = MailBox('imap.gmail.com').login(getenv('MAIL'), getenv('PASS'), initial_folder='INBOX')
    print('\nGmail: conexão bem-sucedida!')
    read_email(mailbox)


def read_email(mailbox):
    mail_list = [i.uid for i in mailbox.fetch()]
    prepare_mail(mailbox) if mail_list else trials()


def prepare_mail(mailbox):
    posts = []
    for msg in mailbox.fetch(A(from_='newsletter@filipedeschamps.com.br')):
        posts = msg.text.replace('*', '').split('\r\n\r\n')
        posts = posts[2:-3]
        mark_as_read(mailbox, msg.uid)
        archive_message(mailbox, msg.uid)
    twitter_connect(posts)


def mark_as_read(mailbox, msg_uid):
    mailbox.flag(msg_uid, MailMessageFlags.SEEN, True)
    print('E-mail marcado como lido.')


def archive_message(mailbox, msg_uid):
    mailbox.move(msg_uid, 'Tweeted')
    print('E-mail arquivado.')


def trials():
    global attempts
    attempts += 1
    print('\nNenhum e-mail encontrado.', end=' ')
    if attempts == 3:
        print('Tentativas excedidas.')
        return
    print('Tentando novamente em 15 minutos...')
    sleep(900)
    mail_connect()
