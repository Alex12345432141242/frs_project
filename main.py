from loader import bot
import handlers  # noqa
from utils import set_default_commands

if __name__ == "__main__":
    set_default_commands(bot)
    bot.infinity_polling()
