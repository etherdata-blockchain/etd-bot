import os
import datetime
import certifi
from pymongo import MongoClient
from pymongo.collection import Collection
from telegram import Update, ChatAction
from telegram.ext import CallbackContext


def device_handler(update: Update, context: CallbackContext):
    client = None
    try:
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        client = MongoClient(os.getenv("MONGODB_URL"), tlsCAFile=certifi.where())
        db = client.etd
        col: Collection = db.devices
        now = datetime.datetime.now(datetime.timezone.utc)
        prev_time = now - datetime.timedelta(minutes=3)
        count = col.count_documents({"lastSeen": {"$gte": prev_time}})
        total_devices = col.estimated_document_count()
        update.message.reply_text(f"Number of online devices: {count} / {total_devices}")

    except Exception as e:
        print(e)
        update.message.reply_text("Cannot get latest status")

    finally:
        if client:
            client.close()
