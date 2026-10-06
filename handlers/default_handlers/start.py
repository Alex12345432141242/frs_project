from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.reply_to(
        message,
        "Привет! 👋\n\n"
        "Я — интерактивный путеводитель.\n\n"
        "С помощью этого бота ты можешь выбирать интересующие места, "
        "смотреть карту и узнавать больше о достопримечательностях.\n\n"
        "Сейчас доступен путеводитель по Нижнему парку Петергофа.\n\n"
        "Чтобы начать путешествие, используй /guide",
    )
