from config import get_config
from twitter_utils import tweet
from database_handler import add_message

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
  return user_id == 39069059

def check_message(message, context = None, bot = None):
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

def post_message(update, context):

  if(check_user(update.message.from_user.id)):
    check_message(update.message.text,
                  update = update,
                  context = context)

    if(add_message(message=update.message.text)):
      status_message = 'The message has been added to the queue!'
    else:
      status_message = 'The message has not added to the queue :('
  else:
    status_message = 'I don’t know you!'
  
  context.bot.send_message(chat_id=update.effective_chat.id, text=status_message)

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), post_message)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)


updater.start_polling()