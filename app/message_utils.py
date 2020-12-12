import re


def text_abuse_check(message_text):
    no_direct_message = r"^d [\w]+"
    no_mentions = r"(?:^|[^\w])@[\w@.]+"

    if re.match(no_direct_message, message_text):
        return(False, 'No direct message allowed')

    if re.match(no_mentions, message_text):
        return(False, 'No mentions allowed')

    return (True, 'All right')
