import tweepy
import math
import textwrap
import os
from dotenv import load_dotenv

load_dotenv()


def post_tweet(tweet_list):
    consumer_key = os.getenv('API_KEY')
    consumer_secret = os.getenv('API_KEY_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    print('Twitter Authenticating...')
    try:
        api.verify_credentials()
        print("Authentication Successful")

        for tweet in tweet_list:
            print("\n" + tweet + "\n")
        
        # tweet = """Intel apresenta nova geração de processador neuromórfico: a CPU “Loihi 2” apresenta mudanças fundamentais de hardware que permitirão a descoberta de padrões e associações de forma mais eficiente em dados. O processador suporta um máximo de 120 milhões de sinapses, uma quantidade pequena quando comparada com as mais de um trilhão no cérebro humano. A computação neuromórfica utiliza abordagens algorítmicas que emulam como o cérebro interage com o mundo para fornecer recursos mais próximos da cognição humana. As informações são do site The Register e Intel"""

        # tweet_length = len(tweet)

        # if tweet_length <= 280:
        #     api.update_status(tweet)
        # elif tweet_length >= 280:
        #     quantity_of_tweets = tweet_length / 280
        #     tweet_chunk_length = tweet_length / math.ceil(quantity_of_tweets)
        #     tweet_chunks = textwrap.wrap(tweet,  math.ceil(
        #         tweet_chunk_length), break_long_words=False)

        #     # iterate over the chunks
        #     original_tweet = []
        #     for i, chunk in zip(range(len(tweet_chunks)), tweet_chunks):
        #         original_tweet.extend([chunk])
        #         if i == 0:
        #             original_tweet[i] = api.update_status(chunk)
        #         else:
        #             print(original_tweet[i])
        #             original_tweet[i] = api.update_status(chunk,
        #                                                   in_reply_to_status_id=original_tweet[i-1].id,
        #                                                   auto_populate_reply_metadata=True)
        #         print(f'{i} -> {original_tweet[i]} <-> {chunk}/n/n')
    except:
        print("Authentication Error\nTry again later")
