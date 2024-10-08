from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
import os
from functions.start import start
from functions.data import data
from functions.high_low import high_low
from functions.supply import supply
from functions.display_top_10_cryptos import display_top_10_cryptos
from flask import Flask, request
from dotenv import load_dotenv
from functions.reply_text import reply_text

load_dotenv()

bot_key = os.getenv("BOT_KEY")

app = Flask(__name__)

# Create Telegram application
ApplicationBuilder().token(bot_key).build()


def message_parser(message):
    chat_id = message["message"]["chat"]["id"]
    text = message["message"]["text"]
    print(f"message: {text}")
    return chat_id, text


wrong_command_message = "wrong command"


@app.route("/webhook", methods=["POST"])
async def webhook():
    json_data = request.get_json()
    chat_id, text = message_parser(json_data)
    message: list = text.split()

    if text == "/start":
        await start(chat_id)
    elif text == "/top10":
        await display_top_10_cryptos(chat_id)
    elif len(message) == 2:
        command = message[0]
        query = message[1]

        if command == "/data":
            await data(chat_id, query)
        elif command == "/highlow":
            await high_low(chat_id, query)
        elif command == "/supply":
            await supply(chat_id, query)

    else:
        await reply_text(chat_id, wrong_command_message)
    return "ok"
