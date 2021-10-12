import os

from pymongo import MongoClient
from pymongo.collection import Collection
from telegram import Update, ChatAction
from telegram.ext import CallbackContext
import certifi


def image_handler(update: Update, context: CallbackContext):
    client = None
    try:
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        client = MongoClient(os.getenv("MONGODB_URL"), tlsCAFile=certifi.where())
        db = client.docker
        col: Collection = db.images
        text = "Latest Docker images' versions\n"
        data = list(col.find({}))
        for i, image in enumerate(data):
            text += f"{i + 1}: {image['repository']['name']} {image['push_data']['tag']}\n"
        update.message.reply_text(text)

    except Exception as e:
        print(e)
        update.message.reply_text("Cannot get latest docker images")
    finally:
        client.close()
