from config import get_config

from mastodon import Mastodon

mastodon_config = get_config()['mastodon']


def new_mastodon():
    # If no config is found, bypass Mastodon and output the toot
    try:
        api_base_url = mastodon_config['api_base_url']
        client_id = mastodon_config['client_id']
        client_secret = mastodon_config['client_secret']
        access_token = mastodon_config['access_token']
    except:
        return False

    return Mastodon(
        api_base_url=api_base_url,
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token
    )


def upload_mastodon_media(media_path, mime_type):
    mastodon = new_mastodon()

    if not mastodon:
        print(media_path)
        return False

    media_upload = mastodon.media_post(media_path, mime_type=mime_type)

    return media_upload


def toot(message, media=[]):
    try:
        toot_visibility = mastodon_config['toot_visibility']
    except:
        return False

    if len(message) > 500:
        message = message[:498] + '…'

    mastodon = new_mastodon()

    if not mastodon:
        print(message)
        return False

    mastodon.status_post(
        message,
        visibility=toot_visibility,
        media_ids=media,
    )

    return True
