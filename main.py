from telegram.ext import Updater
from telegram.ext import CommandHandler
from dotenv import load_dotenv
from telegram.ext import MessageHandler, Filters
import pyowm
import logging
import os
TELEGRAM_KEY = os.getenv("TELEGRAM_KEY")
OPEN_WEATHER_MAP_KEY = os.getenv("OPEN_WEATHER_MAP_KEY")

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def getTemp(location):
    owm = pyowm.OWM(OPEN_WEATHER_MAP_KEY)
    observation = owm.weather_at_place(location)
    weather = observation.get_weather()
    return weather.get_temperature('celsius')["temp"]


updater = Updater(
    token=TELEGRAM_KEY, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, text=getTemp('London,GB') + "celsius")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Sorry, I didn't understand that command.")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
