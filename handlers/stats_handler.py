from telegram import Update, ChatAction
from telegram.ext import CallbackContext
import requests


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def stats_handler(update: Update, context: CallbackContext):
    url = "https://stats.etdchain.net/api/v2/info"
    try:
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        res = requests.get(url)
        data = res.json()
        hash_rate = data['latestDifficulty'] / data['latestAvgBlockTime']
        update.message.reply_text(f"Latest Block Number: {data['latestBlockNumber']}\n"
                                  f"Network HashRate: {human_format(hash_rate)}")

    except Exception as e:
        print(e)
        update.message.reply_text("Cannot get latest status")
