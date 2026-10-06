from telebot.types import Message
import re

from loader import bot
from services.ai import AINotConfiguredError, AIRequestError, ask_about_peterhof
from states.question_states import QuestionState

MAX_QUESTION_LENGTH = 1500

QUESTION_INTRO = (
    "🤖 Задайте свой вопрос о Петергофе:\n\n"
    "Например:\n"
    "• Когда был построен Петергоф?\n"
    "• Почему фонтан «Самсон» стал символом Петергофа?\n"
    "• Сколько времени нужно на прогулку по Нижнему парку?\n"
    "• Какие фонтаны стоит посмотреть в первую очередь?"
)


@bot.message_handler(commands=["question"])
def bot_question(message: Message) -> None:
    bot.set_state(
        message.from_user.id,
        QuestionState.waiting_for_question,
        message.chat.id,
    )
    bot.send_message(message.chat.id, QUESTION_INTRO)


@bot.message_handler(
    state=QuestionState.waiting_for_question,
    content_types=["text"],
)
def receive_peterhof_question(message: Message) -> None:
    question = (message.text or "").strip()
    if not question:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, напишите вопрос текстом.",
        )
        return

    if len(question) > MAX_QUESTION_LENGTH:
        bot.send_message(
            message.chat.id,
            "Вопрос слишком длинный. Пожалуйста, сократите его до 1500 символов.",
        )
        return

    bot.send_message(message.chat.id, "🤔 Думаю над ответом...")

    try:
        answer = ask_about_peterhof(question)
    except AINotConfiguredError:
        bot.send_message(message.chat.id, "AI-сервис пока не настроен.")
    except AIRequestError:
        bot.send_message(
            message.chat.id,
            "К сожалению, сейчас не удалось получить ответ от AI. "
            "Попробуйте немного позже.",
        )
    else:
        answer = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", answer)
        bot.send_message(message.chat.id, answer, parse_mode="HTML")
        bot.send_message(
            message.chat.id,
            "Если хотите задать ещё один вопрос, используйте /question",
        )
    finally:
        bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=QuestionState.waiting_for_question)
def receive_non_text_question(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        "Пожалуйста, отправьте вопрос текстом.",
    )
