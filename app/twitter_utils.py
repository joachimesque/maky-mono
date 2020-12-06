import tweepy
from config import get_config

twitter_config = get_config()['twitter']

def tweet(message):
  # If no config is found, bypass Twitter and output the tweet
  try:
    consumer_key = twitter_config['consumer_key']
    consumer_key_secret = twitter_config['consumer_key_secret']
    access_token = twitter_config['access_token']
    access_token_secret = twitter_config['access_token_secret']
  except:
    return print(message)

  # Authenticate to Twitter
  twitter_auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
  twitter_auth.set_access_token(access_token, access_token_secret)

  # Create API object
  twitter_api = tweepy.API(twitter_auth)

  # Create a tweet
  twitter_api.update_status(message)

  return True