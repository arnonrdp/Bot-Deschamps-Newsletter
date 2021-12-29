from os import getenv
from textwrap import wrap
from time import sleep
from tweepy import OAuthHandler, API


def twitter_connect(tweet_list):
    auth = OAuthHandler(getenv('API_KEY'),
                        getenv('API_KEY_SECRET'))
    auth.set_access_token(getenv('ACCESS_TOKEN'),
                          getenv('ACCESS_TOKEN_SECRET'))
    api = API(auth)
    try:
        api.verify_credentials()
        print('Twitter: conexão bem-sucedida!')
        prepare_tweet(tweet_list, api)
    except BaseException as e:
        print('Twitter: conexão mal-sucedida! Tentando novamente em 2 minutos.\n', e)
        sleep(120)
        twitter_connect(tweet_list)


def prepare_tweet(tweet_list, api):
    for tweet in tweet_list:
        tweet_encoded = tweet.encode("utf-8", "ignore")
        tweet_decoded = tweet_encoded.decode()
        each_tweet = wrap(tweet_decoded, 280, break_long_words=False)
        post_tweet(api, each_tweet)
    print('FIM')


def post_tweet(api, each_tweet):
    original_tweet = []
    for i, chunk in zip(range(len(each_tweet)), each_tweet):
        try:
            original_tweet.extend([chunk])
            print([chunk])
            if i == 0:
                original_tweet[i] = api.update_status(chunk)
            else:
                original_tweet[i] = api.update_status(chunk,
                                                      in_reply_to_status_id=original_tweet[i - 1].id,
                                                      auto_populate_reply_metadata=True)
            sleep(1)
        except Exception as e:
            print('Erro: ', e)
            break
    sleep(300)