from config import get_config

import tweepy

twitter_config = get_config()['twitter']


def new_twitter_api():
    # If no config is found, bypass Twitter and output the tweet
    try:
        consumer_key = twitter_config['consumer_key']
        consumer_key_secret = twitter_config['consumer_key_secret']
        access_token = twitter_config['access_token']
        access_token_secret = twitter_config['access_token_secret']
    except:
        return False

    # Authenticate to Twitter
    twitter_auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    twitter_auth.set_access_token(access_token, access_token_secret)

    # Create API object
    twitter_api = tweepy.API(twitter_auth)

    return twitter_api


def upload_twitter_media(media_path):
    twitter_api = new_twitter_api()

    if not twitter_api:
        print(media_path)
        return False

    media_upload = twitter_api.media_upload(media_path)

    return media_upload


def tweet(message, media_ids=[]):
    if(len(message) > 280):
        message = message[:278] + '…'

    twitter_api = new_twitter_api()

    if not twitter_api:
        print(message)
        return False

    # Create a tweet
    twitter_api.update_status(message, media_ids=media_ids)

    return True
