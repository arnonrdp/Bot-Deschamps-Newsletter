from os import getenv
from textwrap import wrap
from time import sleep
from tweepy import OAuthHandler, API


def prepare_tweet(tweet_list, api):
    auth = OAuthHandler(getenv('API_KEY'),
                        getenv('API_KEY_SECRET'))
    auth.set_access_token(getenv('ACCESS_TOKEN'),
                          getenv('ACCESS_TOKEN_SECRET'))
    api = API(auth)
    api.verify_credentials()
    print('Twitter: conexão bem-sucedida!')
    prepare_tweet(tweet_list, api)
    for tweet in tweet_list:
        each_tweet = wrap(tweet, 280, break_long_words=False)
        post_tweet(api, each_tweet)
    print('FIM')


def post_tweet(api, each_tweet):
    original_tweet = []
    for i, chunk in zip(range(len(each_tweet)), each_tweet):
        original_tweet.extend([chunk])
        print([chunk])
        if i == 0:
            original_tweet[i] = api.update_status(chunk)
        else:
            original_tweet[i] = api.update_status(chunk,
                                                    in_reply_to_status_id=original_tweet[i - 1].id,
                                                    auto_populate_reply_metadata=True)
        sleep(1)
    sleep(300)