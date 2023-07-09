from os import getenv
from time import sleep
from imap_tools import AND, MailBox
from post_tweet import twitter_connect

attempts = 0


def mail_connect():
    mailbox = MailBox(getenv('IMAP')).login(getenv('MAIL'), getenv('PASS'), initial_folder='INBOX')
    print('\nIMAP: conexão bem-sucedida!')
    check_email(mailbox)


def check_email(mailbox):
    read_mail(mailbox) if mailbox.uids() else trials()


def read_mail(mailbox):
    posts = []
    for msg in mailbox.fetch(AND(from_='newsletter@filipedeschamps.com.br')):
        posts = prepare_mail(msg)  # TODO: trabalhar com 'msg.html' futuramente
        archive_message(mailbox, msg.uid)
    twitter_connect(posts)


def prepare_mail(msg):
    posts = msg.text.replace('*', '').split('\r\n\r\n')
    return posts[1:-3]


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
