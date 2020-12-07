from config import get_config
from twitter_utils import tweet
from database_handler import (add_message,
                              edit_message,
                              get_message_by_id,
                              get_message_by_tg_id,
                              get_next_message,
                              get_last_message,
                              delete_message)

import logging
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters)
import datetime

# BASIC CONFIG
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
telegram_config = get_config()['telegram']

# UTILS
def check_user(user_id):
  return user_id == telegram_config['restrict_user']

def check_message_length(message, update = None, context = None):
  status_message = ''

  if(len(message) >= 500):
    status_message = 'Your message is too long for Mastodon and Twitter, it will be cut at publication.'
  elif(len(message) >= 280):
    status_message = 'Your message is too long for Twitter, it will be cut at publication.'

  if(status_message):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=status_message)
  
def get_message_obj(argument):
  message_obj = None

  if(argument.isdigit()):
    message_obj = get_message_by_id(message_id = argument)
  elif(argument == 'last'):
    message_obj = get_last_message()
  elif(argument == 'next'):
    message_obj = get_next_message()

  return message_obj

def check_double_message(message_date, message_id):
  last_message_obj = get_last_message()
  last_message_date = datetime.datetime.fromisoformat(last_message_obj.tg_date)

  message_minus_three_second = message_date - datetime.timedelta(seconds=3)

  if(message_minus_three_second <= last_message_date <= message_date):
    if(last_message_obj.tg_message_id == message_id - 1):
      return last_message_obj

  return False

# START STUFF
updater = Updater(token=telegram_config['token'], use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
  response_text = 'Hello to you, too!'
  context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

def show(update, context):
  if(not context.args):
    response_text = ("No argument given.\n"
      "You can type '/show next', '/show last', "
      "or any message number '/show 666'.")

  for arg in context.args:
    message_obj = get_message_obj(arg)

    if(message_obj):
      response_text = message_obj.message
    else:
      response_text = 'There is no message.'
    
  context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

def delete(update, context):
  if(not context.args):
    response_text = ("No argument given.\n"
      "You can type '/delete next', '/delete last', "
      "or any message number '/delete 666'.")

  for arg in context.args:
    message_obj = get_message_obj(arg)

    if(message_obj):
      delete_message(message_obj.id)
      response_text = 'The message was deleted.'
    else:
      response_text = 'There was no message to delete.'
    
  context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

def post_message(update, context):
  if(update.message):
    if(check_user(update.message.chat.id)):
      check_message_length(update.message.text,
                    update = update,
                    context = context)

      previous_message_obj = check_double_message(update.message.date,
                                                  update.message.message_id)

      post_result = None

      if(previous_message_obj):
        updated_text = '%s\n%s' % (previous_message_obj.message, update.message.text)
        update_result = edit_message(message=updated_text,
                                   message_id= previous_message_obj.id,
                                   date= update.message.date)
      else:
        post_result = add_message(message = update.message.text,
                                  message_id = update.message.message_id,
                                  date = update.message.date)


      if(post_result):
        status_message = 'The message %s has been added to the queue!' % post_result
      elif(update_result):
        status_message = '(and the other thing, too)'
      else:
        status_message = 'The message has not added to the queue :('

    else:
      status_message = 'I don’t know you!'

  elif(update.edited_message):
    if(check_user(update.edited_message.chat.id)):
      check_message_length(update.edited_message.text,
                    update = update,
                    context = context)

      message_obj = get_message_by_tg_id(update.edited_message.message_id)

      post_result = edit_message(message=update.edited_message.text,
                                 message_id= message_obj.id,
                                 date= update.edited_message.date)

      if(post_result):
        status_message = 'The message %s has been edited!' % post_result
      else:
        status_message = 'The message has not been edited :('
 
    else:
        status_message = 'I don’t know you!'
  
  context.bot.send_message(chat_id=update.effective_chat.id, text=status_message)

start_handler = CommandHandler('start', start)
show_handler = CommandHandler('show', show)
delete_handler = CommandHandler('delete', delete)
message_handler = MessageHandler(Filters.text & (~Filters.command), post_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(show_handler)
dispatcher.add_handler(delete_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()