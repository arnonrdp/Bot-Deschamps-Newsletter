from os import getenv
from time import sleep
from imap_tools import AND, MailBox, MailMessageFlags
from post_tweet import twitter_connect

attempts = 0


def check_mail():
    posts = []
    with MailBox(getenv('IMAP')).login(getenv('MAIL'), getenv('PASS')) as mailbox:
        if not mailbox.uids():
            trials()
        for msg in mailbox.fetch(AND(from_='newsletter@filipedeschamps.com.br')):
            mark_as_read(mailbox, msg.uid)
            archive_message(mailbox, msg.uid)
            posts = prepare_mail(msg)  # TODO: utilizar 'msg.html' futuramente
        twitter_connect(posts)
        mailbox.close()
        mailbox.logout()


def prepare_mail(msg):
    posts = msg.text.replace('*', '').split('\r\n\r\n')
    return posts[2:-3]


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
    check_mail()
