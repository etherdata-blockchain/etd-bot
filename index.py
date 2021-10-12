import certifi
import telegram
from flask import Flask, jsonify, request
import logging
from flask_pymongo import PyMongo
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
import os
from config import CONFIGS
from handlers import HANDLERS
import json
import threading

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGODB_URL")
mongo = PyMongo(app, tlsCAFile=certifi.where())
updater = Updater(os.getenv("TELEGRAM_BOT_API"))
dispatcher: Dispatcher = updater.dispatcher
bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_API"))


@app.route("/", methods=["POST"])
def submit_request():
    try:
        data = request.json
        name = data['repository']['repo_name']
        if data['push_data']['tag'] != "latest":
            mongo.db.images.update_one({"repository.repo_name": name}, {"$set": data}, upsert=True)
            return {
                "status": "ok"
            }
        return {
            "status": "false"
        }
    except Exception as e:
        print(e)
        return {
            "status": "false",
        }


def start_bot():
    for i, config in enumerate(CONFIGS):
        command, desc = config
        handler = HANDLERS[i]
        dispatcher.add_handler(CommandHandler(command, handler))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), updater)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


if __name__ == '__main__':
    start_bot()
    app.run(debug=True, host="0.0.0.0", port=8080)
