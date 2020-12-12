import datetime

from database_handler import (get_last_message,
                              get_message_by_id,
                              get_next_message)


def get_message_obj(argument):
    message_obj = None

    if argument.isdigit():
        message_obj = get_message_by_id(message_id=argument)
    elif argument == 'last':
        message_obj = get_last_message()
    elif argument == 'next':
        message_obj = get_next_message()

    return message_obj


def check_double_message(message_date, message_id):
    last_message_obj = get_last_message()

    if not last_message_obj:
        return False

    last_message_date = last_message_obj.tg_date
    last_message_date = datetime.datetime.fromisoformat(last_message_date)

    message_minus_three_second = message_date - datetime.timedelta(seconds=3)

    if message_minus_three_second <= last_message_date <= message_date:
        # Temporary removal of second check (by message_id)
        # if last_message_obj.tg_message_id == message_id - 1:
        return last_message_obj

    return False
