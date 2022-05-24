from read_email import check_mail
from dotenv import load_dotenv


def main():
    load_dotenv()
    check_mail()


if __name__ == '__main__':
    main()
