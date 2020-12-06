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

# START STUFF
updater = Updater(token=telegram_config['token'], use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
  response_text = 'Hello to you, too!'
  context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

def post_message(update, context):
  if(check_user(update.message.from_user.id)):
    if(add_message(message=update.message.text)):
      status_message = 'The message has been shared!'
    else:
      status_message = 'The message has not been shared :('
  else:
    status_message = 'I don’t know you!'
  
  context.bot.send_message(chat_id=update.effective_chat.id, text=status_message)

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), post_message)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)


updater.start_polling()