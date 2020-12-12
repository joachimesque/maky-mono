from config import get_config
from twitter_utils import tweet
from database_handler import (add_message,
                              edit_message,
                              get_message_by_id,
                              get_message_by_tg_id,
                              get_next_message,
                              get_last_message,
                              delete_message,
                              get_images_by_message_id)
from file_handler import store_file, delete_file

import logging
from telegram import (Bot,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          CallbackQueryHandler,
                          Filters)
import datetime
from message_utils import text_abuse_check


# BASIC CONFIG
logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logging_format,
                    level=logging.INFO)
telegram_config = get_config()['telegram']


# UTILS
def check_user(user_id):
    return user_id == telegram_config['restrict_user']


def check_message_length(message, update=None, context=None):
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


# MAIN HANDLERS
def handle_start(update, context):
    response_text = 'Hello to you, too!'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response_text)


def handle_show(update, context):
    if not context.args:
        response_text = ("No argument given.\n"
                         "You can type '/show next', '/show last', "
                         "or any message number '/show 666'.")

    for arg in context.args:
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

            response_text = 'Here’s message {}:\n\n{}'.format(message_obj.id,
                                                              response_text)
        else:
            response_text = 'There is no message.'

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response_text)


def handle_delete(update, context):
    if not context.args:
        response_text = "No argument given.\n" \
                        "You can type '/delete next', '/delete last', " \
                        "or any message number '/delete 666'."
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=response_text)
        return

    keyboard = [
        [
            InlineKeyboardButton("Delete", callback_data=str(context.args)),
            InlineKeyboardButton("Cancel", callback_data='False'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Are you sure?', reply_markup=reply_markup)


def handle_post_message(update, context):
    if update.message:
        message = update.message

        abuse_check_result = text_abuse_check(message.text)
        if abuse_check_result[0] is False:
            status_message = abuse_check_result[1]

        elif check_user(message.chat.id):
            check_message_length(message.text,
                                 update=update,
                                 context=context)

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
                status_message = (f'Message {post_result} '
                                  f'has been added to the queue!')
            elif edit_result:
                status_message = '(and the other thing, too)'
            else:
                status_message = 'The message has not added to the queue :('

        else:
            status_message = 'I don’t know you!'

    elif update.edited_message:
        message = update.edited_message

        abuse_check_result = text_abuse_check(message.text)
        if abuse_check_result[0] is False:
            status_message = abuse_check_result[1]

        elif check_user(message.chat.id):
            check_message_length(message.text,
                                 update=update,
                                 context=context)

            message_obj = get_message_by_tg_id(message.message_id)

            if message_obj:
                post_result = edit_message(message=message.text,
                                           message_id=message_obj.id,
                                           date=message.date)

                if post_result:
                    status_message = f'Message {post_result} ' \
                                      'has been edited!'
                else:
                    status_message = 'The message has not been edited :('
            else:
                status_message = 'The message doesn’t exit :('

        else:
            status_message = 'I don’t know you!'

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=status_message)


def handle_post_image(update, context):
    message_id = None
    update_id = update.update_id
    chat_id = update.message.chat.id

    if update.message.document:
        file_id = update.message.document.file_id
        mime_type = update.message.document.mime_type
    else:
        file_id = update.message.photo[-1].file_id
        mime_type = None

    if update.message.caption:
        check_message_length(update.message.caption,
                             update=update,
                             context=context)

        post_result = add_message(message=update.message.caption,
                                  message_id=update.message.message_id,
                                  date=update.message.date)

        message_id = post_result

    else:
        previous_obj = check_double_message(update.message.date,
                                            update.message.message_id)

        if previous_obj:
            message_id = previous_obj.id

    image_result = store_file(bot=context.bot,
                              file_id=file_id,
                              chat_id=chat_id,
                              update_id=update_id,
                              message_id=message_id,
                              mime_type=mime_type)

    if update.message.caption:
        if post_result:
            if image_result[0]:
                status_message = (f'Message {post_result} '
                                  f'has been added to the queue '
                                  f'along with one image!')
            else:
                status_message = (f'Message {post_result} '
                                  f'has been added to the queue, '
                                  f'but not the image :(')
        else:
            status_message = 'The message has not added to the queue :('
    else:
        if image_result[0]:
            status_message = (f'The image was added to message {post_result}')
        else:
            status_message = 'The image was not added to a message :('

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=status_message)


def handle_button(update, context):
    query = update.callback_query

    query.answer()

    if not bool(query.data):
        query.edit_message_text(text='No message has been deleted.')

        return

    args = query.data.strip('][').split(',')

    for arg in args:
        arg = arg.strip().strip("'")
        message_obj = get_message_obj(argument=arg)

        if message_obj:
            message_images = get_images_by_message_id(message_obj.id)

            for file in message_images:
                delete_file(file.file_path)

            delete_message(message_obj.id)
            response_text = f'Message {message_obj.id} has been deleted.'

            if len(args) > 1:
                response_text = 'All messages have been deleted.'
        else:
            response_text = 'There was no message to delete.'

    query.edit_message_text(text=response_text)


# START STUFF
def main():
    updater = Updater(token=telegram_config['token'], use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', handle_start))
    dispatcher.add_handler(CommandHandler('show', handle_show))
    dispatcher.add_handler(CommandHandler('delete', handle_delete))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command),
                           handle_post_message))
    dispatcher.add_handler(MessageHandler(Filters.photo |
                                          Filters.document.image,
                                          handle_post_image))
    dispatcher.add_handler(CallbackQueryHandler(handle_button))
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
