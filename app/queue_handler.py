from config import get_config

from database_handler import get_next_message, invalidate_message

from mastodon_utils import toot

from twitter_utils import tweet

app_config = get_config()

message_obj = get_next_message()

if(message_obj):
    if(app_config['twitter']['enable']):
        tweet(message_obj.message)

    if(app_config['mastodon']['enable']):
        toot(message_obj.message)

    invalidate_message(message_id=message_obj.id)
