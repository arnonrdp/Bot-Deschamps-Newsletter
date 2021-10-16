from dotenv import load_dotenv
from os import getenv
from textwrap import wrap
from time import sleep
from tweepy import OAuthHandler, API


def twitter_connect(tweet_list):
    load_dotenv()
    consumer_key = getenv('API_KEY')
    consumer_secret = getenv('API_KEY_SECRET')
    access_token = getenv('ACCESS_TOKEN')
    access_token_secret = getenv('ACCESS_TOKEN_SECRET')

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = API(auth)
    try:
        api.verify_credentials()
        print('Twitter: conexão bem-sucedida!')
        post_tweet(tweet_list, api)
    except:
        sleep(120)
        print('Twitter: conexão mal-sucedida! Tentando novamente em 2 minutos.')
        twitter_connect(tweet_list)


def post_tweet(tweet_list, api):
    for tweet in tweet_list:
        tweet_encode = tweet.encode("utf-8", "ignore")
        tweet_decode = tweet_encode.decode()
        print('\n' + tweet_decode + '\n')
        each_tweet = wrap(tweet_decode, 280, break_long_words=False)
        original_tweet = []
        for i, chunk in zip(range(len(each_tweet)), each_tweet):
            original_tweet.extend([chunk])
            print([chunk])
            if i == 0:
                original_tweet[i] = api.update_status(chunk)
            else:
                original_tweet[i] = api.update_status(chunk,
                                                      in_reply_to_status_id=original_tweet[i-1].id,
                                                      auto_populate_reply_metadata=True)
            sleep(1)
        sleep(300)
    print('FIM')
