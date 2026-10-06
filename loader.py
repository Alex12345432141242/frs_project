from telebot import TeleBot
from telebot.custom_filters import StateFilter
from telebot.storage import StateMemoryStorage
from config_data import config

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
bot.add_custom_filter(StateFilter(bot))
