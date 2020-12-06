from mastodon import Mastodon
from config import get_config

mastodon_config = get_config()['mastodon']

def toot(message):
  # If no config is found, bypass Mastodon and output the toot
  try:
    api_base_url = mastodon_config['api_base_url']
    client_id = mastodon_config['client_id']
    client_secret = mastodon_config['client_secret']
    access_token = mastodon_config['access_token']
    toot_visibility = mastodon_config['toot_visibility']
  except:
    return print(message)

  mastodon = Mastodon(
    api_base_url = api_base_url,
    client_id = client_id,
    client_secret = client_secret,
    access_token = access_token
  )

  mastodon.status_post(
    message,
    visibility=toot_visibility,
  )

  return True