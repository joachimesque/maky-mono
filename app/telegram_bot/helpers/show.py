from database_handler import (get_images_by_message_id)

from telegram_bot.utils import get_message_obj


def show(args):
    for arg in args:
        message_obj = get_message_obj(arg)

        if message_obj:
            message_images = get_images_by_message_id(message_obj.id)

            if len(message_images) > 1:
                response_text = '{}\n(+ {} images)'.format(message_obj.message,
                                                           len(message_images))
            elif len(message_images) > 0:
                response_text = '{}\n(+ {} image)'.format(message_obj.message,
                                                          len(message_images))
            else:
                response_text = message_obj.message

            response_text = "Here\'s message {}:\n\n{}".format(message_obj.id,
                                                               response_text)
        else:
            response_text = 'There is no message.'

    return response_text
