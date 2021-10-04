from imaplib import IMAP4_SSL
from email import message_from_string
from os import getenv
from dotenv import load_dotenv
from post_tweet import post_tweet

load_dotenv()


def read_email():
    FROM_EMAIL = getenv('FROM_EMAIL')
    FROM_PWD = getenv('FROM_PWD')
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993

    try:
        print('Gmail Authenticating...')
        mail = IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')
        type, data = mail.search(None, '(FROM "Arnon")')
        for num in data[0].split():
            type, data = mail.fetch(num, '(RFC822)')
            raw_text = (data[0][1])
            msg = message_from_string(raw_text.decode('utf-8'))
            print('Reading email...')
            # print('From: %s' % msg['from'])
            # print('Date: %s' % msg['date'])
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    # print('Body: \n %s ' % part.get_payload(decode=True).decode('utf-8'))
                    body = part.get_payload(decode=True).decode('utf-8')
                    print('Saving into a list...')
                    posts = body.replace('*', '').split('\r\n\r\n')
                    posts.pop(0)
        mail.close()
        mail.logout()

        # for post in posts:
        #     print(post + '\n')
        print('Done √')

        post_tweet()

    except Exception as e:
        print(str(e))
