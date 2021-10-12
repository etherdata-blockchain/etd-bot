from telegram import Update, ForceReply
from telegram.ext import CallbackContext
from config import CONFIGS


def help_handler(update: Update, context: CallbackContext):
    text = "Available commands: \n"
    for command, desc in CONFIGS:
        text += f"/{command} - {desc}\n"

    update.message.reply_text(text)

