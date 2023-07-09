from os import getenv
from textwrap import wrap
from time import sleep

from tweepy import Client


def twitter_connect(tweet_list):
    client = Client(
        consumer_key=getenv('API_KEY'),
        consumer_secret=getenv('API_KEY_SECRET'),
        access_token=getenv('ACCESS_TOKEN'),
        access_token_secret=getenv('ACCESS_TOKEN_SECRET')
    )

    prepare_tweet(tweet_list, client)


def prepare_tweet(tweet_list, client):
    for tweet in tweet_list:
        tweet_encoded = tweet.encode("utf-8", "ignore")
        tweet_decoded = tweet_encoded.decode()
        each_tweet = wrap(tweet_decoded, 280, break_long_words=False)
        post_tweet(client, each_tweet)
    print('FIM')


def post_tweet(client, each_tweet):
    original_tweet = []
    for i, chunk in zip(range(len(each_tweet)), each_tweet):
        try:
            original_tweet.extend([chunk])
            print([chunk])
            if i == 0:
                original_tweet[i] = client.create_tweet(text=chunk)
            else:
                original_tweet[i] = client.create_tweet(text=chunk,
                                                        in_reply_to_tweet_id=original_tweet[i - 1].data['id'])
            sleep(1)
        except Exception as e:
            print('Erro: ', e)
            break
    sleep(600)
