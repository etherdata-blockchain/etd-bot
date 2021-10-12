import os

import telegram
from dotenv import load_dotenv
from telegram.ext import Updater, Dispatcher, CommandHandler

from config import CONFIGS
from handlers import HANDLERS

load_dotenv(dotenv_path=".env")


def start_bot():
    updater = Updater(os.getenv("TELEGRAM_BOT_API"))
    dispatcher: Dispatcher = updater.dispatcher
    for i, config in enumerate(CONFIGS):
        command, desc = config
        handler = HANDLERS[i]
        dispatcher.add_handler(CommandHandler(command, handler, pass_args=True))

    updater.start_polling()


if __name__ == '__main__':
    print("Starting bot")
    start_bot()
