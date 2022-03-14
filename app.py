from read_email import mail_connect
from dotenv import load_dotenv


def main():
    load_dotenv()
    mail_connect()


if __name__ == '__main__':
    main()
