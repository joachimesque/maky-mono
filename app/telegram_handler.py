from config import get_config
from twitter_utils import tweet
from database_handler import (add_message,
                              edit_message,
                              get_message_by_id,
                              get_next_message,
                              get_last_message)

import logging
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters)


# BASIC CONFIG
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
telegram_config = get_config()['telegram']

# UTILS
def check_user(user_id):
  return user_id == telegram_config['restrict_user']

def check_message(message, update = None, context = None):
  status_message = ''

  if(len(message) >= 500):
    status_message = 'Your message is too long for Mastodon and Twitter, it will be cut at publication.'
  elif(len(message) >= 280):
    status_message = 'Your message is too long for Twitter, it will be cut at publication.'

  if(status_message):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=status_message)
  

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
    message_obj = None

    if(arg.isdigit()):
      message_obj = get_message_by_id(message_id = arg)
    elif(arg == 'last'):
      message_obj = get_last_message()
    elif(arg == 'next'):
      message_obj = get_next_message()

    if(message_obj):
      response_text = message_obj.message
    else:
      response_text = 'There is no message.'
    
  context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)



def post_message(update, context):
  if(update.message):
    if(check_user(update.message.chat.id)):
      check_message(update.message.text,
                    update = update,
                    context = context)

      post_result = add_message(message=update.message.text,
                                message_id= update.message.message_id,
                                date= update.message.date)

      if(post_result):
        status_message = 'The message %s has been added to the queue!' % update.message.message_id
      else:
        status_message = 'The message has not added to the queue :('

    else:
      status_message = 'I don’t know you!'

  elif(update.edited_message):
    if(check_user(update.edited_message.chat.id)):
      check_message(update.edited_message.text,
                    update = update,
                    context = context)

      post_result = edit_message(message=update.edited_message.text,
                                 message_id= update.edited_message.message_id,
                                 date= update.edited_message.date)

      if(post_result):
        status_message = 'The message %s has been edited!' % update.edited_message.message_id
      else:
        status_message = 'The message has not been edited :('
 
    else:
        status_message = 'I don’t know you!'
  
  context.bot.send_message(chat_id=update.effective_chat.id, text=status_message)

start_handler = CommandHandler('start', start)
show_handler = CommandHandler('show', show)
message_handler = MessageHandler(Filters.text & (~Filters.command), post_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(show_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()