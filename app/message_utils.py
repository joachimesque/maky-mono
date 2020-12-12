import re


def text_abuse_check(message_text):
    no_direct_message = r"^d [\w]+"
    no_mentions = r"(^|\s)@[\w@.]+"

    if re.search(no_direct_message, message_text):
        return([False, 'No direct message allowed.'])

    if re.search(no_mentions, message_text):
        return([False, 'No mentions allowed.'])

    return ([True, ''])


def message_length_check(message):
    status_message = ''

    if len(message) >= 500:
        status_message = 'Your message is too long for Mastodon' \
                         'and Twitter, it will be cut at publication.'
    elif len(message) >= 280:
        status_message = 'Your message is too long for Twitter,' \
                         'it will be cut at publication.'
    else:
        return ([True])

    return ([False, status_message])
