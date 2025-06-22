from flask import Flask, request
import telebot
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
referrals = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    return 'Invalid request', 403

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    user_id = str(message.from_user.id)
    if len(args) > 1:
        referrer = args[1]
        if referrer != user_id:
            referrals.setdefault(referrer, [])
            if user_id not in referrals[referrer]:
                referrals[referrer].append(user_id)
                bot.send_message(referrer, f"Kamu dapat referral baru: {user_id}")
    bot.send_message(message.chat.id, f"Halo {message.from_user.first_name}! Referral link kamu:\n"
                                      f"https://t.me/{bot.get_me().username}?start={user_id}")

@bot.message_handler(commands=['referrals'])
def my_referrals(message):
    user_id = str(message.from_user.id)
    count = len(referrals.get(user_id, []))
    bot.send_message(message.chat.id, f"Kamu punya {count} referral.")
