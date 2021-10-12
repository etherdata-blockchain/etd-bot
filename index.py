import certifi
import telegram
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGODB_URL")
mongo = PyMongo(app, tlsCAFile=certifi.where())
bot = telegram.bot.Bot(os.getenv("TELEGRAM_BOT_API"))


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


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)
