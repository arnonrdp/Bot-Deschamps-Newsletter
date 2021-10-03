import tweepy
import math
import textwrap
import os
from dotenv import load_dotenv

load_dotenv()


def post_tweet():
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
    except:
        print("Authentication Error")

    tweet = """Novo malware é descoberto no Android: estima-se que o “GriftHorse” já
            tenha infectado mais de 10 milhões de dispositivos globalmente e estava
            presente em diversos aplicativos na Play Store (o Google já os removeu, mas
            ainda podem estar circulando em outras lojas). O trojan engana os usuários
            pedindo seus números de telefone para ganharem um prêmio, mas ao invés
            disso, acaba confirmando um serviço de assinatura baseado em SMS. A lista
            com mais de uma centena de apps maliciosos pode ser conferida no blog da 
            empresa de segurança Zimperium e recomenda-se que sejam desinstalados imediatamente."""

    tweet_length = len(tweet)

    if tweet_length <= 280:
        api.update_status(tweet)
    elif tweet_length >= 280:
        tweet_length_limit = tweet_length / 280
        tweet_chunk_length = tweet_length / math.ceil(tweet_length_limit)
        tweet_chunks = textwrap.wrap(tweet,  math.ceil(
            tweet_chunk_length), break_long_words=False)

        # iterate over the chunks
        for x, chunk in zip(range(len(tweet_chunks)), tweet_chunks):
            api.update_status(chunk)
            if x == 0:
                print(f'1 of {len(tweet_chunks)} {chunk}')
            else:
                print(f'{x+1} of {len(tweet_chunks)} {chunk}')