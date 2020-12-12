from database_handler import (add_message,
                              edit_message,
                              get_message_by_tg_id)

from message_utils import message_length_check, text_abuse_check

from telegram_bot.utils import check_double_message


def post_new_message(message):
    abuse_check_result = text_abuse_check(message.text)
    length_check_result = message_length_check(message.text)

    if abuse_check_result[0] is False:
        status_message = abuse_check_result[1]

    elif length_check_result[0] is False:
        status_message = length_check_result[1]

    else:
        previous_obj = check_double_message(message.date,
                                            message.message_id)

        post_result = None

        if previous_obj:
            updated_text = previous_obj.message + '\n' + message.text
            edit_result = edit_message(message=updated_text,
                                       message_id=previous_obj.id,
                                       date=message.date)
        else:
            post_result = add_message(message=message.text,
                                      message_id=message.message_id,
                                      date=message.date)

        if post_result:
            status_message = ('Message {} has been added '
                              'to the queue!').format(post_result)
        elif edit_result:
            status_message = '(and the other thing, too)'
        else:
            status_message = 'The message has not added to the queue :('

    return status_message


def post_edit_message(message):
    abuse_check_result = text_abuse_check(message.text)
    length_check_result = message_length_check(message.text)

    if abuse_check_result[0] is False:
        status_message = abuse_check_result[1]

    elif length_check_result[0] is False:
        status_message = length_check_result[1]

    else:

        message_obj = get_message_by_tg_id(message.message_id)

        if message_obj:
            post_result = edit_message(message=message.text,
                                       message_id=message_obj.id,
                                       date=message.date)

            if post_result:
                status_message = ('Message {} has been '
                                  'edited!').format(post_result)
            else:
                status_message = 'The message has not been edited :('
        else:
            status_message = 'The message doesn’t exit :('

    return status_message
