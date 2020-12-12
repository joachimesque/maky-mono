import logging

from config import get_config

from telegram.ext import (CallbackQueryHandler,
                          CommandHandler,
                          Filters,
                          MessageHandler,
                          Updater)

from .handlers import (handle_button,
                       handle_delete,
                       handle_post_image,
                       handle_post_message,
                       handle_show,
                       handle_start)


# BASIC CONFIG
logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logging_format,
                    level=logging.INFO)
telegram_config = get_config()['telegram']


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
