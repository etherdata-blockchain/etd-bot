import os

import requests
from pymongo import MongoClient
from pymongo.collection import Collection
from telegram import Update, ChatAction
from telegram.ext import CallbackContext
import certifi


def balance_handler(update: Update, context: CallbackContext):
    client = None
    url = "https://stats.etdchain.net/api/v2/transactions"
    try:
        print("Starting balance")
        address = context.args[0] if len(context.args) > 0 else None
        user_id = update.effective_user.id
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        client = MongoClient(os.getenv("MONGODB_URL"), tlsCAFile=certifi.where())
        db = client.telegram
        col: Collection = db.wallets
        found = col.find_one({"user_id": user_id})
        if found and not address:
            address = found['wallet']
            text = send_user_data_util(address, url)
            update.message.reply_text(text)

        else:
            if not address:
                update.message.reply_text(
                    "You didn't register your wallet address. Try to send message in this format: /balance YOUR_WALLET_ADDRESS. You don't need to provide your wallet address input next time!\n"
                    "你尚未注册你的钱包地址。请尝试用一下一下形式绑定钱包。 /balance YOUR_WALLET_ADDRESS。在这之后你就不需要提供你的钱包地址了。")
            else:
                col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id, "wallet": address}}, upsert=True)
                text = send_user_data_util(address, url)
                update.message.reply_text(text)

    except Exception as e:
        print(e)
        update.message.reply_text("Cannot get balance")
    finally:
        client.close()
        # pass


def send_user_data_util(address, url):
    data = requests.get(f"{url}/{address}").json()
    user_data = data['user']
    text = f"Wallet Address: {address}\nBalance: {round(float(user_data['balance']) / 1000000000000000000, 3)} ETD\n"
    text += "Transactions: \n"
    for i, tx in enumerate(user_data['transactions']):
        is_sent = tx['from'].lower() == address
        text += f"{i + 1}\n"
        text += f"{tx['time']}\n{'Sent' if is_sent else 'Received'}\n"
        text += f"{round(float(tx['value'] )/ 1000000000000000000, 3)} ETD\n"
        text += "\n"

    return text
