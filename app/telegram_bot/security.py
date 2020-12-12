# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#restrict-access-to-a-handler-decorator

from functools import wraps

from config import get_config

telegram_config = get_config()['telegram']
RESTRICT_USERS = [telegram_config['restrict_user']]


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in RESTRICT_USERS:
            print("I don’t know you, {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped
