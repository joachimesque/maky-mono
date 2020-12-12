from database_handler import (add_message,
                              delete_message,
                              get_images_by_message_id)

from file_handler import delete_file, store_file

from message_utils import message_length_check, text_abuse_check

from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup)

import telegram_bot.helpers

from .security import restricted

from .utils import check_double_message, get_message_obj


@restricted
def handle_start(update, context):
    response_text = 'Hello to you, too!'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response_text)


@restricted
def handle_show(update, context):
    if not context.args:
        response_text = ("No argument given.\n"
                         "You can type '/show next', '/show last', "
                         "or any message number '/show 666'.")

    else:
        response_text = telegram_bot.helpers.show(args=context.args)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response_text)


@restricted
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


@restricted
def handle_post_message(update, context):
    if update.message:
        message = update.message
        status_message = telegram_bot.helpers.post_new_message(message)
    elif update.edited_message:
        message = update.edited_message
        status_message = telegram_bot.helpers.post_edit_message(message)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=status_message)


@restricted
def handle_post_image(update, context):
    message_id = None
    update_id = update.update_id
    message = update.message
    chat_id = message.chat.id

    file_infos = telegram_bot.helpers.get_file_info(update.message)

    arguments = {
        'bot': context.bot,
        'file_id': file_infos['file_id'],
        'chat_id': chat_id,
        'update_id': update_id,
        'mime_type': file_infos['mime_type'],
    }

    # If one image was shared with a caption
    if message.caption:

        abuse_check_result = text_abuse_check(message.caption)
        length_check_result = message_length_check(message.caption)

        if abuse_check_result[0] is False:
            status_message = abuse_check_result[1]

        elif length_check_result[0] is False:
            length_check_result = length_check_result[1]

        else:
            post_result = add_message(message=message.caption,
                                      message_id=message.message_id,
                                      date=message.date)

            message_id = post_result

            image_result = store_file(message_id=message_id, **arguments)

            if post_result:
                if image_result[0]:
                    status_message = ('Message {} has been added '
                                      'to the queue along with one image!'
                                      '').format(post_result)
                else:
                    status_message = ('Message {} has been added '
                                      'to the queue, but not the image '
                                      ':(').format(post_result)
            else:
                status_message = 'The message has not added to the queue :('

    # If one or multiple images have been shared
    # at the same time as a message
    else:
        previous_obj = check_double_message(message.date,
                                            message.message_id)

        if previous_obj:
            message_id = previous_obj.id

            image_result = store_file(message_id=message_id, **arguments)

            if image_result[0]:
                status_message = ('The image was added'
                                  ' to message {}').format(message_id)
            else:
                status_message = 'The image was not added to a message :('

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=status_message)


@restricted
def handle_button(update, context):
    query = update.callback_query

    query.answer()

    if not bool(query.data):
        response_text = 'No message has been deleted.'

    else:
        args = query.data.strip('][').split(',')

        for arg in args:
            arg = arg.strip().strip("'")
            message_obj = get_message_obj(argument=arg)

            if message_obj:
                message_images = get_images_by_message_id(message_obj.id)

                for file in message_images:
                    delete_file(file.file_path)

                delete_message(message_obj.id)
                response_text = ('Message {} has been '
                                 'deleted.').format(message_obj.id)

                if len(args) > 1:
                    response_text = 'All messages have been deleted.'
            else:
                response_text = 'There was no message to delete.'

    query.edit_message_text(text=response_text)
