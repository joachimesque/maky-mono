import re


def text_abuse_check(message_text):
    no_direct_message = r"^d [\w]+"
    no_mentions = r"(^|\s)@[\w@.]+"

    if re.search(no_direct_message, message_text):
        return(False, 'No direct message allowed.')

    if re.search(no_mentions, message_text):
        return(False, 'No mentions allowed.')

    return (True, 'All right.')


def message_length_check(message, update=None, context=None):
    status_message = ''

    if len(message) >= 500:
        status_message = 'Your message is too long for Mastodon' \
                         'and Twitter, it will be cut at publication.'
    elif len(message) >= 280:
        status_message = 'Your message is too long for Twitter,' \
                         'it will be cut at publication.'

    if status_message:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=status_message)
