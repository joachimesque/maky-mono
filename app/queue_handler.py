from pathlib import Path

from config import get_config

from database_handler import (get_images_by_message_id,
                              get_next_message,
                              invalidate_message)

from mastodon_utils import toot, upload_mastodon_media

from twitter_utils import tweet, upload_twitter_media

app_config = get_config()


def get_path(media_path):
    return str(Path(__file__).parents[1].joinpath('uploads', media_path))


def main():
    message_obj = get_next_message()
    message_images = get_images_by_message_id(message_obj.id)

    if(message_obj):
        if(app_config['twitter']['enable']):
            media_ids = []

            for media in message_images:
                media_path = get_path(media.file_path)
                uploaded_media = upload_twitter_media(media_path)
                media_ids.append(uploaded_media.media_id_string)

            tweet(message_obj.message, media_ids=media_ids)

        if(app_config['mastodon']['enable']):
            media_list = []

            for media in message_images:
                media_path = get_path(media.file_path)
                mime_type = media.mime_type
                uploaded_media = upload_mastodon_media(media_path,
                                                       mime_type=mime_type)
                media_list.append(uploaded_media)

            toot(message_obj.message, media=media_list)

        invalidate_message(message_id=message_obj.id)


if __name__ == '__main__':
    main()
